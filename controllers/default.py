@auth.requires_login()
def index():
    response.flash = T("Welcome")
    srv_cnt = db(db.db_serverDet.id > 0).count()
    usr_cnt = db(db.db_spinUser.id > 0).count()
    return dict(srv_cnt=srv_cnt, usr_cnt=usr_cnt)
    return dict(srv_cnt=srv_cnt, usr_cnt=usr_cnt)


@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})


@auth.requires_membership('admin')
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)


def user():
    return dict(form=auth())

@cache.action()
def download():
    return response.download(request, db)
