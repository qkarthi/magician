# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Home'), False, URL('default', 'index'), [])
]

# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------

if not configuration.get('app.production'):
    _app = request.application
    response.menu += [
        (T('Server'), False, '#', [
            (T('List'), False, URL('welcome', 'server', 'listServer')),
            (T('Add'), False, URL('welcome', 'server', 'addServer')),
            (T('Remove'), False, URL('welcome', 'server', 'delServer')),
            (T('In-active'), False, URL('welcome', 'server', 'inactServer'))
        ]),
        (T('User'), False, '#', [
            (T('List'), False, URL('welcome', 'user', 'listUser')),
            (T('Add'), False, URL('welcome', 'user', 'addUser')),
            (T('Remove'), False, URL('welcome', 'user', 'delUser')),
            (T('In-active'), False, URL('welcome', 'user', 'inactUser'))
        ]),
        (T('SSH'), False, '#', [
            (T('Audit server wise'), False, URL('welcome', 'sshEngine', 'index')),

            (T('Add 1 User - (N) Server'), False, URL('welcome', 'sshEngine', 'add1ums')),
            (T('DEL 1 User - (N) Server'), False, URL('welcome', 'sshEngine', 'del1ums')),

            (T('Add (N) User - 1 Server'), False, URL('welcome', 'sshEngine', 'addmuss')),
        ]),
        (T('Test'), False, '#', [
            (T('test modules'), False, URL('welcome', 'test', 'index'))
        ]),


    ]

