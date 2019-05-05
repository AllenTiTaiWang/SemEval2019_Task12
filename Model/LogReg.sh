#!/bin/bash
# Your job will use 1 node, 28 cores, and 168gb of memory total.
#PBS -q windfall
#PBS -l select=1:ncpus=28:mem=168gb:pcmem=8gb:ngpus=1
### Specify a name for the job
#PBS -N LogReg
### Specify the group name
#PBS -W group_list=nlp
### Used if job requires partial node only
#PBS -l place=pack:exclhost
### CPUtime required in hhh:mm:ss.
### Leading 0's can be omitted e.g 48:0:0 sets 48 hours
#PBS -l cput=244:00:00
### Walltime is how long your job will run
#PBS -l walltime=8:00:00
#PBS -e /extra/twang3/GEOProject/error/
#PBS -o /extra/twang3/GEOProject/output/

module load python/3
source /extra/twang3/pyvenv/bin/activate
module load python/3
cd $PBS_O_WORKDIR
python3 /extra/twang3/GEOProject/disambiguation/Model/label.py
python3 /extra/twang3/GEOProject/disambiguation/Model/LogReg.py
