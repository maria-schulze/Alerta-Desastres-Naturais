import socket
import threading

clientes = {}
desastres = {
    "1": "⚠️  Terremoto detectado! Afaste-se de janelas e abrigo-se.",
    "2": "🔥  Incêndio! Evacue pela saída mais próxima.",
    "3": "🌊  Inundação! Vá para áreas altas imediatamente.",
    "4": "🏔️  Risco de deslizamento! Saia da área e procure abrigo seguro.",
    "5": "🌩️  Tempestade severa! Fique dentro de casa, longe de janelas."
    }

def broadcast(msg, origem=None):
    for sock in list(clientes):
        if sock != origem:
            try:
                sock.send(msg.encode())
            except:
                sock.close()
                clientes.pop(sock, None)

def handle_cliente(sock, addr):
    ip = addr[0]
    clientes[sock] = ip
    print(f"{ip} conectado.")
    broadcast(f"{ip} entrou no chat.", sock)

    menu = "\nEscolha o número do desastre:\n" + "\n".join(f"{k} - {v}" for k, v in desastres.items()) + "\n"

    sock.send(menu.encode())

    try:
        while True:
            msg = sock.recv(1024).decode().strip()
            if not msg or msg.lower() == 'exit' or msg == 'exit':
                break
            if msg in desastres:
                alerta = desastres[msg]
                print(f"{ip} relatou: {alerta}")
                broadcast(f"{ip} relatou: {alerta}")
            else:
                broadcast(f"{ip}: {msg}", sock)
    except:
        pass
    finally:
        print(f"{ip} saiu.")
        broadcast(f"{ip} saiu.", sock)
        sock.close()
        clientes.pop(sock, None)

def servidor():
    while True:
        msg = input("[Servidor] Mensagem ('exit' p/ sair): ")
        if msg.lower() == 'exit':
            broadcast("Servidor encerrando. Siga as instruções.")
            for c in list(clientes): c.close()
            break
        broadcast(f"Servidor: {msg}")

def start_server():
    s = socket.socket()
    s.bind(('10.1.25.63', 8080))
    s.listen()
    print("🛑 SERVIDOR INICIADO 🛑")

    threading.Thread(target=servidor, daemon=True).start()

    try:
        while True:
            c, addr = s.accept()
            threading.Thread(target=handle_cliente, args=(c, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("Encerrando servidor.")
    finally:
        s.close()

if __name__ == "__main__":
    start_server()
