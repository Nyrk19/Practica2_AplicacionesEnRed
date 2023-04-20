import socket
import selectors
import os

sel = selectors.DefaultSelector() #Creamos una instancia de DefaultSelector, que proporciona una interfaz para esperar eventos en sockets.
conn = {} #Diccionario vacío que se utiliza para almacenar la información de conexión de los sockets que se vayan conectando

def accept(sock_a, mask): #La función accept() se utiliza como un callback cuando el socket del servidor está listo para aceptar una nueva conexión.
    sock_conn, addr = sock_a.accept() #Aceptamos la conexion entrante, guardamos los datos del socket y la dirección
    print('aceptado', sock_conn, ' de', addr)
    sock_conn.setblocking(False) #Indicamos que sera un socket no bloqueante
    sel.register(sock_conn, selectors.EVENT_READ | selectors.EVENT_WRITE, read_write)
    conn[sock_conn] = os.path.join(os.getcwd(),f"audioRec_{addr[0]}_{addr[1]}.mp3") #Se guarda la información de conexión del socket en el diccionario conn


def read_write(sock_c, mask): #La función que se llama cada vez que se detecta un evento de lectura o escritura
    if mask & selectors.EVENT_READ:
        data = sock_c.recv(1024)
        if data:
            print('recibido', sock_c)
            # Abrir archivo en modo append y escribir los datos recibidos
            with open(conn[sock_c], "ab") as f:
                f.write(data)
        else:
            print('cerrando', sock_c)
            sel.unregister(sock_c)
            sock_c.close()
            del conn[sock_c]
    if mask & selectors.EVENT_WRITE:
       print ("")

with socket.socket() as sock_accept:
    sock_accept.bind(('localhost', 12345))
    sock_accept.listen(100)
    sock_accept.setblocking(False)
    sel.register(sock_accept, selectors.EVENT_READ, accept)
    while True:
        print("Esperando evento...")
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)
