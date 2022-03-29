import numpy as np

class UpdatePrefix():
    def __init__(self, comm, clusterSize, nodeRank, divPerNode, S_s, S_p, T_p):
        self.comm           = comm
        self.clusterSize    = clusterSize
        self.nodeRank       = nodeRank
        self.divPerNode     = divPerNode
        self.S_s            = S_s
        self.S_p            = S_p
        self.T_p            = T_p
        self.X              = [np.array([0])] * (self.divPerNode + 1)
        self.Y              = [np.array([0])] * (self.divPerNode + 1)

    def sendRight(self, mat):
        self.comm.send(mat, dest = self.nodeRank + 1, tag = 6)

    def receiveLeft(self):
        return self.comm.recv(source = self.nodeRank - 1, tag = 6)
    
    def sharePrefix(self):
        n = len(self.S_s)

        S_p = self.S_p

        if self.nodeRank != self.clusterSize - 1:
            self.sendRight(S_p)
        
        if self.nodeRank != 0:
            leftS_p = self.receiveLeft()

            for idx in range(n):
                self.S_s[idx] = np.dot(self.S_s[idx], leftS_p)

    def computeY1(self):
            S_11    = np.array([self.T_p[0][0]])
            S_11    = S_11.reshape(S_11.shape[0], -1)
            S_13    = np.array([self.T_p[0][2]])
            S_13    = S_13.reshape(S_13.shape[0], -1)

            X       = np.dot(-np.linalg.inv(S_11), S_13)
            Y       = np.array([X, np.array([0]), np.array([1])], dtype = object)

            return -X[0][0], Y

    def computeX(self):
        self.X[0], self.Y[0] = self.computeY1()
        
        for idx in range(self.divPerNode):
            self.Y[idx + 1] = -np.dot(self.S_s[idx], self.Y[0])
            self.X[idx + 1] = self.Y[idx + 1][0][0]

        if self.nodeRank != 0:
            self.comm.send(self.X[1:], dest = 0, tag = 7)
        else:
            ans = self.X
            for commNode in range(1, self.clusterSize):
                ans.extend(self.comm.recv(source = commNode, tag = 7))


