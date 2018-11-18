#!/bin/bash
# This is a bash script for running ldos_nanoslab.py
rm ldos_slab*.out #remove old .out and .dat files
rm ldos_slab*.dat

for i in `seq 0.5 0.05 0.55`; do #wavelength loop (in um)
    echo "begin wavelength "${i}" μm"
   # python -u ldos_nanoslab.py -res 60 -wvl $i | tee -a ldos_slab${i}.out; #single-processor version
    mpirun -np 10 python -u ldos_nanoslab.py -res 200 -wvl $i | tee -a ldos_slab${i}.out; #parallel version
    # grep refl: ldos_${i}.out | cut -d, -f1- >ldos_${i}.dat;
    grep ldos0: ldos_slab${i}.out |cut -d, -f2- > ldos_slab${i}.dat;
    echo "end wavelength "${i}" μm"
    printf "\n"
done
