import socket
import threading
import time

import generals
# to operate command line commands via python
import os
import subprocess



class echo_client:

    def __init__(self):
        self.PORT = 5050
        self.HEADER = 64  # (bytes) for the first messages that will tell the length of the actual msg length
        self.FORMAT = "utf-8"
        self.CLIENT_DISCONNECT_MESSAGE = "bye"
        self.client_socket_obj = None
        self.CLIENT = None
        self.ADDR = None

    def init(self):
        #ip_address = input(" Please enter ip address or write local -> ") # socket.gethostbyname(socket.gethostname())
        ip_address = 'local'
        if ip_address.lower().strip() == 'local':
            self.CLIENT = socket.gethostbyname(socket.gethostname())
        else:
            self.CLIENT = ip_address

        self.ADDR = (self.CLIENT, self.PORT)
        print(f"Client will connect address: {self.ADDR}")

        self.client_socket_obj = socket.socket(family = socket.AF_INET,     # for sending IPV4 packets over internet
                                               type   = socket.SOCK_STREAM) # for streaming data through the socket
        print("CLIENT: socket created")

        # connect to the server, use server's connection details
        while True:
            try:
                self.client_socket_obj.connect(self.ADDR)
            except socket.error as error:
                print(f"CLIENT: failed to connect server: {self.ADDR}, got error: {error}")
                time.sleep(3)
            else:
                print(f"CLIENT: connected to the ip address {self.ADDR}")
                break

    def send(self, message):
        message = str(message)
        print(f"CLIENT: message: {message} will be send to the server ")
        msg_to_send = message.encode(self.FORMAT)
        length = len(message)

        # make length to be msg as well - to be send as first message
        length_msg = str(length).encode(self.FORMAT)

        # now we need to define header (of 54 bytes) to hold length of the coming message
        # b' ' this means byte representation of ' ' string
        # here we create padding. Padding means spaces. We create message of spaces.
        # Amount of spaces = 64-len of message that holds actual message length
        padding_message = b' ' * (self.HEADER - len(length_msg))
        length_msg += padding_message

        # all ready for send
        # here we can use sendall() to send back all the data we received from client.
        # "send() returns the number of bytes sent, which may be less than the size of the data passed in.
        # You’re responsible for checking this and calling send() as many times as needed to send all of the data"
        self.client_socket_obj.send(length_msg + msg_to_send)
        print(f"CLIENT: message: {message} sent!")


    # through the socket - we send bytes, so we need to encode msg into bytes by specific format utf-8
    def start(self):
        message = input(" -> ")  # ask user to enter message to send to the server from terminal

        while message.lower().strip() != self.CLIENT_DISCONNECT_MESSAGE:
            self.send(message)
            # self.client_socket_obj.send(msg_to_send)

            print("CLIENT: message sent ... and will be replied by the server")
            # received_msg = self.client_socket_obj.recv(2048).decode(self.FORMAT)
            # print(f"CLIENT from send method: {received_msg}")
            message = input(" Please enter message to send to the Server -> ")

        self.client_socket_obj.close()  # 1. first Client closes its connection


    def execute_msg(self, received_msg):
        gen_cmd = generals.generals()

        only_cmd = received_msg.split()[0]
        only_params = received_msg.replace(received_msg.split(" ")[0], "").strip()

        if only_cmd not in gen_cmd.commands_dict:
            print(f"CLIENT: command: {received_msg} is not supported, therefore will not be executed")
        else:

            result = gen_cmd.commands_dict[only_cmd][1](only_params)
            return result


    def handle_server(self):
        print("CLIENT: client thread is ready to get messages from server ")

        while True:
            received_msg = self.client_socket_obj.recv(2048).decode(self.FORMAT)
            print(f"CLIENT: (handle server), received msg: {received_msg}, will be executed ...")

            result = self.execute_msg(received_msg)

            # return result back to the server for further processing
            self.send(result)



    def start_session(self):

        # get messages from server
        thread_server = threading.Thread(target=self.handle_server)
        thread_server.start()

        # send messages to server
        self.start()



if __name__ == "__main__":
    my_client = echo_client()
    try:
        my_client.init()
        my_client.start_session()

    except socket.error as error:
        print(f"CLIENT side got EXCEPTION: {error}")