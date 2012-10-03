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
GENUS = "Coprinopsis"
SPECIES = "cinerea"
STRAIN = "Ok7h130"
# From database
DBNAME = "C cinereus hyphal growth expression"
GROUPS = (("Cc-9D", "9 days - Tip"),
          ("Cc-15D", "15 days - colony"),
          )
# Study information
TITLE = "CcinHyphalGrowth"
AUTHOR = "Stajich"
EXPERIMENT = "Hyphal Growth Time Series"
PMID = ''
CITATION = "Jason Stajich et al (Stajich lab at UC Riverside) Unpublished data"
SUMMARY = "Identify <i>Coprinopsis cinerea</i> genes based on fold change \
expression difference between a \"comparison\" and a \"reference\" sample."
PROTOCOL = ""
DESCRIPTION = "Unpublished data from <a href=\"http://lab.stajich.org\">\
Stajich lab</a> at UC Riverside representing hyphal sections from 2 time points (9 days and 15 \
days) of hyphal growth on solid media for <i>Coprinopsis cinerea</i>. This experiment is \
intended to compare genes expressed on the hyphal edge and in the colony."
CONTACTS = ({'name': 'Jason Stajich',
             'email': 'jason.stajich@ucr.edu',
             'institution': 'University of California, Riverside',
             'address': '900 University Ave',
             'city': 'Riverside',
             'state': 'California',
             'country': 'USA',
             'zip': '92521',
             },)
URLS = ()


def main():
    make_rnaseq(genus=GENUS, species=SPECIES, strain=STRAIN, dbname=DBNAME,
                groups=GROUPS, title=TITLE, author=AUTHOR,
                experiment=EXPERIMENT, pmid=PMID, citation=CITATION,
                summary=SUMMARY, protocol=PROTOCOL, description=DESCRIPTION,
                contacts=CONTACTS, urls=URLS)


if __name__ == '__main__':
    main()
