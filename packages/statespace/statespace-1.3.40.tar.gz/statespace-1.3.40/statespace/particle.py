import numpy as np
import math
import util
import jazwinski1
import jazwinski2

class Particle():
    '''particle filter. monte carlo sampling processor, bootstrap particle filter. the run methods perform particular filters from Bayesian Signal Processing: Classical, Modern, and Particle Filtering Methods.'''
    def __init__(self, mode, innovs=False, dists=False):
        self.innovs = util.Innovs()
        self.dists = util.Dists()
        self.ens = util.DistsEns()
        if mode == 'test':
            for i in range(100):
                m = jazwinski1.Jazwinski1()
                self.run_pf1(m)
                self.ens.update(distslog=self.dists.log)
            self.ens.plot()
        if mode == 'pf1':
            m = jazwinski1.Jazwinski1()
            self.run_pf1(m)
            if dists: self.dists.plot()
        if mode == 'pf2':
            m = jazwinski2.Jazwinski2()
            self.run_pf2(m)
        if innovs: self.innovs.plot()

    def run_pf1(self, m):
        '''particle filter 1.'''
        xhat = 2.05
        x = xhat + math.sqrt(1e-2) * np.random.randn(m.nsamp)
        W = self.normalize(np.ones(m.nsamp))
        for step in m.steps():
            x = self.resample(x, W)
            x = m.Apf(x)
            W = self.normalize(m.Cpf(step[2], x))
            yhat = m.c(xhat, 0)
            xhat = W @ x
            self.innovs.update(t=step[0], xhat=xhat, yhat=yhat, err=step[1] - xhat, inn=step[2] - yhat)
            self.dists.update(t=step[0], tru=m.Apf(step[1]), est=x)

    def run_pf2(self, m):
        '''particle filter 2.'''
        xhat = np.array([2.0, .055, .044])
        x = xhat + np.sqrt(m.Rww) * np.random.randn(m.nsamp, 3)
        W = np.ones((m.nsamp, 3)) / m.nsamp
        for step in m.steps():
            x[:, 0], x[:, 1], x[:, 2] = self.resample(x[:, 0], W[:, 0]), self.roughen(x[:, 1]), self.roughen(x[:, 2])
            x[:, 0] = np.apply_along_axis(m.Apf, 1, x)
            W[:, 0] = self.normalize(m.Cpf(step[2], x[:, 0]))
            yhat = m.c(xhat, 0)
            xhat = [W[:, 0].T @ x[:, 0], W[:, 1].T @ x[:, 1], W[:, 2].T @ x[:, 2]]
            self.innovs.update(t=step[0], xhat=xhat[0], yhat=yhat, err=step[1][0] - xhat[0], inn=step[2] - yhat)

    def resample(self, xi, Wi):
        '''particle resampling.'''
        tmp = []
        for i in range(xi.size):
            tmp.append([xi[i], Wi[i]])
        tmp = sorted(tmp, key=lambda x: x[0])
        cdf = [[tmp[0][0], tmp[0][1]]]
        for i in range(1, len(tmp)):
            cdf.append([tmp[i][0], tmp[i][1] + cdf[i - 1][1]])
        cdf = np.asarray(cdf)
        uk = np.sort(np.random.uniform(size=xi.size))
        xhati, k = [], 0
        for row in cdf:
            while k < uk.size and uk[k] <= row[1]:
                xhati.append(row[0])
                k += 1
        xhati = np.asarray(xhati)
        assert xhati.size == xi.size
        return xhati

    def roughen(self, x):
        return x + .1 * np.random.randn(x.size)

    def normalize(self, W):
        return W / sum(W)

if __name__ == "__main__":
    # Particle('test')
    # Particle('pf1', dists=1, innovs=0)
    Particle('pf2', innovs=1)
