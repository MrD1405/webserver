import socket

class WrongHTTPFormat(Exception):
    pass
def parse_http_headers(structure):
    try:
        http_request=structure.split("\r\n")
        start_line = http_request[0].split(' ')
        http_method = start_line[0]
        request_target=start_line[1]
        headers={}
        for entry in http_request[1:]:
            header_key , header_value = entry.split(':',1)
            header_key=header_key.lower()
            header_value=header_value.strip()
            headers[header_key]=header_value
        return http_method , request_target , headers
    except Exception as e:
        raise WrongHTTPFormat

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.bind(('127.0.0.1',8199))
server.listen(1)
print("server is listening")
while True:
    try:
        client_connection , client_address = server.accept()
        request_stream =b""
        while b"\r\n\r\n" not in request_stream:
            print("loop through first")
            chunk = client_connection.recv(1024)
            if not chunk :
                break
            request_stream+=chunk
        http_structure , _ , body = request_stream.partition(b'\r\n\r\n')
        http_method , request_target , headers = parse_http_headers(http_structure.decode("utf-8"))
        expected_length = int(headers.get('content-length',0))
        while expected_length > 0 :
            print("loop thru second")
            chunk = client_connection.recv(1024)
            print(chunk)
            if not chunk:
                break
            body+=request_stream
            expected_length=expected_length-len(chunk)
            print(f"expec len {expected_length}")
        print("its here")
        http_response=b"""\
    HTTP/1.1 200 OK

    Hello World
    """
        client_connection.sendall(http_response)
        client_connection.close()
    except Exception as e:
        print(f"Bad Request : {e}")
