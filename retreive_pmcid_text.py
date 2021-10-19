import os
from Bio.Entrez import efetch
from Bio import Entrez
from requests import models
from indra.sources import reach
Entrez.email = 'A.N.Other@example.com'

def print_abstract(pmid):
    handle = efetch(db='pubmed', id=pmid,retmode='text', rettype='full')
    print(handle.read())

def  gene_full_text(pmid):
    reach_processor = reach.process_pmc(pmid)

# print_indra()
# print_abstract('2172299')

# pmids = os.listdir("data/partial_txt")
# pmids = [pmid.split('.')[0][3:] for pmid in pmids ]
# print(pmids)

# for pmid in pmids:
#     gene_full_text(pmid)


print_abstract('23085539')



# import indra as indra
# from indra.sources import trips
# from indra import assemblers
# from indra.assemblers.pysb import PysbAssembler 

# sentence = 'MAP2K1 phosphorylates MAPK3 at Thr-202 and Tyr-204'
# trips_processor = trips.process_text(sentence)

# statements = trips_processor.statements

# pa = PysbAssembler()
# pa.add_statements(statements)
# model =pa.make_model(policies='two_step')

# time = linspace(0,300)
# sim_result = odesolve(model, time)









# download microsoft build tools 
# import sys    
# import argparse
# from Bio import Entrez
# from metapub import PubMedFetcher

# fetch = PubMedFetcher()
# article = fetch.article_by_pmid('2070952') #2070952 #2988105 #PMC4252843
# print(article.title)
# print(article.journal, article.year, article.volume, article.issue)
# print(article.authors)


# from lxml.etree import tostring
# inner_html = tostring(article.content)


# print((inner_html))
#  POST_URL = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/epost.fcgi?db=%s' % pubmed '&id=' + pmid_list
#     RET_URL = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=%s&query_key=1&mode=xml&rettype=full' % db



