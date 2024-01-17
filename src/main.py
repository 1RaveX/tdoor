from optparse import OptionParser

from server import generate_server


def generateExe():
    print("Generando el Exe")

# pasar comandos para iniciar esto desde la command line
def main():
    parser = OptionParser()
    parser.add_option('-s','--server-ip',dest='ipserver',help='Ip del servidor')
    parser.add_option('-p','--port',dest='portserver',help="Puerto del servidor")
    parser.add_option('-c','--client-ip',dest='ipclient',help='Ip del Cliente',default=None)
    parser.add_option('-pc','--port-c',dest='portclient',help='Puerto del cliente',default=None)
    (options, args) = parser.parse_args()

    if options.ipserver is None or options.portserver is None:
        parser.error("Los campos ipserver y portserver son obligatorios. Utiliza -h para obtener ayuda.")

    if options.ipclient is not None and options.portclient is not None:
        print("Quieres generar el .exe para el cliente?")
        input("Presiona yes/no para generar el archivo .exe")
        generateExe()   
    else:
        print("Deseas ejecutar el servidor?")
        input("Presiona yes/no para ejecutar el servidor")
        generate_server(options.ipserver,options.portserver)

if __name__ == '__main__':
    main()