import socket
import threading

def receber_mensagens(sock):
    while True:
        try:
            msg = sock.recv(1024).decode('utf-8')
            if not msg:
                break
            print(msg)
        except:
            break

def enviar_mensagens(sock):
    while True:
        try:
            msg = input()
            sock.send(msg.encode('utf-8'))
            if msg.lower() == 'exit':
                break
        except:
            break
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('10.1.25.63', 8080))

    receber_thread = threading.Thread(target=receber_mensagens, args=(client_socket,))
    enviar_thread = threading.Thread(target=enviar_mensagens, args=(client_socket,))

    receber_thread.start()
    enviar_thread.start()

    receber_thread.join()
    enviar_thread.join()

    client_socket.close()
    print("Você saiu do chat.")

if __name__ == "__main__":
    start_client()