# <?xml version="1.0" ?>\n<!DOCTYPE PubmedArticleSet PUBLIC "-//NLM//DTD PubMedArticle, 1st January 2019//EN" "https://dtd.nlm.nih.gov/ncbi/pubmed/out/pubmed_190101.dtd">\n<PubmedArticleSet><PubmedArticle><MedlineCitation Status="MEDLINE" Owner="NLM"><PMID Version="1">2988105</PMID><DateCompleted><Year>1985</Year><Month>07</Month><Day>18</Day></DateCompleted><DateRevised><Year>2019</Year><Month>08</Month><Day>20</Day></DateRevised><Article PubModel="Print"><Journal><ISSN IssnType="Print">0036-5513</ISSN><JournalIssue CitedMedium="Print"><Volume>45</Volume><Issue>2</Issue><PubDate><Year>1985</Year><Month>Apr</Month></PubDate></JournalIssue><Title>Scandinavian journal of clinical and laboratory investigation</Title><ISOAbbreviation>Scand J Clin Lab Invest</ISOAbbreviation></Journal><ArticleTitle>Urinary cyclic AMP in spot urine of healthy children.</ArticleTitle><Pagination><MedlinePgn>185-8</MedlinePgn></Pagination><Abstract><AbstractText>We present reference values for the excretion of cAMP in spot urine collected between 09.00 and 12.00 hours in 143 healthy children aged 2-200 months. The excretion of cAMP was creatinine-corrected and expressed as a substance concentration ratio (UcAMP/crea)U due to a positive significant correlation between the excretion of cAMP and creatinine (r = 0.68, p less than 0.001). The mean value (95% significance limits) for (UcAMP/crea)U was 748 mumol/mol (254-2206 mumol/mol). A 
# logarithmic transformation of the ratio was used, since preliminary analysis showed uneven distribution; when the logarithmic transformation was used, the data appeared evenly distributed. There was no significant difference between the results for girls and boys. The value of lg(UcAMP/crea)U was related to the age or body surface area with decreasing values at higher age or body surface area. (r = -0.55 and r = -0.57, p less than 0.001). Spot urine for measurement of urinary cAMP instead of a 24 h collection appears preferable due to the practicability of the test in children.</AbstractText></Abstract><AuthorList CompleteYN="Y"><Author ValidYN="Y"><LastName>Thode</LastName><ForeName>J</ForeName><Initials>J</Initials></Author><Author ValidYN="Y"><LastName>Jacobsen</LastName><ForeName>B B</ForeName><Initials>BB</Initials></Author><Author ValidYN="Y"><LastName>Holmegaard</LastName><ForeName>S N</ForeName><Initials>SN</Initials></Author></AuthorList><Language>eng</Language><PublicationTypeList><PublicationType UI="D016428">Journal Article</PublicationType></PublicationTypeList></Article><MedlineJournalInfo><Country>England</Country><MedlineTA>Scand J Clin Lab Invest</MedlineTA><NlmUniqueID>0404375</NlmUniqueID><ISSNLinking>0036-5513</ISSNLinking></MedlineJournalInfo><ChemicalList><Chemical><RegistryNumber>AYI8EX34EU</RegistryNumber><NameOfSubstance UI="D003404">Creatinine</NameOfSubstance></Chemical><Chemical><RegistryNumber>E0399OZS9N</RegistryNumber><NameOfSubstance UI="D000242">Cyclic AMP</NameOfSubstance></Chemical></ChemicalList><CitationSubset>IM</CitationSubset><MeshHeadingList><MeshHeading><DescriptorName UI="D000293" MajorTopicYN="N">Adolescent</DescriptorName></MeshHeading><MeshHeading><DescriptorName UI="D002648" MajorTopicYN="N">Child</DescriptorName></MeshHeading><MeshHeading><DescriptorName UI="D002675" MajorTopicYN="N">Child, Preschool</DescriptorName></MeshHeading><MeshHeading><DescriptorName UI="D003404" MajorTopicYN="N">Creatinine</DescriptorName><QualifierName UI="Q000652" MajorTopicYN="N">urine</QualifierName></MeshHeading><MeshHeading><DescriptorName UI="D000242" MajorTopicYN="N">Cyclic AMP</DescriptorName><QualifierName UI="Q000652" MajorTopicYN="Y">urine</QualifierName></MeshHeading><MeshHeading><DescriptorName UI="D005260" MajorTopicYN="N">Female</DescriptorName></MeshHeading><MeshHeading><DescriptorName UI="D005919" MajorTopicYN="N">Glomerular Filtration Rate</DescriptorName></MeshHeading><MeshHeading><DescriptorName UI="D006801" MajorTopicYN="N">Humans</DescriptorName></MeshHeading><MeshHeading><DescriptorName UI="D007223" MajorTopicYN="N">Infant</DescriptorName></MeshHeading><MeshHeading><DescriptorName UI="D008297" MajorTopicYN="N">Male</DescriptorName></MeshHeading><MeshHeading><DescriptorName UI="D012016" MajorTopicYN="N">Reference Values</DescriptorName></MeshHeading></MeshHeadingList></MedlineCitation><PubmedData><History><PubMedPubDate PubStatus="pubmed"><Year>1985</Year><Month>4</Month><Day>1</Day></PubMedPubDate><PubMedPubDate PubStatus="medline"><Year>1985</Year><Month>4</Month><Day>1</Day><Hour>0</Hour><Minute>1</Minute></PubMedPubDate><PubMedPubDate PubStatus="entrez"><Year>1985</Year><Month>4</Month><Day>1</Day><Hour>0</Hour><Minute>0</Minute></PubMedPubDate></History><PublicationStatus>ppublish</PublicationStatus><ArticleIdList><ArticleId IdType="pubmed">2988105</ArticleId><ArticleId IdType="doi">10.3109/00365518509160993</ArticleId></ArticleIdList></PubmedData></PubmedArticle></PubmedArticleSet>


# URL = "https://www.ncbi.nlm.nih.gov/pmc/pmctopmid/"
# ACTION = "POST"
# formData = {

#     "idtype" : "auto",
#     "format" : "html",
#     "Ids" : "PMC2988105",
#     "force_pmc" : "on",
#     "convert_button": "Convert" 
# }
