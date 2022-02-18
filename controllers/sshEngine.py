@auth.requires_login()
def index():
    count = db.db_serverCmdExec.id.max()
    rows = db((db.db_serverCmdExec.instance_id == db.db_serverDet.instance_id) & (
            db.db_serverCmdExec.trans_purp == 'sshKeyFetch') & (db.db_serverCmdExec.xecuted == 1)).select(db.db_serverDet.ALL,db.db_serverCmdExec.ALL,count,orderby=db.db_serverDet.id, groupby=db.db_serverDet.instance_id)
    return dict(rows=rows)
###################################################################################################################
@auth.requires_login()
def updSerNow_init():
    session.serverFetch = 1
    redirect(URL('updSerNow'))
###################################################################################################################
@auth.requires_login()
def updSerNow():
    # Get No.of Records in DB
    if session.serverFetch == 1:
        session.serverFetch = 0
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
                cmd = "cat /home/"+ username+"/.ssh/authorized_keys"
                db.db_serverCmdExec.insert(server_named=server_named, instance_id=instance_id, username=username,
                                           ip_address=ip_address, cred_method=cred_method, trans_purp=trans_purp, cmd=cmd,
                                           xecuted=xecuted)
        else:
            count = db.db_serverDet.instance_id.count()
            for row in db((((db.db_serverCmdExec.trans_purp == "sshKeyFetch") & (db.db_serverCmdExec.xecuted != 0)) & (db.db_serverCmdExec.instance_id == db.db_serverDet.instance_id))|(db.db_serverCmdExec.instance_id != db.db_serverDet.instance_id)).select(db.db_serverDet.ALL, count, groupby=db.db_serverDet.instance_id, orderby=db.db_serverDet.id):
                server_named = row.db_serverDet.name
                instance_id = row.db_serverDet.instance_id
                xecuted = 0
                username = row.db_serverDet.username
                ip_address = row.db_serverDet.pub_ipv4
                cred_method = "sshPubKey"
                trans_purp = "sshKeyFetch"
                cmd = "cat /home/" + username + "/.ssh/authorized_keys"
                db.db_serverCmdExec.insert(server_named=server_named,instance_id=instance_id,username=username,ip_address=ip_address,cred_method=cred_method,trans_purp=trans_purp,cmd=cmd,xecuted=xecuted)
    return dict()
##########################
@auth.requires_login()
def fetchTblValue():
    strSnd = ""
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
##########################
@auth.requires_login()
def fetchProgsValue():
    tots = db((db.db_serverDet.id > 0)).count()
    totSshGdb = db((db.db_serverCmdExec.xecuted == 0) & (db.db_serverCmdExec.trans_purp == "sshKeyFetch")).count()
    serSshRemCnt = 100-((totSshGdb/tots)*100)
    return int(serSshRemCnt)
##########################
#below function for fetcthing individual auth details
@auth.requires_login()
def authSshGet():
    import ast
    for row in db(db.db_serverDet.id == request.args(0, cast=int)).select():
        serverName = row.name
        query = (db.db_serverCmdExec.instance_id == row.instance_id)
        x = db(query).select(db.db_serverCmdExec.ALL, orderby=~db.db_serverCmdExec.id, limitby=(0, 1)).first()
        k = x.stdout_
    return dict(k=ast.literal_eval(k),serverName=serverName)

###################################################################################
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

@auth.requires_login()
def addSshKey(x):
    session.SelServ = x
    redirect(URL('addSshKey_phase1'))

@auth.requires_login()
def addSshKey_phase1():
    #Verification page
    return dict()

@auth.requires_login()
def sshKeyDeploy():
    #session.SelUsr
    #session.SelServ

    import ast
    avail = 0
    k=[]

    userRow = db(db.db_user.id == session.SelUsr).select()
    usrKey = userRow[0].ssh_key_id

    usrName = userRow[0].name
    usrNameinfo = userRow[0].emp_id + " - " + userRow[0].name

    rows = db(db.db_serverDet.id.belongs(session.SelServ)).select()
    for instRow in rows:
        row = db(db.db_serverCmdExec.instance_id == instRow.instance_id).select(db.db_serverCmdExec.ALL,
                                                                                orderby=~db.db_serverCmdExec.id,
                                                                                limitby=(0, 1)).first()
        if row != None:
            if row.stdout_ == None:
                stat = "Not Initiated"
            elif row.stdout_ == 'TimeoutError':
                stat = "U/L"
            elif row.stdout_ == 'ValueError':
                stat = "K/E"
            else:
                stat = "Available"
                k = ast.literal_eval(row.stdout_)
            keyList = []
            for x in k:
                if len(x) > 10:
                    lf = x.rfind(" ")
                    sshKeyId = x[lf:-1]
                    sshKeyId = sshKeyId[1:]
                    keyList.append(sshKeyId)

            if usrKey in keyList:
                stat = "Key Exist - " + str(usrKey)
            else:
                avail = 1
                cred_method = "sshPubKey"
                trans_purp = 'sshKeyAdd'
                username = instRow.username
                instance_id = instRow.instance_id
                xecuted = 0
                server_named = instRow.name
                cmd = "echo \"" + userRow[0].ssh_key + "\" >> /home/"+username+"/.ssh/authorized_keys"
                countPresent = db((db.db_serverCmdExec.instance_id == instRow.instance_id) & (db.db_serverCmdExec.xecuted == 0) & (db.db_serverCmdExec.trans_purp == 'sshKeyAdd') & (db.db_serverCmdExec.info == usrNameinfo)).count()
                print(countPresent)
                if countPresent == 0:
                    db.db_serverCmdExec.insert(server_named=server_named, instance_id=instance_id, username=username,
                                               ip_address=str(instRow.pub_ipv4), cred_method=cred_method, trans_purp=trans_purp,
                                               cmd=cmd, info=usrNameinfo,
                                               xecuted=xecuted)
                    trans_purp = 'sshKeyFetch'
                    cmd = "cat /home/" + username + "/.ssh/authorized_keys"
                    db.db_serverCmdExec.insert(server_named=server_named, instance_id=instance_id, username=username,
                                               ip_address=str(instRow.pub_ipv4), cred_method=cred_method,
                                               trans_purp=trans_purp,
                                               cmd=cmd, info=usrNameinfo,
                                               xecuted=xecuted)
    return dict()

