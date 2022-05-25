#
# ising.py
# --------
# Contains main definition of Ising Model
#
#

import numpy as np


class Ising(object):
    def __init__(self, shape, J = 1, statespace = [-1, 1]):
        """
        Parameters
        ----------

        shape: Tuple
            An array of integers specifying the dimension of the model.
        """
        self._state = np.random.choice(statespace, size=shape)
        self._J = J

    def calculateEnergy(self):
        sigma = self._state
        n = sigma.shape[0]
        m = sigma.shape[1]
        J = self._J

        # TODO generalize to n dimensions
        E1 = 0
        E2 = 0
        for j in range(m):
            for i in range(n):
                E1 -= J * sigma[i, j] * sigma[i, (j + 1) % m]
                E2 -= J * sigma[i, j] * sigma[(i + 1) % n, j]
        return E1 + E2


    def flipSpin(self, i, j):
        self._state[i, j] = 1 if self._state[i, j] == -1 else -1

    def calculateMagnetization(self):
        return np.mean(self._state)

    def monteCarloStep(self, beta):
        # TODO use metropolis class
        sigma = self._state
        n = sigma.shape[0]
        m = sigma.shape[1]
        N = n*m

        for _ in range(N):
            i = np.random.randint(n)
            j = np.random.randint(m)

            Ediff = 2*sigma[i, j] * (sigma[(i+1) % n, j] + sigma[i, (j+1) % m] + sigma[(i-1) % n, j] + sigma[i, (j-1) % m])

            if Ediff < 0:
                self.flipSpin(i, j)
                continue

            p = np.exp(-beta * Ediff)
            reject = np.random.choice([0, 1], 1, p = [p, 1-p])

            if reject == 0:
                self.flipSpin(i, j)


    @property
    def getState(self):
        return self._state
