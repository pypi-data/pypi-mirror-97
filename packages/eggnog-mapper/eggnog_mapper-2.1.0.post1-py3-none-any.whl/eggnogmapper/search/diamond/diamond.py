##
## CPCantalapiedra 2019

from os.path import isdir as pisdir, isfile as pisfile
import shutil
import subprocess
from tempfile import mkdtemp, mkstemp

from ...emapperException import EmapperException
from ...common import DIAMOND, get_eggnog_dmnd_db, ITYPE_CDS, ITYPE_PROTS, ITYPE_GENOME, ITYPE_META
from ...utils import colorify, translate_cds_to_prots

from ..hmmer.hmmer_seqio import iter_fasta_seqs

from ..hits_io import parse_hits, output_hits

SENSMODE_FAST = "fast"
SENSMODE_MID_SENSITIVE = "mid-sensitive"
SENSMODE_SENSITIVE = "sensitive"
SENSMODE_MORE_SENSITIVE = "more-sensitive"
SENSMODE_VERY_SENSITIVE = "very-sensitive"
SENSMODE_ULTRA_SENSITIVE = "ultra-sensitive"
# sens modes in diamond 0.9.24
# SENSMODES = [SENSMODE_FAST, SENSMODE_SENSITIVE, SENSMODE_MORE_SENSITIVE]
# sens modes in diamond 2.0.4
SENSMODES = [SENSMODE_FAST, SENSMODE_MID_SENSITIVE, SENSMODE_SENSITIVE, SENSMODE_MORE_SENSITIVE, SENSMODE_VERY_SENSITIVE, SENSMODE_ULTRA_SENSITIVE]

OVERLAP_TOL_FRACTION = 1/3

def create_diamond_db(dbprefix, in_fasta):
    cmd = (
        f'{DIAMOND} makedb --in {in_fasta} --db {dbprefix}'
    )

    print(colorify('  '+cmd, 'yellow'))
    try:
        completed_process = subprocess.run(cmd, capture_output=True, check=True, shell=True)
    except subprocess.CalledProcessError as cpe:
        raise EmapperException("Error running diamond: "+cpe.stderr.decode("utf-8").strip().split("\n")[-1])
        
    return

