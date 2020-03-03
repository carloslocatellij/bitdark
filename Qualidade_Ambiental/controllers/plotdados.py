# -*- coding: utf-8 -*-

#=====================================================#
###   		 SISTEMA DE VISUALIZAÇAO DE DADOS 		###
###	     		ENTRADAS DE MATERIAIS NOS 			###
###					PONTOS DE Apoio                 ###
#=====================================================#

#==### Vantagens sobre googlechart: Python puro, simplicidade, conhecimento do codigo.
#==### Desvantagem sob googlechart: Menos personalizavel, menos opçoes, nao interativo(ainda).
#==### Vantagens sobre Tk e Qt: Interface web totalmente interoperavel, facil e rapida distribuiçao, padrao MVC pronto.
#==### Desvantagem sob GUIs: desenvolvimento supostamente mais lento.

#=========================================================================================#
### 											 						   	 			###
### Atualmente em funcionamento a geraçao de um grafico em .png.		   	 			###
###  O retorno devera ir para uma tag <img src="{{=URL('plotdados','/'element'.png')}}">###
### 																	   	 			###
### how-to em http://www.web2pyslices.com/article/show/1357/matplotlib-howto 			###
#=========================================================================================#

# IMPORTAÇAO DE BIBLIOTECAS
#import pandas as pd   #lib de manipulaçao de dados p data science MAS E PESADO
#from pandas.tseries.offsets import MonthEnd # para definiçao de tempo

from plotador import * #este modulo se encontra na pasta modules . E o gerador de graficos
import datetime

esteano = datetime.date.today().year
estemes = datetime.date.today().month
estedia = datetime.date.today().day
#ummesatras = datetime.date(year=esteano, month=estemes-1, day=1)
hoje = datetime.date.today()

# CONSULTA AO BANCO DE DADOS
#df_mysql = pd.DataFrame(query.values()) SE FOR USAR PANDAS, MAS É PESAAADO
# SEM USO
# tipoVeic ={'Veic':['CARRO', 'CARROCA', 'PICKUP', 'CARRETA_P', 'CARRETA_G','OUTRO'],
# 'TipoVeic': [1, 2, 3, 4, 5, 6]}
### plotar em interface tk
# chart_type = FigureCanvasTkAgg (fig, root)
# chart_type.get_tk_widget().pack()

@cache.action(time_expire=18, cache_model=cache.disk, quick='V')
def voldia(): # Grafico de volume por dia

	if session.IdPonto:
		DadosPonto = db((EntradaPonto.Data>=datetime.date.strftime(session.Inicio, '%Y-%m-%d')) & (EntradaPonto.Data<datetime.date.strftime(session.Fim, '%Y-%m-%d')) & (EntradaPonto.IdPonto==session.IdPonto))
	else:
		DadosPonto = db((EntradaPonto.Data>=ummesatras) & (EntradaPonto.Data<hoje))

	query = DadosPonto.select(EntradaPonto.Data, EntradaPonto.Volume.sum().with_alias('Volume'), groupby=EntradaPonto.Data, orderby=EntradaPonto.Data ).as_dict()
	response.headers['Content-Type']='image/png'
	ylab = u'Vol. em metros cúbicos (m3)'
	xlab = u'dia do mês'
	title = u'Volume de resíduos por dia no {}'.format(session.pontoformat)
	(x , y) = ([], [])

	for v in query:
		x.append(datetime.date.strftime((query.values()[v]['EntradaPonto']['Data']), '%d/%m'))
	for v in query:
		y.append(int(query[v]['Volume']))
	lxy = []
	for i in zip(x,y):
		lxy.append(i)
	legendgrau = 300
	return plot( title=title, xlab=xlab, ylab=ylab,  mode='bar', data={'soma do volume informados': lxy}, legendgrau=legendgrau)

def pontores(): #Grafico de resíduos no ponto selecionado

	query = db.executesql("SELECT SUM( ( `Volume` * `Entulho` ) / ( `Moveis` + `Ferro` + `Entulho` + `PlastPapel` + `Eletron` + `Poda` ) ) AS `Entulho`, SUM( ( `Volume` * `Poda` ) / ( `Moveis` + `Ferro` + `Entulho` + `PlastPapel` + `Eletron` + `Poda` ) ) AS `Poda`, SUM( ( `Volume` * `Moveis` ) / ( `Moveis` + `Ferro` + `Entulho` + `PlastPapel` + `Eletron` + `Poda` ) ) AS `Moveis`, SUM( ( `Volume` * `Ferro` ) / ( `Moveis` + `Ferro` + `Entulho` + `PlastPapel` + `Eletron` + `Poda` ) ) AS `Ferro`,  SUM( ( `Volume` * `PlastPapel` ) / ( `Moveis` + `Ferro` + `Entulho` + `PlastPapel` + `Eletron` + `Poda` ) ) AS `Plast.Papel`, SUM( ( `Volume` * `Eletron` ) / ( `Moveis` + `Ferro` + `Entulho` + `PlastPapel` + `Eletron` + `Poda` ) ) AS `Eletron.` FROM `DBResiduos`.`UnidadeDestino` AS `UnidadeDestino`, `Tconect`.`EntradaPonto` AS `EntradaPonto` WHERE `UnidadeDestino`.`Id` = `EntradaPonto`.`IdPonto` AND `EntradaPonto`.`Data` BETWEEN '{}' AND '{}' AND `EntradaPonto`.`IdPonto` = '{}'".format(session.Inicio,session.Fim,session.IdPonto), as_dict=True)
	response.headers['Content-Type']='image/png'
	ylab = u'Vol. em metros cúbicos (m3)'
	xlab = u'resíduos'
	title = u'Volume total por resíduos no {}'.format(session.pontoformat)
	(x , y) = ([], [])

	for k, v in query[0].items():
		x.append(k)
		y.append(v)
	lxy = []
	for i in zip(x,y):
		lxy.append(i)
	legendgrau = 315
	return plot( title=title, xlab=xlab, ylab=ylab,  mode='bar', data={u'Volume por resíduo': lxy}, legendgrau=legendgrau)


