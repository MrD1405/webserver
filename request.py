from dataclasses import dataclass , field
from typing import Dict

@dataclass
class HTTPRequest:
    method : str
    path : str
    version : str = "HTTP/1.1"
    headers : Dict[str,str] = field(default_factory=dict)
    body : bytes = b""
    def perform_action(self):
        if self.method == "GET" and self.path == "/user":
            body={"user":"Dushyant"}
            headers={"Content-Length": str(len(body))}
            return 200 , headers , str(body).encode("utf-8") 
        else:
            body={"I dont know what you are searching for"}
            headers={"Content-Length": str(len(body))}
            return 200 , headers , str(body).encode("utf-8")
            