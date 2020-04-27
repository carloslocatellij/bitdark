Cenarios = db.define_table("Cenarios",
    Field('Nome', 'string', unique=True),
    Field('Ambientacao', 'string'),
    Field('Desc_Geral', 'text'),
    Field('Img', 'upload'),
    auth.signature,
    format = '%(Nome)s',

)

Campanhas = db.define_table('Campanhas',
    Field('Nome', 'string', unique=True),
    Field('IdCenario', 'reference Cenarios'),
    Field('IdMestre', 'integer'),
    Field('Ambientacao', 'string'),
    Field('Nv_Desafio_Atual', 'integer'),
    Field('Descriçao', 'text'),
    Field('Min_Jogadores', 'integer'),
    Field('Max_jogadores', 'integer'),
    Field('Img', 'upload'),
    auth.signature,
    format = '%(Nome)s',
)

Quests = db.define_table('Quests',
	Field('Nome', 'string', unique=True),
	Field('Nivel', 'integer'),
	Field('Descriçao', 'text'),
	Field('Img', 'upload'),
    Field('Min_Jogadores', 'integer'),
    Field('Max_jogadores', 'integer'),
	auth.signature,
    format = '%(Nome)s',
)

db.define_table('CampanhaQuest',
	Field('IdCampanha', 'reference Campanhas'),
	Field('IdQuest', 'reference Quests'),

)

Personagens = db.define_table('Personagens',
    Field('Nome', 'string', unique=True),
    Field('IdRaça', 'integer'),
    Field('Sexo', 'string'),
    Field('IdClasseBase', 'integer'),
    Field('IdArquetipo', 'integer'),
    Field('IdProfissao', 'integer'),
    Field('Descriçao', 'text'),
    Field('Img', 'upload'),
	auth.signature,
    format = '%(Nome)s',

)

db.define_table('PersonagemCampanha',
	Field('IdPersonagem', 'reference Personagens'),
	Field('IdCampanha', 'reference Campanhas'),
 )

db.define_table('PersonagemQuest',
	Field('IdPersonagem', 'reference Personagens'),
	Field('IdQuest', 'reference Quests'),
 )


Classes = db.define_table('Classes',
    Field('Nome', 'string', unique=True),
    Field('AtributoBase', 'string'),
    Field('Img', 'upload'),
    auth.signature,
    format = '%(Nome)s',
)