import paramiko

@auth.requires_login()
def index():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect('100.27.11.150', username='ubuntu', password='',
                key_filename="C:\\Users\\karthik\\OneDrive\\OneDrive - Spin Games LLC\\.ssh\\id_rsa")
    stdin, stdout, stderr = ssh_client.exec_command('cat /home/ubuntu/.ssh/authorized_keys')
    k = stdout.readlines()
    ssh_client.close()
    print(k)
    return dict(k=k)



