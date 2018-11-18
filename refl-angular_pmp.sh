#!/bin/bash
#This script runs the parallel version of refl-angular.py

rm flux_t*.dat; #reset .dat and .out files
rm flux_t*.out;

for i in `seq 0 5 85`; do
    echo "begin angle "${i}" deg."
    mpirun -np 10 python -u refl-angular.py -res 200 -theta $i |tee -a flux_t${i}.out;
    #loop over angles(deg) with fixed resolution, output to screen and flux_t{i}.out file.  Append to the file (-a option of tee command).
    grep refl: flux_t${i}.out |cut -d , -f2- > flux_t${i}.dat;
    #grep on "refl:" in the file flux_t${i}.out and pipe to cut at delimiter (,) from the second field to the end (-f2-) and write the cut line to flux_t${i}.dat.
    echo "end angle "${i}" deg."
   printf "\n"
done
