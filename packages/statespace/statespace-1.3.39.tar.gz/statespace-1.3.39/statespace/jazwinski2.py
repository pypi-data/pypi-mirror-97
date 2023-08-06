import math

import numpy as np


class Jazwinski2():
    '''reference problem from Stochastic Processes and Filtering Theory, Jazwinski, and Bayesian Signal Processing: Classical, Modern, and Particle Filtering Methods.'''
    def __init__(self):
        self.tsteps = 1501
        self.dt = .01
        self.x = np.array([2., .05, .04])
        self.Rww = 1e-9 * np.array([1, 1, 1])
        self.Rvv = 9e-2
        self.Sw = np.linalg.cholesky(np.diag(self.Rww))
        self.Sv = np.linalg.cholesky(np.diag(self.Rvv * np.array([1])))
        self.log = []
        self.nsamp = 250
        n = 3
        kappa = 1
        alpha = 1
        beta = 2
        lam = alpha ** 2 * (n + kappa) - n
        wi = 1 / float(2 * (n + lam))
        w0m = lam / float(n + lam)
        w0c = lam / float(n + lam) + (1 - alpha ** 2 + beta)
        self.Wm = np.array([w0m, wi, wi, wi, wi, wi, wi])
        self.Wc = np.array([w0c, wi, wi, wi, wi, wi, wi])
        self.nlroot = math.sqrt(n + lam)
        self.Xtil = np.zeros((3, 7))
        self.Ytil = np.zeros((1, 7))
        self.Pxy = np.zeros((3, 1))
        self.G = np.eye(3)
        self.Q = np.diag(self.Rww)

    def a(self, x, w=0):
        return np.array([(1 - x[1] * self.dt) * x[0] + x[2] * self.dt * x[0] ** 2, x[1], x[2]]) + w

    def c(self, x, v=0):
        return x[0] ** 2 + x[0] ** 3 + v

    def A(self, x):
        A = np.eye(3)
        A[0, 0] = 1 - x[1] * self.dt + 2 * x[2] * self.dt * x[0]
        A[0, 1] = -self.dt * x[0]
        A[0, 2] = self.dt * x[0] ** 2
        return A

    def C(self, x):
        return np.array([2 * x[0] + 3 * x[0] ** 2, 0, 0])

    def X(self, x, C):
        X = np.zeros([3, 7])
        X[:, 0] = x
        X[:, 1] = x + self.nlroot * C.T[:, 0]
        X[:, 2] = x + self.nlroot * C.T[:, 1]
        X[:, 3] = x + self.nlroot * C.T[:, 2]
        X[:, 4] = x - self.nlroot * C.T[:, 0]
        X[:, 5] = x - self.nlroot * C.T[:, 1]
        X[:, 6] = x - self.nlroot * C.T[:, 2]
        return X

    def Xhat(self, X):
        Xhat = np.zeros([3, 7])
        Xhat[:, 0] = X[:, 0]
        Xhat[:, 1] = X[:, 1] + self.nlroot * self.Sw.T[:, 0]
        Xhat[:, 2] = X[:, 2] + self.nlroot * self.Sw.T[:, 1]
        Xhat[:, 3] = X[:, 3] + self.nlroot * self.Sw.T[:, 2]
        Xhat[:, 4] = X[:, 4] - self.nlroot * self.Sw.T[:, 0]
        Xhat[:, 5] = X[:, 5] - self.nlroot * self.Sw.T[:, 1]
        Xhat[:, 6] = X[:, 6] - self.nlroot * self.Sw.T[:, 2]
        return Xhat

    def va(self, X):
        for i in range(7): X[:, i] = self.a(X[:, i], 0)
        return X

    def vc(self, Xhat):
        Y = np.zeros(7)
        for i in range(7): Y[i] = self.c(Xhat[:, i], 0)
        return Y

    def Xtil(self, X, W):
        Xtil = np.zeros((3, 7))
        for i in range(7): Xtil[:, i] = X[:, i] - W @ X.T
        return Xtil

    def ksi(self, Y, W):
        ksi = np.zeros((1, 7))
        for i in range(7): ksi[0, i] = Y[i] - W @ Y.T
        return ksi

    def Apf(self, x):
        return (1 - x[1] * self.dt) * x[0] + x[2] * self.dt * x[0] ** 2

    def Cpf(self, y, x):
        return np.exp(-np.log(2. * np.pi * self.Rvv) / 2. - (y - x ** 2 - x ** 3) ** 2 / (2. * self.Rvv))

    def steps(self):
        for tstep in range(self.tsteps):
            tsec = tstep * self.dt
            w = np.multiply(np.random.randn(1, 3), np.sqrt(np.diag(self.Rww)))
            v = math.sqrt(self.Rvv) * np.random.randn()
            self.x = self.a(self.x, w[0])
            self.y = self.c(self.x, v)
            if tstep == 0: continue
            self.log.append([tsec, self.x, self.y])
            yield (tsec, self.x, self.y)