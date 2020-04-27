# -*- coding: utf-8 -*-

dbdocumentos = DAL('mysql://DBGrnt:,.~~Grnt861@10.7.0.28/DBDocumentos', pool_size=configuration.get('db.pool_size'), migrate_enabled=configuration.get('db.migrate'))

dbentidades = DAL('mysql://DBGrnt:,.~~Grnt861@10.7.0.28/DBEntidades', pool_size=configuration.get('db.pool_size'), migrate_enabled=configuration.get('db.migrate'))

dbpessoas = DAL('mysql://DBGrnt:,.~~Grnt861@10.7.0.28/DBPessoas', pool_size=configuration.get('db.pool_size'), migrate_enabled=configuration.get('db.migrate'))

#dba3p = DAL('mysql://DBGrnt:,.~~Grnt861@10.7.0.28/DBA3P',  migrate_enabled=configuration.get('db.migrate'))

dbconstrucoes = DAL('mysql://DBGrnt:,.~~Grnt861@10.7.0.28/DBConstrucoes',  migrate_enabled=configuration.get('db.migrate'))

dblocais = DAL('mysql://DBGrnt:,.~~Grnt861@10.7.0.28/DBLocais', pool_size=configuration.get('db.pool_size'), migrate_enabled=configuration.get('db.migrate'))

db = DAL('mysql://DBGrnt:,.~~Grnt861@10.7.0.28/Tconect',  migrate_enabled=True)

#dbentidades = DAL('mysql://DBGrnt:,.~~Grnt861@10.7.0.28/dbentidades',  migrate_enabled=configuration.get('db.migrate'))

#BANCO ENTIDADES

Materiais = dbentidades.define_table ('Materiais',
	Field ('Id', 'id', required=True),
	Field ('IdCat', 'integer', required=True),
	Field ('IdSub', 'integer', required=True),
	Field ('Cod', 'integer', required=True),
	Field ('Material', 'text', required=True),
	Field ('Unidade', 'text', length=40),
	format = '%(Material)s',
	migrate = False	)
dbentidades.Materiais.Id.writable = dbentidades.Materiais.Id.readable = False


Estoque = dbentidades.define_table('Estoque',
	Field('Id', 'id'),
	Field('IdMaterial', 'reference Materiais', requires=IS_IN_DB(dbentidades, 'Materiais.Id', dbentidades.Materiais._format)),
	Field('Qtd', 'decimal(10,2)'),
	Field('IdLocal', 'integer'),
	Field('DataValidade', 'date'),
	Field('DataReg', 'datetime'),
	format = '%(IdMaterial)s',
	migrate=False
	)
dbentidades.Estoque.Id.writable = dbentidades.Estoque.Id.readable = False


Predios = db.define_table ('Predios',
	Field('Id', 'id'),
	Field('Predio', 'text', length=75, required=True),
	Field('CodEnergia', 'integer'),
	Field('CodAgua', 'integer'),
	Field('CodDepto', 'reference Dpto', required=True),
	format = '%(Predio)s',
	migrate = False)

db.Predios.Id.writable = db.Predios.Id.readable = False

Dpto = db.define_table('Dpto', 
	Field('Departamento', 'string', required=True),
	Field('Idm', 'integer'),
	Field('Orgao', 'reference Dpto',  ),
	Field('Telefone', 'string'),
	primarykey= ['Idm'], 
	format='%(Departamento)s',
	migrate=False)

db.Dpto.Orgao.requires=IS_IN_DB(db, 'Dpto.Idm', db.Dpto._format)
#Campos Obrigatório para Pessoas


UserDpto = db.define_table('UserDpto',
	Field('id','id'),
	Field('IdUser', 'integer'),
	Field('IdDepto', 'integer'),
	
	)


#BANCO A3P

