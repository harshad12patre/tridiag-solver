#!/bin/sh
#SBATCH --nodes=128
#SBATCH --ntasks-per-node=2
#SBATCH --partition=general-compute
#SBATCH --qos=general-compute
#SBATCH --out=output/tridiag-solver.out
#SBATCH --mail-user=hbarapat@buffalo.edu
#SBATCH --mail-type=ALL
#SBATCH --time=02:00:00
#SBATCH --exclusive
#SBATCH --account=cse633

module load mpi4py/2.0.0-openmpi
module load mpi4py
source activate py36-mpi

mpiexec -np 1 python main.py 1024 1 1000000
mpiexec -np 2 python main.py 1024 1 1000000
mpiexec -np 4 python main.py 1024 1 1000000
mpiexec -np 8 python main.py 1024 1 1000000
mpiexec -np 16 python main.py 1024 1 1000000
mpiexec -np 32 python main.py 1024 1 1000000
mpiexec -np 64 python main.py 1024 1 1000000
mpiexec -np 128 python main.py 1024 1 1000000

mpiexec -np 1 python main.py 32768 1 1000000
mpiexec -np 2 python main.py 32768 1 1000000
mpiexec -np 4 python main.py 32768 1 1000000
mpiexec -np 8 python main.py 32768 1 1000000
mpiexec -np 16 python main.py 32768 1 1000000
mpiexec -np 32 python main.py 32768 1 1000000
mpiexec -np 64 python main.py 32768 1 1000000
mpiexec -np 128 python main.py 32768 1 1000000

mpiexec -np 1 python main.py 1048576 1 1000000
mpiexec -np 2 python main.py 1048576 1 1000000
mpiexec -np 4 python main.py 1048576 1 1000000
mpiexec -np 8 python main.py 1048576 1 1000000
mpiexec -np 16 python main.py 1048576 1 1000000
mpiexec -np 32 python main.py 1048576 1 1000000
mpiexec -np 64 python main.py 1048576 1 1000000
mpiexec -np 128 python main.py 1048576 1 1000000

mpiexec -np 1 python main.py 33554432 1 1000000
mpiexec -np 2 python main.py 33554432 1 1000000
mpiexec -np 4 python main.py 33554432 1 1000000
mpiexec -np 8 python main.py 33554432 1 1000000
mpiexec -np 16 python main.py 33554432 1 1000000
mpiexec -np 32 python main.py 33554432 1 1000000
mpiexec -np 64 python main.py 33554432 1 1000000
mpiexec -np 128 python main.py 33554432 1 1000000

mpiexec -np 1 python main.py 1073741824 1 1000000
mpiexec -np 2 python main.py 1073741824 1 1000000
mpiexec -np 4 python main.py 1073741824 1 1000000
mpiexec -np 8 python main.py 1073741824 1 1000000
mpiexec -np 16 python main.py 1073741824 1 1000000
mpiexec -np 32 python main.py 1073741824 1 1000000
mpiexec -np 64 python main.py 1073741824 1 1000000
mpiexec -np 128 python main.py 1073741824 1 1000000