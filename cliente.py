import socket
import sys

HOST = 'localhost'
PORT = 5555
ADDR = (HOST, PORT)

# Cria o socket do cliente
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta o socket do cliente ao socket do servidor
sock.connect(ADDR)

# Recebe a lista de itens do servidor
data = sock.recv(1024).decode()

# Loop principal do cliente
while True:
    # Recebe a ação desejada pelo cliente
    print('\nO que você deseja fazer?')
    print('LIST - Listar itens para votação')
    print('VOTE - Votar em um item')
    print('RANK - Exibir o ranking dos itens')
    print('QUIT - Sair do programa')
    acao = input('Digite a ação desejada: ').upper()

    # Envia a ação para o servidor
    sock.sendall(acao.encode())

    # Se o cliente desejar listar os itens, recebe a lista do servidor e imprime
    if acao == 'LIST':
        data = sock.recv(1024).decode()
        print(data)

    # Se o cliente desejar votar em um item, solicita o ID do item e envia ao servidor
    elif acao == 'VOTE':
        nome_item = input("Digite o nome do item que deseja votar: ")
        sock.sendall(nome_item.encode())
        print("Voto computado!")


    # Se o cliente desejar ver o ranking dos itens, recebe o ranking do servidor e imprime
    elif acao == 'RANK':
        data = sock.recv(1024).decode()
        print(data)

    # Se o cliente desejar sair, encerra o loop
    elif acao == 'QUIT':
        print("Encerrando conexão com o servidor...")
        break

    # Se a ação digitada for inválida, exibe mensagem de erro
    else:
        print("Ação inválida. Tente novamente.")

# Encerra o socket do cliente
sock.close()
