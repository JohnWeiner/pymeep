#!/bin/bash
# This is a bash script for running ldos_nanoshell.py
rm ldos_*.out #remove old .out and .dat files
rm ldos_*.dat

for i in `seq 200 5 1000`; do
    echo "begin wavelength "${i}" nm";
    mpirun -np 10 python -u ldos_nanoshell.py -res 400 -wvl $i | tee  ldos_${i}_shell.out;
    grep ldos0: ldos_${i}_shell.out | cut -d, -f2- >ldos_${i}_shell.dat;
    echo "end wavelength "${i}" nm"
    printf "\n"
done
