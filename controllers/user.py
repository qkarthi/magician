@auth.requires_login()
def editUser():
    for row in db(db.db_user.id == request.args(0, cast=int)).select():
        update = db.db_user(row.id)
        form = SQLFORM(db.db_user, update, submit_button='update', showid=False)
        form.process(detect_record_change=True)
        if form.accepted:
            redirect(URL('listUser'))
        return dict(form=form)

@auth.requires_login()
def listUser():
    rows = db().select(db.db_user.ALL)
    return dict(rows=rows)

@auth.requires_login()
def addUser():
    form = SQLFORM(db.db_user, submit_button='Add User')
    form.process(detect_record_change=True)
    if form.accepted:
        response.flash = T("User successfully added")
    return dict(form=form)
