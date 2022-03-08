@auth.requires_login()
def listUser():
    form = SQLFORM.grid(db.db_user,  user_signature=False, csv=True,
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
def addUser():
    form = SQLFORM(db.db_user, submit_button='Add User')
    form.process(detect_record_change=True)
    if form.accepted:
        response.flash = T("User successfully added")
    return dict(form=form)

@auth.requires_login()
def archiveUser(x):
    rows = db(db.db_user.id.belongs(x)).select()
    for row in rows:
        db.db_user_arch.insert(name=row.name,last_name=row.last_name, team=row.team, email=row.email, emp_id=row.emp_id, ssh_key=row.ssh_key,
                               ssh_key_id=row.ssh_key_id, development=row.development, testing=row.testing,
                               research=row.research, stage=row.stage, production=row.production)
        db(db.db_user.id == row.id).delete()
    redirect(URL('listUser'))

@auth.requires_login()
def delUser():
    form = SQLFORM.grid(db.db_user,  selectable=lambda ids: archiveUser(ids), user_signature=False,csv=False,
                        searchable=False, create=False, details=False, editable=False, deletable=False)
    return dict(form=form)

@auth.requires_login()
def restoreUser(x):
    rows = db(db.db_user_arch.id.belongs(x)).select()
    for row in rows:
        db.db_user.insert(name=row.name,last_name=row.last_name, team=row.team, email=row.email, emp_id=row.emp_id, ssh_key=row.ssh_key,
                               ssh_key_id=row.ssh_key_id, development=row.development, testing=row.testing,
                               research=row.research, stage=row.stage, production=row.production)
        db(db.db_user_arch.id == row.id).delete()
    redirect(URL('listUser'))

@auth.requires_login()
def inactUser():
    form = SQLFORM.grid(db.db_user_arch,  selectable=lambda ids: restoreUser(ids), user_signature=False,csv=False,
                        searchable=False, create=False, details=False, editable=False, deletable=False)
    return dict(form=form)
