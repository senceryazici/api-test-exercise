import socket 
import sys
import time
import json, yaml

status_code = {
    0: "OK",
    404: "User Not Found",
    502: "Bad Request" 
}

class TestAPI():
    def __init__(self):
        pass
    
    def initialize(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("localhost", 1864))

    def get_user(self, uname):
        req = {
            "type":"get-user",
            "username": uname
        }

        req_json = json.dumps(req)
        self.sock.send(req_json)
        return self.spin()

    def spin(self):
        while True:
            resp = self.sock.recv(2048)
            if resp == "":
                continue

            try: 
                resp_dict = yaml.safe_load(resp.decode())
            except Exception as e:
                print "Deserialization Error", e 
                continue
            code = resp_dict["status-code"]

            if code != 0: 
                msg =  "Status Code:{}, Description:{}".format(code, status_code[code])
                # raise Exception(msg)
                
            return resp_dict["user"], code == 0