class DiamondSearcher:

    name = "diamond"
    
    # Command
    cpu = tool = dmnd_db = temp_dir = no_file_comments = None
    matrix = gapopen = gapextend = None
    block_size = index_chunks = None

    # Filters
    pident_thr = score_thr = evalue_thr = query_cov = subject_cov = None

    # Output format from diamond
    outfmt_short = False

    in_file = None
    itype = None
    translate = None
    query_gencode = None
    
    resume = None

    ##
    def __init__(self, args):
        
        self.itype = args.itype
        self.translate = args.translate
        self.query_gencode = args.trans_table

        self.dmnd_db = args.dmnd_db if args.dmnd_db else get_eggnog_dmnd_db()

        self.cpu = args.cpu

        self.sensmode = args.sensmode
        
        self.query_cov = args.query_cover
        self.subject_cov = args.subject_cover

        self.matrix = args.matrix
        self.gapopen = args.gapopen
        self.gapextend = args.gapextend
        self.block_size = args.dmnd_block_size
        self.index_chunks = args.dmnd_index_chunks

        self.pident_thr = args.pident
        self.evalue_thr = args.dmnd_evalue
        self.score_thr = args.dmnd_score
        # self.excluded_taxa = args.excluded_taxa if args.excluded_taxa else None

        self.outfmt_short = args.outfmt_short
        
        self.temp_dir = mkdtemp(prefix='emappertmp_dmdn_', dir=args.temp_dir)
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
        
        if not DIAMOND:
            raise EmapperException("%s command not found in path" % (DIAMOND))

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
                cmds = self.run_diamond(in_file, hits_file)
                
            hits_generator = self.parse_diamond(hits_file, hits_parser)            
            hits_generator = output_hits(cmds, hits_generator,
                                         seed_orthologs_file, self.resume,
                                         self.no_file_comments, self.outfmt_short)

        except Exception as e:
            raise e
            
        return hits_generator

    ##
    def run_diamond(self, fasta_file, output_file):
        cmds = []
        ##
        # search type
        if self.itype == ITYPE_CDS and self.translate == True:
            tool = 'blastp'
            handle, query_file = mkstemp(dir = self.temp_dir, text = True)
            translate_cds_to_prots(fasta_file, query_file)
        elif self.itype == ITYPE_CDS or self.itype == ITYPE_GENOME or self.itype == ITYPE_META:
            tool = 'blastx'
            query_file = fasta_file
        elif self.itype == ITYPE_PROTS:
            tool = 'blastp'
            query_file = fasta_file
        else:
            raise EmapperException(f"Unrecognized --itype {self.itype}.")

        ##
        #prepare command
        cmd = (
            f'{DIAMOND} {tool} -d {self.dmnd_db} -q {query_file} '
            f'--threads {self.cpu} -o {output_file} '
        )
        
        if self.sensmode != SENSMODE_FAST: cmd += f' --{self.sensmode}'

        if self.evalue_thr is not None: cmd += f' -e {self.evalue_thr}'
        if self.score_thr is not None: cmd += f' --min-score {self.score_thr}'
        if self.pident_thr is not None: cmd += f' --id {self.pident_thr}'
        if self.query_cov is not None: cmd += f' --query-cover {self.query_cov}'
        if self.subject_cov is not None: cmd += f' --subject-cover {self.subject_cov}'

        if self.query_gencode: cmd += f' --query-gencode {self.query_gencode}'
        if self.matrix: cmd += f' --matrix {self.matrix}'
        if self.gapopen: cmd += f' --gapopen {self.gapopen}'
        if self.gapextend: cmd += f' --gapextend {self.gapextend}'
        if self.block_size: cmd += f' --block-size {self.block_size}'
        if self.index_chunks: cmd += f' -c {self.index_chunks}'

        if self.itype == ITYPE_CDS or self.itype == ITYPE_PROTS:
            cmd += " --top 3 "
        else: # self.itype == ITYPE_GENOME or self.itype == ITYPE_META: i.e. gene prediction
            cmd += " --max-target-seqs 0 --max-hsps 0 "

        ##
        # output format
        OUTFMT_SHORT = " --outfmt 6 qseqid sseqid evalue bitscore"
        OUTFMT_LONG = " --outfmt 6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qcovhsp scovhsp"
        if self.itype == ITYPE_GENOME or self.itype == ITYPE_META: # i.e. gene prediction
            cmd += OUTFMT_LONG
        else:
            if self.outfmt_short == True:
                cmd += OUTFMT_SHORT
            else:
                cmd += OUTFMT_LONG

        # NOTE about short output format:
        # diamond should run faster if no pident, qcov, scov values are used either as filter or to be output
        # This is because it needs to compute them, whereas using only evalue and score does not need to recompute.
        # Therefore, the fastest way to obtain diamond alignments is using the OUTFMT_SHORT format and
        # not using --id, --query-cover, --subject-cover thresholds. Of course, does not always fit our needs.

        ##
        # run command
        print(colorify('  '+cmd, 'yellow'))
        try:
            completed_process = subprocess.run(cmd, capture_output=True, check=True, shell=True)
            cmds.append(cmd)
        except subprocess.CalledProcessError as cpe:
            raise EmapperException("Error running diamond: "+cpe.stderr.decode("utf-8").strip().split("\n")[-1])
        
        return cmds


    ##
    def parse_diamond(self, raw_dmnd_file, hits_parser):
        if self.itype == ITYPE_CDS or self.itype == ITYPE_PROTS:
            return self._parse_diamond(raw_dmnd_file, hits_parser)
        else: #self.itype == ITYPE_GENOME or self.itype == ITYPE_META:
            return self._parse_genepred(raw_dmnd_file, hits_parser)
        
    ##
    def _parse_diamond(self, raw_dmnd_file, hits_parser):        

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
        with open(raw_dmnd_file, 'r') as raw_f:
            for line in raw_f:
                if not line.strip() or line.startswith('#'):
                    continue

                fields = list(map(str.strip, line.split('\t')))
                # fields are defined in run_diamond
                # OUTFMT_SHORT = " --outfmt 6 qseqid sseqid evalue bitscore"
                # OUTFMT_LONG = " --outfmt 6 qseqid sseqid pident length mismatch
                # gapopen qstart qend sstart send evalue bitscore qcovhsp scovhsp"
                
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
                
                target = fields[1]

                if self.outfmt_short == True:
                    evalue = float(fields[2])
                    score = float(fields[3])
                    hit = [query, target, evalue, score]
                else:
                    pident = float(fields[2])
                    qstart = int(fields[6])
                    qend = int(fields[7])
                    sstart = int(fields[8])
                    send = int(fields[9])
                    evalue = float(fields[10])
                    score = float(fields[11])
                    qcov = float(fields[12])
                    scov = float(fields[13])
                    hit = [query, target, evalue, score, qstart, qend, sstart, send, pident, qcov, scov]

                yield (hit, False) # hit and dont skip (doesnt exist)
        return

    ##
    def _parse_genepred(self, raw_dmnd_file, hits_parser):

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
        
        with open(raw_dmnd_file, 'r') as raw_f:
            for line in raw_f:
                if not line.strip() or line.startswith('#'):
                    continue

                fields = list(map(str.strip, line.split('\t')))
                # fields are defined in run_diamond
                # OUTFMT_LONG = " --outfmt 6 qseqid sseqid pident length mismatch
                # gapopen qstart qend sstart send evalue bitscore qcovhsp scovhsp"
                
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

                target = fields[1]
                pident = float(fields[2])
                evalue = float(fields[10])
                score = float(fields[11])
                
                qstart = int(fields[6])
                qend = int(fields[7])
                sstart = int(fields[8])
                send = int(fields[9])
                qcov = float(fields[12])
                scov = float(fields[13])
                
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


