##
## CPCantalapiedra 2020

import time

from ..common import get_call_info

from .ncbitaxa.ncbiquery import get_ncbi

#############
# Orthologs

##
def output_orthologs(annots, orthologs_file, resume, no_file_comments):
    start_time = time.time()

    ncbi = get_ncbi(usemem = True)

    if resume == True:
        file_mode = 'a'
    else:
        file_mode = 'w'
        
    with open(orthologs_file, file_mode) as ORTHOLOGS_OUT:
        output_orthologs_header(ORTHOLOGS_OUT, no_file_comments, not resume)

        qn = 0
        for ((hit, annotation), exists) in annots:

            # exists == False (--resume)
            
            if exists == False and annotation is not None:
                output_orthologs_row(ORTHOLOGS_OUT, annotation, ncbi)
                
            yield (hit, annotation), exists
            qn += 1

        elapsed_time = time.time() - start_time
        output_orthologs_footer(ORTHOLOGS_OUT, no_file_comments, qn, elapsed_time)

    if ncbi is not None: ncbi.close()
    
    return

##
def output_orthologs_row(out, annotation, ncbi):
    (query_name, best_hit_name, best_hit_evalue, best_hit_score,
     annotations,
     (narr_og_name, narr_og_cat, narr_og_desc),
     (best_og_name, best_og_cat, best_og_desc),
     match_nog_names,
     all_orthologies, annot_orthologs) = annotation

    all_orthologies["annot_orthologs"] = annot_orthologs

    for target in all_orthologies:
        if target == "all": continue
        if target == "annot_orthologs": continue
        
        query_target_orths = all_orthologies[target]
        if query_target_orths is None or len(query_target_orths) == 0:
            continue

        orthologs_taxids = set([int(x.split(".")[0]) for x in query_target_orths])
        orthologs_taxnames = sorted(ncbi.get_taxid_translator(orthologs_taxids).items(), key=lambda x: x[1])

        for taxid, taxname in orthologs_taxnames:
            orth_names = []
            for orth in [x for x in query_target_orths if int(x.split(".")[0]) == taxid]:
                orth_name = orth.split(".")[1]
                if orth in annot_orthologs:
                    orth_name = f"*{orth_name}"
                orth_names.append(orth_name)

            row = [query_name, target, f"{taxname}({taxid})", ",".join(sorted(orth_names))]
            print('\t'.join(row), file=out)
    return

##
def output_orthologs_header(out, no_file_comments, print_header):
    if not no_file_comments:        
        # Call info
        print(get_call_info(), file=out)

    # Header
    if print_header == True:
        header = ["#query", "orth_type", "species", "orthologs"]
        print('\t'.join(header), file=out)

    return

##
def output_orthologs_footer(out, no_file_comments, qn, elapsed_time):
    # Timings
    if not no_file_comments:
        print('## %d queries scanned' % (qn), file=out)
        print('## Total time (seconds):', elapsed_time, file=out)
        print('## Rate:', "%0.2f q/s" % ((float(qn) / elapsed_time)), file=out)

    return

##############
# Annotations

##

HIT_HEADER = ["query",
              "seed_ortholog",
              "evalue",
              "score",
              "eggNOG_OGs",
              "narr_OG_name",
              "narr_OG_cat",
              "narr_OG_desc"]

BEST_OG_HEADER = ["best_OG_name",
                  "best_OG_cat",
                  "best_OG_desc"]

ANNOTATIONS_HEADER = ['Preferred_name',
                      'GOs',
                      'EC',
                      'KEGG_ko',
                      'KEGG_Pathway',
                      'KEGG_Module',
                      'KEGG_Reaction',
                      'KEGG_rclass',
                      'BRITE',
                      'KEGG_TC',
                      'CAZy',
                      'BiGG_Reaction',
                      'PFAMs']

ANNOTATIONS_WHOLE_HEADER = HIT_HEADER + BEST_OG_HEADER + ANNOTATIONS_HEADER

##
def output_annotations(annots, annot_file, resume, no_file_comments, md5_field, md5_queries):

    if resume == True:
        file_mode = 'a'
    else:
        file_mode = 'w'
        
    start_time = time.time()
    
    with open(annot_file, file_mode) as ANNOTATIONS_OUT:
        output_annotations_header(ANNOTATIONS_OUT, no_file_comments, md5_field, not resume)

        qn = 0
        for (hit, annotation), exists in annots:

            # exists == False (--resume)
            
            if exists == False and annotation is not None:
                output_annotations_row(ANNOTATIONS_OUT, annotation, md5_field, md5_queries)
                
            yield (hit, annotation), exists
            qn += 1
        
        elapsed_time = time.time() - start_time
        output_annotations_footer(ANNOTATIONS_OUT, no_file_comments, qn, elapsed_time)
    return

##
def output_annotations_row(out, annotation, md5_field, md5_queries):

    (query_name, best_hit_name, best_hit_evalue, best_hit_score,
     annotations,
     (narr_og_name, narr_og_cat, narr_og_desc),
     (best_og_name, best_og_cat, best_og_desc),
     match_nog_names,
     all_orthologies, annot_orthologs) = annotation

    annot_columns = [query_name, best_hit_name, str(best_hit_evalue), str(best_hit_score),
                     ",".join(match_nog_names), 
                     narr_og_name, narr_og_cat.replace('\n', ''), narr_og_desc.replace('\n', ' ')]
            
    annot_columns.extend([best_og_name, best_og_cat.replace('\n', ''), best_og_desc.replace('\n', ' ')])
    
    for h in ANNOTATIONS_HEADER:
        if h in annotations:
            annot_columns.append(",".join(sorted(list(annotations[h]))))
        else:
            annot_columns.append('-')
                    
    if md5_field == True:
        query_name = annot_columns[0]
        if query_name in md5_queries:
            annot_columns.append(md5_queries[query_name])
        else:
            annot_columns.append("-")
            
    print('\t'.join([x if x is not None and x.strip() != "" else "-" for x in annot_columns]), file=out)
    
    return

##
def output_annotations_header(out, no_file_comments, md5_field, print_header):

    if not no_file_comments:
        print(get_call_info(), file=out)

    if print_header == True:
        print("#", end="", file=out)
        print('\t'.join(HIT_HEADER), end="\t", file=out)

        print('\t'.join(BEST_OG_HEADER), end="\t", file=out)

        annot_header = ANNOTATIONS_HEADER
        if md5_field == True:
            annot_header.append("md5")

        print('\t'.join(annot_header), file=out)

    return



##
def output_annotations_footer(out, no_file_comments, qn, elapsed_time):
    if not no_file_comments:
        print('## %d queries scanned' % (qn), file=out)
        print('## Total time (seconds):', elapsed_time, file=out)
        print('## Rate:', "%0.2f q/s" % ((float(qn) / elapsed_time)), file=out)

    return

## END
