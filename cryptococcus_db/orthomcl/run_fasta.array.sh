#PBS -N CryptoDB3 -l nodes=1:ppn=4,walltime=36:00:00,mem=2gb -j oe -o CryptoDB3.out 
#PBS -d /bigdata/jstajich/Cryptococcus/CryptoDB/OrthoMCL.Dec2013/split
module load fasta
PREF=CryptoDB3_Dec2013
N=$PBS_ARRAYID
if [ ! $N ]; then
 N=$1
fi

if [ ! $N ]; then
 echo "No PBS_ARRAYID or input num"
 exit 0
fi
fasta36 -m 8c -E 1e-5 -S -T 4 $PREF.$N ../$PREF.seg > $PREF.$N.FASTP.tab
