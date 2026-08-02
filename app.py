import socket
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.bind(('127.0.0.1',8199))
server.listen(1)
print("server is listening")
while True:
    client_connection , client_address = server.accept()
    request_data = client_connection.recv(1024)    
    print(request_data.decode('utf-8'))
    http_response=b"""\
HTTP/1.1 200 OK

Hello World
"""
    client_connection.sendall(http_response)
    client_connection.close()

