class ConstantValues():
    def __init__(self, clusterSize):
        self.clusterSize = clusterSize

        self.matrixSize = 16384
        # print(2 ** 15)
        self.blockSize = 1
        self.numLimit = 10e1

        self.divPerNode = (self.matrixSize * self.blockSize) / self.clusterSize
        if self.divPerNode % self.blockSize != 0:
            raise ValueError('Cluster size {} and matrix size {} are incompatible'.format(clusterSize, self.blockSize))

        self.divPerNode = int(self.divPerNode)