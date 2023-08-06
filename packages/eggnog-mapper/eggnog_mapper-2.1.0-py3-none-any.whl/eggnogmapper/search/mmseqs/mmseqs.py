##
## CPCantalapiedra 2019

from os.path import join as pjoin, isdir as pisdir, isfile as pisfile
import shutil
import subprocess
from tempfile import mkdtemp, mkstemp
import uuid

from ...common import MMSEQS2, get_eggnog_mmseqs_db, ITYPE_CDS, ITYPE_PROTS, ITYPE_GENOME, ITYPE_META
from ...emapperException import EmapperException
from ...utils import colorify, translate_cds_to_prots

from ..hmmer.hmmer_seqio import iter_fasta_seqs

from ..hits_io import parse_hits, output_hits
from ..diamond.diamond import hit_does_overlap

def create_mmseqs_db(dbprefix, in_fasta):
    cmd = (
        f'{MMSEQS2} createdb {in_fasta} {dbprefix}'
    )

    print(colorify('  '+cmd, 'yellow'))
    try:
        completed_process = subprocess.run(cmd, capture_output=True, check=True, shell=True)
    except subprocess.CalledProcessError as cpe:
        raise EmapperException("Error running mmseqs: "+cpe.stderr.decode("utf-8").strip().split("\n")[-1])
        
    return

def create_mmseqs_index(dbprefix, tmp_dir):
    cmd = (
        f'{MMSEQS2} createindex {dbprefix} {tmp_dir}'
    )

    print(colorify('  '+cmd, 'yellow'))
    try:
        completed_process = subprocess.run(cmd, capture_output=True, check=True, shell=True)
    except subprocess.CalledProcessError as cpe:
        raise EmapperException("Error running mmseqs: "+cpe.stderr.decode("utf-8").strip().split("\n")[-1])
    return

