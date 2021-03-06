
import validador

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
	Field('IdUser', requires=IS_IN_DB(db, 'auth_user.id', db.auth_user._format)),
	Field('IdDepto', 'reference Dpto', required=True),
	
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
	Field ('Nome', 'string', length='115', requires = IS_UPPER(),notnull=True),
	Field ('CPF', 'string',[IS_EMPTY_OR(IS_CPF()), IS_EMPTY_OR(IS_NOT_IN_DB(dbpessoas,'Pessoas.CPF'))]),
	Field ('CNPJ', 'string', length='22',  requires=IS_EMPTY_OR(IS_NOT_IN_DB(dbpessoas,'Pessoas.CNPJ')  )),
	Field ('IdEndereco', 'list', requires=IS_EMPTY_OR(IS_IN_DB(dblocais, 'Enderecos.Id', endereco_represent))),
	Field ('Telefone', 'string', length='22'),
	Field ('celular', 'string', length='22'),
	Field ('Email', 'string', length='75'),
	Field ('Categoria', 'text', length='150'),
	format = '%(Nome)s - %(CPF)s',
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
	format = '%(Logradouro)s - %(Cep)s',
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



Obras = dbconstrucoes.define_table('Obras',
    Field('Id', 'id'),
    Field('CadMunicipal', 'string'),
    Field('Alvara', 'string'),
    Field('DataAlvara', 'date'),
    Field('IdGerador', 'integer', requires=IS_IN_DB(dbpessoas, 'Pessoas.Id', dbpessoas.Pessoas._format) ),
    Field('IdEndereco', 'list', requires=IS_EMPTY_OR(IS_IN_DB(dblocais, 'Enderecos.Id', endereco_represent))),
    Field('Finalidade', 'string'),
    Field('PrazoExec', 'decimal(7,2)'),
    Field('AreaTerreno', 'decimal(7,2)'),
    Field('AreaConstrExist', 'decimal(7,2)'),
    Field('AreaConstrDemolir', 'decimal(7,2)'),
    Field('AreaConstrExecutar', 'decimal(7,2)'),
    Field('Corte', 'decimal(7,2)'),
    Field('Aterro', 'decimal(7,2)'),
    Field('PavtosSubS', 'integer'),
    Field('PavtosSobreS', 'integer'),
    Field('Nquartos', 'integer'),
    Field('Edicula', 'integer', requires= validador.IS_CHKBOX01(on=1, off=0) ,widget=SQLFORM.widgets.boolean.widget),
    Field('Piscina', 'integer', requires= validador.IS_CHKBOX01(on=1, off=0) ,widget=SQLFORM.widgets.boolean.widget),
    Field('CobertMetalica', 'integer', requires= validador.IS_CHKBOX01(on=1, off=0) ,widget=SQLFORM.widgets.boolean.widget),
    Field('MadeiraReflorest', 'integer', requires= validador.IS_CHKBOX01(on=1, off=0) ,widget=SQLFORM.widgets.boolean.widget),
    format = '%(CadMunicipal)s - %(Alvara)s',
    migrate=False
    )

DofsObra = dbconstrucoes.define_table('DofsObra',
    Field('IdDof','string', 'primarykey',  ),
    Field('IdObra', 'integer', requires=IS_IN_DB(dbconstrucoes, 'Obras.Id', dbconstrucoes.Obras._format)),
    fake_migrate = 'True',
    migrate='False'
    )


servicos = [(1 , 	'AUTORIZAÇÃO DE PODA'),(2 , 'AUTORIZAÇÃO DE ERRADICAÇÃO'),(3 , 'HABITE-SE'),(4 , 'PGRCC'),(5 , 'MOVIMENTAÇÃO DE SOLO'),(6 , 'ATIVIDADE MINERARIA'),(7 , 'ANÁLISE ARBÓREA'),(8 , 'PARECER AMBIENTAL'),(9 , 'OFÍCIO')	,(10 , 'INTERNO'),(11 , 'MEMORANDO'),(12 , 'SOLICITAÇÃO DE COMPRA'),(13 , 'RECONSIDERAÇÃO HABITE-SE'),(14 , 'RECONSIDERAÇÃO PGRCC')]
import datetime
Processos = dbdocumentos.define_table('Processos',
    Field('Protocolo', 'integer', 'primarykey ',readable=True, writable=True,),
    Field('IdPessoa',  requires=IS_IN_DB(dbpessoas, 'Pessoas.Id', dbpessoas.Pessoas._format), Label='Requerente' ),
    Field('DataReg', 'datetime', readable=False, default=datetime.datetime.now() ),
    Field('IdDpto', 'integer', requires=IS_IN_DB(db, 'Dpto.Idm', db.Dpto._format), default=1024412 ,Label='Dpto'),
    Field('IdTipo', 'integer', requires = IS_IN_SET(servicos), Label='Tipo' ),
    Field('Assunto', 'string', readable=False, writable=False),
    Field('IdCateg', 'integer', readable=False, writable=False),
    
    #fake_migrate=True,
    migrate=True
)

dbdocumentos.Processos.Protocolo.represent = lambda Protocolo, row: row.id

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
    auth.signature,
    format = '%(Titulo)s',
    migrate=True,
    )

db.A3pDica.Titulo.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, 'A3pDica.Titulo')]
