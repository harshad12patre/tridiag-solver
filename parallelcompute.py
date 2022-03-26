import numpy as np

class ParallelCompute():
    def __init__(self, comm, clusterSize, nodeRank, S_s):
        self.comm           = comm
        self.clusterSize    = clusterSize
        self.nodeRank       = nodeRank
        self.S_s            = S_s
        self.S_p, self.T_p  = None, None

    def getCommNode(self, i, d):
        procNums = [format(i, '0' + str(d) + 'b') for i in range(self.clusterSize)]

        commNode = procNums[self.nodeRank]
        x = "0" if commNode[d-i-1] == "1" else "1"
        commNode = commNode[:d-i-1] + x + commNode[d-i:]
        commNode = int(commNode, 2)

        return commNode


    def computePrefix(self):
        d = int(np.log2(self.clusterSize))

        S_p = self.S_s[-1]
        T_p = self.S_s[-1]

        for i in range(d):
            commNode = self.getCommNode(i, d)

            self.comm.send(T_p, dest = commNode, tag = 5)
            T_temp = self.comm.recv(source = commNode, tag = 5)

            if commNode < self.nodeRank:
                T_p = np.dot(T_p, T_temp)
                S_p = np.dot(S_p, T_temp)
            else:
                T_p = np.dot(T_temp, T_p)

        return S_p, T_p