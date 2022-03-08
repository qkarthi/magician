@auth.requires_login()
def listServer():
    form = SQLFORM.grid(db.db_serverDet,  user_signature=False, csv=True,
                        searchable=True, create=False, details=False, editable=True, deletable=False ,
                        exportclasses=dict(
                            csv_with_hidden_cols=False,
                            xml=False,
                            html=False,
                            csv=True,
                            json=False,
                            tsv_with_hidden_cols=False,
                            tsv=False)
                        )
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
                                    vpn=row.vpn)
        db(db.db_serverDet.id == row.id).delete()
    redirect(URL('listServer'))

def delServer():
    form = SQLFORM.grid(db.db_serverDet,  selectable=lambda ids: ArchiveServer(ids), user_signature=False,csv=True,
                        paginate=500,searchable=False, create=False, details=False, editable=False, deletable=False,
                        exportclasses=dict(
                            csv_with_hidden_cols=False,
                            xml=False,
                            html=False,
                            csv=True,
                            json=False,
                            tsv_with_hidden_cols=False,
                            tsv=False)
                        )
    if form.elements('th'):
        form.elements('th')[0].append(SPAN('All', BR(), INPUT(_type='checkbox',
                                                          _onclick="jQuery('input:checkbox').not(this).prop('checked', this.checked);"
                                                          )))
    return dict(form=form)


def restoreServer(x):
    rows = db(db.db_serverDet_arch.id.belongs(x)).select()
    for row in rows:
        db.db_serverDet.insert(name=row.name, instance_id=row.instance_id, pub_ipv4=row.pub_ipv4, pri_ipv4=row.pri_ipv4,
                               pub_ipv4_dns=row.pub_ipv4_dns, username=row.username, credential=row.credential,
                               category=row.category, purpose=row.purpose, hosted_region=row.hosted_region,
                               vpn=row.vpn)
        db(db.db_serverDet_arch.id == row.id).delete()
    redirect(URL('listServer'))


def inactServer():
    form = SQLFORM.grid(db.db_serverDet_arch,  selectable=lambda ids: restoreServer(ids), user_signature=False,csv=True,
                        paginate=500, searchable=True, create=False, details=False, editable=False, deletable=False,
                        exportclasses=dict(
                            csv_with_hidden_cols=False,
                            xml=False,
                            html=False,
                            csv=True,
                            json=False,
                            tsv_with_hidden_cols=False,
                            tsv=False)
                        )
    if form.elements('th'):
        form.elements('th')[0].append(SPAN('All', BR(), INPUT(_type='checkbox',
                                                              _onclick="jQuery('input:checkbox').not(this).prop('checked', this.checked);"
                                                              )))
    return dict(form=form)