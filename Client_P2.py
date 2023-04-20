import socket

server_address = "localhost"  # dirección IP o nombre de dominio del servidor
server_port = 12345  # puerto del servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: #Creamos el socket
    sock.connect((server_address, server_port)) #Establece una conexión con el servidor
    filename = input("Ingrese el nombre del archivo: ")  # nombre del archivo de audio que se quiere enviar
    """Abre el archivo de audio especificado por filename en modo de lectura binaria ("rb") lee todo su contenido en
        una variable llamada data, y luego envía todo el contenido del archivo al servidorutilizando el método sendall()."""
    with open(filename, "rb") as f:
        data = f.read()
        sock.sendall(data)
    print("Archivo de audio enviado con éxito.")
