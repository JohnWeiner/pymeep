#!/bin/bash
# This is a bash script for running ldos_nanoslab.py
#-----------------------------------------------------------------
#remove old *.out and *.dat files
#rm ldos_slab*.out 
#rm ldos_slab*.dat
#rm flux_slab*.dat

for i in `seq 0.400 0.005 0.905`; do #wavelength loop (in um)
    echo "begin wavelength "${i}" μm"
   # python -u ldos_nanoslab.py -res 60 -wvl $i | tee -a ldos_slab${i}.out; #single-processor version
    #mpirun -np 10 python -u ldos_nanoslab_pmp.py -res 200 -wvl $i | tee -a ldos_slab${i}.out; #parallel version
    # grep refl: ldos_${i}.out | cut -d, -f1- >ldos_${i}.dat;
    grep ldos0: ldos_slab${i}.out |cut -d, -f2- >> ldos_slab.dat;
    grep fractional ldos_slab${i}.out | cut -d, -f2- >> flux_slab.dat;
    #grep wavelength ldos_slab${i}.out | cut -d' = ' -f2-  >>wvl_slab.dat;
    echo "${i}">>wvl_slab.dat;
    echo "end wavelength "${i}" μm"
    printf "\n"
done
