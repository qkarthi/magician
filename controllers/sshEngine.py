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
###################################################################################################################
###################################################################################################################
@auth.requires_login()
def index():
    # Get No.of Records in DB
    row = db(db.db_serverCmdExec.id > 0).select(db.db_serverCmdExec.ALL, orderby=~db.db_serverCmdExec.id, limitby=(0, 1)).first()
    if row == None:
        session.TblLstRow = 0
    else:
        session.TblLstRow = row.id
    # collect make a request to handler
    cnt = db(db.db_serverCmdExec.id > 0).count()
    if cnt == 0:
        for row in db(db.db_serverDet.instance_id>0).select(orderby=db.db_serverDet.id):
            server_named = row.name
            instance_id = row.instance_id
            xecuted = 0
            username = row.username
            ip_address = row.pub_ipv4
            cred_method = "sshPubKey"
            trans_purp = "sshKeyFetch"
            cmd = "cat /home/ubuntu/.ssh/authorized_keys"
            db.db_serverCmdExec.insert(server_named=server_named, instance_id=instance_id, username=username,
                                       ip_address=ip_address, cred_method=cred_method, trans_purp=trans_purp, cmd=cmd,
                                       xecuted=xecuted)
    else:
        count = db.db_serverDet.instance_id.count()
        for row in db(((db.db_serverCmdExec.trans_purp == "sshKeyFetch") & (db.db_serverCmdExec.xecuted != 0)) & (db.db_serverCmdExec.instance_id == db.db_serverDet.instance_id)).select(db.db_serverDet.ALL, count, groupby=db.db_serverDet.instance_id, orderby=db.db_serverDet.id):
            server_named = row.db_serverDet.name
            instance_id = row.db_serverDet.instance_id
            xecuted = 0
            username = row.db_serverDet.username
            ip_address = row.db_serverDet.pub_ipv4
            cred_method = "sshPubKey"
            trans_purp = "sshKeyFetch"
            cmd = "cat /home/ubuntu/.ssh/authorized_keys"
            db.db_serverCmdExec.insert(server_named=server_named,instance_id=instance_id,username=username,ip_address=ip_address,cred_method=cred_method,trans_purp=trans_purp,cmd=cmd,xecuted=xecuted)
    return dict()

@auth.requires_login()
def fetchTblValue():
    strSnd = "<tr><th><b>Ins.Id</b></th><th><b>Instance name</b></th><th><b>Category</b></th><th><b>Purpose</b></th><th><b>IPV4</b></th><th><b>Region</b></th><th><b>Last Check</b></th><th><b>Action</b></th></tr>"
    rowsALL = db((db.db_serverCmdExec.id > session.TblLstRow) & (
            db.db_serverCmdExec.instance_id == db.db_serverDet.instance_id) & (db.db_serverCmdExec.xecuted == 1) & (db.db_serverCmdExec.trans_purp == "sshKeyFetch")).select()
    if rowsALL != None:
        for row in rowsALL:
            if row.db_serverCmdExec.stdout_ == None:
                btn = "Not Initiated"
            elif row.db_serverCmdExec.stdout_ == 'TimeoutError':
                btn = "U/L"
            elif row.db_serverCmdExec.stdout_ == 'ValueError':
                btn = "I/K"
            else:
                btn = "<a href=\"javascript:window.open('authSshGet/" + str(row.db_serverDet.id) + "');\">Audit</a>"

            # {{_href = URL(\"authSshGet\", args=row.id)))}}
            # btn = "<form method=\"post\" action=\"authSshGet/"+str(row.db_serverDet.id)+"\"><input type=\"submit\" value=\"Audit\"></form>"
            # btn = "<a href=\"javascript:window.open('authSshGet/" +str(row.db_serverDet.id) +"', '_blank', 'width=200,height=150');\">Audit</a>"

            strSnd = strSnd + "<tr><td>" + str(row.db_serverDet.id) + "</td><td>" + str(
                row.db_serverDet.name) + "</td><td>" + str(row.db_serverDet.category) + "</td><td>" + str(
                row.db_serverDet.purpose) + "</td><td>" + str(row.db_serverDet.pub_ipv4) + "</td><td>" + str(
                row.db_serverDet.hosted_region) + "</td><td>" + str(
                row.db_serverCmdExec.modified_on) + "</td> <td>" + btn + "</td></tr>"
    return strSnd

@auth.requires_login()
def fetchProgsValue():
    tots = db((db.db_serverDet.id > 0)).count()
    totSshGdb = db((db.db_serverCmdExec.xecuted == 0) & (db.db_serverCmdExec.trans_purp == "sshKeyFetch")).count()
    serSshRemCnt = 100-((totSshGdb/tots)*100)
    return int(serSshRemCnt)

@auth.requires_login()
def authSshGet():
    import ast
    for row in db(db.db_serverDet.id == request.args(0, cast=int)).select():
        query = (db.db_serverCmdExec.instance_id == row.instance_id)
        x = db(query).select(db.db_serverCmdExec.ALL, orderby=~db.db_serverCmdExec.id, limitby=(0, 1)).first()
        k = x.stdout_
    return dict(k=ast.literal_eval(k))

@auth.requires_login()
def addSshKey(x):
    session.SelServ = x
    redirect(URL('addSshKey_phase1'))

@auth.requires_login()
def addSshKey_phase1():
    strSnd = "<tr><th><b>Ins.Id</b></th><th><b>Instance name</b></th><th><b>Category</b></th><th><b>Purpose</b></th><th><b>IPV4</b></th><th><b>Region</b></th><th><b>Last Check</b></th><th><b>Action</b></th></tr>"
    rows = db(db.db_serverDet.id.belongs(session.SelServ)).select()
    for instRow in rows:
        row = db(db.db_serverCmdExec.instance_id == instRow.instance_id).select(db.db_serverCmdExec.ALL, orderby=~db.db_serverCmdExec.id, limitby=(0, 1)).first()
        if row != None:
            if row.stdout_ == None:
                stat = "Not Initiated"
            elif row.stdout_ == 'TimeoutError':
                stat = "U/L"
            elif row.stdout_ == 'ValueError':
                stat = "I/K"
            else:
                stat = "DEPLOYABLE"
            strSnd = strSnd + "<tr><td>" + str(instRow.id) + "</td><td>" + str(
                instRow.name) + "</td><td>" + str(instRow.category) + "</td><td>" + str(
                instRow.purpose) + "</td><td>" + str(instRow.pub_ipv4) + "</td><td>" + str(
                instRow.hosted_region) + "</td><td>" + str(row.modified_on) + "</td> <td>" + stat + "</td></tr>"

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
    session.SelUsr = x
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
