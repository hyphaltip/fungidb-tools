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

# Species information
GENUS = "Coccidioides"
SPECIES = "immitis"
STRAIN = "RS"
# Study information
AUTHOR = "Taylor"
EXPERIMENT = "Comparative Transcriptomics"
CITATION = "TODO"
DESCRIPTION = "TODO"
TITLE = "CimmComTran"
# From database
DBNAME = "C immitis saprobic hyphae and parasitic spherules"
GROUPS = (("Spherules", "Parasitic spherule"),
          ("Hyphae", "Saprobic hyphae"),
          )

full_species = "{genus} {species}".format(genus=GENUS, species=SPECIES)
abbrev_species = "{genus}. {species}".format(genus=GENUS[0], species=SPECIES)
short_species = "{genus}{species}".format(genus=GENUS[0], species=SPECIES[:3])
full_strain = "{short_species}{strain}".format(short_species=short_species,
                                               strain=STRAIN)
per_dbname = "percentile - {dbname}".format(dbname=DBNAME)
diff_dbname = "{dbname}-diff".format(dbname=DBNAME)

perl_dir = "{full_strain}".format(full_strain=full_strain)
perl_script = "RnaSeq{title}".format(title=TITLE)
print("""mkdir $PROJECT_HOME/ApiCommonWebsite/View/lib/perl/GraphPackage/FungiDB/{perl_dir}
touch $PROJECT_HOME/ApiCommonWebsite/View/lib/perl/GraphPackage/FungiDB/{perl_dir}/{perl_script}.pm
#< $PROJECT_HOME/ApiCommonWebsite/View/lib/perl/GraphPackage/FungiDB/{perl_dir}/{perl_script}.pm

package ApiCommonWebsite::View::GraphPackage::FungiDB::{perl_dir}::{perl_script};

use strict;
use vars qw( @ISA );

@ISA = qw( ApiCommonWebsite::View::GraphPackage::SimpleRNASeq );
use ApiCommonWebsite::View::GraphPackage::SimpleRNASeq;


sub init {{
  my $self = shift;

  $self->SUPER::init(@_);

  #$self->setPlotWidth(800);
  #$self->setBottomMarginSize(7);

  $self->setAdditionalRCode(\"colnames(profile.df) =  sub(\\\".fastq\\\", \\\"\\\", colnames(profile.df));\");
  $self->setMinRpkmProfileSet(\"{dbname}\");
  $self->setDiffRpkmProfileSet(\"{diff_dbname}\");
  $self->setPctProfileSet(\"{per_dbname}\");
  $self->setColor(\"#29ACF2\");
  $self->makeGraphs(@_);

  return $self;
}}


1;

""".format(perl_dir=perl_dir, perl_script=perl_script, dbname=DBNAME,
           diff_dbname=diff_dbname, per_dbname=per_dbname))

graph = "{perl_script}_graph".format(perl_script=perl_script)
graph_display = "{abbrev_species} RNASeq - Graph".format(
    abbrev_species=abbrev_species)
print("""#< $PROJECT_HOME/ApiCommonShared/Model/lib/wdk/apiCommonModel/records/geneRecord.xml

                <textAttribute name=\"{graph}\"
                    displayName=\"{graph_display}\"
                    attributeCategory=\"trasexpr\"
                    inReportMaker=\"false\" truncateTo=\"100000\" sortable=\"false\"
                    includeProjects=\"FungiDB\">
                    <text>
                        <![CDATA[
                        <img src=\"/cgi-bin/dataPlotter.pl?type={perl_dir}::{perl_script}&project_id=FungiDB&fmt=png&id=$$primary_key$$&thumb=1&vp=coverage\"/>
                        ]]>
                    </text>
                </textAttribute>

""".format(graph=graph, graph_display=graph_display, perl_dir=perl_dir,
           perl_script=perl_script))

qryname = "{title}RnaSeqProfiles".format(title=TITLE)
per_qryname = "{title}RnaSeqPercentiles".format(title=TITLE)
print("""#< $PROJECT_HOME/ApiCommonShared/Model/lib/wdk/apiCommonModel/questions/params/geneParams.xml

        <sqlQuery name=\"{qryname}\" includeProjects=\"FungiDB\">
            <column name=\"display\"/>
            <column name=\"internal\"/>
            <column name=\"term\"/>
            <sql>
                Select name as term,
                profile_set_id as internal,
                \'{experiment}\' as display
                from apidb.profileset
                where name like \'{dbname}\'
            </sql>
        </sqlQuery>

        <sqlQuery name=\"{per_qryname}\" includeProjects=\"FungiDB\">
            <column name=\"display\"/>
            <column name=\"internal\"/>
            <column name=\"term\"/>
            <sql>
                Select name as term,
                profile_set_id as internal,
                \'{experiment}\' as display
                from apidb.profileset
                where name like \'{per_dbname}\'
            </sql>
        </sqlQuery>

""".format(qryname=qryname, per_qryname=per_qryname, dbname=DBNAME,
           per_dbname=per_dbname, experiment=EXPERIMENT))

