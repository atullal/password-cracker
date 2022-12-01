import socket
import string
import sys
import threading
from multiprocessing import Pool
import argparse
import datetime as dt
import os
import time
from threading import Thread

MSG_LENGTH = 1024

small_letters = [*string.ascii_lowercase]
capital_letters = [*string.ascii_uppercase]
all_letters = small_letters+capital_letters
file_names = os.listdir("./dictionary")
connections = []
clients_in_use = []

class ThreadReturn(Thread):
    
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

def create_dictionary(l1):
    if 'A' <= l1 <= 'Z':
        prefix = "capital_"
    else:
        prefix = "small_"
    file = open("./dictionary/"+prefix+l1+".txt", "w")
    file_names.append(prefix+l1+".txt")
    print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Creating dictionary {prefix+l1+'.txt'}")
    for l2 in all_letters:
        for l3 in all_letters:
            for l4 in all_letters:
                for l5 in all_letters:
                    file.write(l1+l2+l3+l4+l5+"\n")
    file.close()
    print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Saved dictionary {prefix+l1+'.txt'}")
    return None


def client_handler(conn, addr, string_to_decode):
    try:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Total Number of Active Connections on SERVER is {threading.active_count() - 1}\n")
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Connected to client {addr}\n")
        while file_names:
            if file_names[0].startswith("."):
                file_names.pop(0)
            conn.send(string_to_decode.encode())
            response = conn.recv(MSG_LENGTH).decode()
            print(f"Response String: {response}")
            conn.send(file_names[0].encode())
            response = conn.recv(MSG_LENGTH).decode()
            print(f"Response File name : {response}")
            filename= "./dictionary/"+file_names[0]
            file_names.pop(0)
            file = open(filename, "rb")
            data = file.read()
            file.close()
            conn.send(data)
            conn.send("FOE".encode())
            response = conn.recv(MSG_LENGTH).decode()
            print(f"Response File data : {response}")
            response = conn.recv(MSG_LENGTH).decode()
            print(f"Final Response : {response}")
            if response == "Password not found":
                continue
            else:
                # todo: terminate all threads
                break
    except (socket.error, socket.gaierror, socket.herror) as error:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Socket Error: {error}")
        conn.close()
    except (ConnectionError, ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError) as error:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Connection Error : {error}")
        conn.close()
    except Exception as error:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Other Error : {error}")
        conn.close()
    except (KeyboardInterrupt, InterruptedError) as error:
        print(f"Interrupt Error : {error}")
        conn.close()
    finally:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Server has a total of {threading.active_count() - 2} active connection(s) "
              f"with the client(s).\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("server_port",
                        help="Enter the port number on which you want to start the socket on the server.",
                        type=int)
    parser.add_argument("string_to_decode",
                        help="Enter the string that you want to decode.",
                        type=str)
    args = parser.parse_args()
    server_port = args.server_port
    string_to_decode = args.string_to_decode
    if len(string_to_decode) != 32:
        print("Invalid String")
        exit()
    addr = ('', server_port)
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(addr)
        server.listen(10)
        for l1 in all_letters:
            thread = threading.Thread(target=create_dictionary, args=l1)
            thread.start()
        thread.join()
        print(file_names)
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Server is listening.\n")
        while True:
            conn, addr = server.accept()
            print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] CLIENT {addr[0]} connected to the SERVER.")
            thread = threading.Thread(target=client_handler, args=(conn, addr, string_to_decode))
            thread.start()
    except (socket.error, socket.gaierror, socket.herror) as error:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Socket Error : {error}")
    except socket.timeout:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Connection timed out!!")
    except (ConnectionError, ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError) as error:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Connection Error : {error}")
    except Exception as error:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Other Error : {error}")
    except (KeyboardInterrupt, InterruptedError) as error:
        print(f"Interrupt Error : {error}")
    finally:
        exit(0)

def get_available_clients():
    response = []
    for client in connections:
        is_in_use = False
        if client in clients_in_use:
            is_in_use = True
        response.append({
            "address": client[0][0],
            "port": client[0][1],
            "inUse": is_in_use
        })
    return {
        "available_clients": response
    }

