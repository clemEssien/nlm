import os
import csv
from collections import defaultdict
from mylib import string_lib as str_lib

class evaluate:
    def __init__(self) -> None:
        self.ALL_GENES_FILE = "data/manual_annotations/45_all_text.csv"
        self.ALVA_BIOBERT_PATH = "data/alvaroalon2_biobert_genetic_ner_results/"
        self.GENE_NAMES_PUBTATOR = "data/gene_names_from_pubtator/"
        self.gene_results = [gene_file.split("_")[1].split(".")[0] for gene_file in os.listdir(self.ALVA_BIOBERT_PATH)]


    def retrieve_pmcids_from_path_figs(self):
        genes_per_pmcid = defaultdict(list)
        with open(self.ALL_GENES_FILE, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                pmcid = row["fig_name"].split('_')[0] 
                if pmcid in self.gene_results:
                    genes_per_pmcid[pmcid].append(row["display_text"].strip().lower())
        return genes_per_pmcid

    
    # creating a dictionary to store PMCIDs as keys and the predicted genes from BIOBERT as keys
    def retrieve_ner_results(self,path):
        genes_per_pred = defaultdict(list)       
        for result_file in os.listdir(path):
            pmcid = result_file.split("_")[1].split(".")[0]
            with open(path+result_file, 'r', encoding="UTF8") as f:
                pmcid_genes = list(set(f.read().lower().strip().split('\n')))
                genes_per_pred[pmcid].extend(pmcid_genes)
        return genes_per_pred

    
    # writing out the matching genes with scores to csv
    def write_output_to_csv(self,file, genes_per_pmcid, genes_per_pred):    
        with open(file, newline='', mode='w') as mf:
            csv_writer = csv.writer(mf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(["S/N","PMCID", "GENES", "MATCH COUNT", "SCORE"])
            count = 0
            for key, value in genes_per_pmcid.items():
                count += 1
                matches = str_lib.str_list_ops.common_elements(genes_per_pred[key], value)
                total_matches = len(matches)
                score = round(str_lib.str_list_ops.intersection_over_union(genes_per_pred[key], value), 4)
                matches = ",".join(matches)
                csv_writer.writerow([count, key, matches, total_matches, score])







