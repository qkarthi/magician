# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))
auth.settings.extra_fields['auth_user'] = [
Field ('xxid', length=128,writable=False,readable=False)
]
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#

signature = db.Table(db,'auth_signature',
        Field('time_stamp','datetime',default=request.now,
            writable=False,readable=False, label=T('Created on')),
        Field('created_by','reference %s' % auth.settings.table_user_name,default=auth.user_id,
            writable=False,readable=False, label=T('Created by')),
        Field('modified_on','datetime',update=request.now,default=request.now,
            writable=False,readable=False, label=T('Modified on')),
        Field('modified_by','reference %s' % auth.settings.table_user_name,default=auth.user_id,
            update=auth.user_id,writable=False,readable=False, label=T('Modified by'))
      )
db._common_fields.append(signature) #db._common_fields is a list of fields that should belong to all the tables


db.define_table('db_serverDet',
                Field('name', 'string', requires=IS_NOT_EMPTY()),
                Field('instance_id', 'string', requires=IS_NOT_EMPTY()),
                Field('pub_ipv4', label=T('IPV4 Public Address')),  # need a regular expression
                Field('pri_ipv4', label=T('IPV4 Private Address')),  # need a regular expression
                Field('pub_ipv4_dns', 'string'),
                Field('username', 'string', requires=IS_NOT_EMPTY()),
                Field('credential', 'string'),
                Field('category', 'string', requires=IS_IN_SET(['Development', 'Testing', 'Research', 'Stage', 'Production'])),
                Field('purpose', 'string', requires=IS_IN_SET(['Webserver', 'Load_balancer', 'Database', 'Backup'])),
                Field('hosted_region', 'string', requires=IS_IN_SET(['N_virginia', 'Oregon', 'Sydney'])),
                Field('vpn', requires=IS_IN_SET(['N/A', 'NJ', 'MI', 'PA']))
                )




db.define_table('db_serverDet_arch',
                Field('name', 'string', requires=IS_NOT_EMPTY()),
                Field('instance_id', 'string', requires=IS_NOT_EMPTY()),
                Field('pub_ipv4', requires=IS_MATCH('((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}'), label=T('IPV4 Public Address')),  # need a regular expression
                Field('pri_ipv4', requires=IS_MATCH('((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}'), label=T('IPV4 Private Address')),  # need a regular expression
                Field('pub_ipv4_dns', 'string'),
                Field('username', 'string', requires=IS_NOT_EMPTY()),
                Field('credential', 'string'),
                Field('category', 'string', requires=IS_IN_SET(['Development', 'Testing', 'Research', 'Stage', 'Production'])),
                Field('purpose', 'string', requires=IS_IN_SET(['Webserver', 'Load_balancer', 'Database', 'Backup'])),
                Field('hosted_region', 'string', requires=IS_IN_SET(['N_virginia', 'Oregon', 'Sydney'])),
                Field('vpn', requires=IS_IN_SET(['N/A', 'NJ', 'MI', 'PA']))
                )

db.define_table('db_user',
                Field('name', 'string', requires=IS_NOT_EMPTY()),
                Field('last_name', 'string', requires=IS_NOT_EMPTY()),
                Field('team', 'string', requires=IS_IN_SET(['DevOps', 'Development', 'QA', 'Testing'])),
                Field('email', 'string', requires=IS_EMAIL()),
                Field('emp_id', 'string', requires= IS_NOT_EMPTY()),
                Field('ssh_key', 'text', requires=IS_NOT_EMPTY()),
                Field('ssh_key_id', 'string', requires=IS_NOT_EMPTY()),
                Field('development', 'boolean'),
                Field('testing', 'boolean'),
                Field('research', 'boolean'),
                Field('stage', 'boolean'),
                Field('production', 'boolean')
                )



db.define_table('db_user_arch',
                Field('name', 'string', requires=IS_NOT_EMPTY()),
                Field('last_name', 'string', requires=IS_NOT_EMPTY()),
                Field('team', 'string', requires=IS_IN_SET(['DevOps', 'Development', 'QA', 'Testing'])),
                Field('email', 'string', requires=IS_EMAIL()),
                Field('emp_id', 'string', requires=IS_NOT_EMPTY()),
                Field('ssh_key', 'text', requires=IS_NOT_EMPTY()),
                Field('ssh_key_id', 'string', requires=IS_NOT_EMPTY()),
                Field('development', 'boolean'),
                Field('testing', 'boolean'),
                Field('research', 'boolean'),
                Field('stage', 'boolean'),
                Field('production', 'boolean')
                )


db.define_table('db_serverCmdExec',
                Field('server_named', 'string', requires=IS_NOT_EMPTY()),
                Field('instance_id', 'string', requires=IS_NOT_EMPTY()),
                Field('ip_address', 'string'),
                Field('username', 'string'),
                Field('cred_method', 'string'),
                Field('trans_purp', 'string'),
                Field('cmd', 'text'),
                Field('stdout_', 'text'),
                Field('xecuted', 'boolean'),
                Field('info', 'string')
                )







db.db_serverDet.name.requires = IS_NOT_IN_DB(db, 'db_serverDet.name')
db.db_serverDet.instance_id.requires = IS_NOT_IN_DB(db, 'db_serverDet.instance_id')
db.db_serverDet.pub_ipv4_dns.requires = IS_NOT_IN_DB(db, 'db_serverDet.pub_ipv4_dns')
db.db_serverDet.pub_ipv4.requires = IS_NOT_IN_DB(db, 'db_serverDet.pub_ipv4')
db.db_serverDet.pub_ipv4.requires = IS_NOT_IN_DB(db, 'db_serverDet.pub_ipv4')
#db.db_serverDet.pri_ipv4.requires = IS_MATCH('((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}')
#db.db_serverDet.pri_ipv4.requires = IS_MATCH('((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}')

db.db_user.email.requires = IS_NOT_IN_DB(db, 'db_user.email')
db.db_user.emp_id.requires = IS_NOT_IN_DB(db, 'db_user.emp_id')
db.db_user.ssh_key.requires = IS_NOT_IN_DB(db, 'db_user.ssh_key')
db.db_user.ssh_key_id.requires = IS_NOT_IN_DB(db, 'db_user.ssh_key_id')
db.db_user.emp_id.requires = IS_UPPER()














# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)
