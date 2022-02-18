@auth.requires_login()
def listServer():
    rows = db().select(db.db_serverDet.ALL)
    return dict(rows=rows)

@auth.requires_login()
def editServer():
    for row in db(db.db_serverDet.id == request.args(0, cast=int)).select():
        update = db.db_serverDet(row.id)
        form = SQLFORM(db.db_serverDet, update, submit_button='update', showid=False)
        form.process(detect_record_change=True)
        if form.accepted:
            redirect(URL('listServer'))
        return dict(form=form)

@auth.requires_login()
def addServer():
    form = SQLFORM(db.db_serverDet, submit_button='Add Sever')
    form.process(detect_record_change=True)
    if form.accepted:
        response.flash = T("Server successfully added")
    return dict(form=form)

def ArchiveServer(x):
    rows = db(db.db_serverDet.id.belongs(x)).select()
    for row in rows:
        db.db_serverDet_arch.insert(name=row.name,instance_id=row.instance_id,pub_ipv4=row.pub_ipv4,pri_ipv4=row.pri_ipv4,pub_ipv4_dns=row.pub_ipv4_dns,
                                    username=row.username,credential=row.credential,category=row.category,purpose=row.purpose,hosted_region=row.hosted_region,
                                    vpn=row.vpn,ssh_fetch=row.ssh_fetch)
        db(db.db_serverDet.id == row.id).delete()
    redirect(URL('listServer'))

def delServer():
    form = SQLFORM.grid(db.db_serverDet,  selectable=lambda ids: ArchiveServer(ids), user_signature=False,csv=False,
                        searchable=False, create=False, details=False, editable=False, deletable=False)
    return dict(form=form)


def restoreServer(x):
    rows = db(db.db_serverDet_arch.id.belongs(x)).select()
    for row in rows:
        db.db_serverDet.insert(name=row.name, instance_id=row.instance_id, pub_ipv4=row.pub_ipv4, pri_ipv4=row.pri_ipv4,
                               pub_ipv4_dns=row.pub_ipv4_dns, username=row.username, credential=row.credential,
                               category=row.category, purpose=row.purpose, hosted_region=row.hosted_region,
                               vpn=row.vpn, ssh_fetch=row.ssh_fetch)
        db(db.db_serverDet_arch.id == row.id).delete()
    redirect(URL('listServer'))


def inactServer():
    form = SQLFORM.grid(db.db_serverDet_arch,  selectable=lambda ids: restoreServer(ids), user_signature=False,csv=False,
                        searchable=False, create=False, details=False, editable=False, deletable=False)
    return dict(form=form)