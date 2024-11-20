# import socket

# class Network:
#     def __init__(self):
#         self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.server = "10.2.1.255"
#         self.port = 8080
#         self.addr = (self.server, self.port)
#         self.id = self.connect()
#         print(self.id)

#     def connect(self):
#         try:
#             self.client.connect(self.addr)
#             return self.client.recv(2048).decode()
#         except:
#             pass

#     def send(self, data):

# n = Network()

