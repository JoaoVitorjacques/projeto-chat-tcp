# ---server.py ---
import socket
import threading


HOST = '127.0.0.1'  
PORT = 50001        

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            remove_client(client)

def remove_client(client_socket):
    if client_socket in clients:
        index = clients.index(client_socket)
        nickname = nicknames[index]
        
        clients.pop(index)
        nicknames.pop(index)
        
        client_socket.close()
        
        print(f"[STATUS] {nickname} desconectado.")
        broadcast(f"SYSTEM: {nickname} saiu do chat.".encode('utf-8'))

def handle_client(client_socket):
    try:
        nickname = client_socket.recv(1024).decode('utf-8')
        
        if nickname in nicknames:
            client_socket.send('ERR apelido_em_uso'.encode('utf-8'))
            client_socket.close()
            return
            
        nicknames.append(nickname)
        clients.append(client_socket)
        
        client_socket.send('New User. Você está conectado!'.encode('utf-8'))
        
        print(f"[STATUS] User {nickname} entrou.")
        broadcast(f"SYSTEM: {nickname} entrou no chat.".encode('utf-8'))
        
    except Exception as e:
        print(f"[ERRO] Erro ao registrar apelido: {e}")
        client_socket.close()
        return

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            
            if message == 'QUIT':
                break
            
            
            # 1. Comando WHO 
            if message.upper() == 'WHO':
                # Cria a lista de usuários e envia SÓ para quem pediu
                user_list = "Usuários conectados: " + ", ".join(nicknames)
                client_socket.send(f"SYSTEM: {user_list}".encode('utf-8'))
            
            # 2. Mensagem Direta (DM) [cite: 14]
            elif message.startswith('@'):
                try:
                    # Formato: @apelido sua mensagem
                    parts = message.split(' ', 1)
                    target_nickname = parts[0][1:] # Pega o nome sem o '@'
                    dm_content = parts[1]
                    
                    # Procura o apelido na lista
                    if target_nickname in nicknames:
                        target_index = nicknames.index(target_nickname)
                        target_socket = clients[target_index]
                        
                        # Envia a DM formatada [cite: 15]
                        formatted_dm = f"FROM {nickname} [dm]: {dm_content}"
                        target_socket.send(formatted_dm.encode('utf-8'))
                        
                        client_socket.send(f"SYSTEM: DM para {target_nickname} enviada.".encode('utf-8'))
                    else:
                        # Usuário não encontrado [cite: 23, 40]
                        client_socket.send(f"ERR user_not_found".encode('utf-8'))
                
                except IndexError:
                    client_socket.send("SYSTEM: Formato de DM inválido. Use: @apelido <mensagem>".encode('utf-8'))
            
            # 3. Mensagem Broadcast (padrão) [cite: 11]
            else:
                formatted_message = f"FROM {nickname} [all]: {message}"
                print(f"[CHAT] {formatted_message}")
                broadcast(formatted_message.encode('utf-8'))
            
        except:
            break
            
    remove_client(client_socket)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
    except OSError:
        print(f"[ERRO FATAL] A porta {PORT} já está em uso.")
        return
        
    server.listen()
    print(f"[STATUS] Servidor escutando em {HOST}:{PORT}...")

    while True:
        try:
            client_socket, address = server.accept()
            print(f"[CONEXÃO] Nova conexão de {str(address)}")
            
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()
            
        except KeyboardInterrupt:
            print("\n[STATUS] Desligando servidor...")
            server.close()
            break
        except Exception as e:
            print(f"[ERRO] Erro no servidor: {e}")
            break

if __name__ == "__main__":
    start_server()