ContasEnergia = dbentidades.define_table ('ContasEnergia',
	Field('Id', 'id'),
	Field('CodCPFL', 'integer'),
	Field('Mes', 'date', required=True),
	Field('Valor', 'decimal(10,2)', required=True),
	Field('Kwh','integer', required=True),
	migrate = False
	)

ContasAgua = dbentidades.define_table ('ContasAgua',
	Field('Id', 'id'),
	Field('CodSemae', 'integer'),
	Field('Data', 'date', required=True),
	Field('NDias', 'integer'),
	Field('Consumo', 'integer', required=True),
	Field('Valor', 'decimal(7,2)'),
	migrate= False
	)


A3pLixos = dbentidades.define_table('A3pLixos', 
	Field('Id', 'id'),
	Field('IdPredio', 'integer', requires=IS_IN_DB(dbentidades, 'Predios.Id', db.Predios._format)),
	Field('Data', 'date'),
	Field('Tipo', 'list:text', requires=IS_IN_SET(['Rec','Org'])),
	Field('Qtd', 'decimal(7,2)'),
	migrate=False
	)


#BANCO PESSOAS

def endereco_represent(row):
	endereco = dblocais( (dblocais.Enderecos.Id == row.id) & (dblocais.Enderecos.IdLogradouro == dblocais.Logradouros.Id )).select(dblocais.Logradouros.Logradouro, dblocais.Enderecos.Num).first()
	pessoa_end = endereco.Logradouros.Logradouro + ', ' + str(endereco.Enderecos.Num)
	return pessoa_end

from validador import IS_CPF
Pessoas = dbpessoas.define_table ('Pessoas',
	Field ('Id', 'id'),
	Field ('Idm', 'integer' ,readable=False),
	Field ('Nome', 'string', length='115', notnull=True),
	Field ('CPF', 'string',requires=IS_CPF()),
	Field ('CNPJ', 'string', length='22'),
	Field ('IdEndereco', 'list', requires=IS_IN_DB(dblocais, 'Enderecos.Id', endereco_represent)),
	Field ('Telefone', 'string', length='22'),
	Field ('celular', 'string', length='22'),
	Field ('Email', 'string', length='75'),
	Field ('Categoria', 'text', length='150'),
	format = '%(Nome)s',
	migrate = False
	)

#BANCO DOCUMENTOS



#BANCO LOCAIS
Cidades = dblocais.define_table ('Cidades',
	Field ('Cidade', 'string'),
	Field ('CEP', 'integer'),
	Field ('Id', 'id'),
	format = '%(Cidade)s',
	migrate = False)

Bairros = dblocais.define_table ('Bairros',
   	Field ('Id', 'id'),
   	Field ('Bairro', 'string'),
   	Field ('Cor', 'string', IS_IN_SET(['VERDE', 'LARANJA','AMARELA','AZUL'])),
   	Field ('IdCidade', 'reference Cidades'), 		
	Field ('Regiao', 'integer'),
	format = '%(Bairro)s',
	migrate = False)

Logradouros = dblocais.define_table ('Logradouros',
	Field ('Logradouro', 'string'),
	Field ('Cep', 'integer'),
	Field ('Id', 'id'),
	Field ('Denominacao', 'list:string', IS_IN_SET(['RUA','ALAMEDA','AVENIDA','ESTRADA','PRAÇA','RODOVIA','TRAVESSA',
'VIA','ALAMENDA','ESTR. MUN.'])),
	Field ('Prefixo', 'list:string', IS_IN_SET(['','DR.','COM.','GOV.','PRES.','PE.','CAP.','CEL.','DRA.','GAL.','PROF.','MAJ.','MISSIO','PAST',
'PAST.','SGTO.','FREI','BRIG.','IRMÃ','TEN.','PROFA.','SARG.','SRA.'])),
	Field ('No', 'integer'),
	Field ('NoInicial','integer'),
	Field ('NoFinal', 'integer'),
	Field ('Lado','boolean'),
	Field ('Complemento', 'string'),
	Field ('IdBairro', 'reference Bairros'),
	Field ('IdCidade', 'reference Cidades'),
	format = '%(Logradouro)s',
	migrate = False)

