import os
import csv
from collections import defaultdict
from mylib import string_lib as str_lib


ALVA_BIOBERT_PATH = "data/alvaroalon2_biobert_genetic_ner_results/"
ALL_GENES_FILE = "data/manual_annotations/45_all_text.csv"
GENE_NAMES_PUBTATOR = "data/gene_names_from_pubtator/"
genes_per_pmcid = defaultdict(list)
genes_per_pred = defaultdict(list)
genes_per_pub_res = defaultdict(list)

files = os.listdir(ALVA_BIOBERT_PATH)
gene_results = [gene_file.split("_")[1].split(".")[0] for gene_file in files]

# creating a dictionary to store PMCIDs as keys and the predicted genes from BIOBERT as keys
for result_file in os.listdir(ALVA_BIOBERT_PATH):
    pmcid = result_file.split("_")[1].split(".")[0]
    with open(ALVA_BIOBERT_PATH+result_file, 'r', encoding="UTF8") as f:
        pmcid_genes = list(set(f.read().lower().strip().split('\n')))
        genes_per_pred[pmcid].extend(pmcid_genes)


# creating a dictionary to store PMCIDs as keys and the genes in each from the pathway figures 
with open(ALL_GENES_FILE, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        pmcid = row["fig_name"].split('_')[0] 
        if pmcid in gene_results:
            genes_per_pmcid[pmcid].append(row["display_text"].strip().lower())

# writing out the matching genes to csv
with open('data/gene_biobert_matches.csv', newline='', mode='w') as mf:
    csv_writer = csv.writer(mf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(["S/N","PMCID", "GENES", "SCORE"])
    count = 0
    for key, value in genes_per_pmcid.items():
        count += 1
        matches = str_lib.str_list_ops.common_elements(genes_per_pred[key], value)
        score = round(str_lib.str_list_ops.intersection_over_union(genes_per_pred[key], value), 4)
        if len(matches)>0:
            matches = ",".join(matches)
            csv_writer.writerow([count, key, matches, score])

