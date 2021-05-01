#!/usr/bin/env bash

#SBATCH --job-name=nb-little
#SBATCH --output=nb-little.out
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=smp
#SBATCH --cluster=smp
#SBATCH --time=2-0:00:00

module load python/3.7.0
pip install wikipedia
time python nbgrid.py
