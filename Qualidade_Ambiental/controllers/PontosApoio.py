#!/usr/bin/python3.8
# -*- coding: utf-8 -*-

#=====================================================#
###           SISTEMA DE VISUALIZAÇAO DE DADOS     ###
###	     		ENTRADAS DE MATERIAIS NOS 			###
###					PONTOS DE Apoio                 ###
#=====================================================#


@auth.requires_login()
@cache.action(time_expire=180, cache_model=cache.ram, quick='VS')
def Pontos_de_Apoio():
	response.flash = T("Bem Vindo!")
	return response.render(dict(message=T('Sitema Web do Dept. de Qualidade Ambiental')))

@auth.requires_login()
def grafico_por_ponto():
	import datetime
	import plotador
	ctrlgrf = SQLFORM.factory(
		Field('IdPonto',db.EntradaPonto.IdPonto, label='Ponto', requires=IS_IN_DB(db((db.UnidadeDestino.Tipo=='Ponto de Apoio')) , 'UnidadeDestino.Id', db.UnidadeDestino._format)),
		Field('Inicio', label='Inicio', type='date', requires= IS_DATE_IN_RANGE(format=T('%d/%m/%Y'),minimum=datetime.date(2019, 6, 1), maximum=datetime.date.today(), error_message='deve ser ANO-Mês-Dia valido!'),),
		Field('Fim', label='Fim', type='date', requires=IS_DATE_IN_RANGE(format=T('%d/%m/%Y'),minimum=datetime.date(2019, 6, 1), maximum=datetime.date.today(), error_message='deve ser ANO-Mês-Dia valido!'),),
		table_name='EntradaPonto',
		formstyle='table3cols',
		buttons = [INPUT(_name='Gerar', _class='btn btn-primary btn-lg',_type="submit", value='Gerar', _value="Gerar", _onclick="this.form.action.value=Gerar;this.form.submit()")])

	if ctrlgrf.process().accepted:
		session.IdPonto = ctrlgrf.vars.IdPonto
		session.pontoformat = db(UnidadeDestino.id == session.IdPonto).select(UnidadeDestino.Atividade).as_list()
		session.pontoformat = session.pontoformat[0]['Atividade']
		session.Inicio = ctrlgrf.vars.Inicio
		session.Fim = ctrlgrf.vars.Fim
		response.flash = 'Exibindo dados para: ',str(session.pontoformat),str(session.Inicio),str(session.Fim)
	elif ctrlgrf.errors:
		response.flash = 'Erro no formulario'

	return dict(ctrlgrf=ctrlgrf)

