#PBS -l nodes=1:ppn=1 -j oe
module load stajichlab
module load stajichlab-perl
module load orthoMCL
module load mysql

PREF=CryptoDB3_Dec2013
orthomclLoadBlast orthomcl.config $PREF.FASTP.bpo
orthomclPairs orthomcl.config orthomcl_pairs.log cleanup=no
orthomclDumpPairsFiles orthomcl.config
