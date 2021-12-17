from os import path
import numpy as np
from .math_gf2 import *


class IKKRKeys:
    def __init__(self, k=8, n=255, t=1):
        self.k = k
        self.n = n
        self.t = t

        self.G = self.read_ham_matrix('./data/ham_matrix/ham.h5')
        self.H = self.read_ham_matrix('./data/ham_matrix/ham2.h5')

    @staticmethod
    def read_ham_matrix(path_to_file):
        f = h5py.File(path_to_file, 'r')
        matrix = np.array(f["DS1"][:])
        matrix = matrix.T
        matrix = np.round(matrix)
        matrix = matrix.astype(int)

        return matrix

    @staticmethod
    def read_public_key(path_to_file):
        m = np.loadtxt(path_to_file, dtype=int)
        n = len(m[0])
        E_pub = m[: n]
        G_pub = m[n:]

        return G_pub, E_pub

    @staticmethod
    def read_private_key(path_to_file):
        m = np.loadtxt(path_to_file, dtype=int)
        n = len(m[0])
        M = m[: n]
        P = m[n: 2 * n]
        C_n = m[2 * n:]

        return M, P, C_n

    def write_public_keys(self, path_to_file):
        np.savetxt(path_to_file, np.vstack((self.E_pub, self.G_pub)))

    def write_private_keys(self, path_to_file):
        np.savetxt(path_to_file, np.vstack((self.M, self.P, self.C_n)))

    def generate_keys(self):
        self.M = gen_non_singular((self.n, self.n))
        self.W = gen_non_singular((self.n, self.n))

        D = gen_diag(self.t, self.n)
        self.P = gen_permutation(self.n)

        self.C_n = gen_cn(self.G)

        self.G_pub = mul(self.G, self.M)
        self.E_pub = mul(self.W, mul(D, mul(add(self.C_n, self.P), self.M)))


def decrypt(cipher_message, path_to_public_keys, path_to_private_keys):
    H = IKKRKeys.read_ham_matrix('./data/ham_matrix/ham2.h5')
    G_pub, E_pub = IKKRKeys.read_public_key(path_to_public_keys)
    n = len(E_pub)
    k = len(G_pub)
    M, P, C_n = IKKRKeys.read_private_key(path_to_private_keys)

    y_i = mul(cipher_message, inv(M))

    e_ii = np.zeros(shape=(1, n), dtype=int)
    e_ii[0, 0] = 1

    count = 0

    if np.all(mul(y_i, H.T) == 0):
        e_ii = np.zeros(shape=(1, n), dtype=int)
    else:
        while not np.all(add(mul(y_i, H.T), mul(e_ii, H.T)) == 0):
            e_ii = np.roll(e_ii, 1)
            count = count + 1

    e_i = mul(e_ii, inv(P))

    mG_pub = add(cipher_message, -mul(e_i, mul(add(C_n, P), M)))

    indices = np.arange(n)
    G_pub_cut = G_pub[:, indices[0:k]]

    while round(np.linalg.det(G_pub_cut)) % 2 == 0:
        np.random.shuffle(indices)
        G_pub_cut = G_pub[:, indices[0:k]]

    mG_pub_cut = mG_pub[0, indices[0:k]]

    return mul(mG_pub_cut, inv(G_pub_cut))


def encrypt(message, path_to_public_keys):
    G_pub, E_pub = IKKRKeys.read_public_key(path_to_public_keys)
    n = len(E_pub)
    e = np.random.randint(low=0, high=1023, size=(1, n)) % 2

    return add(mul(message, G_pub), mul(e, E_pub))


def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result


def frombits(bits):
    chars = []
    for b in range(int(len(bits) / 8)):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)
