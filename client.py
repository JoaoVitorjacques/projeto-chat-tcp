# ---client.py ---
import socket
import threading
import sys

# Configurações do Cliente
HOST = '127.0.0.1'  # O IP do servidor
PORT = 50001        # A Porta do servidor

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            
            if not message or message == 'ERR apelido_em_uso':
                if message == 'ERR apelido_em_uso':
                    print("[ERRO] Este apelido já está em uso. Encerrando.")
                else:
                    print("[STATUS] Desconectado do servidor. Encerrando...")
                client_socket.close()
                sys.exit()
            
            print(f"\r{message}\n", end="")
            
        except Exception as e:
            client_socket.close()
            sys.exit()

def send_messages(client_socket):
    while True:
        try:
            message_to_send = input()
            
            if message_to_send.upper() == 'QUIT':
                client_socket.send('QUIT'.encode('utf-8'))
                client_socket.close()
                print("[STATUS] Você saiu do chat.")
                sys.exit()
                break
                
            client_socket.send(message_to_send.encode('utf-8'))
            
        except (EOFError, KeyboardInterrupt):
            client_socket.send('QUIT'.encode('utf-8'))
            client_socket.close()
            print("[STATUS] Desconectando...")
            sys.exit()
            break
        except Exception as e:
            client_socket.close()
            sys.exit()
            break

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
except ConnectionRefusedError:
    print("[ERRO] Não foi possível conectar ao servidor. Ele está online?")
    sys.exit()

nickname = input("Escolha seu apelido: ")
client.send(nickname.encode('utf-8'))

receive_thread = threading.Thread(target=receive_messages, args=(client,))
receive_thread.daemon = True
receive_thread.start()

send_messages(client)