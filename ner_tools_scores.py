from collections import defaultdict
import evaluate_tool as tool

eval = tool.evaluate()

genes_per_pmcid = eval.retrieve_pmcids_from_path_figs()
biobert_genes_per_pred = eval.retrieve_ner_results("data/alvaroalon2_biobert_genetic_ner_results/")


biobert_genes = []
for gene in list(biobert_genes_per_pred.values()):
    gene = [g.strip() for g in gene]
    biobert_genes.extend(gene)

biobert_dict = (eval.human_gene_reference(biobert_genes))
eval.resolve_ref_file(biobert_dict, "data/ref/biobert_ref_genes.csv")

neji_genes_per_pred = eval.retrieve_ner_results("data/neji_output_results/")


neji_genes = []
for gene in list(neji_genes_per_pred.values()):
    neji_genes.extend(gene)

neji_dict = (eval.human_gene_reference(neji_genes))


eval.resolve_ref_file(neji_dict, "data/ref/neji_ref_genes.csv")

bern_genes_per_pred = eval.retrieve_ner_results("data/bern_output_results/")

bern_genes = []
for gene in list(bern_genes_per_pred.values()):
    bern_genes.extend(gene)

bern_dict = (eval.human_gene_reference(bern_genes))
eval.resolve_ref_file(bern_dict, "data/ref/bern_ref_genes.csv")


eval.write_csv_to_pandas('data/ref/')


#resolve genes_per_pmcid
resolved_gene_per_pmcid = defaultdict(list)
for key  in genes_per_pmcid:
    resolved_gene_per_pmcid[key].extend(list(eval.human_gene_reference(genes_per_pmcid[key]).values()))

eval.write_output_to_csv("data/scores/gene_biobert.csv",resolved_gene_per_pmcid,biobert_genes_per_pred)
eval.write_output_to_csv("data/scores/gene_neji_matches.csv", resolved_gene_per_pmcid, neji_genes_per_pred)
eval.write_output_to_csv("data/scores/gene_bern_matches.csv", resolved_gene_per_pmcid, bern_genes_per_pred)

