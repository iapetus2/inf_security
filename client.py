from __future__ import print_function

import logging

import grpc
from crypto_math.crypto import *
import server_pb2
import server_pb2_grpc


def join_np_array(data):
    s = ''
    for i in data:
        s += str(i)
        s += ' '

    return s[:-1]


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = server_pb2_grpc.IKKRStub(channel)

        crypto_keys = IKKRKeys(k=8, n=255, t=1).generate_keys()
        E_pub, G_pub = crypto_keys.get_public_keys()
        keys = np.vstack((E_pub, G_pub))
        stub.PutPublicKeys(server_pb2.PutKeysInput(
            listofbits=[join_np_array(list_of_bits) for list_of_bits in keys])
        )

        response = stub.GetPublicKeys(server_pb2.GetKeysInput())
        keys = []
        for string_of_bits in response.listofbits:
            keys.append(list(map(int, string_of_bits.split())))
        n = len(keys[0])  
        E_pub = np.array(keys[:n])
        G_pub = np.array(keys[n:])

        message = ''
        while message != 'end':
            message = input("Enter your message: ")
            if message == 'end':
                break

            ciphered_message = []
            for symbol in message:
                bits = tobits(symbol)
                ciphered_symbol = encrypt(
                    bits, 
                    public_keys=crypto_keys.get_curr_keys(E_pub, G_pub)
                )
                ciphered_message.append(ciphered_symbol[0])

            response = stub.ReadThis(server_pb2.ReadInput(
                listofbits=[
                    join_np_array(list_of_bits)
                    for list_of_bits in ciphered_message
                ]
            ))

            ciphered_message = []
            for string_of_bits in response.listofbits:
                ciphered_message.append(list(map(int, string_of_bits.split())))

            deciphered_message = []
            for ciphered_symbol in ciphered_message:
                bits = decrypt(
                    ciphered_symbol,
                    public_keys=crypto_keys.get_public_keys(),
                    private_keys=crypto_keys.get_private_keys()
                )
                curr_symbol = frombits(bits)
                deciphered_message.append(curr_symbol)

            message = ''.join(deciphered_message)
            print(message)


if __name__ == '__main__':
    logging.basicConfig()
    run()
