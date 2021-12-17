import numpy as np
from crypto_math.crypto import *

keys_generator = IKKRKeys(k=8, n=255, t=1)
keys_generator.generate_keys()
keys_generator.write_public_keys('C:/Users/khafi/IdeaProjects/Bob/inf_security_main/src/main/java/application/python/data/keys/public_key.txt')
keys_generator.write_private_keys('C:/Users/khafi/IdeaProjects/Bob/inf_security_main/src/main/java/application/python/data/keys/private_key.txt')

message = input('Message: ')
ciphered_message = []
for symbol in message:
    bits = tobits(symbol)
    ciphered_symbol = encrypt(bits, 'C:/Users/khafi/IdeaProjects/Bob/inf_security_main/src/main/java/application/python/data/keys/public_key.txt')
    ciphered_message.append(ciphered_symbol[0])


print(len(ciphered_message))


deciphered_message = []
for ciphered_symbol in ciphered_message:
    bits = decrypt(ciphered_symbol, 'C:/Users/khafi/IdeaProjects/Bob/inf_security_main/src/main/java/application/python/data/keys/public_key.txt', 'C:/Users/khafi/IdeaProjects/Bob/inf_security_main/src/main/java/application/python/data/keys/private_key.txt')
    curr_symbol = frombits(bits)
    deciphered_message.append(curr_symbol)

print(''.join(deciphered_message))
