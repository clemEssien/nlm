from collections import defaultdict
import evaluate_tool as tool

eval = tool.evaluate()

genes_per_pmcid = eval.retrieve_pmcids_from_path_figs()

biobert_genes_per_pred = eval.retrieve_ner_results("data/alvaroalon2_biobert_genetic_ner_results/")


neji_genes_per_pred = eval.retrieve_ner_results("data/neji_output_results/")

bern_genes_per_pred = eval.retrieve_ner_results("data/bern_output_results/")

hugo_genes_per_pred = eval.retrieve_ner_results("data/hugo_ner_results/")

eval.write_pred_results_to_json(hugo_genes_per_pred)

eval.write_output_to_csv("data/scores/gene_biobert.csv", genes_per_pmcid, biobert_genes_per_pred)
eval.write_output_to_csv("data/scores/gene_neji_matches.csv", genes_per_pmcid, neji_genes_per_pred)
eval.write_output_to_csv("data/scores/gene_bern_matches.csv", genes_per_pmcid, bern_genes_per_pred)
eval.write_output_to_csv("data/scores/gene_hugo_matches.csv", genes_per_pmcid, hugo_genes_per_pred)

# writing combined output results
eval.write_combined_predicted_outputs("data/scores/combined.csv", genes_per_pmcid, biobert_genes_per_pred, neji_genes_per_pred, bern_genes_per_pred, hugo_genes_per_pred)
    
