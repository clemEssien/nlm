import os
import csv
import pandas as pd
import glob
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


    def retreive_human_gene_alias(self):
        human_gene_dict = defaultdict(list)
 
        with open("data/unite_gene_alias.csv", mode='r', encoding="UTF8", newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                lower_cased_row = [r.lower().strip() for r in row]
                human_gene_dict[row[0]].extend(lower_cased_row)
        return human_gene_dict 

    def human_gene_reference(self, gene_list):
        human_gene_dict = self.retreive_human_gene_alias()
        gene_ref = {}

        for gene in gene_list:
            for key, value in human_gene_dict.items():
                record  = []
                record.append(key.lower())
                record.extend(value)
                if gene in record:    
                            gene_ref[gene] = record[0]
            if gene not in gene_ref.keys():     
                gene_ref[gene] = gene
        return gene_ref

    #Name resolution for gene name from predicted gene_outputs
    def resolve_ref_file(self, gene_dict, file_name):
        with open(file_name, newline='', mode='w',encoding="UTF8") as csv_file:
            csv_columns = ['Gene', 'Reference']
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(csv_columns)
            for key, value in gene_dict.items():
                csv_writer.writerow([key,value])

    def write_csv_to_pandas(self, directory):
        csv_files = glob.glob(directory + "/*.csv")

        pd_list = []

        for filename in csv_files:
            df = pd.read_csv(filename, index_col=None, header=0)
            pd_list.append(df)

        frame = pd.concat(pd_list, axis=0, ignore_index=True)
        new_df = frame.drop_duplicates(
                    subset = ['Gene', 'Reference'],
                    keep = 'last').reset_index(drop = True)
    
        new_df.to_csv('data/gene_reference_dict.csv', index=False)

    
    def normalize_gene_names(self,gene_dict):
        ref_dict = pd.read_csv('data/gene_reference_dict.csv')
        formatted_dict = defaultdict(list)
        for key in gene_dict.keys():
            values = gene_dict[key]
            values_arr = []
            for value in values:
                data = ref_dict[ref_dict["Gene"] == value]['Reference']
                values_arr.append(data.to_string().split('    ')[1].strip())
            formatted_dict[key].append(values_arr)
        return formatted_dict



    # writing out the matching genes with scores to csv
    def write_output_to_csv(self,file, genes_per_pmcid, genes_per_pred):    
        with open(file, newline='', mode='w') as mf:
            csv_writer = csv.writer(mf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(["S/N","PMCID", "GENES", "MATCH COUNT", "SCORE"])
            count = 0
            genes_per_pred = self.normalize_gene_names(genes_per_pred)

            for key, value in genes_per_pmcid.items():
                count += 1
                matches = str_lib.str_list_ops.common_elements(genes_per_pred[key][0], value)
                total_matches = len(matches)
                score = round(str_lib.str_list_ops.match_ratio(genes_per_pred[key][0], value), 4)
                matches = ",".join(matches)
                csv_writer.writerow([count, key, matches, total_matches, score])
