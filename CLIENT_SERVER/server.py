import socket
import sys
import threading
import generals




# Server must start running first - else if the client is started first before the server program is started
# an error will be reported, stating ConnectionRefusedError: [Errno 61] Connection refused
# CLIENT_DISCONNECT_MESSAGE = when server receives this kind of message - we disconnect client
class echo_server:

    def __init__(self):
        self.SERVER   = socket.gethostbyname(socket.gethostname())
        self.PORT   = 5050
        self.ADDR   = (self.SERVER, self.PORT)
        self.HEADER = 64  # (bytes) for the first messages that will tell the length of the actual msg length
        self.FORMAT = "utf-8"
        self.server_socket_obj = None
        self.all_client_connections = {}
        self.num_of_clients = 0

        #self.all_commands = {Commands.GET_ALL_PROCESSES: "tasklist"}


    # The main difference between Server and Client is that Server must perform a bind operation.
    # server must bind together the address and host.
    # SOCK_STREAM (simply called TCP) means data is sent in sequential order and not in random order, SOCK_DGRAM (called UDP)
    # it tells how to package the data for sending, these are most common ways to talk
    # AF_INET (Address Format Internet) tells the socket to communicate with IP addresses
    # it is important to know that data you send (payload) is packed into packets with external metadata
    def init(self):

        print(f"SERVER: host: {str(self.SERVER)}, port: {str(self.PORT)}")

        try:
            # create socket object to communicate with socket
            self.server_socket_obj = socket.socket(family=socket.AF_INET,
                                                   type  =socket.SOCK_STREAM)
        except socket.error as error:
            print(f"SERVER: failed to create socket, reason: {str(error)}")
            sys.exit()
        print("SERVER: socket created, going to bind socket to IP address & Port ")

        # bind socket to IP address and port at the server's PC
        try:
            self.server_socket_obj.bind(self.ADDR)
        except socket.error as msg:
            print
            'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()
        print("SERVER: socket binding completed")

    # pay attention this method will run per client connection in parallel
    # recv() is blocking method - means wait for info from client - that is why we must do it in thread
    # so other clients can also connect to the server. then upon receive we will do something about received msg
    # here we will extract data in 2 steps: 1. extract data that tells us about the real data length, 2. extract real data

    # when client wishes to disconnect - it sends message !DISCONNECT - and right after it closes connection
    # at this moment at the server side we will breake from blocking wait on method recv() and tmp_msg will be None (null)
    # this means upon client disconnection the server receives empty message
    # if client sends message where there is a single space - it is not None therefor Server receives this message and
    # does not close the Client connection !!
    def handle_client(self, conn, addr, client_number):
        print(f"\nSERVER: [NEW CLIENT CONNECTION] {addr} is now connected\n")

        # also possible to use block with, this way:
        # with conn:
        # and do not use explicitly the conn.close() it will be called implicitly after with block
        while True:
            tmp_msg = conn.recv(self.HEADER).decode(self.FORMAT)

            if not tmp_msg:
                break

            length = int(tmp_msg)
            actual_msg = conn.recv(length).decode(self.FORMAT)

            print(f"SERVER: received: {actual_msg} from {addr}")

            # here we can use sendall() to send back all the data we received from client.
            # "send() returns the number of bytes sent, which may be less than the size of the data passed in.
            # You’re responsible for checking this and calling send() as many times as needed to send all of the data"
            #conn.send(f"replied message {actual_msg}, for client connection {addr}".encode(self.FORMAT))

        conn.close()
        print(f"SERVER: disconnected Client {addr} ")
        # remove client connection from dict
        self.all_client_connections.pop(addr)

        self.list_connections()

    def print_supported_functionalities(self):
        print("send - Send messages to specific client. Format: <send> <Client_index> <message>")
        print("conns - Get existing Client connections. Format: <conns>")
        print("cmds - Get available commands to be executed by Server. Format: <comms>")


    def list_supported_commands(self):
        print("\nList of supported command:")
        gen_cmd = generals.generals()
        [print(f"Command: {cmd_name}, functionality: {cmd}\n") for cmd_name, cmd in gen_cmd.commands_dict.items()]


    def get_functionality(self, request):
        request = str(request)

        if request == "help":
            self.print_supported_functionalities()
            return None

        elif request == "conns":
            self.list_connections()
            return None

        elif request.startswith("send"):
            return "send"

        elif request.startswith("cmds"):
            self.list_supported_commands()
            return None
        else:
            # incorrect format to send msg from server -> client
            self.print_supported_functionalities()
            return None


    def parse_send_command(self, command_line_msg):
        if not command_line_msg or not command_line_msg.strip():
            print("SERVER: nothing to execute")
            return False, -1, -1

        command_line_msg = command_line_msg.replace("send", "").strip()
        if len(command_line_msg.split(" ")) < 2:
            print("SERVER: incorrect server message format,\nformat is: <send> <client index> <message>")
            return False, -1, -1

        # check client index indicated not as white space
        if not command_line_msg.split(" ")[0] or not command_line_msg.split(" ")[0].strip():
            print("SERVER: Client index: was not indicated !")
            return False, -1, -1

        # check if client index indicated as digital
        if not command_line_msg.split(" ")[0].isdigit():
            print("SERVER: incorrect format! Second parameter must be numeric, it represents client index")
            return False, -1, -1

        client_index = int(command_line_msg.split(" ")[0].strip())

        if client_index not in self.all_client_connections:
            print(f"SERVER: Client: {client_index}, is not connected")
            return False, -1, -1
                  #f" connection: {self.all_client_connections[index]}")

        print(f"SERVER: Client: {client_index} found, connection: {self.all_client_connections[client_index]}")

        if not command_line_msg.replace(command_line_msg.split(" ")[0], "") or \
           not command_line_msg.replace(command_line_msg.split(" ")[0], "").strip():
            print("SERVER: command: was not indicated !")
            return False, -1, -1

        cmd = command_line_msg.replace(command_line_msg.split(" ")[0], "").strip()

        # get command only without params - to check if supported
        only_cmd = cmd.split()[0]

        print(f"SERVER: user asked to send msg: {cmd} to Client[{client_index}], conn:{self.all_client_connections[client_index]}")
        gen_cmd = generals.generals()
        if only_cmd not in gen_cmd.commands_dict:
            print(f"SERVER: command: {cmd} is not supported")
            return False, -1, -1

        print(f"SERVER: command: {cmd} is supported and will be sent")
        return True, client_index, cmd


    # Server thread to send messages to the Client
    def handle_server(self):

        while True:
            # read msg for client only if there are connected clients (at least one client)
            if self.all_client_connections:
                request = input("Waiting for request \n"
                                "'help' - to get directions,\n"
                                "'send' - to send command to client from the list of available cmds,\n"
                                "'conns' - to see all existing clients connections)\n"
                                "'cmds' - to get all supported commands\n-> ")

                if not request or not request.strip():
                    print("SERVER: incorrect server message format, msg is missing!")
                else:
                    res = self.get_functionality(request)

                    if res == "send":
                        success, client_index, cmd = self.parse_send_command(request)

                        if success:
                            # build message
                            msg = cmd.encode(self.FORMAT)  # or this way: bytes(msg, self.FORMAT)
                            # length = len(msg)
                            # length_msg = str(length).encode(self.FORMAT)
                            # padding_msg = b'' * (self.HEADER - len(length_msg))
                            # length_msg += padding_msg
                            # ---

                            conn = self.all_client_connections[client_index][0]
                            print(f"SERVER: sending message {msg} to the client")
                            conn.send(msg)
                            print("SERVER: message sent !")



    # listen()
    # we are moving socket to the state where it is listening for incoming connections.
    # From general socket object we make it to be -> server socket
    # socket enters into the TCP state WAIT. We actually make server listen to incoming connections
    # listening method is not blocking
    # accept()
    # it is blocking method - it will wait till the new client connection occurs, and then at the moment it occurs we
    # save its address and actual client socket object to be able to send back data to the client
    def start(self):
        print("SERVER: is starting ...")

        self.server_socket_obj.listen(10)
        print(f"SERVER: now is listening on {self.SERVER} ")

        thread_server = threading.Thread(target=self.handle_server)
        thread_server.start()


        while True:
            conn, addr = self.server_socket_obj.accept()

            self.all_client_connections[self.num_of_clients] = (conn, addr)
            self.num_of_clients += 1

            thread_handles_client_connection = threading.Thread(target = self.handle_client, # method to handle new client
                                                                args   = (conn, addr, threading.activeCount() - 2))       # client connection details
            thread_handles_client_connection.start()
            # tell us how many threads (clients) are active (connected) in this python process
            # we subtract 1 because of the current thread we run,
            # inside which we wait with method accept() for new client to connect and upon connection create new thread



            self.list_connections()


    def list_connections(self):
        if len(self.all_client_connections) > 0:
            print(f"SERVER: Currently connected client connections are: {len(self.all_client_connections)} ({self.num_of_clients})")
            [print(f"Index: {key}, Client: {value[1]}") for key, value in self.all_client_connections.items()]
        else:
            print("No Client connections exist")

if __name__ == "__main__":
    my_server = echo_server()
    try:
        my_server.init()
        my_server.start()
    except socket.error as error:
        print(f"SERVER side got exception {error}")
