## in file /app/private/mail_queue.py
import datetime
import time
def sshShell(endpoint, username, credential, cmd):
    import paramiko
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    k = ""
    try:
        ssh_client.connect(endpoint, username=username, password=credential,
                       key_filename="C:\\Users\\karthik\\OneDrive\\OneDrive - Spin Games LLC\\.ssh\\id_rsa")
        stdin, stdout, stderr = ssh_client.exec_command(cmd)
        k = stdout.readlines()
        print("ssh key fetched")
    except TimeoutError:
        print("ssh key failed - TimeoutError")
        k = "TimeoutError"
    except ValueError:
        print("ssh key failed - ValueError")
        k = "ValueError"
    finally:
        ssh_client.close()
    return k


def authSsFetch():
    for row in db(db.db_serverCmdExec.xecuted == 0).select():
        ip_add = row.ip_address
        print(ip_add)
        username = row.username
        print(username)
        cmd = row.cmd
        print(cmd)
        k = sshShell(ip_add, username, "", cmd)
        row.update_record(xecuted=1, stdout_=k, modified_on=datetime.datetime.now(), modified_by=2)
        db.commit()

while True:
    authSsFetch()
    time.sleep(3)

# python ..\..\.\web2py.py -S welcome -M -R applications/welcome/private/serverConMan.py