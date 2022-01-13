@auth.requires_login()
def index():
    rows = db().select(db.db_serverDet.ALL)
    return dict(rows=rows)

@auth.requires_login()
def authSshGet():
    import paramiko
    for row in db(db.db_serverDet.id == request.args(0, cast=int)).select():
        ip_add = row.pub_ipv4

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(ip_add, username='ubuntu', password='',
                key_filename="C:\\Users\\karthik\\OneDrive\\OneDrive - Spin Games LLC\\.ssh\\id_rsa")
    stdin, stdout, stderr = ssh_client.exec_command('cat /home/ubuntu/.ssh/authorized_keys')
    k = stdout.readlines()
    ssh_client.close()
    print(k)
    return dict(k=k)


