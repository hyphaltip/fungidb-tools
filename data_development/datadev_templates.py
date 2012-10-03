"""Templates to generate data development files.

2012/10/02
Edward Liaw
"""


def make_perl_script(**kwargs):
    """Usage:
    print(make_perl_script(perl_dir=perl_dir, perl_script=perl_script,
                           dbname=DBNAME, diff_dbname=diff_dbname,
                           pct_dbname=pct_dbname))
    """
    return """
mkdir $PROJECT_HOME/ApiCommonWebsite/View/lib/perl/GraphPackage/FungiDB/{perl_dir}
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
  $self->setPctProfileSet(\"{pct_dbname}\");
  $self->setColor(\"#29ACF2\");
  $self->makeGraphs(@_);

  return $self;
}}


1;
""".format(**kwargs)


def make_geneRecord(**kwargs):
    """Usage:
    print(make_geneRecord(graph=graph, graph_display=graph_display,
                          perl_dir=perl_dir, perl_script=perl_script))
    """
    return """
#< $PROJECT_HOME/ApiCommonShared/Model/lib/wdk/apiCommonModel/records/geneRecord.xml

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
""".format(**kwargs)


def make_geneParams(**kwargs):
    """Usage:
    print(make_geneParams(qryname=qryname, pct_qryname=pct_qryname, dbname=DBNAME,
                          pct_dbname=pct_dbname, display=EXPERIMENT))
    """
    return """
#< $PROJECT_HOME/ApiCommonShared/Model/lib/wdk/apiCommonModel/questions/params/geneParams.xml

        <sqlQuery name=\"{qryname}\" includeProjects=\"FungiDB\">
            <column name=\"display\"/>
            <column name=\"internal\"/>
            <column name=\"term\"/>
            <sql>
                Select name as term,
                profile_set_id as internal,
                \'{display}\' as display
                from apidb.profileset
                where name like \'{dbname}\'
            </sql>
        </sqlQuery>

        <sqlQuery name=\"{pct_qryname}\" includeProjects=\"FungiDB\">
            <column name=\"display\"/>
            <column name=\"internal\"/>
            <column name=\"term\"/>
            <sql>
                Select name as term,
                profile_set_id as internal,
                \'{display}\' as display
                from apidb.profileset
                where name like \'{pct_dbname}\'
            </sql>
        </sqlQuery>
""".format(**kwargs)


def make_geneQuestions(**kwargs):
    """Usage:
    print(make_geneQuestions(fc_question=fc_question, pct_question=pct_question,
                             display=display, short_display=short_display,
                             graph=graph, qryname=qryname, pct_qryname=pct_qryname,
                             fc_summary=fc_summary, pct_summary=pct_summary,
                             fc_description=DESCRIPTION,
                             pct_description=DESCRIPTION))
    """
    return """
#< $PROJECT_HOME/ApiCommonShared/Model/lib/wdk/apiCommonModel/questions/geneQuestions.xml

    <question name=\"{fc_question}\" includeProjects=\"FungiDB\"
        displayName=\"{display} (fold change)\"
        shortDisplayName=\"{short_display} fc\"
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
            {fc_summary}
            ]]>
        </summary>

        <description>
            <![CDATA[
            {fc_description}
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

    <question name=\"{pct_question}\" includeProjects=\"FungiDB\"
        displayName=\"{display} (percentile)\"
        shortDisplayName=\"{short_display} pct\"
        searchCategory=\"Transcript Expression\"
        queryRef=\"GeneId.GenesByGenericPercentile\"
        recordClassRef=\"GeneRecordClasses.GeneRecordClass\">

        <paramRef ref=\"geneParams.profileset_generic\" queryRef=\"GeneVQ.{pct_qryname}\"/>

        <attributesList
            summary=\"organism,product,min_percentile_chosen,max_percentile_chosen,{graph}\"
            sorting=\"percentile desc\"
            />

        <summary>
            <![CDATA[
            {pct_summary}
            ]]>
        </summary>

        <description>
            <![CDATA[
            {pct_description}
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
""".format(**kwargs)


def make_categories(**kwargs):
    """Usage:
    print(make_categories(fc_question=fc_question, pct_question=pct_question))
    """
    return """
#< $PROJECT_HOME/ApiCommonShared/Model/lib/wdk/apiCommonModel/questions/categories.xml

            <questionRef includeProjects=\"FungiDB\">GeneQuestions.{fc_question}</questionRef>
            <questionRef includeProjects=\"FungiDB\">GeneQuestions.{pct_question}</questionRef>
""".format(**kwargs)


