# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
def index():
    response.flash = T(" RPGestor")
    #grd_campanhas = SQLFORM.grid(Campanhas)
    li_campanhas = db().select(Campanhas.Nome, Campanhas.Img, orderby=Campanhas.Nome)

    return dict(message=T('Bem Vindo ao RPGestor, Sistema de Gestão de jogos de RPG!'),
        msg_campanhas=T('Campanhas em andamento:'),

       # grd_campanhas=grd_campanhas,
        li_campanhas = li_campanhas,

        msg_personagens=T('Ultimos Personagens criados:'),

        msg_cenarios=T('Cenários em destaque:'),
        )

def Campanha():
    campanha = Campanhas(request.args(0, cast=int)) or redirect(URL('index'))

    return dict(campanha = campanha)




def Criar_Personagem():
	form = SQLFORM(db.Personagens)
	return dict(form = form)


def Criar_Cenario():
    form = SQLFORM(Cenarios)
    return dict(form = form)


def Criar_Campanha():
    form = SQLFORM(Campanhas)
    return dict(form = form)



# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})



# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki()

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
