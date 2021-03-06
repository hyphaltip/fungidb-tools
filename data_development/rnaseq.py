#!/usr/bin/env python
"""Generate data development text for RNAseq experiments.

Usage: Change the values of the first few strings to match the experiment
information.  Then run:

    python rnaseq.py > cpos.txt

You can follow filenames in VIM (gf) and run shell commands by selecting the
line (V) and (:w !sh).  Filenames are preceded by '#< ' in the output file.

2012/09/27
Edward Liaw
"""

from datadev_templates import (make_perl_script, make_geneRecord,
                               make_geneParams, make_geneQuestions,
                               make_categories, make_queryList,
                               make_GenesByRNASeqEvidence, make_fungidb_conf,
                               make_gbrowseImageUrls, make_tuningManager,
                               make_attributions, make_contact_block,
                               make_url_block)

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


def make_rnaseq(genus, species, strain, dbname, groups, title, author,
                experiment, pmid, citation, summary, protocol, description,
                contacts, urls):
    """Usage:
    make_rnaseq(genus=GENUS, species=SPECIES, strain=STRAIN, dbname=DBNAME,
                groups=GROUPS, title=TITLE, author=AUTHOR,
                experiment=EXPERIMENT, pmid=PMID, citation=CITATION,
                summary=SUMMARY, protocol=PROTOCOL, description=DESCRIPTION,
                contacts=CONTACTS, urls=URLS)
    """
    full_species = "{genus} {species}".format(genus=genus, species=species)
    short_species = "{genus}.{species}".format(genus=genus[0], species=species)
    abbrev_species = "{genus}{species}".format(genus=genus[0],
                                               species=species[:3])
    abbrev_strain = "{abbrev_species}{strain}".format(
        abbrev_species=abbrev_species, strain=strain)
    pct_dbname = "percentile - {dbname}".format(dbname=dbname)
    diff_dbname = "{dbname}-diff".format(dbname=dbname)

    perl_dir = "{abbrev_strain}".format(abbrev_strain=abbrev_strain)
    perl_script = "{title}RnaSeq".format(title=title)

    print(make_perl_script(perl_dir=perl_dir, perl_script=perl_script,
                           dbname=dbname, diff_dbname=diff_dbname,
                           pct_dbname=pct_dbname))

    graph = "{perl_script}_graph".format(perl_script=perl_script)
    graph_display = "{short_species} {experiment} RNASeq - Graph".format(
        short_species=short_species, experiment=experiment)

    print(make_geneRecord(graph=graph, graph_display=graph_display,
                          perl_dir=perl_dir, perl_script=perl_script))

    qryname = "{title}RnaSeqProfiles".format(title=title)
    pct_qryname = "{title}RnaSeqPercentiles".format(title=title)

    print(make_geneParams(qryname=qryname, pct_qryname=pct_qryname,
                          dbname=dbname, pct_dbname=pct_dbname,
                          display=experiment))

    fc_question = "GenesByRnaSeqFoldChange{title}".format(title=title)
    pct_question = "GenesByRnaSeqPercentile{title}".format(title=title)
    display = "{abbrev_species} {experiment} Rna Seq".format(
        abbrev_species=abbrev_species, experiment=experiment)
    short_display = "{abbrev_species} RNASeq".format(
        abbrev_species=abbrev_species)
    fc_summary = "Identify <i>{full_species}</i> genes based on expression \
fold change.".format(full_species=full_species)
    pct_summary = "Identify <i>{full_species}</i> genes based on expression \
percentiles.".format(full_species=full_species)

    print(make_geneQuestions(fc_question=fc_question, pct_question=pct_question,
                             display=display, short_display=short_display,
                             graph=graph, qryname=qryname,
                             pct_qryname=pct_qryname, fc_summary=fc_summary,
                             pct_summary=pct_summary,
                             fc_description=description,
                             pct_description=description))

    print(make_categories(fc_question=fc_question, pct_question=pct_question))

    print(make_queryList(abbrev_species=abbrev_species,
                         full_species=full_species))

    print(make_GenesByRNASeqEvidence(abbrev_species=abbrev_species,
                                     study=experiment, fc_question=fc_question,
                                     pct_question=pct_question))

    long_title = "RnaSeq{title}".format(title=title)
    study_name = "{abbrev_strain}_{author}_{experiment}_rnaSeq_RSRC".format(
        abbrev_strain=abbrev_strain, author=author,
        experiment=experiment.replace(' ', ''))
    key = "{abbrev_strain} mRNA RNASeq {author} {experiment}".format(
        abbrev_strain=abbrev_strain, author=author, experiment=experiment)
    sep = '\n' + ' ' * 18
    table = sep.join(":'{}' {} ;".format(l, s) for s, l in groups)

    print(make_fungidb_conf(track=long_title, feature=study_name,
                            table=table, key=key, citation=citation))

    print(make_gbrowseImageUrls(track=long_title))

    print(make_tuningManager(dbname=dbname, perl_dir=perl_dir,
                             perl_script=perl_script, description=description))

    print("""
#<
bldw ApiCommonWebsite/Site $WWW/etc/webapp.prop
bld ApiCommonShared/Model
instance_manager manage FungiDB reload fungidb.edliaw
cd $HOME/GUS/gusApps
gusenv
tuningManager --instance fungbl3n --propFile $WWW/gus_home/config/tuningManagerProp.xml --doUpdate --tables 'ProfileGraphs,ProfileGraphDescrip' --configFile $WWW/project_home/ApiCommonData/Load/lib/xml/tuningManager.xml
    """)

    attr_display = "{display} Expression Data".format(display=display)

    print(make_attributions(study_name=study_name, pmid=pmid,
                            attr_display=attr_display,
                            contact_block=make_contact_block(contacts),
                            summary=summary, protocol=protocol,
                            description=description,
                            url_block=make_url_block(urls)))


def main():
    make_rnaseq(genus=GENUS, species=SPECIES, strain=STRAIN, dbname=DBNAME,
                groups=GROUPS, title=TITLE, author=AUTHOR,
                experiment=EXPERIMENT, pmid=PMID, citation=CITATION,
                summary=SUMMARY, protocol=PROTOCOL, description=DESCRIPTION,
                contacts=CONTACTS, urls=URLS)


if __name__ == '__main__':
    main()
