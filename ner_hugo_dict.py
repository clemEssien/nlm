import evaluate_tool as tool
import pandas as pd
import os
from tqdm import tqdm
from mylib import string_lib
from mylib import file_ops
from collections import defaultdict


eval = tool.evaluate()
FULL_TEXT = "data/full_text/" 
HUGO_OUTPUT = "data/hugo_ner_results/"

file_ops.file_ops.remove_files_in_directory(HUGO_OUTPUT)
stopwords = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 
'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 
'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 
'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 
'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 
'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 
'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than', '0','1','2','3','4','5','6','7','8','9','0']



gene_list = eval.convert_csv_files_to_list("data/unite_gene_alias.csv")

gene_list = string_lib.str_list_ops.filter_stop_words(gene_list, stopwords)
df_genes = pd.DataFrame(gene_list, columns=['Genes'])

df_genes.to_csv('data/genes_from_hugo.csv', index=False)

files = os.listdir(FULL_TEXT)
pmid_gene_dict = defaultdict(list)
for file in tqdm(files):
    with open (FULL_TEXT+file, 'r') as f:
        pmid = file.split('.txt')[0]
        content = f.read().strip()
        tokens = content.split()
        filtered_tokens = string_lib.str_list_ops.filter_stop_words(tokens, stopwords)
        common_elements = string_lib.str_list_ops.common_elements(filtered_tokens, gene_list)
        pmid_gene_dict[pmid].extend(common_elements)
    


#writing out the gene_entities to files
print(pmid_gene_dict)
for key, value in pmid_gene_dict.items():
    
    with open(HUGO_OUTPUT+key+'.txt', 'a') as f:
        content = '\n'.join(value)
        content = content.lower()
        f.write(content)
