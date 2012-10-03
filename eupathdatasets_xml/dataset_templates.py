"""Templates to make dataset xmls.

2012/10/02
Edward Liaw
"""


def make_fungidb_xml(**kwargs):
    """Usage:
    print(make_fungidb_xml(abbrev_strain=, strain_tax_id=STRAIN_TAX_ID, tax_name=TAX_NAME, file_name=, species_tax_id=SPECIES_TAX_ID,
        is_ref_strain=, abbrev_ref_strain=, short_species=, strain=STRAIN, source=SOURCE, haploid='true', genus=GENUS,
        has_trna=, version=VERSION))
    """
    return """
        <dataset class=\"organism\">
            <prop name=\"organismAbbrev\">{abbrev_strain}</prop>
            <prop name=\"projectName\">$$projectName$$</prop>
            <prop name=\"ncbiTaxonId\">{strain_tax_id}</prop>
            <prop name=\"publicOrganismAbbrev\">{abbrev_strain}</prop>
            <prop name=\"organismFullName\">{tax_name}</prop>
            <prop name=\"organismNameForFiles\">{file_name}</prop>
            <prop name=\"speciesNcbiTaxonId\">{species_tax_id}</prop>
            <prop name=\"isReferenceStrain\">{is_ref_strain}</prop>
            <prop name=\"referenceStrainOrganismAbbrev\">{abbrev_ref_strain}</prop>
            <prop name=\"isAnnotatedGenome\">true</prop>
            <prop name=\"hasTemporaryNcbiTaxonId\">false</prop>
            <prop name=\"orthomclAbbrev\">{short_species}</prop>
            <prop name=\"strainAbbrev\">{strain}</prop>
            <prop name=\"genomeSource\">{source}</prop>
            <prop name=\"isHaploid\">{haploid}</prop>
            <prop name=\"taxonHierarchyForBlastxFilter\">Eukaryota Fungi {genus}</prop>
            <prop name=\"annotationIncludesTRNAs\">{has_trna}</prop>
            <prop name=\"runExportPred\">false</prop>
            <prop name=\"maxIntronSize\">700</prop>
            <prop name=\"skipGenomeAnalysis\">false</prop>
            <prop name=\"hasDeprecatedGenes\">false</prop>
            <prop name=\"genomeVersion\">{version}</prop>
        </dataset>
""".format(**kwargs)


def make_ref_strain(**kwargs):
    """Usage:
    print(make_ref_strain(abbrev_strain=abbrev_strain))
    """
    return """
        <dataset class=\"referenceStrain\">
            <prop name=\"organismAbbrev\">{abbrev_strain}</prop>
            <prop name=\"isAnnotatedGenome\">true</prop>
        </dataset>
""".format(**kwargs)


def make_organism_xml(**kwargs):
    """Usage:
    print(make_organism_xml(abbrev_strain=, strain=STRAIN, strain_tax_id=STRAIN_TAX_ID, species_tax_id=SPECIES_TAX_ID,
        version=VERSION, abbrev_ref_strain=, source=SOURCE, file_type=FILE_TYPE))
    """
    return """
<datasets>
    <constant name=\"organismAbbrev\" value=\"{abbrev_strain}\"/>
    <constant name=\"strainAbbrev\" value=\"{strain}\"/>
    <constant name=\"projectName\" value=\"FungiDB\"/>
    <constant name=\"ncbiTaxonId\" value=\"{strain_tax_id}\"/>
    <constant name=\"speciesNcbiTaxonId\" value=\"{species_tax_id}\"/>
    <constant name=\"genomeVersion\" value=\"{version}\"/>
    <constant name=\"referenceStrainOrganismAbbrev\" value=\"{abbrev_ref_strain}\"/>

    <dataset class=\"validateOrganismInfo\">
        <prop name=\"organismAbbrev\">$$organismAbbrev$$</prop>
        <prop name=\"strainAbbrev\">$$strainAbbrev$$</prop>
        <prop name=\"projectName\">$$projectName$$</prop>
        <prop name=\"ncbiTaxonId\">$$ncbiTaxonId$$</prop>
        <prop name=\"speciesNcbiTaxonId\">$$speciesNcbiTaxonId$$</prop>
        <prop name=\"genomeVersion\">$$genomeVersion$$</prop>
    </dataset>

<!--
    <dataset class=\"productNames\">
        <prop name=\"name\">{source}</prop>
        <prop name=\"version\">$$genomeVersion$$</prop>
        <prop name=\"projectName\">$$projectName$$</prop>
        <prop name=\"organismAbbrev\">$$organismAbbrev$$</prop>
    </dataset>
-->

    <dataset class=\"transcriptsFromReferenceStrain\">
        <prop name=\"referenceStrainOrganismAbbrev\">$$referenceStrainOrganismAbbrev$$</prop>
    </dataset>

    <dataset class=\"epitopesFromReferenceStrain\">
        <prop name=\"referenceStrainOrganismAbbrev\">$$referenceStrainOrganismAbbrev$$</prop>
    </dataset>

    <dataset class=\"isolatesFromReferenceStrain\">
        <prop name=\"name\">{file_type}</prop>
        <prop name=\"referenceStrainOrganismAbbrev\">$$referenceStrainOrganismAbbrev$$</prop>
    </dataset>

    <dataset class=\"dbxref_gene2Entrez\">
        <prop name=\"projectName\">$$projectName$$</prop>
        <prop name=\"organismAbbrev\">$$organismAbbrev$$</prop>
        <prop name=\"ncbiTaxonId\">$$ncbiTaxonId$$</prop>
        <prop name=\"genomeVersion\">$$genomeVersion$$</prop>
        <prop name=\"version\">2011-11-29</prop>
    </dataset>

    <dataset class=\"dbxref_gene2Uniprot\">
        <prop name=\"projectName\">$$projectName$$</prop>
        <prop name=\"organismAbbrev\">$$organismAbbrev$$</prop>
        <prop name=\"ncbiTaxonId\">$$ncbiTaxonId$$</prop>
        <prop name=\"genomeVersion\">$$genomeVersion$$</prop>
        <prop name=\"version\">2011-11-29</prop>
    </dataset>

    <dataset class=\"dbxref_gene2PubmedFromNcbi\">
        <prop name=\"projectName\">$$projectName$$</prop>
        <prop name=\"organismAbbrev\">$$organismAbbrev$$</prop>
        <prop name=\"ncbiTaxonId\">$$ncbiTaxonId$$</prop>
        <prop name=\"genomeVersion\">$$genomeVersion$$</prop>
        <prop name=\"version\">2011-12-17</prop>
    </dataset>

</datasets>
""".format(**kwargs)


