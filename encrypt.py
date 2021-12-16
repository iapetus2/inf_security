import numpy as np
from crypto_math.crypto import tobits, encrypt

with open('data/encr/input.txt', 'r') as f:
    message = f.read()

ciphered_message = []
for symbol in message:
    bits = tobits(symbol)
    ciphered_symbol = encrypt(
        bits,
        'data/keys/another_public_key.txt'
    )
    ciphered_message.append(ciphered_symbol[0])

np.savetxt('data/encr/output.txt', np.array(ciphered_message))
