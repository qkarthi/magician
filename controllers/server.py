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