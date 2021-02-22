# -*- coding: utf-8 -*-

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
