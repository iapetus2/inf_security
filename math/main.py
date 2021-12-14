import numpy as np
from crypto import Decryptor, Encryptor
from gf2 import inv, mul, add

I = np.array([[0, 1, 0],
              [1, 0, 0],
              [0, 0, 1]])

decryptor = Decryptor()
E_pub_de = decryptor.E_pub
G_pub_de = decryptor.G_pub

encryptor = Encryptor(G_pub_de, E_pub_de)

message = np.random.randint(low=0, high=1023, size=(1, 4)) % 2
print(message)

y = encryptor.encrypt(message)

m_d = decryptor.decrypt(y, encryptor.e)
print(m_d)

for i in range(10):
    print(2 ** i - i - 1)






