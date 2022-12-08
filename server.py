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

filename_hash_dict = {'small_a.txt': '8b6670b4e685ac42f4a42e6f4620f194', 'small_b.txt': '3da8214e632c76ababb2f3b3cf7b6c0a', 'small_c.txt': 'c476bbffd8933af9179d52b9eeb7b84b', 'small_d.txt': '55dd0d4d51d4f73cd4f4440606ba1a67', 'small_e.txt': 'b368d28eb5e14c9df56b3fd7f6da9a9b', 'small_f.txt': 'c2c08a1874beed7f7e53478765e7c0d8', 'small_g.txt': '68795ad898fa887d5acba86a2c2d44b2', 'small_h.txt': 'edf59c8ed0b103916d39ba3b695b505e', 'small_i.txt': '37b641eac0ca579b9dda34b87827627a', 'small_j.txt': '2ff59494ad0c1e141049f058563b06b5', 'small_k.txt': '82caa3421043750d0d9926d56d786ab5', 'small_l.txt': 'c9d5fa14076a78156849cf6cff1ba80b', 'small_m.txt': 'b39a8b43d784fe7ac272e2545c8981a7', 'small_n.txt': 'd1a3fbd26f20479a69bf04180c608317', 'small_o.txt': 'd5cc4eb4f1dd2acf615ce2cdff40fdea', 'small_p.txt': 'c1001fc6c472c6c94fc8623effd8f829', 'small_q.txt': 'a1eceeb6a0f2941a3e9ca6efb4bffe23', 'small_r.txt': '4e4f7e012dd9f718d5b024ffc532e1e9', 'small_s.txt': '9abfab217d508ed00500254dbbb0ef46', 'small_t.txt': '52388f2f2bfa58899017713399bcfb75', 'small_u.txt': '880ba0410ff1f35061081a760051dfdb', 'small_v.txt': 'cacb7c4e6302743440f98a630b0bb750', 'small_w.txt': '491597331daa737f88dd3e001332a9ad', 'small_x.txt': '81cd3f2d225badf2279e5da8acb03ea9', 'small_y.txt': 'd58c08a5401e3f277a99e4652468480d', 'small_z.txt': 'dd1fbfe282afd1198aa7fe420f408736', 'capital_A.txt': 'a32a656790c98caba9abc5e5b57ea2c6', 'capital_B.txt': '65d71a9c5dd1b0faabb5ac919a98fae7', 'capital_C.txt': '347216d1708219fc7ec359e368760706', 'capital_D.txt': '3ad72a248cdf6d21f793d139f65c49b5', 'capital_E.txt': '41039429bc2570c180a372915fde94d2', 'capital_F.txt': '321c836a13b75421a892b9c029199fa3', 'capital_G.txt': 'f91e318038dc6509e4b7417147c65aac', 'capital_H.txt': '075ed126bab0730e622278c28c91e088', 'capital_I.txt': '4382d5fd50c66265c295aa706a68fcc3', 'capital_J.txt': '454f0c3b6e217c365372c84d0a608eb0', 'capital_K.txt': 'cf9fc93f5672138ca563f91867e759f4', 'capital_L.txt': 'b04d79463d2a2a802494cbaf68c3c6c9', 'capital_M.txt': 'ede9e2ecc17b753c85f58ecbba25977b', 'capital_N.txt': '7eb96be1406d1fb84fb9b6746fbb5352', 'capital_O.txt': '68e73d9ce206bc3d62e9993ef04bc3fd', 'capital_P.txt': '3fe3b4bdf5393035ed22029a2c318bea', 'capital_Q.txt': '26009bde5bf4651a5784e2ac2255c63d', 'capital_R.txt': '778ee57411f17b39c19a7df77b9272df', 'capital_S.txt': 'f97aad33df795f6626660c99867f3a90', 'capital_T.txt': '5875fc701ca9b0603ca8d5ae5716084b', 'capital_U.txt': 'e94c862d95597f3add51eb5f37670291', 'capital_V.txt': '1532a75445c70bc3efe0b6142d2887b9', 'capital_W.txt': 'ec1dc37232702ab7f655d428dc6b7632', 'capital_X.txt': 'a7fa370a9fec30e803e41914961ecce5', 'capital_Y.txt': '88ad78b99517ebb1b29d329b69b1026c', 'capital_Z.txt': 'edb2d0e61c7dfd41910d6321fb289dd2'}

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

# def create_dictionary(l1l2):
#     l1, l2 = l1l2
#     if 'A' <= l1 <= 'Z':
#         prefix1 = "capital_"
#     else:
#         prefix1 = "small_"
        
#     if 'A' <= l2 <= 'Z':
#         prefix2 = "capital_"
#     else:
#         prefix2 = "small_"

#     filename = prefix1+l1+prefix2+l2+".txt"
#     newpath = r'./dictionary/'+filename
#     if (os.path.exists(newpath) and filename_hash_dict[filename] == hashlib.md5(open(newpath,'rb').read()).hexdigest()):
#         return None
#     file = open("./dictionary/"+filename, "w")
#     file_names.append(filename)
#     print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Creating dictionary {filename}")
#     for l3 in all_letters:
#         for l4 in all_letters:
#             for l5 in all_letters:
#                 file.write(l1+l2+l3+l4+l5+"\n")
#     file.close()
#     print(f"[Time:{dt.datetime.now().strftime('%H:%M:%S')}] Saved dictionary {filename}")
#     return None

def create_dictionary(l1):
    if 'A' <= l1 <= 'Z':
        prefix = "capital_"
    else:
        prefix = "small_"
    filename = prefix+l1+".txt"
    newpath = r'./dictionary/'+filename
    if (os.path.exists(newpath) and filename_hash_dict[filename] == hashlib.md5(open(newpath,'rb').read()).hexdigest()):
        return None
    file = open("./dictionary/"+filename, "w")
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
    # l1l2list = []
    # for letter1 in all_letters:
    #     for letter2 in all_letters:
    #         l1l2list.append([letter1, letter2])
    with Pool(52) as p:
        p.map(create_dictionary, all_letters)

def process_hash(sock, client, request_id, hash_string):
    try:
        conn = client[1]
        result = "Not found"
        while len(files_processing[request_id]):
            start = timeit.default_timer()
            file_to_process = files_processing[request_id].pop(0)
            print(hash_string.encode())
            conn.send(hash_string.encode())
            response = conn.recv(MSG_LENGTH).decode()
            print(f"Response String: {response}")

            conn.send(file_to_process.encode())
            print(file_to_process.encode())
            response = conn.recv(MSG_LENGTH).decode()
            print(f"Response File name : {response}")

            filename= "./dictionary/"+file_to_process
            file = open(filename, "rb")
            data = file.read()
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

    
    # file_combinations = []
    # letter_combinations = ["small_"+name for name in small_letters]
    # letter_combinations.extend(["capital_"+name for name in capital_letters])
    # for file_letter1 in letter_combinations:
    #     for file_letter2 in letter_combinations:
    #         file_combinations.append(file_letter1+file_letter2+'.txt')
    file_combinations = ["small_"+name+".txt" for name in small_letters]
    file_combinations.extend(["capital_"+name+".txt" for name in capital_letters])

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
            foundClient = None
            for client in connections:
                if client[0][0] == addr[0]:
                    foundClient = client
            if(foundClient != None):
                connections.remove(client)
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
    total_hashes_processed =  (len(stats_request_id[request_id]) - 1) * 7311616
    l1 = password[0]

    if 'A' <= l1 <= 'Z':
        prefix = "capital_"
    else:
        prefix = "small_"

    file_name_with_password = prefix+l1+'.txt'

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