@auth.requires_login()
def Relatorio_dos_Pontos_de_Apoio():
	import datetime
	ctrlrelat = SQLFORM.factory(
		Field('Inicio', label='Inicio', type='date', requires= IS_EMPTY_OR(IS_DATE_IN_RANGE(format=T('%d/%m/%Y'),minimum=datetime.date(2019, 6, 1), maximum=datetime.date.today(), error_message='deve ser no formato DD/MM/AAAA!'))),
		Field('Fim', label='Fim', type='date', requires= IS_EMPTY_OR(IS_DATE_IN_RANGE(format=T('%d/%m/%Y'),minimum=datetime.date(2019, 6, 1), maximum=datetime.date.today(), error_message='deve ser no formato DD/MM/AAAA!'))),
		table_name='EntrPonto',
		formstyle='divs',
		buttons = [INPUT(_name='Gerar', _class='btn btn-primary btn-lg',_type="submit", value='Gerar', _value="Consulta", _onclick="this.form.action.value=Gerar;this.form.submit()")])

	if ctrlrelat.process().accepted:
		session.Inicio = ctrlrelat.vars.Inicio
		session.Fim = ctrlrelat.vars.Fim
		response.flash = 'Exibindo dados para: ',str(session.Inicio),str(session.Fim)
	elif ctrlrelat.errors:
		response.flash = 'Erro no formulário'

	if session.Inicio and session.Fim:

		query = db((EntradaPonto.Data>=session.Inicio) & (EntradaPonto.Data<=session.Fim) & (EntradaPonto.IdPonto == UnidadeDestino.Id))
	else:
		query = db(EntradaPonto.IdPonto == UnidadeDestino.Id)

	datamin = query.select(EntradaPonto.Data.min()).as_dict()
	datamax = query.select(EntradaPonto.Data.max()).as_dict()

	filds = ['Entulho', 'Poda', 'Moveis', 'Ferro', 'PlastPapel', 'Eletron' ]
	columns = ['Atividade', 'Volume_m3' ,'Entulho_m3', 'Poda_m3', 'Moveis_m3', 'Ferro_m3', 'PlastPapel_m3', 'Eletron_m3', 'Sofa_un', 'Colchão_un' ]
	columnsT = [ 'Volume_m3' ,'Entulho_m3', 'Poda_m3', 'Moveis_m3', 'Ferro_m3', 'PlastPapel_m3', 'Eletron_m3', 'Sofa_un', 'Colchão_un' ]
 	sqlquery = ''
	for f in filds:
		sqlquery = sqlquery+',ROUND(SUM( ( `Volume` * `{}` ) / ( `Moveis` + `Ferro` + `Entulho` + `PlastPapel` + `Eletron` + `Poda` ) ),2) AS `{}`'.format(f,f)

	sqlstrpponto = "SELECT `UnidadeDestino`.`Atividade` as `Atividade`, SUM(`Volume`) as `Volume` {}, SUM(`Sofa`), SUM(`Colchão`) FROM `UnidadeDestino`, `EntradaPonto`  WHERE `UnidadeDestino`.`Id` = `EntradaPonto`.`IdPonto` AND `EntradaPonto`.`Data` BETWEEN '{}' AND '{}' GROUP BY `EntradaPonto`.`IdPonto`".format( sqlquery,session.Inicio,session.Fim)
	sqlstrT = "SELECT SUM(`Volume`) as `Volume` {} , SUM(`Sofa`), SUM(`Colchão`) FROM `UnidadeDestino`, `EntradaPonto`  WHERE `UnidadeDestino`.`Id` = `EntradaPonto`.`IdPonto` AND `EntradaPonto`.`Data` BETWEEN '{}' AND '{}'".format( sqlquery,session.Inicio,session.Fim)

	ConsultaPPonto =  db.executesql(sqlstrpponto)
	ConsultaSomaPontos = db.executesql(sqlstrT)

	return response.render(dict( ctrlrelat=ctrlrelat ,columns=columns, columnsT=columnsT,\
	 querysql=ConsultaPPonto , somaRelatPontos=ConsultaSomaPontos, datamin=datamin[0]['_extra']['MIN(`EntradaPonto`.`Data`)'],\
	 datamax=datamax[0]['_extra']['MAX(`EntradaPonto`.`Data`)']))

@auth.requires_login()
@cache.action(time_expire=30, cache_model=cache.ram, quick='VP')
def relatorio_de_placas():
	ctrlplaca = SQLFORM.factory(
		#Field('IdPonto',db.EntradaPonto.IdPonto, label='Ponto'),
		Field('Placa',db.EntradaPonto.IdPonto, label='Placa'),
		formstyle='divs',
		buttons = [INPUT(_name='Consulta', _class='btn btn-primary btn-lg',_type="submit", value='Gerar', _value="Gerar", _onclick="this.form.action.value=Gerar;this.form.submit()")])
	placa = None
	columns = []
	if ctrlplaca.process().accepted:
		placa = ctrlplaca.vars.Placa
		response.flash = 'Exibindo dados para: ',str(placa)
	elif ctrlplaca.errors:
		response.flash = 'Erro no formulário'

	if placa != None:
		query = db((EntradaPonto.IdPonto == UnidadeDestino.Id) & (EntradaPonto.Placa.contains(str(ctrlplaca.vars.Placa))) )
		grdRelatPlaca = query.select(
			EntradaPonto.Placa.with_alias('Placa'),
			EntradaPonto.Data.with_alias('Data'),
			EntradaPonto.Volume.with_alias('Volume_m3'),
			EntradaPonto.Entulho.with_alias('Entulho_viagens'),
			EntradaPonto.Poda.with_alias('Poda_viagens'),
			EntradaPonto.Sofa.with_alias('Sofa_un'),
			EntradaPonto.Colchao.with_alias('Colchão_un'),
			UnidadeDestino.Atividade.with_alias('Ponto'),			
			orderby= ~EntradaPonto.Data | EntradaPonto.Volume )

	elif placa == None:
		#query = db((EntradaPonto.IdPonto == UnidadeDestino.Id) & (~EntradaPonto.Placa.contains('###')) )
		columns = ['Placa', 'Volume_m3' ,'Entulho_viagens', 'Poda_viagens', 'Sofa_(un)', 'Colchão_(un)']
		grdRelatPlaca = db.executesql(
"SELECT `EntradaPonto`.`Placa` as `Placa`, SUM(COALESCE(`EntradaPonto`.`Volume`, 0 )) as `Volume`, SUM(COALESCE(`EntradaPonto`.`Entulho`, 0 )) as `Entulho`, SUM(COALESCE(`EntradaPonto`.`Poda`, 0 )) as `Poda`,  SUM(COALESCE(`EntradaPonto`.`Sofa`, 0)) as `Sofa` , SUM(COALESCE(`EntradaPonto`.`Colchão`, 0 )) as `Colchao` FROM `EntradaPonto`, `UnidadeDestino`  WHERE `UnidadeDestino`.`Id` = `EntradaPonto`.`IdPonto` GROUP BY `EntradaPonto`.`PLaca` ORDER BY `EntradaPonto`.`Volume` DESC LIMIT  200 "
			)

	return response.render(dict(grdRelatPlaca=grdRelatPlaca, ctrlplaca=ctrlplaca, columns = columns, placa = placa))