def make_queryList(**kwargs):
    """Usage:
    print(make_queryList(abbrev_species=abbrev_species, full_species=full_species))
    """
    return """
#< $PROJECT_HOME/ApiCommonWebsite/Site/webapp/WEB-INF/tags/site/queryList.tag

<c:when test=\"${{prefix == \'{abbrev_species}\'}}\">
    <c:set var=\"org\" value=\"{full_species}\"/>
</c:when>
""".format(**kwargs)


def make_GenesByRNASeqEvidence(**kwargs):
    """Usage:
    print(make_GenesByRNASeqEvidence(abbrev_species=abbrev_species,
                                     study=EXPERIMENT, fc_question=fc_question,
                                     pct_question=pct_question))
    """
    return """
#< $PROJECT_HOME/ApiCommonWebsite/Site/webapp/wdkCustomization/jsp/questions/InternalQuestions.GenesByRNASeqEvidence.form.jsp

{abbrev_species}study:{study},GeneQuestions.{fc_question},GeneQuestions.{pct_question}
""".format(**kwargs)


def make_fungidb_conf(**kwargs):
    """Usage:
    print(make_fungidb_conf(track=long_title, feature=study_name,
                            table=table, key=key, citation=CITATION))
    """
    return """
#< $PROJECT_HOME/ApiCommonWebsite/Site/conf/gbrowse.conf/fungidb.conf

[{track}]
feature      = NextGenSeq:{feature}
sqlName      = NextGenSeq:coverageLogSubtracks
sqlParam     = edname:\'{feature}\'&&operator:=&&negativeValuesField:multiple&&subtrackField:is_reversed
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
""".format(**kwargs)


def make_gbrowseImageUrls(**kwargs):
    """Usage:
    print(make_gbrowseImageUrls(track=long_title))
    """
    return """
#< $PROJECT_HOME/ApiCommonShared/Model/lib/xml/gbrowseImageUrls.xml

    <track name="{track}" />
""".format(**kwargs)


def make_tuningManager(**kwargs):
    """Usage:
    print(make_tuningManager(dbname=DBNAME, perl_dir=perl_dir,
                             perl_script=perl_script, description=DESCRIPTION))
    """
    return """
#< $PROJECT_HOME/ApiCommonData/Load/lib/xml/tuningManager.xml

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
""".format(**kwargs)


CONTACT_ORDER = ('name', 'email', 'institution', 'address', 'city', 'state',
                 'country', 'zip')
CONTACT_HEAD = "      <contact isPrimaryContact=\"{primary}\">"
CONTACT_BODY = "        <{key}>{val}</{key}>"
CONTACT_TAIL = "      </contact>"
URL_TEMPLATE = """      <link>
        <!-- downloadFile, SupplementaryData, sampleStrategy, publicUrl -->
        <type>publicUrl</type>
        <url>{url}</url>
        <linkDescription></linkDescription>
      </link>"""


def make_contact_block(contacts):
    """Generate xml section for contacts."""
    contact_block = []
    primary = 'true'
    for contact in contacts:
        contact_block.append(CONTACT_HEAD.format(primary=primary))
        primary = 'false'
        contact_block.append('\n'.join(
            CONTACT_BODY.format(key=next_field, val=contact[next_field])
            for next_field in CONTACT_ORDER if next_field in contact))
        contact_block.append(CONTACT_TAIL)
    return '\n'.join(contact_block)


def make_url_block(urls):
    """Generate url section for links."""
    return '\n'.join(URL_TEMPLATE.format(url=url) for url in urls)


def make_attributions(**kwargs):
    """Usage:
    print(make_attributions(study_name=study_name, pmid=PMID,
                            attr_display=attr_display,
                            contact_block=make_contact_block(CONTACTS),
                            summary=SUMMARY, protocol=PROTOCOL,
                            description=DESCRIPTION,
                            url_block=make_url_block(URLS)))
    """
    return """
#< $PROJECT_HOME/ApiCommonShared/Model/lib/xml/dataSourceAttributions/FungiDB.xml

  <dataSourceAttribution resource=\"{study_name}\" overridingType=\"\" overridingSubtype=\"\" ignore=\"False\">

    <publications>
      <publication pmid=\"{pmid}\"/>
    </publications>

    <contacts>
{contact_block}
    </contacts>

    <displayName>{attr_display}</displayName>
    <summary>
      <![CDATA[
      {summary}
      ]]>
    </summary>
    <protocol>
      <![CDATA[
      {protocol}
      ]]>
    </protocol>
    <caveat><![CDATA[]]></caveat>
    <acknowledgement><![CDATA[]]></acknowledgement>
    <releasePolicy></releasePolicy>
    <description>
      <![CDATA[
      {description}
      ]]>
    </description>

    <links>
{url_block}
    </links>

    <wdkReference recordClass=\"\" type=\"\" name=\"\"/>

  </dataSourceAttribution>

""".format(**kwargs)
