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
GENUS = "Rhizopus"
SPECIES = "oryzae"
STRAIN = "99880"
# From database
DBNAME = "R oryzae hyphal growth on solid media"
GROUPS = (("RO3H", "Ro 3 hrs"),
          ("RO5H", "Ro 5 hrs"),
          ("RO20H", "Ro 20 hrs"),
          )
# Study information
TITLE = "RoryHyphalGrowth"
AUTHOR = "Stajich"
EXPERIMENT = "Hyphal Growth Time Series"
PMID = ''
CITATION = "Jason Stajich et al (Stajich lab at UC Berkeley) Unpublished data"
SUMMARY = "Identify <i>Rhizopus oryzae</i> genes based on fold change \
expression difference between a \"comparison\" and a \"reference\" sample."
PROTOCOL = ""
DESCRIPTION = "Unpublished data from <a href=\"http://lab.stajich.org\">\
Stajich lab</a> at UC Riverside representing 3 time points (3hrs, 5hr, and \
20hrs) of hyphal growth on solid media for <i>Rhizopus oryzae</i>."
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
