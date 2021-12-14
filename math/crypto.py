import numpy as np
from gf2 import inv, mul, add, gen_non_singular, gen_permutation, gen_diag, gen_cn


class Decryptor:
    k = 4
    n = 12
    t = 1

    M = np.empty((n, n))
    W = np.empty((n, n))
    D = np.empty((n, n))
    P = np.empty((n, n))
    G = np.empty((k, n))
    C_n = np.empty((n, n))

    G_pub = np.empty((k, n))
    E_pub = np.empty((n, n))

    def __init__(self, k=4, n=12, t=1):
        self.M = gen_non_singular((n, n))
        self.W = gen_non_singular((n, n))
        self.D = gen_diag(t, n)
        self.P = gen_permutation(n)

        self.G = np.array([[0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0],
                           [0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0],
                           [1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
                           [1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0]], dtype=int) ## TMP

        self.C_n = mul(gen_cn(self.G), self.P)

        self.G_pub = mul(self.G, self.M)
        self.E_pub = mul(self.W, mul(self.D, mul(add(self.C_n, self.P), self.M)))

    def decrypt(self, y, e):
        y_i = mul(y, inv(self.M))

        e_ii = mul(e, mul(self.W, mul(self.D, self.P)))
        e_i = mul(e_ii, inv(self.P))

        mGpub = add(y, -mul(e_i, mul(add(self.C_n, self.P), self.M)))

        indices = np.arange(self.n)
        Gpub_cut = self.G_pub[:, indices[0:self.k]]

        while round(np.linalg.det(Gpub_cut)) % 2 == 0:
            np.random.shuffle(indices)
            Gpub_cut = self.G_pub[:, indices[0:self.k]]

        mGpub_cut = mGpub[0, indices[0:self.k]]

        return mul(mGpub_cut, inv(Gpub_cut))


class Encryptor:

    k = 4
    n = 12
    t = 1
    e = np.empty((1, n))

    G_pub = np.empty((k, n))
    E_pub = np.empty((n, n))

    def __init__(self,  G_pub_de, E_pub_de, k=4, n=12, t=1):
        self.G_pub = G_pub_de
        self.E_pub = E_pub_de
        self.e = np.random.randint(low=0, high=1023, size=(1, self.n)) % 2

    def encrypt(self, message):
        return add(mul(message, self.G_pub), mul(self.e, self.E_pub))