def hit_does_overlap(hit, hits):
    does_overlap = False

    hitstart = hit[4]
    hitend = hit[5]
    if hitstart > hitend:
        hitend = hit[4]
        hitstart = hit[5]

    for o in hits:
        ostart = o[4]
        oend = o[5]
        if ostart > oend:
            oend = o[4]
            ostart = o[5]

        overlap = get_overlap(hitstart, hitend, ostart, oend)

        if overlap is not None and overlap > 0:
            does_overlap = True
            break

    return does_overlap


def get_overlap(hitstart, hitend, ostart, oend, allow_diff_frame = False):
    overlap = None

    # if different frame and not allow different frame to compute overlap
    # return overlap None
    # If allow different frame is True, overlap will be computed
    if abs(hitstart - ostart) % 3 != 0 and allow_diff_frame == False:
        overlap = None
    else:        
        # no overlap
        if hitend <= ostart:
            overlap = hitend - ostart

        # no overlap
        elif hitstart >= oend:
            overlap = oend - hitstart

        # envelopes
        elif (hitstart >= ostart and hitend <= oend) or (ostart >= hitstart and oend <= hitend):
            overlap_start = max(hitstart, ostart)
            overlap_end = min(hitend, oend)
            overlap = overlap_end - (overlap_start - 1)

        # overlap, no envelope
        else:
            hittol = (hitend - (hitstart - 1)) * OVERLAP_TOL_FRACTION
            otol = (oend - (ostart - 1)) * OVERLAP_TOL_FRACTION
            # the tolerance to apply to each end
            # depends on which sequence overhangs on that specific end
            if hitstart < ostart:
                tol1 = hittol
                tol2 = otol
            else:
                tol1 = otol
                tol2 = hittol

            hang_left = abs(hitstart - ostart)
            hang_right = abs(hitend - oend)

            if hang_left > tol1 and hang_right > tol2:
                overlap = -1 # consider as no overlapping
            else:
                overlap_start = max(hitstart, ostart)
                overlap_end = min(hitend, oend)
                overlap = overlap_end - (overlap_start - 1)
            
    return overlap

## END
