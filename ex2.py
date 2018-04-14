import socket

target_host = "0.0.0.0"
target_port = 9999

clinent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clinent_socket.connect((target_host, target_port))

#clinent_socket.send(bytes("GET / HTTP/1.1\r\nHost: www.baidu.com\r\n\r\n", "utf-8"))
clinent_socket.send("ABCDEFi\r\n".encode("utf-8"))
msg = "123".encode('utf-8')

response = clinent_socket.recv(4096)

print (response + msg)
print("\n")
print("ininini")

clinent_socket.close()
