import socket
import threading
import time 
import json
import random


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(("localhost", 1864))
sock.listen(1)
print "Server Started"

users = {}

users["user1"] = {
    "last-login": time.ctime(),
    "pub-key": "ssh-rsa +V3nkTWbFg66vQs1+St/+ZMlKszLzLFiV+28lV4DEDorDKfi9us5a3tc03FInmbA7eCHgL6I5DOdhp0cgKN0/+dtzshnfAb1hQEKkHep8GszARQTAh1go0cln user1@desktop",
    "password": "12345"
}

users["user2"] = {
    "last-login": time.ctime(time.time() - 10000),
    "pub-key": None,
    "password": "LOL.passwd"
}


def get_user(uname):
    global users
    if uname in users.keys():
        return users[uname]
    else:
        return None

def send_resp(client, resp):
    user_str = json.dumps(resp)
    client.send(user_str)


def callback(client, addr):
    global users
    while True:
        msg = client.recv(1024)
        if msg != "":
            print "Message:{message}, from {port}".format(message=msg, port=addr[1])


            # API Protocol Begin

            # Request
            # {
            #     "type": "get-user",
            #     "username": "test"
            # }

            # Response
            # {
            #     "type": "get-user",
            #     "uid": random.randint(0, 100),
            #     "user": { ... },
            #     "status-code": 123678
            # }
            try:
                msg_dict = json.loads(msg)
            except Exception as e:
                print "Serialization Error", e
                continue

            if not msg_dict.has_key("type"):
                continue
            
            # Get user Handler
            if msg_dict["type"] == "get-user":
                resp = {
                    "type": "get-user",
                    "uid": random.randint(0, 100),
                    "status-code": 0
                }

                if not msg_dict.has_key("username"):
                    resp["status-code"] = 502

                
                user = get_user(
                    msg_dict["username"])
                if user is None:
                    print "User not found,",  msg_dict["username"]
                    resp["status-code"] = 404
                
                resp["user"] = user
                send_resp(client, resp)

while True:
    conn, client_addr = sock.accept()
    x = threading.Thread(target=callback, args=(conn, client_addr,))
    x.setDaemon(True)
    x.start()

    # x.join()
    print "Accepted Connection From:", client_addr
