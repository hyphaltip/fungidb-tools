#PBS -l nodes=1:ppn=2,walltime=96:00:00 -q highmem -j oe
module load stajichlab
module load orthoMCL
module load stajichlab-perl
module load pigz

PREF=CryptoDB3_Dec2013
cat split/$PREF.?.FASTP.tab split/$PREF.??.FASTP.tab | grep -v ^# > /dev/shm/$PREF.FASTP.tab
orthomclBlastParser /dev/shm/$PREF.FASTP.tab clean > $PREF.FASTP.bpo
pigz /dev/shm/$PREF.FASTP.tab
mv /dev/shm/$PREF.FASTP.tab.gz .

qsub -d `pwd` scripts/04_loadprocess.sh
