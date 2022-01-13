@auth.requires_login()
def listServer():
    rows = db().select(db.db_serverDet.ALL)
    return dict(rows=rows)
