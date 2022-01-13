import paramiko
ssh_client = paramiko.SSHClient()
def index():
    return dict()

def sshStart():
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect("54.163.48.245", username="ubuntu", password="",
                       key_filename="C:\\Users\\karthik\\OneDrive\\OneDrive - Spin Games LLC\\.ssh\\id_rsa")
    s = "started"
    return s

def sshStop():
    ssh_client.close()
    s = "stopped"
    return s


def sshCmd():
    cmd = request.vars.q
    print(cmd)
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect("54.163.48.245", username="ubuntu", password="",
                       key_filename="C:\\Users\\karthik\\OneDrive\\OneDrive - Spin Games LLC\\.ssh\\id_rsa")
    stdin, stdout, stderr = ssh_client.exec_command(cmd)

    ec = stdout.readlines()
    ssh_client.close()
    return ec




