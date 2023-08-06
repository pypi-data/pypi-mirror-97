import math

import numpy as np


class Jazwinski1():
    '''reference problem from Stochastic Processes and Filtering Theory, Jazwinski, and Bayesian Signal Processing: Classical, Modern, and Particle Filtering Methods.'''
    def __init__(self):
        self.tsteps = 151
        self.dt = .01
        self.x = 2.
        self.Rww = 1e-6
        self.Rvv = 9e-2
        self.log = []
        self.va = np.vectorize(self.a)
        self.vc = np.vectorize(self.c)
        bignsubx = 1
        kappa = 1
        k0 = bignsubx + kappa
        k1 = kappa / float(k0)
        k2 = 1 / float(2 * k0)
        self.nsamp = 250
        self.W = np.array([k1, k2, k2])
        self.k0 = k0
        self.kappa = kappa

    def a(self, x, w=0):
        return (1 - .05 * self.dt) * x + (.04 * self.dt) * x ** 2 + w

    def c(self, x, v=0):
        return x ** 2 + x ** 3 + v

    def A(self, x):
        return 1 - .05 * self.dt + .08 * self.dt * x

    def C(self, x):
        return 2 * x + 3 * x ** 2

    def X(self, xhat, Ptil):
        return [xhat, xhat + math.sqrt(self.k0 * Ptil), xhat - math.sqrt(self.k0 * Ptil)]

    def Xhat(self, X, Rww):
        return [X[0], X[1] + self.kappa * math.sqrt(Rww), X[2] - self.kappa * math.sqrt(Rww)]

    def Apf(self, x):
        return (1 - .05 * self.dt) * x + (.04 * self.dt) * x ** 2 + math.sqrt(self.Rww) * np.random.randn(self.nsamp)

    def Cpf(self, y, x):
        return np.exp(-np.log(2. * np.pi * self.Rvv) / 2. - (y - x ** 2 - x ** 3) ** 2 / (2. * self.Rvv))

    def steps(self):
        for tstep in range(self.tsteps):
            tsec = tstep * self.dt
            w = math.sqrt(self.Rww) * np.random.randn()
            v = math.sqrt(self.Rvv) * np.random.randn()
            self.x = self.a(self.x, w)
            self.y = self.c(self.x, v)
            if tstep == 0: continue
            self.log.append([tsec, self.x, self.y])
            yield (tsec, self.x, self.y)