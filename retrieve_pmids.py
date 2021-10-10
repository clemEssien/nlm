from Bio import Entrez

Entrez.email = "dmitrivdexter@yahoo.com"
handle = Entrez.esearch(db="pmc", term="GENE AND DISEASE AND PROTEIN AND CELLLINE AND CHEMICAL AND SPECIES AND MUTATION", retmax=60000)
record = Entrez.read(handle)

print(len(record["IdList"]))
print(record["IdList"])

idlist = "\n".join(record["IdList"])

with open("id_list.txt", "w") as f:
	f.write(idlist)
