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

Tconect = DAL('mysql://DBGrnt:,.~~Grnt861@10.7.0.28/Tconect' )


if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL('mysql://DBGrnt:,.~~Grnt861@10.7.0.28/Tconect',
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=True,
             #fake_migrate_all=True,
             check_reserved=['mysql'])

else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL(u'google:datastore+ndb')
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
auth = Auth(db,
    cas_provider='https://qa.riopreto.sp.gov.br/MeioAmbienteRP/default/user/cas',
     )

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------



auth.define_tables(username=True, signature=False)

from validador import IS_CPF
auth.settings.extra_fields['auth_user'] = [
    Field('IdDepto', 'integer'),
    Field('CPF', 'text', requires=IS_CPF()),
    ]


auth.settings.update_fields = [ 'first_name', 'last_name', 'username', 'email', 'CPF', 'IdDepto']

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = configuration.get('smtp.server') # 'logging' if request.is_local else 
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
# auth.settings.registration_requires_verification = True
# auth.settings.registration_requires_approval = False
# auth.settings.reset_password_requires_verification = True

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
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
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




UnidadeDestino = db.define_table('UnidadeDestino',
    Field ('Id', 'id'),
    Field ('IdEmpreendedor', 'integer'),
    Field ('IdEndereco', 'integer'),
    Field ('Tipo', 'text'),
    Field ('Atividade', 'text',),
    Field ('Coordenadas', 'text'),
    Field ('Matricula', 'text'),
    Field ('Area', 'decimal(8,2)'),
    format = '%(Atividade)s',
    migrate = False )



veiculos = [(1, 'Carro'), (2, 'CARROCA'), (3, 'PICKUP'), (4, 'CARRETA_P'), (5, 'CARRETA_G'), (6, 'OUTRO')]

from validador import IS_CHKBOX01



EntradaPonto = db.define_table('EntradaPonto',
    Field ('Id', 'id'),
    Field ('Placa',  'string', length='9', required=True, requires = IS_MATCH('[ABCDEFGHIJKLMNOPQRSTUVWXYZ#]{3}', error_message='Não é Placa')),
    Field ('TipoVeic', 'integer', requires = IS_IN_SET(veiculos)),
    Field ('Data', 'date', required=True),
    Field ('Volume', 'decimal(3,2)', default=1.0 ,requires=IS_IN_SET([1.0, 2.0 ]), widget=SQLFORM.widgets.radio.widget ),
    Field ('Sofa', 'integer',default=0 ,requires=IS_IN_SET([0, 1, 2, 3, 4 ]), widget=SQLFORM.widgets.radio.widget), 
    Field ('Colchao' , 'integer', default=0 ,requires=IS_IN_SET([0, 1, 2, 3, 4 ]), widget=SQLFORM.widgets.radio.widget, rname='Colchão'),
    Field ('Poda', 'integer', requires= IS_CHKBOX01(on=1, off=0) ,widget=SQLFORM.widgets.boolean.widget),
    Field ('Moveis', 'integer',requires= IS_CHKBOX01(on=1, off=0) ,widget=SQLFORM.widgets.boolean.widget), 
    Field ('Ferro', 'integer', requires= IS_CHKBOX01(on=1, off=0) ,widget=SQLFORM.widgets.boolean.widget),
    Field ('Entulho', 'integer',  requires= IS_CHKBOX01(on=1, off=0) ,widget=SQLFORM.widgets.boolean.widget),
    Field ('PlastPapel', 'integer', requires= IS_CHKBOX01(on=1, off=0) ,widget=SQLFORM.widgets.boolean.widget),
    Field ('Eletron', 'integer', requires= IS_CHKBOX01(on=1, off=0) ,widget=SQLFORM.widgets.boolean.widget),
    Field ('Outros', 'string', length='15',),
    Field ('IdPonto', 'reference UnidadeDestino', requires=IS_IN_DB(db(db.UnidadeDestino.Tipo=='Ponto de Apoio'), 'UnidadeDestino.Id', \
        db.UnidadeDestino._format)),
    migrate = False )

MedicoesOpac = db.define_table('MedicoesOpac',
    Field ('ID', 'id'),
    Field('PM', 'string', length='6'),
    Field('Placa','string', length='9', required=True, requires = IS_MATCH('[ABCDEFGHIJKLMNOPQRSTUVWXYZ#]{3}', error_message='Não é Placa')),
    Field('Data', 'date', required=True),
    Field('Hora', 'time', required=True),
    Field('Kmaximo', 'decimal(3,2)'),
    Field('KMedido', 'decimal(3,2)'),
    Field('Resultado', 'text' ),
    Field('BaseLegal', 'text', length='25'),
    Field('NvRingelmann', 'integer', requires=IS_IN_SET([1,2,3,4,5]), widget=SQLFORM.widgets.radio.widget),
    Field('Obs', 'text', length='150'),
    migrate = False
    )
