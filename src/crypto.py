import numpy as np
from .gf2 import *


class Decryptor:
    def __init__(self, k=8, n=255, t=1):
        self.n = n
        self.k = k
        self.t = t

        self.G = read_matrix('data/ham.h5')
        self.H = read_matrix('data/ham2.h5')

        self.M = gen_non_singular((self.n, self.n))
        self.W = gen_non_singular((self.n, self.n))

        self.D = gen_diag(self.t, self.n)
        self.P = gen_permutation(self.n)

        self.C_n = gen_cn(self.G)

        self.G_pub = mul(self.G, self.M)
        self.E_pub = mul(self.W, mul(
            self.D, mul(add(self.C_n, self.P), self.M)))

    def get_public_key(self):
        return (self.E_pub, self.G_pub)

    def decrypt(self, y):
        y_i = mul(y, inv(self.M))

        e_ii = np.zeros(shape=(1, self.n), dtype=int)
        e_ii[0, 0] = 1

        count = 0

        if np.all(mul(y_i, self.H.T) == 0):
            e_ii = np.zeros(shape=(1, self.n), dtype=int)
        else:
            while not np.all(add(mul(y_i, self.H.T), mul(e_ii, self.H.T)) == 0):
                e_ii = np.roll(e_ii, 1)
                count = count + 1

        e_i = mul(e_ii, inv(self.P))

        mG_pub = add(y, -mul(e_i, mul(add(self.C_n, self.P), self.M)))

        indices = np.arange(self.n)
        G_pub_cut = self.G_pub[:, indices[0:self.k]]

        while round(np.linalg.det(G_pub_cut)) % 2 == 0:
            np.random.shuffle(indices)
            G_pub_cut = self.G_pub[:, indices[0:self.k]]

        mG_pub_cut = mG_pub[0, indices[0:self.k]]

        return mul(mG_pub_cut, inv(G_pub_cut))


class Encryptor:
    def __init__(self,  G_pub, E_pub, k=8, n=255, t=1):
        self.n = n
        self.k = k
        self.t = t

        self.G_pub = G_pub
        self.E_pub = E_pub
        self.e = np.random.randint(low=0, high=1023, size=(1, self.n)) % 2

    def encrypt(self, message):
        return add(mul(message, self.G_pub), mul(self.e, self.E_pub))
