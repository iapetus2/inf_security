import numpy
import numpy as np


def add(arg1, arg2):
    return (arg1 + arg2) % 2


def mul(arg1, arg2):
    return (arg1 @ arg2) % 2


def inv(arg):
    inv_f = np.linalg.inv(arg) * np.linalg.det(arg)
    inv_f = numpy.round(inv_f)
    inv_i = inv_f.astype(int)
    return inv_i % 2


def gen_non_singular(shape):
    s = np.random.randint(low=0, high=1023, size=shape) % 2
    while round(np.linalg.det(s)) % 2 == 0:
        s = np.random.randint(low=0, high=1023, size=shape) % 2

    return s


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

    u_rand = np.random.randint(low=0, high=1023, size=(1, k)) % 2
    while np.sum(u_rand ** 2) == 0:
        u_rand = np.random.randint(low=0, high=1023, size=(1, k)) % 2



    c = mul(u_rand, G)

    C_n = np.zeros(shape=(n, n), dtype=int)
    cnt = 0

    for i in range(n):
        if c[0, i] == 0:
            C_n[i] = np.random.randint(low=0, high=1023, size=n) % 2
        else:
            cnt = cnt + 1

    u_rand_2 = np.random.randint(low=0, high=1023, size=(cnt, k)) % 2
    while np.sum(u_rand_2 ** 2) == 0:
        u_rand_2 = np.random.randint(low=0, high=1023, size=(cnt, k)) % 2

    c_2 = mul(u_rand_2, G)

    summa = np.zeros(shape=n, dtype=int)

    cnt1 = 0
    for i in range(n):
        if c[0, i] == 1:
            if cnt1 == cnt - 1:
                C_n[i] = add(c, -summa)
            else:
                C_n[i] = c_2[cnt1]
                summa = add(summa, c_2[cnt1])
                cnt1 = cnt1 + 1

    return C_n






