import socket
import argparse
import hashlib
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("server_ip", help="Enter the IP address or the hostname of the server.", type=str)
    parser.add_argument("server_port", help="Enter the port number of the server to create a socket connection.",
                        type=int)
    args = parser.parse_args()
    server_ip = args.server_ip
    server_port = args.server_port

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(3600)
        client.connect((server_ip, server_port))
        print(f"Connected to the server {server_ip} on port {server_port}.\n")
        while True:
            string_to_decode = client.recv(1024).decode()
            print(f"String to decode : {string_to_decode}")
            client.sendall("String OK".encode())
            file_name = client.recv(1024).decode()
            print(f"File name : {file_name}")
            client.sendall("File name OK".encode())
            all_data = []
            
            if(string_to_decode.strip() == "" and len(string_to_decode.strip()) == 0):
                client.sendall("Password not found".encode())
                continue 
            with open("./client/"+file_name, "ab") as file:
                while True:
                    data = client.recv(1024)
                    if data.decode()[-1:-4:-1] == "$$$":
                        all_data.append(data.decode()[:-4].encode())
                        break
                    all_data.append(data)
                file.write(b"".join(all_data))
            file.close()
            client.sendall("File data OK".encode())
            password_found = False
            password = " "
            len_line = 0
            with open("./client/"+file_name, "r") as file:
                for line in file:
                    len_line = len_line + 1
                    if hashlib.md5(line.strip().encode()).hexdigest() == string_to_decode:
                        password_found = True
                        password = line.strip()
                        break
                file.close()
                os.remove("./client/"+file_name)
            if password_found:
                client.sendall(password.encode())
            else:
                client.sendall("Password not found".encode())
    except socket.timeout:
        print(f"Connection timed out!!")
        main()
    except (socket.error, socket.gaierror, socket.herror) as error:
        print(f"Socket Error : {error}")
        main()
    except (ConnectionError, ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError) as error:
        print(f"Connection Error : {error}")
    except Exception as error:
        print(f"Other Error : {error}")
    except (KeyboardInterrupt, InterruptedError) as error:
        print(f"Interrupt Error : {error}")

def create_client_folder():
    client_path = r'./client' 
    if not os.path.exists(client_path):
        os.makedirs(client_path)

if __name__ == "__main__":
    create_client_folder()
    main()