def respontos(): # Grafico do volume por ponto do resíduo selecionado

	if session.Residuo == 'Entulho':
		query = db.executesql("SELECT `UnidadeDestino`.`Atividade`, SUM( ( `Volume` * `Entulho` ) / ( `Moveis` + `Ferro` + `Entulho` + `PlastPapel` + `Eletron` + `Poda` ) ) AS `Entulho` FROM `UnidadeDestino`, `EntradaPonto`  WHERE `UnidadeDestino`.`Id` = `EntradaPonto`.`IdPonto` AND `EntradaPonto`.`Data` BETWEEN '{}' AND '{}' GROUP BY `EntradaPonto`.`IdPonto`".format(session.Inicio,session.Fim), as_dict=True)
	elif session.Residuo == 'Poda':
		query = db.executesql("SELECT `UnidadeDestino`.`Atividade`, SUM( ( `Volume` * `Poda` ) / ( `Moveis` + `Ferro` + `Entulho` + `PlastPapel` + `Eletron` + `Poda` ) ) AS `Poda` FROM `UnidadeDestino`, `EntradaPonto`  WHERE `UnidadeDestino`.`Id` = `EntradaPonto`.`IdPonto` AND `EntradaPonto`.`Data` BETWEEN '{}' AND '{}' GROUP BY `EntradaPonto`.`IdPonto`".format(session.Inicio,session.Fim), as_dict=True)
	elif session.Residuo == 'Moveis':
		query = db.executesql("SELECT `UnidadeDestino`.`Atividade`, SUM( ( `Volume` * `Moveis` ) / ( `Moveis` + `Ferro` + `Entulho` + `PlastPapel` + `Eletron` + `Poda` ) ) AS `Moveis` FROM `UnidadeDestino`, `EntradaPonto`  WHERE `UnidadeDestino`.`Id` = `EntradaPonto`.`IdPonto` AND `EntradaPonto`.`Data` BETWEEN '{}' AND '{}' GROUP BY `EntradaPonto`.`IdPonto`".format(session.Inicio,session.Fim), as_dict=True)
	elif session.Residuo == 'Ferro':
		query = db.executesql("SELECT `UnidadeDestino`.`Atividade`, SUM( ( `Volume` * `Ferro` ) / ( `Moveis` + `Ferro` + `Entulho` + `PlastPapel` + `Eletron` + `Poda` ) ) AS `Ferro` FROM `UnidadeDestino`, `EntradaPonto`  WHERE `UnidadeDestino`.`Id` = `EntradaPonto`.`IdPonto` AND `EntradaPonto`.`Data` BETWEEN '{}' AND '{}' GROUP BY `EntradaPonto`.`IdPonto`".format(session.Inicio,session.Fim), as_dict=True)
	elif session.Residuo == 'Plastico/ Papel':
		query = db.executesql("SELECT `UnidadeDestino`.`Atividade`, SUM( ( `Volume` * `PlastPapel` ) / ( `Moveis` + `Ferro` + `Entulho` + `PlastPapel` + `Eletron` + `Poda` ) ) AS `Plast.Papel`FROM `UnidadeDestino`, `EntradaPonto`  WHERE `UnidadeDestino`.`Id` = `EntradaPonto`.`IdPonto` AND `EntradaPonto`.`Data` BETWEEN '{}' AND '{}' GROUP BY `EntradaPonto`.`IdPonto`".format(session.Inicio,session.Fim), as_dict=True) 
	elif session.Residuo == 'Eletronico':
		query = db.executesql("SELECT `UnidadeDestino`.`Atividade`, SUM( ( `Volume` * `Eletron` ) / ( `Moveis` + `Ferro` + `Entulho` + `PlastPapel` + `Eletron` + `Poda` ) ) AS `Eletron.` FROM `UnidadeDestino`, `EntradaPonto`  WHERE `UnidadeDestino`.`Id` = `EntradaPonto`.`IdPonto` AND `EntradaPonto`.`Data` BETWEEN '{}' AND '{}' GROUP BY `EntradaPonto`.`IdPonto`".format(session.Inicio,session.Fim), as_dict=True)
	elif session.Residuo ==  'Volume total':
		query = db.executesql("SELECT `UnidadeDestino`.`Atividade`, SUM(`Volume`) FROM `UnidadeDestino`, `EntradaPonto`  WHERE `UnidadeDestino`.`Id` = `EntradaPonto`.`IdPonto` AND `EntradaPonto`.`Data` BETWEEN '{}' AND '{}' GROUP BY `EntradaPonto`.`IdPonto`".format(session.Inicio,session.Fim), as_dict=True)
	else:
		query = 'Erro no parametro'

	response.headers['Content-Type']='image/png'
	ylab = u'Vol. em metros cúbicos (m3)'
	xlab = u'Pontos de Apoio'
	title = u'Volume de {} nos Pontos de Apoio.'.format(session.Residuo)
	(x , y) = ([], [])
	lxy = []

	for i in query:
		x.append(i['Atividade'].replace('Ponto de Apoio - ','')) #.encode('utf-8'))
		for k,v in i.items():
			if k != 'Atividade':
				if v != None:
					y.append(v)
	for i in zip(x,y):
		lxy.append(i)
	legendgrau = 340
	return plot( title=title, xlab=xlab, ylab=ylab,  mode='bar', data={u'Volume por P.A.': lxy}, legendgrau=legendgrau)