class MMseqs2Searcher:

    name = "mmseqs2"
    
    # Command
    cpu = targetdb = temp_dir = no_file_comments = None
    start_sens = 3
    sens_steps = 3
    final_sens = 7    

    # Filters
    pident_thr = score_thr = evalue_thr = query_cov = subject_cov = None # excluded_taxa = None

    # MMseqs2 options
    sub_mat = None

    in_file = None
    itype = None
    translate = None
    translation_table = None

    resume = None

    ##
    def __init__(self, args):

        self.itype = args.itype
        self.translate = args.translate

        self.targetdb = args.mmseqs_db if args.mmseqs_db else get_eggnog_mmseqs_db()
        self.cpu = args.cpu
        self.start_sens = args.start_sens
        self.sens_steps = args.sens_steps
        self.final_sens = args.final_sens
        
        self.query_cov = args.query_cover
        self.subject_cov = args.subject_cover

        self.pident_thr = args.pident
        self.evalue_thr = args.mmseqs_evalue
        self.score_thr = args.mmseqs_score
        # self.excluded_taxa = args.excluded_taxa if args.excluded_taxa else None

        self.sub_mat = args.mmseqs_sub_mat
        
        # self.temp_dir = args.temp_dir
        self.temp_dir = mkdtemp(prefix='emappertmp_mmseqs_', dir=args.temp_dir)
        self.no_file_comments = args.no_file_comments

        self.resume = args.resume
        
        return
    
    ##
    def clear(self):
        if self.temp_dir is not None and pisdir(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        return

    ##
    def search(self, in_file, seed_orthologs_file, hits_file):
        hits_generator = None
        
        if not MMSEQS2:
            raise EmapperException("%s command not found in path" % (MMSEQS2))

        self.in_file = in_file
        
        try:
            cmds = None
            hits_parser = None
            if self.resume == True:
                if pisfile(hits_file):
                    if pisfile(seed_orthologs_file):
                        hits_parser = parse_hits(seed_orthologs_file)
                else:
                    raise EmapperException(f"Couldn't find hits file {hits_file} to resume.")
            else:
                querydb = pjoin(self.temp_dir, uuid.uuid4().hex)
                # print(f'Querydb {querydb}')
                resultdb = pjoin(self.temp_dir, uuid.uuid4().hex)
                # print(f'ResultDB {resultdb}')
                bestresultdb = pjoin(self.temp_dir, uuid.uuid4().hex)
                # print(f'BestResultDB {bestresultdb}')
            
                alignmentsdb, cmds = self.run_mmseqs(in_file, querydb,
                                                     self.targetdb, resultdb, bestresultdb)
                shutil.copyfile(f'{alignmentsdb}.m8', hits_file)
                
            hits_generator = self.parse_mmseqs(hits_file, hits_parser)
            hits_generator = output_hits(cmds, hits_generator,
                                         seed_orthologs_file, self.resume,
                                         self.no_file_comments, False)

        except Exception as e:
            raise e
            
        return hits_generator
    
    def run_mmseqs(self, fasta_file, querydb, targetdb, resultdb, bestresultdb):
        cmds = []

        if self.itype == ITYPE_CDS and self.translate == True:
            handle, query_file = mkstemp(dir = self.temp_dir, text = True)
            translate_cds_to_prots(fasta_file, query_file)
        else:
            query_file = fasta_file
            
        cmd = self.createdb(query_file, querydb)
        cmds.append(cmd)

        cmd = self.search_step(querydb, targetdb, resultdb)
        cmds.append(cmd)

        if self.itype == ITYPE_CDS or self.itype == ITYPE_PROTS:
            cmd = self.filterdb_step(resultdb, bestresultdb)
            cmds.append(cmd)
        else:
            bestresultdb = resultdb

        cmd = self.convertalis_step(querydb, targetdb, bestresultdb)
        cmds.append(cmd)

        return bestresultdb, cmds

    def createdb(self, fasta_file, querydb):
        # mmseqs createdb examples/QUERY.fasta queryDB
        cmd = (
            f'{MMSEQS2} createdb {fasta_file} {querydb}'
        )
        if self.itype == ITYPE_PROTS or self.translate == True:
            cmd += ' --dbtype 1' # aas queries (proteins)
        else:
            cmd += ' --dbtype 2' # nts queries (CDS, contig, ...)
            
        print(colorify('  '+cmd, 'yellow'))
        try:
            completed_process = subprocess.run(cmd, capture_output=True, check=True, shell=True)
        except subprocess.CalledProcessError as cpe:
            raise EmapperException("Error running 'mmseqs createdb': "+cpe.stderr.decode("utf-8").strip().split("\n")[-1])
        return cmd

    def search_step(self, querydb, targetdb, resultdb):
        # mmseqs search queryDB targetDB resultDB tmp
        cmd = (
            f'{MMSEQS2} search -a true {querydb} {targetdb} {resultdb} {self.temp_dir} '
            f'--start-sens {self.start_sens} --sens-steps {self.sens_steps} -s {self.final_sens} '
            f'--threads {self.cpu}'
        )

        if self.sub_mat is not None: cmd += f' --sub-mat {self.sub_mat}'
        if self.translation_table is not None: cmd += f' --translation-table {self.translation_table}'
        
        print(colorify('  '+cmd, 'yellow'))
        try:
            completed_process = subprocess.run(cmd, capture_output=True, check=True, shell=True)
        except subprocess.CalledProcessError as cpe:
            raise EmapperException("Error running 'mmseqs search': "+cpe.stderr.decode("utf-8").strip().split("\n")[-1])
        return cmd

    ##
    def filterdb_step(self, resultdb, bestresultdb):
        # mmseqs filterdb resultDB bestResultDB --extract-lines 1
        cmd = (
            f'{MMSEQS2} filterdb {resultdb} {bestresultdb} --threads {self.cpu}'
        )
        cmd += " --extract-lines 1 "
        
        print(colorify('  '+cmd, 'yellow'))
        try:
            completed_process = subprocess.run(cmd, capture_output=True, check=True, shell=True)
        except subprocess.CalledProcessError as cpe:
            raise EmapperException("Error running 'mmseqs filterdb': "+cpe.stderr.decode("utf-8").strip().split("\n")[-1])                
        
        return cmd
    
    ##
    def convertalis_step(self, querydb, targetdb, resultdb):
        # mmseqs convertalis queryDB targetDB resultDB resultDB.m8
        cmd = (
            f'{MMSEQS2} convertalis {querydb} {targetdb} {resultdb} {resultdb}.m8 --threads {self.cpu}'
        )
        if self.sub_mat is not None: cmd += f' --sub-mat {self.sub_mat}'
            
        if self.translation_table is not None: cmd += f' --translation-table {self.translation_table}'

        # outfmt
        cmd += f' --format-output "query,target,pident,alnlen,qstart,qend,tstart,tend,evalue,bits,qcov,tcov"'
        print(colorify('  '+cmd, 'yellow'))
        try:
            completed_process = subprocess.run(cmd, capture_output=True, check=True, shell=True)
        except subprocess.CalledProcessError as cpe:
            raise EmapperException("Error running 'mmseqs convertalis': "+cpe.stderr.decode("utf-8").strip().split("\n")[-1])        
        return cmd

    
    ##
    def parse_mmseqs(self, raw_mmseqs_file, hits_parser):
        if self.itype == ITYPE_CDS or self.itype == ITYPE_PROTS:
            return self._parse_mmseqs(raw_mmseqs_file, hits_parser)
        else: #self.itype == ITYPE_GENOME or self.itype == ITYPE_META:
            return self._parse_genepred(raw_mmseqs_file, hits_parser)
    
    ##
    def _parse_mmseqs(self, raw_mmseqs_file, hits_parser):

        # previous hits from resume are yielded
        last_resumed_query = None
        if hits_parser is not None:
            for hit in hits_parser:
                yield (hit, True) # hit and skip (already exists)
                last_resumed_query = hit[0]

        # semaphore to start processing new hits
        last_resumed_query_found = False if last_resumed_query is not None else True

        prev_query = None
        # parse non-resumed hits
        with open(raw_mmseqs_file, 'r') as raw_f:
            for line in raw_f:
                if not line.strip() or line.startswith('#'):
                    continue
                
                fields = list(map(str.strip, line.split('\t')))
                # check fields in convertalis_step()
        
                query = fields[0]

                if last_resumed_query is not None:
                    if query == last_resumed_query:
                        last_resumed_query_found = True
                        continue
                    else:
                        if last_resumed_query_found == False:
                            continue
                        else:
                            last_resumed_query = None # start parsing new queries
                            
                # only one result per query
                if prev_query is not None and query == prev_query:
                    continue
                else:
                    prev_query = query
                    
                pident = float(fields[2])
                evalue = float(fields[8])
                score = float(fields[9])
                qcov = float(fields[10]) * 100 # mmseqs uses 0-1 values
                scov = float(fields[11]) * 100 # mmseqs uses 0-1 values

                # note: this could be done with mmmseqs filterdb, but I dont know how to do it in a single step
                if ((self.pident_thr is not None and pident < self.pident_thr) or 
                    (self.evalue_thr is not None and evalue > self.evalue_thr) or
                    (self.score_thr is not None and score < self.score_thr) or
                    (self.query_cov is not None and qcov < self.query_cov) or
                    (self.subject_cov is not None and scov < self.subject_cov)):
                    continue
                
                target = fields[1]
                length = int(fields[3])
                qstart = int(fields[4])
                qend = int(fields[5])
                sstart = int(fields[6])
                send = int(fields[7])

                hit = [query, target, evalue, score, qstart, qend, sstart, send, pident, qcov, scov]
                yield (hit, False) # hit and dont skip (doesnt exist)
        return

    ##
    def _parse_genepred(self, raw_mmseqs_file, hits_parser):
        
        # previous hits from resume are yielded
        last_resumed_query = None
        if hits_parser is not None:
            for hit in hits_parser:
                yield (hit, True) # hit and skip (already exists)
                last_resumed_query = hit[0]

        # semaphore to start processing new hits
        last_resumed_query_found = False if last_resumed_query is not None else True
        
        curr_query_hits = []
        prev_query = None
        queries_suffixes = {}        
        
        with open(raw_mmseqs_file, 'r') as raw_f:
            for line in raw_f:
                if not line.strip() or line.startswith('#'):
                    continue
                
                fields = list(map(str.strip, line.split('\t')))
                # check fields in convertalis_step()
                # cmd += f' --format-output "query,target,pident,alnlen,
                #qstart,qend,tstart,tend,evalue,bits,qcov,tcov"'

                query = fields[0]
                
                if last_resumed_query is not None:
                    if query == last_resumed_query:
                        last_resumed_query_found = True
                        continue
                    else:
                        if last_resumed_query_found == False:
                            continue
                        else:
                            last_resumed_query = None # start parsing new queries
                
                pident = float(fields[2])
                evalue = float(fields[8])
                score = float(fields[9])
                qcov = float(fields[10]) * 100 # mmseqs uses 0-1 values
                scov = float(fields[11]) * 100 # mmseqs uses 0-1 values

                # note: this could be done with mmmseqs filterdb, but I dont know how to do it in a single step
                if ((self.pident_thr is not None and pident < self.pident_thr) or 
                    (self.evalue_thr is not None and evalue > self.evalue_thr) or
                    (self.score_thr is not None and score < self.score_thr) or
                    (self.query_cov is not None and qcov < self.query_cov) or
                    (self.subject_cov is not None and scov < self.subject_cov)):
                    continue
                
                query = fields[0]
                target = fields[1]
                length = int(fields[3])
                qstart = int(fields[4])
                qend = int(fields[5])
                sstart = int(fields[6])
                send = int(fields[7])
                
                hit = [query, target, evalue, score, qstart, qend, sstart, send, pident, qcov, scov]

                if query == prev_query:
                    if not hit_does_overlap(hit, curr_query_hits):
                        if query in queries_suffixes:
                            queries_suffixes[query] += 1
                            suffix = queries_suffixes[query]
                        else:
                            suffix = 0
                            queries_suffixes[query] = suffix
                            
                        yield ([f"{hit[0]}_{suffix}"]+hit[1:], False) # hit and doesnt exist
                        curr_query_hits.append(hit)
                else:
                    if query in queries_suffixes:
                        queries_suffixes[query] += 1
                        suffix = queries_suffixes[query]
                    else:
                        suffix = 0
                        queries_suffixes[query] = suffix
                            
                    yield ([f"{hit[0]}_{suffix}"]+hit[1:], False) # hit and doesnt exist
                    curr_query_hits = [hit]
                    
                prev_query = query    
                
        return
    
## END
