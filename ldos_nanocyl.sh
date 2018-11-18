#!/bin/bash
# This is a bash script for running ldos_nanosphere.py
#rm ldos_*.out #remove old .out and .dat files
rm ldos_cyl*_5.dat

for i in `seq 25 5 45`; do
    echo "begin wavelength "${i}" μm"
    python -u ldos_nanocyl.py -res 50 -wvl $i | tee -a ldos_cyl${i}.out
   # mpirun -np 10 python -u ldos_nanoshell.py -res 80 -wvl $i | tee -a ldos_${i}.out;
    # grep refl: ldos_${i}.out | cut -d, -f1- >ldos_${i}.dat;
    grep ldos0: ldos_cyl${i}.out |cut -d, -f2- > ldos_cyl${i}_5.dat;
    echo "end wavelength "${i}" μm"
    printf "\n"
done
