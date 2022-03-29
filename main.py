import time
import sys
from mpi4py import MPI
from init import MatrixDistribute, LocalMatrixInitialize
from serialcompute import SerialCompute
from parallelcompute import ParallelCompute
from finalization import UpdatePrefix

comm = MPI.COMM_WORLD
clusterSize = comm.Get_size()
nodeRank = comm.Get_rank()

# Initialize Constants
try:
    matrixSize = int(sys.argv[1])
    blockSize = 1
    numLimit = int(sys.argv[2])
except:
    matrixSize = 8
    blockSize = 1
    numLimit = 10
divPerNode = (matrixSize * blockSize) / clusterSize
if divPerNode % blockSize != 0:
    raise ValueError('Cluster size {} and matrix size {} are incompatible'.format(clusterSize, blockSize))
divPerNode = int(divPerNode)

# Initialization
dist = MatrixDistribute(comm, clusterSize, nodeRank, matrixSize, blockSize, numLimit, divPerNode)
dist.A, dist.b, dist.L, dist.D, dist.U = \
    dist.distributeData(dist.comm, dist.clusterSize, dist.nodeRank)
lmat = LocalMatrixInitialize(blockSize, divPerNode, dist.A, dist.b, dist.L, dist.D, dist.U)
lmat.B = lmat.constructB(lmat.D_til, lmat.L_til, lmat.b_til)

# Start Time
startTime = time.time()

# Serial Prefix Step
serial = SerialCompute(lmat.B)
serial.S_s = serial.computePrefix(serial.B)

# Parallel Prefix Step
parallel = ParallelCompute(comm, clusterSize, nodeRank, serial.S_s)
parallel.S_p, parallel.T_p = parallel.computePrefix()

# Finalization
update = UpdatePrefix(comm, clusterSize, nodeRank, divPerNode, serial.S_s, parallel.S_p, parallel.T_p)
update.sharePrefix()
update.computeX()

comm.Barrier()

# End Time
endTime = time.time()

# Program Run Time
if nodeRank == 0:
    print(endTime - startTime)
    sys.exit()