def create_dictionaries():
    with Pool(52) as p:
        p.map(create_dictionary, all_letters)

def connect_client(conn, addr):
    try:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Total Number of Active Connections on SERVER is {threading.active_count() - 2}\n")
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Connected to client {addr}\n")
        while file_names:
            if file_names[0].startswith("."):
                file_names.pop(0)
            conn.send(string_to_decode.encode())
            response = conn.recv(MSG_LENGTH).decode()
            print(f"Response String: {response}")
            conn.send(file_names[0].encode())
            response = conn.recv(MSG_LENGTH).decode()
            print(f"Response File name : {response}")
            filename= "./dictionary/"+file_names[0]
            file_names.pop(0)
            file = open(filename, "rb")
            data = file.read()
            file.close()
            conn.send(data)
            conn.send("FOE".encode())
            response = conn.recv(MSG_LENGTH).decode()
            print(f"Response File data : {response}")
            response = conn.recv(MSG_LENGTH).decode()
            print(f"Final Response : {response}")
            if response == "Password not found":
                continue
            else:
                # todo: terminate all threads
                break
    except (socket.error, socket.gaierror, socket.herror) as error:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Socket Error: {error}")
        conn.close()
    except (ConnectionError, ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError) as error:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Connection Error : {error}")
        conn.close()
    except Exception as error:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Other Error : {error}")
        conn.close()
    except (KeyboardInterrupt, InterruptedError) as error:
        print(f"Interrupt Error : {error}")
        conn.close()
    finally:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Server has a total of {threading.active_count() - 2} active connection(s) "
              f"with the client(s).\n")

def send_to_client(conn, file_to_process, hash_string):
    try:
        conn.send(hash_string.encode())
        response = conn.recv(MSG_LENGTH).decode()
        print(f"Response String: {response}")

        conn.send(file_to_process.encode())
        response = conn.recv(MSG_LENGTH).decode()
        print(f"Response File name : {response}")

        filename= "./dictionary/"+file_to_process
        file = open(filename, "rb")
        data = file.read()
        file.close()
        conn.send(data)
        conn.send("FOE".encode())
        response = conn.recv(MSG_LENGTH).decode()
        print(f"Response File data : {response}")
        response = conn.recv(MSG_LENGTH).decode()
        print(f"Final Response : {response}")
    except (socket.error, socket.gaierror, socket.herror) as error:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Socket Error: {error}")
        conn.close()
    except (ConnectionError, ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError) as error:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Connection Error : {error}")
        conn.close()
    except Exception as error:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Other Error : {error}")
        conn.close()
    except (KeyboardInterrupt, InterruptedError) as error:
        print(f"Interrupt Error : {error}")
        conn.close()
    finally:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Server has a total of {threading.active_count() - 2} active connection(s) "
              f"with the client(s).\n")

