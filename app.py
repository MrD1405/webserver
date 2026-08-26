import socket
import os
import time
from concurrent.futures import ThreadPoolExecutor
from response import HTTPResponse
from request import HTTPRequest

class WrongHTTPFormat(Exception):
    pass
class HTTPServer:
    def __init__(self, host:str = "127.0.0.1" , port:int="8199" ,max_workers:int = 10 ):
        self.host=host
        self.port=port
        self.count=0
        self.executor= ThreadPoolExecutor(max_workers=max_workers)
    def parse_http_headers(self,structure):
        try:
            http_structure=structure.decode("utf-8")
            http_request=http_structure.split("\r\n")
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
    def handle_client_connection(self, client_connection , client_address):
        try:
            client_connection.settimeout(5.0)
            request_stream =b""
            #accept until the headers are not complete
            while b"\r\n\r\n" not in request_stream:
                chunk = client_connection.recv(1024)
                if not chunk :
                    break
                request_stream+=chunk
            http_structure , _ , body = request_stream.partition(b'\r\n\r\n')
            http_method , request_target , headers = self.parse_http_headers(http_structure)
            request = HTTPRequest(method=http_method , path=request_target , headers=headers)
            #based on content length , listen and append to the body
            expected_length = int(headers.get('content-length',0))
            while expected_length > 0 :
                chunk = client_connection.recv(1024)
                if not chunk:
                    break
                body+=chunk
                expected_length=expected_length-len(chunk)
            request.body=body
            status_code , headers , body = request.perform_action()
            response=HTTPResponse(status_code=status_code,headers=headers,body=body)
            http_response=response.construct_response()
            self.count+=1
            print(f"you are getting this one from thread {self.count}")
            time.sleep(3)
            #send reply and close all connections 
            client_connection.sendall(http_response)
            client_connection.close()
        except Exception as e:
            print(f"Bad Request : {e!s}")
        
    def start_server(self):
        #continuously listen to tcp connection on a specific port
        server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        server.bind(('127.0.0.1',8199))
        server.listen(256)
        print("server is listening")
        while True:
            try:
                client_connection , client_address = server.accept()
                self.executor.submit(self.handle_client_connection,client_connection , client_address)
            except Exception as e:
                print(f"Error while processing request {e!s}")
                
if __name__ == "__main__":
    server = HTTPServer()
    server.start_server()
    
                