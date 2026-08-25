from dataclasses import dataclass , field
from typing import Dict

STATUS_REASONS = {
    200: "OK",
    400: "Bad Request",
    403: "Forbidden",
    404: "Not Found",
    500: "Internal Server Error",
}

@dataclass
class HTTPResponse:
    status_code: int = 200
    headers: Dict[str,str]=field(default_factory=dict)
    body : bytes =b""
    def construct_response(self):
        reason = STATUS_REASONS.get(self.status_code , "Unknown")
        status_line = f"HTTP/1.1 {self.status_code} {reason}"
        self.headers["Content-Length"]=str(len(self.body))
        headers_str = "".join(f"{k}: {v}\r\n" for k,v in self.headers.items())
        header_byte_format=f"{status_line}\r\n{headers_str}\r\n".encode('utf-8')
        return header_byte_format + self.body
    
        