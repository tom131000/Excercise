#!/usr/bin/python3
import sys
import threading
import socket


def server_loop(local_host, local_port, remote_host, remote_port,
                receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except:
        print("[!!] Failed to listen on %s:%d" % (local_host,local_port))
        print("[!!] Check for other listening sockets or correct permissongs.")
        sys.exit(0)

    print("[*] Listening on %s:%d " % (local_host, local_port))


    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # 打印出本地连接信息
        print ("【==》】 Received incoming connection from %s:%d" %
               (addr[0],addr[1]))

        # 开启一个线程与远程主机通信
        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket,
                                                                    remote_host
                                                                    ,remote_port
                                                                    ,receive_first))

        proxy_thread.start()


def proxy_handler(client_socket, remote_host, remote_port, receive_first):

    # 连接到远程主机
    remote_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    remote_socket.connect((remote_host,remote_port))

    # 如果要从远程主机接收数据
    if receive_first:

        remote_buffer = receive_from(remote_socket)
        hexdumo(remote_buffer)

        # 发送给我们的响应处理
        remote_buffer = response_handler(remote_buffer)

        # 如果我们有数据传递给本地客户端，发送他
        if len(remote_buffer):
            print("[<==] Sending %d bytes to localhost." % len(remote_buffer))
            client_socket.send(remote_buffer)

    # 现在我们从本地循环读取数据，发送给远程主机和本地主机
    while True:

        # 从本地读取数据
        local_buffer = receive_from(client_socket)

        if len(local_buffer):
            print("[==>] Received %d bytes from localhost." % len(local_buffer))
            hexdump(local_buffer)

            # 发送给我们的本地请求
            local_buffer = request_handler(local_buffer)

            # 向远程主机发送数据
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote.")

        # 接收响应的数据
        remote_buffer = receive_from(remote_socket)

        if len(remote_buffer):

            print("[<==] Received %d bytes from remote." % len(remote_buffer))
            hexdump(remote_buffer)

            # send to our response handler
            remote_buffer = response_handler(remote_buffer)

            # send the response to the local socket
            client_socket.send(remote_buffer)

            print("[<==] Sent to localhost.")

        # if no more data on the either side, close the connections
        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections.")

            break


def main():

    # 没有华丽的命令行解析
    if len(sys.argv[1:]) != 5:
        print("Usage: ./pyProxy.py [localhost] [localport] [remotehost]"
              "[remoteport [receive_first]]")
        print("Example: ./pyProxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)


    # 设置本地监听参数
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    # 设置远程目标
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    # 告诉代理在发送给远程主机之前连接和接受数据
    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    # 现在设置好我们的监听socket
    server_loop(local_host,local_port,remote_host,remote_port,receive_first)

if __name__ == '__main__':
    main()
