import socket

HOST = 'localhost'  # endereço IP do servidor (em branco)
PORT = 5555  # porta do servidor
ITEMS = ['One Piece', 'Naruto', 'Jujutsu Kaizen', 'Boku no Hero']  # lista de itens para votação
VOTES = [0] * len(ITEMS)  # lista de votos inicializada com zeros

# cria o socket do servidor
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# associa o socket com o endereço e porta do servidor
sock.bind((HOST, PORT))

# configura o socket para aguardar conexões
sock.listen()

print(f"Servidor aguardando conexões em {HOST}:{PORT}...")

# cria um dicionário para armazenar os votos de cada item
votos = {item: 0 for item in ITEMS}

# loop principal do servidor
while True:
    # aguarda uma conexão
    conn, addr = sock.accept()
    print(f"Conexão estabelecida com {addr}")

    # envia a lista de itens para o cliente
    conn.sendall(str(ITEMS).encode())

    # loop para receber a ação do cliente e processá-la
    while True:
        # recebe a ação do cliente
        data = conn.recv(1024).decode().strip()
        if not data:
            continue
        print(f"Ação recebida: {data}")

        # lista os itens disponíveis
        if data == "LIST":
            conn.sendall(str(ITEMS).encode())

        # vota em um item
        elif data == "VOTE":
            # recebe o ID do item
            item_nome = conn.recv(1024).decode().strip()
            print(f"Item selecionado: {item_nome}")
            # verifica se o nome do item é válido
            if item_nome not in ITEMS:
                conn.sendall("Erro: item inválido.".encode())
            else:
                # incrementa o voto correspondente ao item selecionado
                votos[item_nome] += 1
                conn.sendall("Voto computado!".encode())

        # mostra o ranking dos itens
        elif data == "RANK":
            # ordena os itens pelo número de votos em ordem decrescente
            ranking = sorted(votos.items(), key=lambda x: x[1], reverse=True)
            # envia o ranking para o cliente
            conn.sendall(str(ranking).encode())

        # encerra a conexão com o cliente
        elif data == "QUIT":
            print(f"Conexão encerrada com {addr}")
            conn.close()
            break

        # ação inválida
        else:
            conn.sendall("Erro: comando inválido.".encode())

    print(f"Cliente {addr[0]}:{addr[1]} desconectado.")
    conn.close()

# encerra o socket do servidor
sock.close()