question = "GenesByRnaSeqFoldChange{title}".format(title=TITLE)
per_question = "GenesByRnaSeqPercentile{title}".format(title=TITLE)
display = "{short_species} {experiment} Rna Seq (fold change)".format(
    short_species=short_species, experiment=EXPERIMENT)
per_display = "{short_species} {experiment} Rna Seq (percentile)".format(
    short_species=short_species, experiment=EXPERIMENT)
short_display = "{short_species} RNASeq fc".format(short_species=short_species)
summary = "Identify <i>{full_species}</i> genes based on expression fold \
change.".format(full_species=full_species)
print("""#< $PROJECT_HOME/ApiCommonShared/Model/lib/wdk/apiCommonModel/questions/geneQuestions.xml

    <question name=\"{question}\" includeProjects=\"FungiDB\"
        displayName=\"{display}\"
        shortDisplayName=\"{short_display}\"
        searchCategory=\"Transcript Expression\"
        queryRef=\"GeneId.GenesByGenericFoldChange\"
        recordClassRef=\"GeneRecordClasses.GeneRecordClass\">

        <attributesList
            summary=\"organism,product,fold_change_chosen,chose_group_two,chose_group_one,{graph}\"/>

        <paramRef ref=\"geneParams.profileset_generic\" queryRef=\"GeneVQ.{qryname}\"/>
        <paramRef ref=\"geneParams.global_min_max\" visible=\"false\"/>
        <sqlParamValue name=\"isLogged\">0</sqlParamValue>
        <sqlParamValue name=\"shift\">1</sqlParamValue>

        <summary>
            <![CDATA[
            {summary}
            ]]>
        </summary>

        <description>
            <![CDATA[
            {description}
            ]]>
        </description>

        <dynamicAttributes>
            <columnAttribute name=\"fold_change_avg\" displayName=\"Fold Change (Avg)\" align=\"center\"/>
            <columnAttribute name=\"fold_change_chosen\" displayName=\"Fold Change\" align=\"center\"/>
            <columnAttribute name=\"avg_group_one\" displayName=\"Avg Comp (log2)\" align=\"center\"/>
            <columnAttribute name=\"avg_group_two\" displayName=\"Avg Ref (log2)\" align=\"center\"/>
            <columnAttribute name=\"min_group_one\" displayName=\"Min Comp (log2)\" align=\"center\"/>
            <columnAttribute name=\"min_group_two\" displayName=\"Min Ref (log2)\" align=\"center\"/>
            <columnAttribute name=\"max_group_one\" displayName=\"Max Comp (log2)\" align=\"center\"/>
            <columnAttribute name=\"max_group_two\" displayName=\"Max Ref (log2)\" align=\"center\"/>
            <columnAttribute name=\"chose_group_one\" displayName=\"Chosen Comp (log2)\" align=\"center\"/>
            <columnAttribute name=\"chose_group_two\" displayName=\"Chosen Ref (log2)\" align=\"center\"/>
            <columnAttribute name=\"time_of_min_expr\" displayName=\"Time of Min Expression\" align=\"center\"/>
            <columnAttribute name=\"time_of_max_expr\" displayName=\"Time of Max Expression\" align=\"center\"/>
        </dynamicAttributes>

        <propertyList name=\"specificAttribution\">
            <value></value>
        </propertyList>
    </question>

    <question name=\"{per_question}\" includeProjects=\"FungiDB\"
        displayName=\"{per_display}\"
        shortDisplayName=\"{short_display}\"
        searchCategory=\"Transcript Expression\"
        queryRef=\"GeneId.GenesByGenericPercentile\"
        recordClassRef=\"GeneRecordClasses.GeneRecordClass\">

        <paramRef ref=\"geneParams.profileset_generic\" queryRef=\"GeneVQ.{per_qryname}\"/>

        <attributesList
            summary=\"organism,product,min_percentile_chosen,max_percentile_chosen,{graph}\"
            sorting=\"percentile desc\"
            />

        <summary>
            <![CDATA[
            {summary}
            ]]>
        </summary>


        <description>
            <![CDATA[
            {description}
            ]]>
        </description>


        <dynamicAttributes>
            <columnAttribute name=\"min_percentile_chosen\" displayName=\"Min %ile (Within Chosen Samples)\" align=\"center\"/>
            <columnAttribute name=\"max_percentile_chosen\" displayName=\"Max %ile (Within Chosen Samples)\" align=\"center\"/>
        </dynamicAttributes>

        <propertyList name=\"specificAttribution\">
            <value></value>
        </propertyList>
    </question>

""".format(question=question, per_question=per_question, display=display,
           per_display=per_display, short_display=short_display, graph=graph,
           qryname=qryname, per_qryname=per_qryname, summary=summary,
           description=DESCRIPTION))

