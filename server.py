from concurrent import futures
import logging

import grpc
import server_pb2
import server_pb2_grpc

from crypto_math.crypto import *
import numpy as np


def join_np_array(data):
    s = ''
    for i in data:
        s += str(i)
        s += ' '

    return s[:-1]


class IKKR(server_pb2_grpc.IKKRServicer):
    def __init__(self):
        self.keys = IKKRKeys(k=8, n=255, t=1).generate_keys()
        self.keys.write_public_keys('data/keys/server_public_key.txt')
        self.keys.write_private_keys('data/keys/server_private_key.txt')

    def GetPublicKeys(self, request, context):
        E_pub, G_pub = self.keys.get_public_keys()
        keys = np.vstack((E_pub, G_pub))

        return server_pb2.GetKeysOutput(listofbits=[join_np_array(list_of_bits) for list_of_bits in keys])

    def PutPublicKeys(self, request, context):
        keys = []
        for string_of_bits in request.listofbits:
            keys.append(list(map(int, string_of_bits.split())))
        n = len(keys[0])
        self.E_pub = np.array(keys[:n])
        self.G_pub = np.array(keys[n:])

        return server_pb2.GetKeysOutput()

    def ReadThis(self, request, context):
        ciphered_message = []
        for string_of_bits in request.listofbits:
            ciphered_message.append(list(map(int, string_of_bits.split())))
        deciphered_message = []
        for ciphered_symbol in ciphered_message:
            bits = decrypt(
                ciphered_symbol,
                public_keys=self.keys.get_public_keys(),
                private_keys=self.keys.get_private_keys()
            )
            curr_symbol = frombits(bits)
            deciphered_message.append(curr_symbol)

        message = ''.join(deciphered_message)
        print(message)

        message = input("Enter you message: ")
        ciphered_message = []
        for symbol in message:
            bits = tobits(symbol)
            ciphered_symbol = encrypt(
                bits,
                public_keys=self.keys.get_curr_keys(self.E_pub, self.G_pub)
            )
            ciphered_message.append(ciphered_symbol[0])

        return server_pb2.ReadOutput(
            listofbits=[join_np_array(list_of_bits) for list_of_bits in ciphered_message
                        ]
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_pb2_grpc.add_IKKRServicer_to_server(IKKR(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
