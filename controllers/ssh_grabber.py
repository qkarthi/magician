@auth.requires_login()
def sshShell(endpoint, username, credential, cmd):
    import paramiko
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(endpoint, username=username, password=credential,
                       key_filename="C:\\Users\\karthik\\OneDrive\\OneDrive - Spin Games LLC\\.ssh\\id_rsa")
    stdin, stdout, stderr = ssh_client.exec_command(cmd)
    k = stdout.readlines()
    print(k)
    ssh_client.close()
    return k

# sed '/ karthikeyan.p@spingames.net/d'
# ("echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDNllUA9r0dMwAj75+I+/Lq3Vpsux+7mfk08eoeTL5DxOoQQrZNcxEXJkIM6V2knPXbH9m2Wcyz1Yq7y+l5JIq6B1n2zva7cSiGh2rGKIANXXs+xjUnFzQjJjF+UCHS2k7Z+dxoq6oy/88lLWWYubrAxkNPTCJ39OQtKK85beiq/rbJGx4Kp0DvBybpcTsHQvkV0QqiHvtJ7Um39Ao2RgpNydtlRBExpqHRFVOT2sRfHSpE+lEzlXjwD/w5XVqAD53VCYDzEgbEouRmMeqjIT1xEHF5wUR1rNfJ/b9noA6rRCP56TnOfzKsneKUCerpQa7xJHU3A9DfHaTtuWYELUailIXByWHptecWPs1VmOvy/Jw6WuQxElLyuGqnDTwCvTl/TQv494SQWEXvf/k4a2ilkoFKa1zxocN58UkOKky1wcKKdnn+1b3wZI4nq5ppfT3mvJJya1FCmXSNsTlAM0ndMn9Jbzoz4tU6sDd+4jTStBIs0Ox7ypTzzU1KEJKw4BLilBxDkpIMJnj6Bgyy2JLcsTmmg8xDbI8pFbcoE1fwO7iYLvqW0ylvGIlXPFmZYecGOYxzhr9FAKyLdUEP/wXx9Z5t3PKBtYEYtWspALZQDEmHA81EW5tjVloyfHFwCB8nWQNUnuqmuOtqIGwBbG3Oy/tvStmyataMnqK9aty2pw== hemalathar@spingames.net' >> /home/ubuntu/.ssh/authorized_keys")


@auth.requires_login()
def index():
    row = db(db.db_serverSshData.id > 0).select(db.db_serverSshData.ALL, orderby=~db.db_serverSshData.id, limitby=(0, 1)).first()
    session.TblLstRow = row.id
    rows = db().select(db.db_serverDet.ALL)
    db(db.db_serverDet.ssh_fetch == 0).update(ssh_fetch=1)
    return dict(rows=rows)

def fetchTblValue():
    strSnd = "<tr><th><b>Ins.Id</b></th><th><b>Instance name</b></th><th><b>Category</b></th><th><b>Purpose</b></th><th><b>IPV4</b></th><th><b>Region</b></th><th><b>Last Check</b></th><th><b>Action</b></th></tr>"
    rowsCount = db((db.db_serverSshData.id > session.TblLstRow) & (db.db_serverSshData.instance_id == db.db_serverDet.instance_id)).count()
    rowsALL = db((db.db_serverSshData.id > session.TblLstRow) & (
                db.db_serverSshData.instance_id == db.db_serverDet.instance_id)).select()
    if rowsCount > 0:
        for row in rowsALL:
            if row.db_serverSshData.auth_keys == None:
                 lastFetch = "Not Initiated"
                 print(lastFetch)
            elif row.db_serverSshData.auth_keys == 'TimeoutError':
                 lastFetch = "N/A"
            elif row.db_serverSshData.auth_keys == 'ValueError':
                lastFetch = "N/A"
            else:
                lastFetch = row.db_serverSshData.time_stamp
            strSnd = strSnd + "<tr><td>" + str(row.db_serverDet.id) + "</td><td>" + str(row.db_serverDet.name) + "</td><td>" + str(row.db_serverDet.category) + "</td><td>" + str(row.db_serverDet.purpose) + "</td><td>" + str(row.db_serverDet.pub_ipv4) + "</td><td>" + str(row.db_serverDet.hosted_region) + "</td><td>" + str(lastFetch) + "</td></tr>"
    return strSnd


@auth.requires_login()
def fetchProgsValue():
    totS = db(db.db_serverDet).count()
    query = (db.db_serverDet.ssh_fetch == 0)
    totSshGdb = db(query).count()
    serSshRemCnt = (totSshGdb/totS)*100
    return int(serSshRemCnt)



@auth.requires_login()
def authSshGet():
    import ast
    for row in db(db.db_serverDet.id == request.args(0, cast=int)).select():
        query = (db.db_serverSshData.instance_id == row.instance_id)
        x = db(query).select(db.db_serverSshData.ALL, orderby=~db.db_serverSshData.id, limitby=(0, 1)).first()
        k = x.auth_keys
    return dict(k=ast.literal_eval(k))

def addSshKey(x):
    for row in db(db.db_serverDet.id == request.args(0, cast=int)).select():
        ip_add = row.pub_ipv4
    return dict()

@auth.requires_login()
def del1ums():
    return dict()

@auth.requires_login()
def addmuss():
    query = db.db_user.id > 0
    fields = (db.db_user.name, db.db_user.team, db.db_user.ssh_key_id, db.db_user.emp_id)
    form = SQLFORM.grid(query, fields, selectable=lambda ids : addSshKey(ids), user_signature=False, csv=False, searchable=False, create=False, details=False, editable=False, deletable=False)
    return dict(form=form)

@auth.requires_login()
def add1ums():
    rows = db().select(db.db_user.ALL)
    return dict(rows=rows)
@auth.requires_login()
def add1ums_phase1():
    x = request.args(0, cast=int)
    queCat1 = "NULL"
    queCat2 = "NULL"
    queCat3 = "NULL"
    queCat4 = "NULL"
    queCat5 = "NULL"
    for row in db(db.db_user.id == request.args(0, cast=int)).select():
        if (row.production):
            queCat1 = 'Production'
        if(row.stage):
            queCat2 = 'Stage'
        if (row.testing):
            queCat3 = 'Testing'
        if (row.research):
            queCat4 = 'Research'
        if (row.development):
            queCat5 = 'Development'
    fields_x = (db.db_serverDet.name, db.db_serverDet.purpose, db.db_serverDet.category, db.db_serverDet.pub_ipv4, db.db_serverDet.pri_ipv4, db.db_serverDet.hosted_region)
    query = ((db.db_serverDet.category == queCat1) | (db.db_serverDet.category == queCat2) | (db.db_serverDet.category == queCat3) | (db.db_serverDet.category == queCat4) | (db.db_serverDet.category == queCat5))
    form = SQLFORM.grid(query, fields = fields_x, selectable=lambda ids: addSshKey(ids), user_signature=False, csv=False,
                        searchable=False, create=False, details=False, editable=False, deletable=False)

    return dict(form=form)
