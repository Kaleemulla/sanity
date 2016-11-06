import socket
import paramiko

def ssh_collect(server, user, port, timeout, command):
        if (user == "em7admin"):
                passwd = "em7admin"
        else:
                passwd = "ast4roslab"
        try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(server, username=user, password=passwd, port=int(port), timeout=timeout)
                stdin, stdout, stderr = ssh.exec_command(command)
                return (stdin.readlines, stdout.readlines(), stderr.readlines(), ssh)
        except paramiko.AuthenticationException, e:
                return ("", "Error1", "Default Password Not Working", ssh)
        except socket.error, e:
                return ("", "Error2", "Server Not Found", ssh)

