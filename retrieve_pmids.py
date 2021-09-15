from Bio import Entrez

Entrez.email = "dmitrivdexter@yahoo.com"
handle = Entrez.esearch(db="pmc", term="GENE AND DISEASE AND PROTEIN AND CELLLINE AND CHEMICAL AND SPECIES AND MUTATION", retmax=60000)
record = Entrez.read(handle)

print(len(record["IdList"]))
print(record["IdList"])

idlist = "\n".join(record["IdList"])

with open("id_list.txt", "w") as f:
	f.write(idlist)

#53522
#8437627', '8437465', '8435934', '8435787', '8435730'
#https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmids=84376270&concepts=bioc
#https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmids=19894120&concepts=gene

# https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson?pmids=28483577,28483578,28483579
