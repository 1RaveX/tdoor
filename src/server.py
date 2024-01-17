import socket
import threading

from config import SIZE_RECV


def generate_server(ip_temp, port):
    address = (ip_temp,port)

    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind(address)
    sock.listen(1)

    print(f"[+] Escuchando en el puerto {port}")

    while True:
        conn, addr = sock.accept()
        thread = threading.Thread(target=threading_client,name=str(addr), args=(conn,addr))
        thread.start()
        print(f"Conexiones: {threading.activeCount() - 1}")

        # buscar un metodo para salir y cerrar el servidor

    sock.close()


def threading_client(conn,addr):
    print(f"\nNueva Conexion: {addr}")
    conected = True

    while conected:
        try:
            message_client = conn.recv(SIZE_RECV)
            if len(str(message_client.decode())):
                print("\nMensaje: " + message_client.decode("utf-8" + "\n"))
            
            command = input("\n" + str(addr) + ":") 
            

            if command == "exit":
                message_server = command.encode()
                conn.send(message_server)
                conected = False

            elif command.split(" ")[0] == "download":
                '''
                    Este comando abre un txt y descarga el contenido de ese archivo
                '''            
                file_name = str(command).split(" ")[1:]
                listToStr = ' '.join([str(elem) for elem in file_name])
                conn.send(command.encode())

                with open(listToStr, 'w') as f:
                    f.close()
                with open(listToStr, "r+") as f:
                    while len(str(message_client.decode())) != 0:
                        read_data = conn.recv(1024).decode()
                        #print(read_data)
                        f.write(read_data)
                        f.read()
                    

            elif command == "ls":
                message_server = command.encode()
                conn.send(message_server)
                
            elif command == "sysinfo":
                message_server = command.encode()
                conn.send(message_server)

            elif command.split(" ")[0] == "cd":
                message_server = command.encode()
                conn.send(message_server)

            else:
                print("Comando desconocido")
                conn.send("-".encode())
        except Exception:
            break