@auth.requires_login()
def FormEntradaPonto():
	if session.campospersits:
		for k in session.campospersits:
			db['EntradaPonto'][k].default = session.campospersits[k]
		form = SQLFORM( db.EntradaPonto ,formstyle='table3cols', editable=True)
		#form.Placa.upper()

	else:
		form = SQLFORM( db.EntradaPonto ,formstyle='table3cols', editable=True)


	if form.process().accepted:
		itenresiduo = []
		for k, v in request.vars.items():
			if v == 'on':
				itenresiduo.append(k)
			if k == 'Outros' and v != None:
				itenresiduo.append(v)

		response.flash = 'REGISTRADO! \t - {} ,  {} ,  {}m³, {} '.format(request.vars.Placa, request.vars.Data, request.vars.Volume, str(itenresiduo))
		session.campospersits={'IdPonto':form.vars.IdPonto,'Data':form.vars.Data}
		#redirect(URL('FormEntradaPonto', args=form.vars.id))
	elif form.errors:
		response.flash = 'Ocorreu um erro no registro'
	else:
		response.flash = 'Preencher campos'

	return dict(form=form)

@auth.requires_login()
def GridEntradaPonto():
	grid = SQLFORM.smartgrid(db.EntradaPonto, fields=[db.EntradaPonto.Placa,  db.EntradaPonto.Data , db.EntradaPonto.IdPonto] \
		,editable=True, deletable=True, orderby=~db.EntradaPonto.Id , field_id=db.EntradaPonto.Id \
		,links = dict(header='Placa',body= lambda ids : A(URL('PontosApoio', 'GridEntradaPonto', Placa=ids))), user_signature=False)
	return locals() #dict(grid=grid)

@auth.requires_login()
def grafico_por_residuo():
	import datetime
	import plotador
	ctrlresiduo = SQLFORM.factory(
		Field('Residuo', requires=IS_IN_SET(['Volume total', 'Entulho', 'Poda','Moveis', 'Ferro', 'Plastico/ Papel', 'Eletronico' ]), label=u'Resíduo'),
		Field('Inicio', label='Inicio', type='date', requires= IS_DATE_IN_RANGE(format=T('%Y-%m-%d'),minimum=datetime.date(2019, 6, 1), maximum=datetime.date.today(), error_message='deve ser YYYY-MM-DD!')),
		Field('Fim', label='Fim', type='date', requires=IS_DATE_IN_RANGE(format=T('%Y-%m-%d'),minimum=datetime.date(2019, 6, 1), maximum=datetime.date.today(), error_message='deve ser YYYY-MM-DD!')),
		table_name='EntrResiduo',
		formstyle='table3cols',
		buttons = [INPUT(_name='Gerar', _class='btn btn-primary btn-lg',_type="submit", value='Gerar', _value="Gerar", _onclick="this.form.action.value=Gerar;this.form.submit()")])
	if ctrlresiduo.process().accepted:
		session.Residuo = ctrlresiduo.vars.Residuo
		session.Inicio = ctrlresiduo.vars.Inicio
		session.Fim = ctrlresiduo.vars.Fim
		response.flash = 'Exibindo dados para: ',str(session.Residuo),str(session.Inicio),str(session.Fim)
	elif ctrlresiduo.errors:
		response.flash = 'Erro no formulário'

	
	return response.render(dict(ctrlresiduo=ctrlresiduo, ))
