import numpy as np

class SerialCompute():
    def __init__(self, B):
        self.B = B
        self.S_s = None

    def computePrefix(self, B):
        prefix = [B[0]]
        for i in range(1, len(B)):
            prefix.append(np.dot(B[i], prefix[i-1]))

        return prefix