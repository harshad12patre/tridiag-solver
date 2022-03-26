import time
from mpi4py import MPI
from init import MatrixDistribute, LocalMatrixInitialize
from serialcompute import SerialCompute
from parallelcompute import ParallelCompute
from finalization import UpdatePrefix

comm = MPI.COMM_WORLD
clusterSize = comm.Get_size()
nodeRank = comm.Get_rank()

# Initialization
dist = MatrixDistribute(comm, clusterSize, nodeRank)
dist.A, dist.b, dist.L, dist.D, dist.U = \
    dist.distributeData(dist.comm, dist.clusterSize, dist.nodeRank)
lmat = LocalMatrixInitialize(clusterSize, dist.A, dist.b, dist.L, dist.D, dist.U)
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
update = UpdatePrefix(comm, clusterSize, nodeRank, lmat.constant.divPerNode, serial.S_s, parallel.S_p, parallel.T_p)
update.sharePrefix()
update.computeX()

comm.Barrier()

# End Time
endTime = time.time()

# Program Run Time
if nodeRank == 0:
    print(nodeRank, endTime - startTime)