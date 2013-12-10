#PBS -l nodes=1:ppn=4 -j oe
module load stajichlab
module load stajichlab-perl
module load orthoMCL
module load mysql

mcl mclInput -te 4 --abc -I 1.5 -o mclOutput.I15.out
mcl mclInput -te 4 --abc -I 1.8 -o mclOutput.I18.out
mcl mclInput -te 4 --abc -I 2 -o mclOutput.I20.out
mcl mclInput -te 4 --abc -I 3 -o mclOutput.I30.out

orthomclMclToGroups OG15_ 1 < mclOutput.I15.out > mclGroups.I15.txt
orthomclMclToGroups OG18_ 1 < mclOutput.I18.out > mclGroups.I18.txt
orthomclMclToGroups OG20_ 1 < mclOutput.I20.out > mclGroups.I20.txt
orthomclMclToGroups OG30_ 1 < mclOutput.I30.out > mclGroups.I30.txt

