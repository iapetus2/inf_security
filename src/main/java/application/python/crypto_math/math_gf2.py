import numpy as np
import h5py


def add(arg1, arg2):
    return (arg1 + arg2) % 2


def mul(arg1, arg2):
    return (arg1 @ arg2) % 2


def inv(arg):
    inv_f = np.linalg.inv(arg) * np.linalg.det(arg)
    inv_f = np.round(inv_f)
    inv_i = inv_f.astype(int)
    return inv_i % 2


def gen_non_singular(shape):
    s = np.identity(shape[0], dtype=int)
    np.random.shuffle(s)
    return inv(s)


def gen_diag(t, dim):
    d = np.zeros(shape=(dim, dim), dtype=int)
    arr = np.zeros(shape=dim, dtype=int)
    arr[:t] = 1
    np.random.shuffle(arr)

    for i in range(dim):
        if arr[i] == 1:
            d[i, i] = 1

    return d


def gen_permutation(dim):
    p = np.identity(dim, dtype=int)
    np.random.shuffle(p)
    return p


def gen_cn(G):
    k = np.shape(G)[0]
    n = np.shape(G)[1]

    U_rand = np.random.randint(low=0, high=1023, size=(n, k)) % 2
    C_n = mul(U_rand, G)
    return C_n
