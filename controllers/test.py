def index():
    session.x = 1
    rows = db().select(db.db_serverDet.ALL)
    return dict(rows=rows)

def resetValue():
    session.x = 1
    return ()


def fetchTime():
    import time
    s = time.time()
    local_time= time.ctime(s)
    #redirect(URL('welcome', 'server', 'listServer'))
    return (local_time)

def fetchValue():
    session.x = 1 + session.x
    return (session.x)


def sshCmd():
    import paramiko
    ssh_client = paramiko.SSHClient()
    cmd = request.vars.q
    print(cmd)
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect("54.163.48.245", username="ubuntu", password="",
                       key_filename="C:\\Users\\karthik\\OneDrive\\OneDrive - Spin Games LLC\\.ssh\\id_rsa")
    stdin, stdout, stderr = ssh_client.exec_command(cmd)

    ec = stdout.readlines()
    ssh_client.close()
    return ec




