#!/usr/bin/python3.8
# -*- coding: utf-8 -*-

#=====================================================#
###     	SISTEMA DE GESTÃO DA QUALIDADE DO AR    ###              
#=====================================================#


def QA_inicio():

	ItensPlanoQualidadeAr = {'QualidadeAr':['Formulario_opacidade', 'Emissões Moveis'], 'Mobilidade':'', 'Queimadas': ['Urbanas', 'Rurais'], 'Clima':'', 'Produção_e_Consumo':'' }
	
	return dict(sistema=T('Sistema de Dados de Qualidade do Ar!'), ItensPlanoQualidadeAr = ItensPlanoQualidadeAr)



def Formulario_opacidade():
	form = SQLFORM( db.MedicoesOpac, formstyle='table3cols', editable=True)
	
	if form.process().accepted:
		response.flash = 'Registrado'

	elif form.errors:
		response.flash = 'Ocorreu um erro no registro'

	else:
		response.flash = 'Preencher valores indicados'
		
		return dict(form=form)


		
def Grade_opacidade():
	grid = SQLFORM.smartgrid(db.MedicoesOpac, fields=[db.MedicoesOpac.ID, db.MedicoesOpac.PM, db.MedicoesOpac.Placa,  db.MedicoesOpac.Data , db.MedicoesOpac.Hora, db.MedicoesOpac.NvRingelmann]\
		,editable=True, deletable=False, orderby=~db.MedicoesOpac.ID , field_id=db.MedicoesOpac.ID \
		,links = dict(header='ID',body= lambda ids : URL('QualidadeAr', 'Formulario_opacidade', Id=ids)))
	return locals() #dict(grid=grid)