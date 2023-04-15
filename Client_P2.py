import socket

def send_audio_file(filename, server_address, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((server_address, server_port))
        with open(filename, "rb") as f:
            data = f.read()
            sock.sendall(data)
        print("Archivo de audio enviado con éxito.")

if __name__ == "__main__":
    filename = "audio.mp3" # nombre del archivo de audio que se quiere enviar
    server_address = "localhost" # dirección IP o nombre de dominio del servidor
    server_port = 12345 # puerto del servidor
    send_audio_file(filename, server_address, server_port)