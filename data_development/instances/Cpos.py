#!/usr/bin/env python
"""Generate data development text for RNAseq experiments.

Usage: Change the values of the first few strings to match the experiment
information.  Then run:

    python rnaseq_data_dev.py > cimm.txt

You can follow filenames in VIM (gf) and run shell commands by selecting the
line (V) and (:w !sh).  Filenames are preceded by '#< ' in the output file.

2012/09/27
Edward Liaw
"""
from rnaseq import make_rnaseq

# Species information
GENUS = "Coccidioides"
SPECIES = "posadasii"
STRAIN = "C735"
# From database
DBNAME = "C. posadasii saprobic hyphae and parasitic spherules"
GROUPS = (("Spherules", "Parasitic spherule"),
          ("Hyphae", "Saprobic hyphae"),
          )
# Study information
TITLE = "CposComTran"
AUTHOR = "Taylor"
EXPERIMENT = "Comparative Transcriptomics"
PMID = '22911737'
CITATION = "Emily Whiston et al (Taylor lab at UC Berkeley) Comparative \
Transcriptomics of the Saprobic and Parasitic Growth Phases in \
Coccidioides spp."
SUMMARY = "Comparative transcriptomics were used to identify gene \
expression differences between the saprobic and parasitic growth phases of \
Coccidiodes immitis and C. posadasii. Of the 9,910 total predicted genes in \
Coccidioides, 1,298 genes were observed to be up-regulated in the saprobic \
phase of both C. immitis and C. posadasii and 1,880 genes were observed to be \
up-regulated in the parasitic phase of both species"
PROTOCOL = "Illumina mRNA sequencing libraries for saprobic-phase hyphae and \
parasitic-phase spherules in vitro for C. immitis isolate RS and C. posadasii \
isolate C735 were prepared in biological triplicate"
DESCRIPTION = "Comparative transcriptomics were used to identify gene \
expression differences between the saprobic and parasitic growth phases. \
The results highlighted a number of genes that may be crucial to dimorphic \
phase-switching and virulence in Coccidioides."
CONTACTS = ({'name': 'Emily Whiston',
             'email': 'whiston@berkeley.edu',
             'institution': 'University of California, Berkeley',
             },)
URLS = ('http://trace.ncbi.nlm.nih.gov/Traces/sra/?study=SRP013923',)


def main():
    make_rnaseq(genus=GENUS, species=SPECIES, strain=STRAIN, dbname=DBNAME,
                groups=GROUPS, title=TITLE, author=AUTHOR,
                experiment=EXPERIMENT, pmid=PMID, citation=CITATION,
                summary=SUMMARY, protocol=PROTOCOL, description=DESCRIPTION,
                contacts=CONTACTS, urls=URLS)


if __name__ == '__main__':
    main()
