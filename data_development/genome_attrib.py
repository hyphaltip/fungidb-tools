#!/usr/bin/env python
"""Template for data source attribution xml.

2012/10/01
Edward Liaw
"""

from datadev_templates import (make_attributions, make_contact_block,
                               make_url_block)

GENUS = "Coccidioides"
SPECIES = "posadasii"
STRAIN = "C735"
AUTHOR = "Taylor"
EXPERIMENT = "Comparative Transcriptomics"
PMID = '22911737'
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


short_species = "{genus}{species}".format(genus=GENUS[0], species=SPECIES[:3])
abbrev_strain = "{short_species}{strain}".format(short_species=short_species,
                                                 strain=STRAIN)
full_strain = "{genus} {species} {strain}".format(genus=GENUS, species=SPECIES,
                                                  strain=STRAIN)
study_name = "{abbrev_strain}_primary_genome_RSRC".format(
    abbrev_strain=abbrev_strain)
attr_display = "{full_strain} Sequence and Annotation".format(
    full_strain=full_strain)


print(make_attributions(study_name=study_name, pmid=PMID,
                        attr_display=attr_display,
                        contact_block=make_contact_block(CONTACTS),
                        summary=SUMMARY, protocol=PROTOCOL,
                        description=DESCRIPTION,
                        url_block=make_url_block(URLS)))
