from crypto_math.crypto import IKKRKeys

keys_generator = IKKRKeys(k=8, n=255, t=1)
keys_generator.generate_keys()
keys_generator.write_public_keys('C:/Users/khafi/IdeaProjects/Bob/inf_security_main/data/keys/my_public_key.txt')
keys_generator.write_private_keys('C:/Users/khafi/IdeaProjects/Bob/inf_security_main/data/keys/my_private_key.txt')