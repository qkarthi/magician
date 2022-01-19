def index():
    session.x = 1
    rows = db().select(db.db_serverDet.ALL)
    return dict(rows=rows)

# sed '/ karthikeyan.p@spingames.net/d'
# ("echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDNllUA9r0dMwAj75+I+/Lq3Vpsux+7mfk08eoeTL5DxOoQQrZNcxEXJkIM6V2knPXbH9m2Wcyz1Yq7y+l5JIq6B1n2zva7cSiGh2rGKIANXXs+xjUnFzQjJjF+UCHS2k7Z+dxoq6oy/88lLWWYubrAxkNPTCJ39OQtKK85beiq/rbJGx4Kp0DvBybpcTsHQvkV0QqiHvtJ7Um39Ao2RgpNydtlRBExpqHRFVOT2sRfHSpE+lEzlXjwD/w5XVqAD53VCYDzEgbEouRmMeqjIT1xEHF5wUR1rNfJ/b9noA6rRCP56TnOfzKsneKUCerpQa7xJHU3A9DfHaTtuWYELUailIXByWHptecWPs1VmOvy/Jw6WuQxElLyuGqnDTwCvTl/TQv494SQWEXvf/k4a2ilkoFKa1zxocN58UkOKky1wcKKdnn+1b3wZI4nq5ppfT3mvJJya1FCmXSNsTlAM0ndMn9Jbzoz4tU6sDd+4jTStBIs0Ox7ypTzzU1KEJKw4BLilBxDkpIMJnj6Bgyy2JLcsTmmg8xDbI8pFbcoE1fwO7iYLvqW0ylvGIlXPFmZYecGOYxzhr9FAKyLdUEP/wXx9Z5t3PKBtYEYtWspALZQDEmHA81EW5tjVloyfHFwCB8nWQNUnuqmuOtqIGwBbG3Oy/tvStmyataMnqK9aty2pw== hemalathar@spingames.net' >> /home/ubuntu/.ssh/authorized_keys")


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