###################################################################################
@auth.requires_login()
def del1ums():
    rows = db().select(db.db_user.ALL)
    return dict(rows=rows)
#######################################
@auth.requires_login()
def del1ums_phase1():
    import ast
    x = request.args(0, cast=int)
    session.SelUsr = x
    serverFiltered=[]
    userRow = db(db.db_user.id == session.SelUsr).select()
    usrKey = userRow[0].ssh_key_id
    keyList = []
    count = db.db_serverCmdExec.id.max()
    for row in db((db.db_serverCmdExec.instance_id == db.db_serverDet.instance_id)&(db.db_serverCmdExec.trans_purp == 'sshKeyFetch')&(db.db_serverCmdExec.xecuted == 1)).select(db.db_serverCmdExec.ALL, count, groupby=db.db_serverDet.instance_id):
        if row != None:
            if ((row.db_serverCmdExec.stdout_ != None) & (row.db_serverCmdExec.stdout_ != 'TimeoutError') & (row.db_serverCmdExec.stdout_ != 'ValueError')):
                k = ast.literal_eval(row.db_serverCmdExec.stdout_)
                keyList = []
                for x in k:
                    if len(x) > 10:
                        lf = x.rfind(" ")
                        sshKeyId = x[lf:-1]
                        sshKeyId = sshKeyId[1:]
                        keyList.append(sshKeyId)
                if usrKey in keyList:
                    serverFiltered.append(row.db_serverCmdExec.instance_id)
    query = db(db.db_serverDet.instance_id.belongs(serverFiltered))
    fields_x = (db.db_serverDet.name, db.db_serverDet.purpose, db.db_serverDet.category, db.db_serverDet.pub_ipv4,
                db.db_serverDet.pri_ipv4, db.db_serverDet.hosted_region)
    form = SQLFORM.grid(query, fields=fields_x, selectable=lambda ids: delsshKey_phase1(ids), user_signature=False, csv=False,
                        searchable=False, create=False, details=False, editable=False, deletable=False)
    return dict(form=form)

def delsshKey_phase1(x):
    print(x)
    userRow = db(db.db_user.id == session.SelUsr).select()
    usrKey = userRow[0].ssh_key_id
    usrNameinfo = userRow[0].emp_id + " - " + userRow[0].name
    for instRow in db(db.db_serverDet.id.belongs(x)).select():
        cred_method = "sshPubKey"
        trans_purp = 'sshKeyDel'
        username = instRow.username
        instance_id = instRow.instance_id
        xecuted = 0
        server_named = instRow.name
        #sed '/ karthikeyan.p@spingames.net/d' authorized_keys1 > authorized_keys
        cmd = "sudo sed -i '/" + usrKey + "/d' /home/"+ username +"/.ssh/authorized_keys"
        countPresent = db((db.db_serverCmdExec.instance_id == instRow.instance_id) & (db.db_serverCmdExec.xecuted == 0) & (
                    db.db_serverCmdExec.trans_purp == 'sshKeyDel') & (db.db_serverCmdExec.info == usrNameinfo)).count()
        print(countPresent)
        if countPresent == 0:
            db.db_serverCmdExec.insert(server_named=server_named, instance_id=instance_id, username=username,
                                       ip_address=str(instRow.pub_ipv4), cred_method=cred_method, trans_purp=trans_purp,
                                       cmd=cmd, info=usrNameinfo,
                                       xecuted=xecuted)
            trans_purp = 'sshKeyFetch'
            cmd = "cat /home/"+ username +"/.ssh/authorized_keys"
            db.db_serverCmdExec.insert(server_named=server_named, instance_id=instance_id, username=username,
                                       ip_address=str(instRow.pub_ipv4), cred_method=cred_method,
                                       trans_purp=trans_purp,
                                       cmd=cmd, info=usrNameinfo,
                                       xecuted=xecuted)
        redirect(URL('delsshKey_phase2'))

def delsshKey_phase2():
    return dict()
###################################################################################


@auth.requires_login()
def addmuss():
    query = db.db_user.id > 0
    fields = (db.db_user.name, db.db_user.team, db.db_user.ssh_key_id, db.db_user.emp_id)
    form = SQLFORM.grid(query, fields, selectable=lambda ids : addSshKey(ids), user_signature=False, csv=False, searchable=False, create=False, details=False, editable=False, deletable=False)
    return dict(form=form)



