#!/bin/bash
# This is a bash script for running ldos_nanoslab.py
#-----------------------------------------------------------------
#remove old  files
rm ldos_slab*.out 
rm ldos_slab*.dat
rm flux_slab*.dat
rm w_slab*.dat

for i in `seq 0 1 10`; do #slab thickness increment index loop (in um)
   # python -u ldos_nanoslab.py -res 60 -wvl $i | tee -a ldos_slab${i}.out; #single-processor version
    mpirun -np 10 python -u ldos_nanoslab_pmp.py -res 500  -wvl 0.500 -w_init 0.050 -dw 0.002 -n ${i} | tee -a ldos_slab_${i}.out; #parallel version, 10 cores
    grep ldos0: ldos_slab_${i}.out |cut -d, -f2- >> ldos_slab.dat;
    grep normalised ldos_slab_${i}.out | cut -d, -f2- >> flux_slab.dat;
    grep 'slab thickness' ldos_slab_${i}.out | cut -d, -f2- >>w_slab.dat;
    printf "\n"
done
