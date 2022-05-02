#!/bin/sh
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=2
#SBATCH --partition=debug
#SBATCH --qos=debug
#SBATCH --out=output/tridiag-solver.out
#SBATCH --mail-user=hbarapat@buffalo.edu
#SBATCH --mail-type=ALL
#SBATCH --time=00:10:00
#SBATCH --exclusive
#SBATCH --account=cse633

module load mpi4py/2.0.0-openmpi
module load mpi4py
source activate py36-mpi

mpiexec -np 2 python main.py 1024 1 1000000
mpiexec -np 4 python main.py 1024 1 1000000
