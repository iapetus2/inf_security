import numpy as np
from crypto import Decryptor, Encryptor


decryptor = Decryptor(k=8, n=255, t=1)
E_pub = decryptor.E_pub
G_pub = decryptor.G_pub

encryptor = Encryptor(G_pub, E_pub, k=8, n=255, t=1)

message = np.random.randint(low=0, high=1023, size=(1, 8)) % 2
print('Message:')
print(message)
ciphered_message = encryptor.encrypt(message)

print('Decrypted message:')
decrypted_message = decryptor.decrypt(ciphered_message)
print(decrypted_message)
