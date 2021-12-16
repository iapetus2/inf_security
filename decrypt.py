import numpy as np
from crypto_math.crypto import decrypt, frombits

ciphered_message = np.loadtxt('data/decr/input.txt', dtype=int)

deciphered_message = []
for ciphered_symbol in ciphered_message:
    bits = decrypt(
        ciphered_symbol,
        'data/keys/my_public_key.txt',
        'data/keys/my_private_key.txt'
    )
    curr_symbol = frombits(bits)
    deciphered_message.append(curr_symbol)

with open('data/decr/output.txt', 'w') as f:
    f.write(''.join(deciphered_message))
