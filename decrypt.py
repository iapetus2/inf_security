import numpy as np
from crypto_math.crypto import decrypt, frombits

ciphered_message = np.loadtxt('C:/Users/khafi/IdeaProjects/Bob/inf_security_main/data/decr/input.txt', dtype=int)

deciphered_message = []
for ciphered_symbol in ciphered_message:
    bits = decrypt(
        ciphered_symbol,
        'C:/Users/khafi/IdeaProjects/Bob/inf_security_main/data/keys/my_public_key.txt',
        'C:/Users/khafi/IdeaProjects/Bob/inf_security_main/data/keys/my_private_key.txt'
    )
    curr_symbol = frombits(bits)
    deciphered_message.append(curr_symbol)

with open('C:/Users/khafi/IdeaProjects/Bob/inf_security_main/data/decr/output.txt', 'w') as f:
    f.write(''.join(deciphered_message))
