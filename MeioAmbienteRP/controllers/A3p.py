# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------------------------------------------------
# Gera os mecaninsmos de controle da página da A3p
# ----------------------------------------------------------------------------------------------------------------------
#As funções sem argumentos são definições de páginas e contem o algoritimo provedor dos dados da página
# -------------------------------------------------------------------------


user_dpto = db(db.UserDpto.IdUser == auth.user_id).select(db.UserDpto.IdDepto)
@auth.requires_login()
def FConsultA3P():
    formConsultA3P = SQLFORM.factory(Field('IdPredio',db.Predios, requires=IS_IN_DB(db(db.Predios.CodDepto == user_dpto[0]['IdDepto']), 'Predios.Id', '%(Predio)s'), label='Local'),
                                     # Field('selectgraf',label='Segmento A3P',requires=IS_IN_SET(['Energia','Água','Resíduo', 'Recursos'])),
                                     Field('slcAno', label='Ano', requires=IS_IN_SET(['2016','2017','2018','2019'])),
                            table_name='ConsultA3p',
                            formstyle='bootstrap',
                            buttons = [INPUT(_name='Agua', _class='btn btn-primary btn-lg',_type="submit", value='Água', _value="Água", _onclick="this.form.action.value=Água;this.form.submit()"),
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
    formA3pAgua = SQLFORM(db.ContasAgua, submit_button='Enviar')
    db.ContasAgua.CodSemae.requires=IS_IN_DB(db(db.Predios.CodDepto == user_dpto[0]['IdDepto']), 'Predios.CodAgua')
    return dict(formA3pAgua=formA3pAgua)





def Dicas():
    dicas = db().select(db.A3pDicas.id, db.A3pDicas.Titulo,db.A3pDicas.Tags, orderby=db.A3pDicas.Titulo)
    Rtags = db().select(db.Tags.id, db.Tags.Tag)
    dtag = {}
    combtag = []
    tagdica = []
    for row in range(0 ,len(Rtags)-1):
        combtag = combtag + list((Rtags[row]['Tag'].split()))
    for row in dicas:
        tagdica = tagdica + list(db.A3pDicas.Tags.represent(row.Tags).split())
    for t in combtag:
        for tt in tagdica:
            if t != tt:
                dtag[t] = 1
            else:
                dtag[t] = dtag[t]*2
    
    return dict(dicas=dicas, dtag=dtag)


@auth.requires_login()
def PostaDica():
    """Cria um Post de Dica"""
    form = SQLFORM(db.A3pDicas).process(next=URL('Dicas'))
    return dict(form=form)

def MostraDica():
    """Mostra dica postada"""
    dica = db(db.A3pDicas.id==request.args(0, cast=int)).select(A3pDicas.Titulo, A3pDicas.Tags , A3pDicas.body, A3pDicas.created_by ,A3pDicas.created_on ) or redirect(URL('Dicas'))
#     ntag = db(db.A3pDicas).select(db.A3pDicas.Tags)
    combtag = []
    dtag = {}
    for row in dica:
            combtag = combtag + list(db.A3pDicas.Tags.represent(row.Tags).split())
    for t in combtag:
        if t not in dtag:
            dtag[t] = 1
        else:
            dtag[t] = dtag[t] +1
    tg = (dica[0])
    tags = db.A3pDicas.Tags.represent(tg.Tags).replace(',','')
    Titulo = dica[0]['Titulo']
    body = dica[0]['body']
    autor = db.A3pDicas.created_by.represent(dica[0].created_by)
    datapost = dica[0]['created_on']
    return dict(Titulo=Titulo, body=body, autor=autor, datapost=datapost, tags=tags.split(), combtag=combtag ,dtag=dtag)

@auth.requires_login()
def EditaDica():
    """edita uma dica existente"""
    this_page = db.A3pDicas(request.args(0, cast=int)) or redirect(URL('Dicas'))
    form = SQLFORM(db.A3pDicas, this_page, deletable=True).process(
        next = URL('MostraDica', args=request.args))
    return dict(form=form)

def busca():
    """API de Busca Ajax"""
    return dict(form=FORM(INPUT(_id='keyword',
                                _name='keyword',
                                _onkeyup="ajax('callback', ['keyword'], 'target');")),
                target_div=DIV(_id='target'))


def callback():
    """A chamada de procedimento Ajax que returna a <ul> do links para as dicas"""
    query = db.A3pDicas.Titulo.contains(request.vars.keyword)
    dicas = db(query).select(orderby=db.A3pDicas.Titulo)
    links = [A(p.Titulo, _href=URL('MostraDica', args=p.id)) for p in dicas]
    return UL(*links)

def noticias():
    """gerador de rss feed do blog"""
    response.generic_patterns = ['.rss']
    pages = db().select(db.A3pDicas.ALL, orderby=db.A3pDicas.Titulo)
    return dict(title='feed de notícias A3p',
                link='https://127.0.0.1:8000/MeioAmbienteRP/A3p/Dicas',
                description='A3p news',
                created_on=request.now,
                items=[dict(Titulo=row.Titulo,
                            link=URL('Dicas', args=row.id, scheme=True, host=True, extension=False),
                            description=MARKMIN(row.body).xml(),
                            created_on=row.created_on) for row in pages])
