
import socket
from  threading import Thread

SERVER = None
PORT = None
IP_ADDRESS = None

CLIENTS = {}

playerNames=[]



def acceptConnections():
    global CLIENTS
    global SERVER

    while True:
        player_socket, addr = SERVER.accept()
        player_name = player_socket.recv(1024).decode().strip()
        if len(CLIENTS.keys()) == 0:
            CLIENTS[player_name] = {'player_type': 'player1'}
        else:
            CLIENTS[player_name] = {'player_type': 'player2'}

        CLIENTS[player_name]['player_socket'] = player_socket
        CLIENTS[player_name]['address'] = addr
        CLIENTS[player_name]['player_name'] = player_name
        CLIENTS[player_name]['turn'] = False

        print(f'Connection Established with {player_name}: {addr}')

        thread1 = Thread(target=handleclient, args=(player_socket, player_name))
        thread1.start()

def handleclient(player_socket, player_name):
    global CLIENTS
    global playerNames
    player_type = CLIENTS[player_name][player_type]

    if player_type == 'player1':
        CLIENTS[player_name]['turn'] = True
        player_socket.send(str({'player_type' : CLIENTS[player_name]["player_type"] , 'turn': CLIENTS[player_name]['turn'], 'player_name' : player_name }).encode())

    else:
        CLIENTS[player_name]['turn'] = False
        player_socket.send(str({'player_type' : CLIENTS[player_name]["player_type"] , 'turn': CLIENTS[player_name]['turn'], 'player_name' : player_name }).encode())
    
    playerNames.append({"name": player_name, "type": CLIENTS[player_name]["player_type"]})
    
    if(len(playerNames) > 0 and len(playerNames) <= 2):
        for cName in CLIENTS:
            cSocket = CLIENTS[cName]["player_socket"]
            cSocket.send(str({"player_names" : playerNames}).encode())

    while True:
        try:
            message =  player_socket.recv(1024)
            if message:
                for i in CLIENTS:
                    p1 = CLIENTS[i]['player_socket']
                    p1.send(message)
                    
        except:
            pass



def setup():
    print("\n")
    print("\t\t\t\t\t\t*** LUDO LADDER ***")


    global SERVER
    global PORT
    global IP_ADDRESS

    IP_ADDRESS = '127.0.0.1'
    PORT = 5000
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))

    SERVER.listen(10)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...")
    print("\n")

    acceptConnections()


setup()
