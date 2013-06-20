ct=`ls split | wc -l`
pwd=`pwd`
JOBID=`qsub -d $pwd -q highmem -t 1-$ct run_fasta.array.sh`
qsub -d $pwd -W afterokarray:$JOBID 03_parseblast.sh
