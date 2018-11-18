#!/bin/bash

python -u refl-quartz.py |tee flux.out
grep refl: flux.out |cut -d , -f2- > flux.dat
