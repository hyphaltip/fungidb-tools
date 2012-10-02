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

from datadev_templates import (make_perl_script, make_geneRecord,
                               make_geneParams, make_geneQuestions,
                               make_categories, make_queryList,
                               make_GenesByRNASeqEvidence, make_fungidb_conf,
                               make_gbrowseImageUrls, make_tuningManager,
                               make_attributions, make_contact_block,
                               make_url_block)

# Species information
GENUS = "Coccidioides"
SPECIES = "immitis"
STRAIN = "RS"
# From database
DBNAME = "C immitis saprobic hyphae and parasitic spherules"
GROUPS = (("Spherules", "Parasitic spherule"),
          ("Hyphae", "Saprobic hyphae"),
          )
# Study information
TITLE = "CimmComTran"
AUTHOR = "Taylor"
EXPERIMENT = "Comparative Transcriptomics"
PMID = '22911737'
CITATION = "Emily Whiston et al (Taylor lab at UC Berkeley) Comparative \
Transcriptomics of the Saprobic and Parasitic Growth Phases in \
Coccidioides spp."
SUMMARY = "TODO"
PROTOCOL = "TODO"
DESCRIPTION = "This study used comparative transcriptomics to identify gene \
expression differences between the saprobic and parasitic growth phases. They \
prepared Illumina mRNA sequencing libraries for saprobic-phase hyphae and \
parasitic-phase spherules in vitro for C. immitis isolate RS and C. posadasii \
isolate C735 in biological triplicate."
CONTACTS = ({'name': 'John'},)
URLS = ('',)


full_species = "{genus} {species}".format(genus=GENUS, species=SPECIES)
abbrev_species = "{genus}. {species}".format(genus=GENUS[0], species=SPECIES)
short_species = "{genus}{species}".format(genus=GENUS[0], species=SPECIES[:3])
full_strain = "{short_species}{strain}".format(short_species=short_species,
                                               strain=STRAIN)
pct_dbname = "percentile - {dbname}".format(dbname=DBNAME)
diff_dbname = "{dbname}-diff".format(dbname=DBNAME)

perl_dir = "{full_strain}".format(full_strain=full_strain)
perl_script = "{title}RnaSeq".format(title=TITLE)


print(make_perl_script(perl_dir=perl_dir, perl_script=perl_script,
                       dbname=DBNAME, diff_dbname=diff_dbname,
                       pct_dbname=pct_dbname))


graph = "{perl_script}_graph".format(perl_script=perl_script)
graph_display = "{abbrev_species} RNASeq - Graph".format(
    abbrev_species=abbrev_species)


print(make_geneRecord(graph=graph, graph_display=graph_display,
                      perl_dir=perl_dir, perl_script=perl_script))


qryname = "{title}RnaSeqProfiles".format(title=TITLE)
pct_qryname = "{title}RnaSeqPercentiles".format(title=TITLE)


print(make_geneParams(qryname=qryname, pct_qryname=pct_qryname, dbname=DBNAME,
                      pct_dbname=pct_dbname, display=EXPERIMENT))


fc_question = "GenesByRnaSeqFoldChange{title}".format(title=TITLE)
pct_question = "GenesByRnaSeqPercentile{title}".format(title=TITLE)
display = "{short_species} {experiment} Rna Seq".format(
    short_species=short_species, experiment=EXPERIMENT)
short_display = "{short_species} RNASeq".format(short_species=short_species)
fc_summary = "Identify <i>{full_species}</i> genes based on expression \
fold change.".format(full_species=full_species)
pct_summary = "Identify <i>{full_species}</i> genes based on expression \
percentiles.".format(full_species=full_species)


print(make_geneQuestions(fc_question=fc_question, pct_question=pct_question,
                         display=display, short_display=short_display,
                         graph=graph, qryname=qryname, pct_qryname=pct_qryname,
                         fc_summary=fc_summary, pct_summary=pct_summary,
                         fc_description=DESCRIPTION,
                         pct_description=DESCRIPTION))

print(make_categories(fc_question=fc_question, pct_question=pct_question))

print(make_queryList(short_species=short_species, full_species=full_species))

print(make_GenesByRNASeqEvidence(short_species=short_species,
                                 study=EXPERIMENT, fc_question=fc_question,
                                 pct_question=pct_question))


long_title = "RnaSeq{title}".format(title=TITLE)
study_name = "{full_strain}_{author}_{experiment}_rnaSeq_RSRC".format(
    full_strain=full_strain, author=AUTHOR, experiment=EXPERIMENT.replace(' ',
                                                                          ''))
key = "{full_strain} mRNA RNASeq {author} {experiment}".format(
    full_strain=full_strain, author=AUTHOR, experiment=EXPERIMENT)
sep = '\n' + ' ' * 18
table = sep.join(":'{}' {} ;".format(l, s) for s, l in GROUPS)


print(make_fungidb_conf(track=long_title, feature=study_name,
                        table=table, key=key, citation=CITATION))

print(make_gbrowseImageUrls(track=long_title))

print(make_tuningManager(dbname=DBNAME, perl_dir=perl_dir,
                         perl_script=perl_script, description=DESCRIPTION))

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


print(make_attributions(study_name=study_name, pmid=PMID,
                        attr_display=attr_display,
                        contact_block=make_contact_block(CONTACTS),
                        summary=SUMMARY, protocol=PROTOCOL,
                        description=DESCRIPTION,
                        url_block=make_url_block(URLS)))
