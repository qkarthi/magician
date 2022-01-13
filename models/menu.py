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
            (T('Edit'), False, URL('welcome', 'server', 'editServer')),
            (T('Remove'), False, URL('welcome', 'server', 'delServer')),
            (T('In-active'), False, URL('welcome', 'server', 'inactServer'))
        ]),
        (T('User'), False, '#', [
            (T('List'), False, URL('welcome', 'user', 'listUser')),
            (T('Add'), False, URL('welcome', 'user', 'addUser')),
            (T('Edit'), False, URL('welcome', 'user', 'editUser')),
            (T('Remove'), False, URL('welcome', 'user', 'delUser')),
            (T('In-active'), False, URL('welcome', 'user', 'inactUser'))
        ]),
        (T('SSH'), False, '#', [
            (T('Audit'), False, URL('welcome', 'ssh_grabber', 'index')),
        ]),


    ]

