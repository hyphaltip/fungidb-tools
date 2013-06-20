module load orthoMCL
module load wu-blast
SPLIT_SIZE=2000
rm -rf clean
mkdir -p clean

cd clean
orthomclAdjustFasta ANID ../input/A_nidulans_FGSC_A4_current_orf_trans_all.fasta 1
orthomclAdjustFasta CALB ../input/C_albicans_SC5314_A21_current_orf_trans_all.fasta 1
orthomclAdjustFasta SCER ../input/S_cerevisiae_S288C_current.2011-02-03.fasta 1
orthomclAdjustFasta SPOM ../input/Schizosaccharomyces_pombe.ASM294v1.17.pep.all.fasta 1
orthomclAdjustFasta CGATR ../input/FungiDB-CURRENT_Cgattii_R265_AnnotatedProteins.fasta 2
orthomclAdjustFasta CGATW ../input/FungiDB-CURRENT_Cgattii_WM276_AnnotatedProteins.fasta 2
orthomclAdjustFasta CGRU ../input/FungiDB-CURRENT_Cneoformans_var_grubiiH99_AnnotatedProteins.fasta 2
orthomclAdjustFasta CNEOB ../input/FungiDB-CURRENT_Cneoformans_var._neoformans_B3501_AnnotatedProteins.fasta 2
orthomclAdjustFasta CNEOJ ../input/FungiDB-CURRENT_Cneoformans_var_neoformans_JEC21_AnnotatedProteins.fasta 2

perl -i -p -e 's/\*$//' *.fasta
cd ..
orthomclFilterFasta clean 20 10
pseg goodProteins.fasta -q -z 1 > CryptoDB2.seg
rm -rf split
mkdir -p split
cd split
bp_dbsplit --size $SPLIT_SIZE -p CryptoDB2 ../CryptoDB2.seg
cd ..
