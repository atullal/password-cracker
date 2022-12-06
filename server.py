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
import hashlib
import filename_hash
import timeit

MSG_LENGTH = 1024

small_letters = [*string.ascii_lowercase]
capital_letters = [*string.ascii_uppercase]
all_letters = small_letters+capital_letters
request_id_counter = 1
file_names = os.listdir("./dictionary")
connections = []
clients_in_use = []
files_processing = {}
threads_request_id = {}
stats_request_id = {}

filename_hash_dict = filename_hash.filename_hash_dictionary

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

def create_dictionary(l1l2):
    l1, l2 = l1l2
    if 'A' <= l1 <= 'Z':
        prefix1 = "capital_"
    else:
        prefix1 = "small_"
        
    if 'A' <= l2 <= 'Z':
        prefix2 = "capital_"
    else:
        prefix2 = "small_"

    filename = prefix1+l1+prefix2+l2+".txt"
    newpath = r'./dictionary/'+filename
    if (os.path.exists(newpath) and filename_hash_dict[filename] == hashlib.md5(open(newpath,'rb').read()).hexdigest()):
        return None
    file = open("./dictionary/"+filename, "w")
    file_names.append(filename)
    print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Creating dictionary {filename}")
    for l3 in all_letters:
        for l4 in all_letters:
            for l5 in all_letters:
                file.write(l1+l2+l3+l4+l5+"\n")
    file.close()
    print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Saved dictionary {filename}")
    return None


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
    dictionary_path = r'./dictionary' 
    if not os.path.exists(dictionary_path):
        os.makedirs(dictionary_path)
    l1l2list = []
    for letter1 in all_letters:
        for letter2 in all_letters:
            l1l2list.append([letter1, letter2])
    with Pool(52) as p:
        p.map(create_dictionary, l1l2list)

def process_hash(sock, client, request_id, hash_string):
    try:
        conn = client[1]
        result = "Not found"
        while len(files_processing[request_id]):
            start = timeit.default_timer()
            file_to_process = files_processing[request_id].pop(0)
            conn.send(hash_string.encode())
            response = conn.recv(MSG_LENGTH).decode()
            print(f"Response String: {response}")

            conn.send(file_to_process.encode())
            response = conn.recv(MSG_LENGTH).decode()
            print(f"Response File name : {response}")

            filename= "./dictionary/"+file_to_process
            file = open(filename, "rb")
            data = file.read()
            if(len(data) != 843648):
                print(len(data))
            file.close()
            conn.send(data)
            conn.send("$$$".encode())
            response = conn.recv(MSG_LENGTH).decode()
            print(f"Response File data : {response}")
            response = conn.recv(MSG_LENGTH).decode()
            print(f"Final Response : {response}")
            stop = timeit.default_timer()
            if(request_id not in stats_request_id):
                stats_request_id[request_id] = [stop - start]
            else:
                stats_request_id[request_id].append(stop-start)
            if response == "Password not found":
                sock.send({
                    "success": 0,
                    "file": file_to_process
                })
                continue
            else:
                # todo: terminate all threads, find a better way
                for i in range(len(files_processing[request_id])):
                    files_processing[request_id].pop(0)
                if client in clients_in_use:
                    clients_in_use.remove(client)
                print(f"Returning Final Response : {response}")
                sock.send({
                    "success": 1,
                    "password": response
                })
                result = response
                return response
                break
        if client in clients_in_use:
            clients_in_use.remove(client)
        print("Returning: "+result)
        return result
    except (socket.error, socket.gaierror, socket.herror) as error:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Socket Error: {error}")
        if client in clients_in_use:
            clients_in_use.remove(client)
        if client in connections:
            connections.remove(client)
        conn.close()
    except (ConnectionError, ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError) as error:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Connection Error : {error}")
        if client in clients_in_use:
            clients_in_use.remove(client)
        if client in connections:
            connections.remove(client)
        conn.close()
    except Exception as error:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Other Error : {error}")
        if client in clients_in_use:
            clients_in_use.remove(client)
        if client in connections:
            connections.remove(client)
        conn.close()
    except (KeyboardInterrupt, InterruptedError) as error:
        print(f"Interrupt Error : {error}")
        if client in clients_in_use:
            clients_in_use.remove(client)
        if client in connections:
            connections.remove(client)
        conn.close()
    finally:
        print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Server has a total of {threading.active_count() - 2} active connection(s) "
              f"with the client(s).\n")
        if client in clients_in_use:
            clients_in_use.remove(client)


    # if(len(file_combinations) == 0):
    #     break
    # file_to_process = file_combinations.pop(0)
    # conn = connections.pop(0)

def add_client(sock, request_id, required_clients, hash_string):
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
        thread = ThreadReturn(target=process_hash, args=(sock, conn, request_id, hash_string))
        request_threads.append(thread)
        thread.start()

    threads_request_id[request_id].extend(request_threads)

    return {
        "requestId": request_id
    }
    
def decrypt_md5(sock, hash_string, required_clients):
    global request_id_counter
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

    
    file_combinations = []
    letter_combinations = ["small_"+name for name in small_letters]
    letter_combinations.extend(["capital_"+name for name in capital_letters])
    for file_letter1 in letter_combinations:
        for file_letter2 in letter_combinations:
            file_combinations.append(file_letter1+file_letter2+'.txt')

    request_id = request_id_counter
    files_processing[request_id] = file_combinations
    request_id_counter = request_id_counter + 1
    request_threads = []

    for conn in selected_clients:
        print("Starting a new thread")
        thread = ThreadReturn(target=process_hash, args=(sock, conn, request_id, hash_string))
        request_threads.append(thread)
        thread.start()
    threads_request_id[request_id] = request_threads

    return {
        "requestId": request_id
    }

def send_password_response(sock, request_id):
    results = []
    for request_thread in threads_request_id[request_id]:
        results.append(request_thread.join())

    for result in results:
        if result != "Not found":
            return {
                "password": result
            }
        else:
            return {
                "err": "Password not found."
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

def start_webserver_node(server_port):
    addr = ('', server_port)
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(addr)
        server.listen(10)

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

def calculate_statistics(request_id, password):
    total_time = 0
    for ptime in stats_request_id[request_id]:
        total_time = total_time + ptime
    total_hashes_processed =  (len(stats_request_id[request_id]) - 1) * 140608
    l1 = password[0]
    l2 = password[1]

    if 'A' <= l1 <= 'Z':
        prefix1 = "capital_"
    else:
        prefix1 = "small_"
    if 'A' <= l2 <= 'Z':
        prefix2 = "capital_"
    else:
        prefix2 = "small_"
    file_name_with_password = prefix1+l1+prefix2+l2+'.txt'

    with open("./dictionary/"+file_name_with_password, "r") as file:
        for line in file:
            total_hashes_processed = total_hashes_processed + 1
            if line.strip().encode() == password:
                break
    return {
        "totalTime": total_time,
        "numberOfFiles": len(stats_request_id[request_id]),
        "totalHashes": total_hashes_processed
    }

def start_server_node_thread(server_port):
    thread = threading.Thread(target=start_server_node, args=(server_port, ))
    thread.start()

if __name__ == "__main__":
    create_dictionaries()
    start_server_node_thread(5002)
    time.sleep(5)
    decrypt_md5("b1a1bca13bc04f19384049a0093413b0")
