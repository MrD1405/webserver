import socket

class WrongHTTPFormat(Exception):
    pass
def parse_request_stream(request_stream):
    try:
        http_request=request_stream.split("\r\n")
        start_line = http_request[0].split(' ')
        http_method = start_line[0]
        request_target=start_line[1]       
        print(request_target)
        print(http_method)
        print(http_request)
    except Exception as e:
        raise WrongHTTPFormat

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.bind(('127.0.0.1',8199))
server.listen(1)
print("server is listening")
while True:
    client_connection , client_address = server.accept()
    request_stream = client_connection.recv(1024) 
    request_data = parse_request_stream(request_stream.decode("utf-8"))   
    #print(request_data)  
    http_response=b"""\
HTTP/1.1 200 OK

Hello World
"""
    client_connection.sendall(http_response)
    client_connection.close()

