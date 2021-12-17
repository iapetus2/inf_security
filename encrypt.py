import numpy as np
from crypto_math.crypto import tobits, encrypt

with open('C:/Users/khafi/IdeaProjects/Bob/inf_security_main/data/encr/input.txt', 'r') as f:
    message = f.read()

ciphered_message = []
for symbol in message:
    bits = tobits(symbol)
    ciphered_symbol = encrypt(
        bits,
        'C:/Users/khafi/IdeaProjects/Bob/inf_security_main/data/keys/another_public_key.txt'
    )
    ciphered_message.append(ciphered_symbol[0])

np.savetxt('C:/Users/khafi/IdeaProjects/Bob/inf_security_main/data/encr/output.txt', np.array(ciphered_message))
