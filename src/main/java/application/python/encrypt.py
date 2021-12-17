import numpy as np
from crypto_math.crypto import tobits, encrypt

with open('C:/Users/khafi/IdeaProjects/Bob/inf_security_main/src/main/java/application/python/data/encr/input.txt', 'r') as f:
    message = f.read()

ciphered_message = []
for symbol in message:
    bits = tobits(symbol)
    ciphered_symbol = encrypt(
        bits,
        'C:/Users/khafi/IdeaProjects/Bob/inf_security_main/src/main/java/application/python/data/keys/another_public_key.txt'
    )
    ciphered_message.append(ciphered_symbol[0])

np.savetxt('C:/Users/khafi/IdeaProjects/Bob/inf_security_main/src/main/java/application/python/data/encr/output.txt', np.array(ciphered_message))