Enderecos = dblocais.define_table ('Enderecos',
	Field ('Id', 'id'),
	Field ('IdLogradouro', 'reference Logradouros', dblocais.Logradouros._format),
	Field ('Num', 'integer'),
	Field ('Quadra', 'string', length='8'),
	Field ('Lote', 'string', length='8'),
	Field ('Tipo', 'string', IS_IN_SET(['-','BL.','FRENTE','ESQ.','FUNDO','SL.','N','ANDAR','LJ.','CASA','MARJ.'])),
	Field ('Complemento', 'string', length='18'),
	Field ('TipoB', 'string', IS_IN_SET(['-','BL.','FRENTE','ESQ.','FUNDO','SL.','N','ANDAR','LJ.','CASA','MARJ.'])),
	Field ('ComplementoB', 'string', length='18'),
	migrate = False)






def estoque_represent(row):
    material = dbentidades( (dbentidades.Estoque.id == row.id) & (dbentidades.Materiais.Id == dbentidades.Estoque.IdMaterial)).select(dbentidades.Materiais.Material).first()

    
    return material.Material


#qEstoqMat = dbentidades(dbentidades.Estoque.IdMaterial == dbentidades.Materiais.Id).select(dbentidades.Materiais.Material)
ControleRetirada = dbdocumentos.define_table ('ControleRetirada',
	Field('Id', 'id'),
	Field('IdEstoque', 'list', requires=IS_IN_DB(dbentidades, 'Estoque.Id', estoque_represent)),
	Field('Qtd', 'decimal(10,2)'),
	Field('DataReg', 'datetime'),
	Field('IdPessoa', 'integer', requires=IS_IN_DB(dbpessoas, 'Pessoas.Id', dbpessoas.Pessoas._format)),
	Field('Uso', 'text', length='512'),
	Field('QtdDevolvido', 'decimal(8,2)'),
	migrate = False)




ListasCompra = dbdocumentos.define_table ('ListasCompra',
	Field ('Id', 'id'),
	Field ('Protocolo', 'integer'),
	Field ('IdMaterial', 'integer', requires=IS_IN_DB(dbentidades, 'Materiais.Id', dbentidades.Materiais._format)),
	Field ('Qtd', 'integer'),
	Field ('DataReg', 'datetime'),
	migrate = False
	)

dbdocumentos.ListasCompra.Id.writable = dbdocumentos.ListasCompra.Id.readable = False


#BANCO CONSTRUCOES

MadeirasDof = dbconstrucoes.define_table ('MadeirasDof',
	Field('Id', 'id'),
	Field('IdDof', 'text', length=19, required=True),
	Field('Item', 'decimal(2,0)',required=True),
	Field('Produto', 'text', length=45, required=True),
	Field('Especie', 'text', length=55, required=True),
	Field('Popular', 'text', length=35, required=True),
	Field('Qtd', 'decimal(7,4)',required=True ),
	Field('Unidade', 'text', length=2, required=True),
	Field('Valor', 'text', length=10, required=True),
	migrate=False)
					


#---------------------------------------------------------------------------------
# BLOG DA A3P - tabelas do blog A3P
#---------------------------------------------------------------------------------

from plugin_ckeditor import CKEditor
ckeditor = CKEditor(db)
ckeditor.define_tables()

Tags = db.define_table ('Tags',
    Field ('Tag', 'string', length='20', required=True),
    format = '%(Tag)s',
    migrate=False
    )

A3pDica = db.define_table ('A3pDica',
    Field ('Titulo', 'string'),
    Field ('body', 'text', widget=ckeditor.widget),
    Field ('Tags', 'list:reference Tags'),
    #auth.signature,
    format = '%(Titulo)s',
    migrate=True,
    )

db.A3pDica.Titulo.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, 'A3pDica.Titulo')]
