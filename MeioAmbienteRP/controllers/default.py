# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Este é um controlador de amostra
# este arquivo é liberado sob domínio público e você pode usar sem limitações
# -------------------------------------------------------------------------

# ---- exemplo de pagina index _Alterei para que exibisse o Titulo inicial e um contador do númedo de visitas do visitante ----

#user_dpto = db(db.auth_user.id == auth.user_id).select(db.auth_user.Idm)
def index():
    response.flash = ("Seja Bem Vindo")
    session.counter = (session.counter or 0) + 1
    return dict(message=T('Sistema de Dados da Secretaria Municipal de Meio Ambiente - São José do Rio Preto'), counter=session.counter)

@auth.requires_login()
def FConsultA3P():
    formConsultA3P = SQLFORM.factory(Field('IdPredio',db.Predios, requires=IS_IN_DB(dbentidades(db.Predios.CodDepto == user_dpto[0]['Idm']), 'Predios.Id', '%(Predio)s'), label='Local'),
                                     # Field('selectgraf',label='Segmento A3P',requires=IS_IN_SET(['Energia','Água','Resíduo', 'Recursos'])),
                                     Field('slcAno', label='Ano', requires=IS_IN_SET(['2016','2017','2018','2019'])),
                            table_name='ConsultA3p',
                            formstyle='bootstrap' 
                            , buttons = [INPUT(_name='Agua', _class='btn btn-primary btn-lg',_type="submit", value='Água', _value="Água", _onclick="this.form.action.value=Água;this.form.submit()"),
                                        INPUT(_name='Energia', _class='btn btn-primary btn-lg',_type="submit", value='Energia', _value="Energia", _onclick="this.form.action.value=Botao;this.form.submit()"),
                                        INPUT(_name='Residuo', _class='btn btn-primary btn-lg',_type="submit", value='Resíduo',  _value="Resíduo"),
                                        INPUT(_name='Recursos', _class='btn btn-primary btn-lg',_type="submit", value='Recursos',  _value="Recursos")]
                            )

    if formConsultA3P.accepts(request.vars):
        if formConsultA3P.vars.Agua:
             session.selectgraf = 'Água'
        elif formConsultA3P.vars.Energia:
             session.selectgraf = 'Energia'
        elif formConsultA3P.vars.Residuo:
             session.selectgraf = 'Resíduo'
        else:
             session.selectgraf = 'Recursos'
        session.IdPredio = request.vars.IdPredio
        session.slcAno = request.vars.slcAno
        response.flash = 'Dados Recebidos: :',str(session.IdPredio),str(session.selectgraf),str(session.slcAno) 
        redirect (URL('graficos','plotA3P'))       
    elif formConsultA3P.errors:
        response.flash = 'Erro no formulário'  
    return dict(formConsultA3P=formConsultA3P)

@auth.requires_login()
def FA3pAgua():
    formA3pAgua = SQLFORM(dbentidades.ContasAgua, submit_button='Registrar', formstyle='divs' )
    dbentidades.ContasAgua.CodSemae.requires=IS_IN_DB(dbentidades(db.Predios.CodDepto == user_dpto[0]['Idm']), 'Predios.CodAgua')
    return dict(formA3pAgua=formA3pAgua)

@auth.requires_login()
def GestaoDeEstoque():
    fields = [dbentidades.Estoque.Id, dbentidades.Materiais.Material, dbentidades.Materiais.Cod, dbentidades.Materiais.Unidade, dbentidades.Estoque.Qtd, dbentidades.Estoque.DataValidade]
    return dict(grade=SQLFORM.grid(dbentidades.Estoque.IdMaterial == dbentidades.Materiais.Id, deletable=False,
            editable=True, fields=fields))


@auth.requires_login()
def ControleDeRetiradas():
    formRetiradas = SQLFORM(ControleRetirada, submit_button='Registrar', formstyle='divs' ).process()
    
    return dict(formRetiradas=formRetiradas)


# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})






#----Queimadas-----

def mapas_focos():

    return locals()


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
    expõe:
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
    para decorar funções que precisam de controle de acesso
    Observe também que há http: //..../ [app] / appadmin / manage / auth para permitir que o administrador gerencie usuários"""
    return dict(form=auth())

# ---- ação ao conteúdo estático enviado pelo servidor (required) ---
@cache.action()
def download():
    """
    permite o download de arquivos enviados
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def Departamentos():
    form= SQLFORM(db.Dpto, submit_button='Alterar', formstyle='divs' )
    
    return dict(form=form)
    