def make_broad(**kwargs):
    """Usage:
    print(make_broad(so_term=SO_TERM))
    """
    return """
    <!-- fasta -->
    <dataset class=\"fasta_primary_genome_sequence\">
        <prop name=\"name\">broad</prop>
        <prop name=\"version\">$$genomeVersion$$</prop>
        <prop name=\"table\">DoTS::ExternalNASequence</prop>
        <prop name=\"soTerm\">{so_term}</prop>
        <prop name=\"sourceIdRegex\">^>(\\S+)</prop>
        <prop name=\"projectName\">$$projectName$$</prop>
        <prop name=\"organismAbbrev\">$$organismAbbrev$$</prop>
        <prop name=\"ncbiTaxonId\">$$ncbiTaxonId$$</prop>
    </dataset>

    <!-- gff -->
    <dataset class=\"Broad_GFF_primary_genome_features\">
        <prop name=\"projectName\">$$projectName$$</prop>
        <prop name=\"organismAbbrev\">$$organismAbbrev$$</prop>
        <prop name=\"ncbiTaxonId\">$$ncbiTaxonId$$</prop>
        <prop name=\"version\">$$genomeVersion$$</prop>
        <prop name=\"soTerm\">{so_term}</prop>
    </dataset>
""".format(**kwargs)


def make_genbank(**kwargs):
    """Usage:
    print(make_genbank(source=SOURCE, so_term=SO_TERM))
    """
    return """
    <!-- genbank -->
        <dataset class=\"genbank_primary_genome\">
        <prop name=\"projectName\">$$projectName$$</prop>
        <prop name=\"organismAbbrev\">$$organismAbbrev$$</prop>
        <prop name=\"ncbiTaxonId\">$$ncbiTaxonId$$</prop>
        <prop name=\"name\">{source}</prop>
        <prop name=\"version\">$$genomeVersion$$</prop>
        <prop name=\"soTerm\">{so_term}</prop>
        <prop name=\"mapFile\">FungiDB/fungiGenbank2gus.xml</prop>
    </dataset>
""".format(**kwargs)


def make_ref_strain_org_xml(**kwargs):
    """Usage:
    print(make_ref_strain_org_xml())
    """
    return """
	<dataset class=\"referenceStrain-dbEST\">
		<prop name=\"projectName\">$$projectName$$</prop>
		<prop name=\"organismAbbrev\">$$organismAbbrev$$</prop>
		<prop name=\"speciesNcbiTaxonId\">$$speciesNcbiTaxonId$$</prop>
	</dataset>

	<dataset class=\"referenceStrain-epitope_sequences_IEDB\">
		<prop name=\"organismAbbrev\">$$organismAbbrev$$</prop>
		<prop name=\"speciesNcbiTaxonId\">$$speciesNcbiTaxonId$$</prop>
		<prop name=\"version\">2.4</prop>
	</dataset>

	<dataset class=\"referenceStrain-isolatesGenbank\">
		<prop name=\"organismAbbrev\">$$organismAbbrev$$</prop>
		<prop name=\"speciesNcbiTaxonId\">$$speciesNcbiTaxonId$$</prop>
	</dataset>
""".format(**kwargs)
