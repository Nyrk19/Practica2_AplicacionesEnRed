import sys
import socket
import selectors
import types
import logging
sel = selectors.DefaultSelector()

def accept(sock_a, mask):
    sock_conn, addr = sock_a.accept()  # Should be ready
    print('aceptado', sock_conn, ' de', addr)
    sock_conn.setblocking(False)
    sel.register(sock_conn, selectors.EVENT_READ | selectors.EVENT_WRITE, read_write)

def read_write(sock_c, mask):
    if mask & selectors.EVENT_READ:
        data = sock_c.recv(1024)  # Should be ready
        if data:
            print('recibido', repr(data), 'a', sock_c)
            # Abrir archivo en modo append y escribir los datos recibidos
            with open("audio_received.mp3", "ab") as f:
                f.write(data)
        else:
            print('cerrando', sock_c)
            sel.unregister(sock_c)
            sock_c.close()
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