from re import A
import numpy as np
from constants import ConstantValues

np.random.seed(0)

class MatrixGenerate():
    def __init__(self, matrixSize, blockSize, numLimit):
        self.matrixSize                         = matrixSize
        self.numLimit                           = numLimit
        self.blockSize                          = blockSize

        self.A, self.b, self.L, self.D, self.U  = self.tridiagMatrix()
    
    def generateBlock(self):
        return np.random.randint(1, self.numLimit, \
            size = (self.blockSize, self.blockSize))
    
    def generateIdentity(self):
        return np.identity(self.blockSize, \
            dtype = int)

    def generateMatrix(self):
        A = np.zeros((self.matrixSize * self.blockSize, self.matrixSize * self.blockSize), \
            dtype = int)
        b = np.random.randint(1, self.numLimit, \
            size = (self.matrixSize, self.blockSize))

        return A, b

    def tridiagMatrix(self):
        if self.matrixSize % self.blockSize != 0:
                raise ValueError('Block size {} and matrix size {} are incompatible.' \
                    .format(self.blockSize, self.matrixSize))

        A, b    = self.generateMatrix()
        L, D, U = [], [], []
        L.append(self.generateIdentity())

        for idx in range(self.matrixSize):
            k                                   = idx * self.blockSize
            mat                                 = self.generateBlock()
            D.append(mat)
            A[k: k + self.blockSize, \
                k: k + self.blockSize]          = mat

            if idx == 0:
                m                               = k + self.blockSize
                mat                             = self.generateBlock()
                U.append(mat)
                A[k: k + self.blockSize, \
                    m: m + self.blockSize]      = mat
            elif idx == self.matrixSize - 1:
                m                               = k - self.blockSize
                mat                             = self.generateBlock()
                L.append(mat)
                A[k: k + self.blockSize, \
                    m: m + self.blockSize]      = mat
            else:
                mat                             = self.generateBlock()
                L.append(mat)
                A[k: k + self.blockSize, \
                    k - self.blockSize: k]      = mat
                mat                             = self.generateBlock()
                U.append(mat)
                A[k: k + self.blockSize, \
                    k + self.blockSize: k + \
                        2 * self.blockSize]     = mat

        U.append(self.generateIdentity())

        # print(A)
        # print(b)

        return A, b, L, D, U
        
class MatrixDistribute():
    def __init__(self, comm, clusterSize, nodeRank):
        self.comm           = comm
        self.clusterSize    = clusterSize
        self.nodeRank       = nodeRank

        self.A, self.b, self.L, self.D, self.U = None, None, None, None, None

    def distributeData(self, comm, clusterSize, nodeRank):
        if nodeRank == 0:
            constant    = ConstantValues(clusterSize)
            matrix      = MatrixGenerate(int(constant.matrixSize), \
                                            int(constant.blockSize), \
                                            int(constant.numLimit))

            for i in range(1, clusterSize):
                comm.send(matrix.A[i * constant.divPerNode: (i + 1) * constant.divPerNode], dest = i, tag = 0)
                comm.send(matrix.b[i * constant.divPerNode: (i + 1) * constant.divPerNode], dest = i, tag = 1)
                comm.send(matrix.L[i * constant.divPerNode: (i + 1) * constant.divPerNode], dest = i, tag = 2)
                comm.send(matrix.D[i * constant.divPerNode: (i + 1) * constant.divPerNode], dest = i, tag = 3)
                comm.send(matrix.U[i * constant.divPerNode: (i + 1) * constant.divPerNode], dest = i, tag = 4)
            
            A = matrix.A[0: constant.divPerNode]
            b = matrix.b[0: constant.divPerNode]
            L = matrix.L[0: constant.divPerNode]
            D = matrix.D[0: constant.divPerNode]
            U = matrix.U[0: constant.divPerNode]

        else:
            A = comm.recv(source = 0, tag = 0)
            b = comm.recv(source = 0, tag = 1)
            L = comm.recv(source = 0, tag = 2)
            D = comm.recv(source = 0, tag = 3)
            U = comm.recv(source = 0, tag = 4)

        return A, b, L, D, U

class LocalMatrixInitialize():
    def __init__(self, clusterSize, A, b, L, D, U):
        self.constant = ConstantValues(clusterSize)

        self.A = A
        self.b = b
        self.L = L
        self.D = D
        self.U = U

        self.U_inv = self.computeInverse(self.U)
        self.D_til = self.computeTilda(self.D)
        self.L_til = self.computeTilda(self.L)
        self.b_til = self.computeTilda(self.b)

        self.B = None
    
    def generateIdentity(self):
        return np.identity(self.constant.blockSize, \
            dtype = int)
    
    def computeInverse(self, U):
        U_inv = []
        for mat in U:
            U_inv.append(np.linalg.inv(mat))
        
        return U_inv

    def computeTilda(self, M):
        M_til = []
        for idx in range(len(M)):
            M_til.append(np.dot(-self.U_inv[idx], M[idx]))

        return M_til

    def constructB(self, D_til, L_til, b_til):
        B = []
        for idx in range(self.constant.divPerNode):
            mat = np.zeros((3, 3))
            mat[0][0] = D_til[idx]
            mat[0][1] = L_til[idx]
            mat[0][2] = b_til[idx]
            mat[1][0] = self.generateIdentity()
            mat[2][2] = 1
            B.append(mat)

        return B