def process_hash(conn, file_combinations, hash_string):
    try:
        result = "Not found"
        while len(file_combinations):
            file_to_process = file_combinations.pop(0)
            conn.send(hash_string.encode())
            response = conn.recv(MSG_LENGTH).decode()
            print(f"Response String: {response}")

            conn.send(file_to_process.encode())
            response = conn.recv(MSG_LENGTH).decode()
            print(f"Response File name : {response}")

            filename= "./dictionary/"+file_to_process
            file = open(filename, "rb")
            data = file.read()
            file.close()
            conn.send(data)
            conn.send("FOE".encode())
            response = conn.recv(MSG_LENGTH).decode()
            print(f"Response File data : {response}")
            response = conn.recv(MSG_LENGTH).decode()
            print(f"Final Response : {response}")
            if response == "Password not found":
                continue
            else:
                # todo: terminate all threads, find a better way
                for i in range(len(file_combinations)):
                    file_combinations.pop(0)
                if conn in clients_in_use:
                    clients_in_use.remove(conn)
                print(f"Returning Final Response : {response}")
                result = response
                return response
                break
        clients_in_use.remove(conn)
        print("Returning: "+result)
        return result
    except (socket.error, socket.gaierror, socket.herror) as error:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Socket Error: {error}")
        if conn in clients_in_use:
            clients_in_use.remove(conn)
        if conn in connections:
            connections.remove(conn)
        conn.close()
    except (ConnectionError, ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError) as error:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Connection Error : {error}")
        if conn in clients_in_use:
            clients_in_use.remove(conn)
        if conn in connections:
            connections.remove(conn)
        conn.close()
    except Exception as error:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Other Error : {error}")
        if conn in clients_in_use:
            clients_in_use.remove(conn)
        if conn in connections:
            connections.remove(conn)
        conn.close()
    except (KeyboardInterrupt, InterruptedError) as error:
        print(f"Interrupt Error : {error}")
        if conn in clients_in_use:
            clients_in_use.remove(conn)
        if conn in connections:
            connections.remove(conn)
        conn.close()
    finally:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Server has a total of {threading.active_count() - 2} active connection(s) "
              f"with the client(s).\n")
        if conn in clients_in_use:
            clients_in_use.remove(conn)


    # if(len(file_combinations) == 0):
    #     break
    # file_to_process = file_combinations.pop(0)
    # conn = connections.pop(0)

def decrypt_md5(hash_string, required_clients):
    print(hash_string)
    file_combinations = ["small_"+name+".txt" for name in small_letters]
    file_combinations.extend(["capital_"+name+".txt" for name in capital_letters])

    for requested_client in required_clients:
        for in_use_client in clients_in_use:
            if in_use_client[0][0] == requested_client["address"] and in_use_client[0][1] == requested_client["port"]:
                return {
                    "err": "Requested clients not available"
                }
    selected_clients = []
    for requested_client in required_clients:
        for client in connections:
            if client[0][0] == requested_client["address"] and client[0][1] == requested_client["port"]:
                selected_clients.append(client)
                clients_in_use.append(client)
    
    request_threads = []

    for conn in selected_clients:
        thread = ThreadReturn(target=process_hash, args=(conn[1], file_combinations, hash_string))
        request_threads.append(thread)
        thread.start()
    
    results = []
    for request_thread in request_threads:
        results.append(request_thread.join())

    for result in results:
        if result != "Not found":
            return {
                "password": result
            }

def start_server_node(server_port):
    addr = ('', server_port)
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(addr)
        server.listen(10)

        print(file_names)
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Server is listening.\n")
        while True:
            conn, addr = server.accept()
            print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] CLIENT {addr[0]} connected to the SERVER.")
            connections.append([addr, conn])
            # thread = threading.Thread(target=connect_client, args=(conn, addr))
            # thread.start()
    except (socket.error, socket.gaierror, socket.herror) as error:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Socket Error : {error}")
    except socket.timeout:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Connection timed out!!")
    except (ConnectionError, ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError) as error:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Connection Error : {error}")
    except Exception as error:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Other Error : {error}")
    except (KeyboardInterrupt, InterruptedError) as error:
        print(f"Interrupt Error : {error}")
    finally:
        exit(0)

def start_server_node_thread(server_port):
    thread = threading.Thread(target=start_server_node, args=(server_port, ))
    thread.start()

if __name__ == "__main__":
    create_dictionaries()
    start_server_node_thread(5002)
    time.sleep(5)
    decrypt_md5("b1a1bca13bc04f19384049a0093413b0")


# Solution 1
# Start server nodes
# Add client nodes
# Request comes with hash
# Insert all combinations of (hash, filename) into the queue
# Notify workers to check queue
# Dequeue and process
# Problems - when we find the solution, we need to ignore all the items with same hash (which is not ideal, there can two requests of same hash) or we still need to keep on processing

# Solution 2
# Start server nodes
# Add client nodes
# Request comes with hash
# Insert hash into the queue
# Notify a single worker thread, which creates a new queue on demand with all possible filenames for the request
# After creating the queue, it starts threads of clients to process the request (for loop)
# Dequeue and process