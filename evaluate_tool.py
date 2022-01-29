from difflib import SequenceMatcher
import os
import csv
import re
import string
import pandas as pd
import glob
import json
from collections import defaultdict
from mylib import string_lib as str_lib
from tqdm import tqdm

class evaluate:
    def __init__(self) -> None:
        self.ALL_GENES_FILE = "data/manual_annotations/45_all_text.csv"
        self.ALVA_BIOBERT_PATH = "data/alvaroalon2_biobert_genetic_ner_results/"
        # self.GENE_NAMES_PUBTATOR = "data/gene_names_from_pubtator/"
        self.GENE_NAMES_PUBTATOR = "../Fei/gene_names_from_pubtator/"
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


    def convert_csv_files_to_list(sef,csv_file):
        gene_list = []
        with open(csv_file, mode='r', encoding="UTF8", newline='') as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                row_values = list(row.values())
                gene_string = str_lib.str_list_ops.format_gene_array(''.join( str(e) for e in row_values))
                gene_string = [gene.lower() for gene in gene_string]
                gene_list.extend(gene_string)
        return gene_list 


    def fuzzy_rule(self, name):
        name = name.upper()
        name = name.replace(' ', '')  # remove space
        name = name.replace('.', '')  # remove dot *
        name = re.sub(u"\\(.*?\\)", "", name)  # remove brackets and its content
        name = name.replace('(', "").replace(')', "")  # remove single brackets
        name = name.rstrip(string.digits)  # *

        if name.find("-") >= 0:
            if not name[name.find("-") + 1:len(name)].isalpha() or len(name[name.find("-") + 1:len(name)]) < len(
                    name[0:name.find("-")]):
                name = name[0:name.find("-")]
            if name.find("-") < 2:
                name = name[name.find("-") + 1:len(name)]
        # name = name.replace("-", "")

        return name

    
    def string_similarity(self, a , b):
        return SequenceMatcher(None, a, b).ratio()
        
    def fuzzy_gene_match(self,gene_dict_list, tokens_from_text_list, similarity_threshold):
        gene_list = []
        for gene in tqdm(gene_dict_list):
            gene = self.fuzzy_rule(gene)
            for token in tokens_from_text_list:
                if self.string_similarity(token, gene) >= similarity_threshold:
                # if token == gene or token in gene or self.string_similarity(token, gene) >= similarity_threshold:
                    gene_list.append(token)
        return gene_list
        
    # writing out the matching genes with scores to csv
    def write_output_to_csv(self,file, genes_per_pmcid, genes_per_pred):    
        with open(file, newline='', mode='w') as mf:
            csv_writer = csv.writer(mf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(["S/N","PMCID", "GENES", "MATCH COUNT", "SCORE"])
            count = 0
            # genes_per_pred = self.normalize_gene_names(genes_per_pred)

            for key, value in genes_per_pmcid.items():
                count += 1
                # matches = str_lib.str_list_ops.common_elements(genes_per_pred[key][0], value)
                matches = list(set(self.fuzzy_gene_match(genes_per_pred[key], value, 0.1)))
                matches = [match for match in matches if len(match.strip()) > 0]
                total_matches = len(matches)
                score = round(str_lib.str_list_ops.match_ratio(value, matches), 4)
                matches = ",".join(matches)
                csv_writer.writerow([count, key, matches, total_matches, score])

    
    def calculate_match_score(self, genes_per_pred, output_file):
        genes = []
        for gene in list(genes_per_pred):
            gene = [g.strip() for g in gene]
            genes.extend(gene)

        genes_dict = (self.human_gene_reference(genes))
        self.resolve_ref_file(genes_dict, output_file)
    
    def write_combined_predicted_outputs(self, file, genes_per_pmcid, biobert, neji, bern, hugo):
        json_dict = defaultdict(list)
        with open(file, newline='', mode='w') as mf:
            csv_writer = csv.writer(mf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(["S/N","PMCID", "GENES", "MATCH COUNT", "SCORE"])
            count = 0
            # genes_per_pred = self.normalize_gene_names(genes_per_pred)

            for key, value in genes_per_pmcid.items():
                count += 1
                # matches = str_lib.str_list_ops.common_elements(genes_per_pred[key][0], value)
                match_bert = list(set(self.fuzzy_gene_match(biobert[key], value, 0.1)))
                match_neji = list(set(self.fuzzy_gene_match(neji[key], value, 0.1)))
                match_bern = list(set(self.fuzzy_gene_match(bern[key], value, 0.1)))
                match_hugo = list(set(self.fuzzy_gene_match(hugo[key], value, 0.1)))
                matches = list(set(match_bert + match_neji + match_bern + match_hugo)) 
                matches = [match for match in matches if len(match.strip()) > 0]
                total_matches = len(matches)
                score = round(str_lib.str_list_ops.match_ratio(value, matches), 4)
                matches = ",".join(matches)
                json_dict[key].append(matches)
                csv_writer.writerow([count, key, matches, total_matches, score])
            # json_data = json.dumps(json_dict, indent=2)
            with open("data/output.json", "w") as f:
                json.dump(json_dict, f, indent=3)


    def write_pred_results_to_json(self, gene_dict):
        json_dict = defaultdict(list)
        stopwords = str_lib.str_list_ops.return_stop_words()
        for key, value in gene_dict.items():
            formatted_values = [val for val in value if val  not in stopwords]
            formatted_values = [val for val in formatted_values if not val.isdigit() ]
            formatted_values = [val for val in formatted_values if len(val)>2 ]
            json_dict[key].extend(formatted_values)
        with open("data/hugo_output.json", "w") as f:
                json.dump(json_dict, f, indent=3)

    # def compare_pred_with_pathway(self, pred_dict, pathway):
    #     match_dict = defaultdict(list)
    #     for key, value in pathway.items():
    #         matches = str_lib.str_list_ops.fuzzy_gene_match(pred_dict[key], value, 0.5)
    #         match_dict[key].append(matches)
    #     return match_dict
        
    #     with open('data/scores/match_hugo_ner.csv', newline='', mode='w',encoding="UTF8") as csv_file:
    #         csv_columns = (["S/N","PMCID", "GENES", "MATCH COUNT", "SCORE"])
    #         csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #         csv_writer.writerow(csv_columns)
    #         for key, value in match_dict.items():
    #             csv_writer.writerow([key,value])