print("""#< $PROJECT_HOME/ApiCommonShared/Model/lib/wdk/apiCommonModel/questions/categories.xml

            <questionRef includeProjects=\"FungiDB\">GeneQuestions.{question}</questionRef>
            <questionRef includeProjects=\"FungiDB\">GeneQuestions.{per_question}</questionRef>

""".format(question=question, per_question=per_question))

print("""#< $PROJECT_HOME/ApiCommonWebsite/Site/webapp/wdkCustomization/jsp/questions/InternalQuestions.GenesByRNASeqEvidence.form.jsp

{short_species}study:{experiment},GeneQuestions.{question},GeneQuestions.{per_question}

""".format(short_species=short_species, experiment=EXPERIMENT,
           question=question, per_question=per_question))

print("""#< $PROJECT_HOME/ApiCommonWebsite/Site/webapp/WEB-INF/tags/site/queryList.tag

<c:when test=\"${{prefix == \'{short_species}\'}}\">
    <c:set var=\"org\" value=\"{full_species}\"/>
</c:when>

""".format(short_species=short_species, full_species=full_species))

long_title = "RnaSeq{title}".format(title=TITLE)
study_name = "{full_strain}_{author}_{experiment}_rnaSeq_RSRC".format(
    full_strain=full_strain, author=AUTHOR, experiment=EXPERIMENT.replace(' ',
                                                                          ''))
key = "{full_strain} mRNA RNASeq {author} {experiment}".format(
    full_strain=full_strain, author=AUTHOR, experiment=EXPERIMENT)
sep = '\n' + ' ' * 18
table = sep.join(":'{}' {} ;".format(l, s) for s, l in GROUPS)
print("""#< $PROJECT_HOME/ApiCommonWebsite/Site/conf/gbrowse.conf/fungidb.conf

[{long_title}]
feature      = NextGenSeq:{study_name}
sqlName      = NextGenSeq:coverageLogSubtracks
sqlParam     = edname:\'{study_name}\'&&operator:=&&negativeValuesField:multiple&&subtrackField:is_reversed
category     = Transcript Expression Evidence: B. RNA-seq
glyph        = xyplot
graph_type   = boxes
bump density = 1
scale        = right
bgcolor      = blue
part_color   = sub {{ GBrowse::Display::colorByRnaSeq(shift,\'blue\') }}
height       = 25
min_score    = -5
max_score    = 10
clip         = 1
label        = 0
subtrack select = Sample tag_value sample;
subtrack table  = {table}
key          = {key}
group_label  = 1
citation     = {citation}

""".format(long_title=long_title, study_name=study_name, table=table, key=key,
           citation=CITATION))

print("""#< $PROJECT_HOME/ApiCommonShared/Model/lib/xml/gbrowseImageUrls.xml


    <track name="{long_title}" />

""".format(long_title=long_title))

print("""#< $PROJECT_HOME/ApiCommonData/Load/lib/xml/tuningManager.xml

select \'{dbname}\' as profile_name,
       \'{perl_dir}::{perl_script}\' as module,
       \'RNA Seq\' as display_name,
       \'{description}\' as description,
       \'Sample Time point (hours)\' as x_axis,
       \'log2 of the transcript levels of reads per kilobase of exon model per million mapped reads (RPKM).  Stacked bars indicate unique and non-uniquely mapped sequences.  Non-Unique sequences are plotted to indicate the maximum expression potential of this gene.
       \' as y_axis,
       10 as order_num,
       \'TRUE\' as mainOpen,
       \'FALSE\' as dataOpen,
       \'coverage,percentile\' as visible_parts,
       \'\' as dataTable,
       \'expression\' as type,
       \'\' as attribution
    from dual

    UNION

""".format(dbname=DBNAME, perl_dir=perl_dir, perl_script=perl_script,
           description=DESCRIPTION))

print("""#<
bldw ApiCommonWebsite/Site $WWW/etc/webapp.prop
bld ApiCommonShared/Model
instance_manager manage FungiDB reload fungidb.edliaw
cd $HOME/GUS/gusApps
gusenv
tuningManager --instance fungbl3n --propFile $WWW/gus_home/config/tuningManagerProp.xml --doUpdate --tables 'ProfileGraphs,ProfileGraphDescrip' --configFile $WWW/project_home/ApiCommonData/Load/lib/xml/tuningManager.xml
""")
