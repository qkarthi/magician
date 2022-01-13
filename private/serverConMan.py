## in file /app/private/mail_queue.py
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
    for row in db(db.db_serverDet.ssh_fetch == 1).select():
        ip_add = row.pub_ipv4
        username = row.username
        k = 'cat /home/ubuntu/.ssh/authorized_keys'
        k = sshShell(ip_add, username, "", k)
        print(k)
        print(type(k))
        row.update_record(ssh_fetch = 0)
        db.commit()
        db.db_serverSshData.insert(created_by = 2, server_named=row.name, instance_id=row.instance_id, username=row.username, auth_keys=k )
        db.commit()

while True:
    authSsFetch()
    time.sleep(3)

# python3 .\web2py.py -S welcome -M -R applications/welcome/private/serverConMan.py