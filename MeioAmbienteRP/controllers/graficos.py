# -*- coding: ISO-8859-1 -*-


def graficos():
    """usado com a visualização .load para criar um gráfico do google. Como isso é usado em uma visualização LOAD, os parâmetros são retornados do navegador como vars na URL. As vars complulsory incluem: 'type', uma string que define o chart_type 'data_url', que é uma URL da função que retorna os dados a serem colocados no gráfico. O uso na visão é assim (incluindo um exemplo de URL de dados
    {{data_url = URL ('plugin_google_chart', 'plugin_return_data.json', user_signature = True)}}
    ... {{= LOAD ('plugin_google_chart', 'plugin_google_chart.load', ajax = True,  user_signature = True, vars = {'tipo': 'bar', 'data_url': data_url})}} """
    chart_type = request.vars.type
    data_url = request.vars.data_url
    options_dict = request.vars.options_dict or ''
    if chart_type and data_url:
        return dict(chart_type=chart_type,data_url=data_url,
                    options_dict=options_dict)
    else:
        return dict()

def return_data():
    """Esta é uma função de exemplo para retornar uma matriz codificada em JSON para o plug-in de gráfico do Google.
    O URL deve ter um sufixo .json. Isso também pode usar o @ auth.requires_signature () decorator
    data = [['Year','Sales','Expenses'],["2004",1000,400],["2005",1100,440],["2006",1200,600],["2007",1500,800],["2008",1600,850],["2009",1800,900]]
    return dict(data=data)   """
    
    mes_ext = {1: 'jan', 2 : 'fev', 3: 'mar', 4: 'abr', 5: 'mai', 6: 'jun', 7: 'jul', 8: 'ago', 9: 'set', 10: 'out', 11: 'nov', 12: 'dez'}

    #queryEnegIdm = db((db.ContasEnergia.CodCPFL == db.Predios.CodEnergia) & (db.ContasEnergia.Mes >= '2017/01/01' ) ).iterselect(db.ContasEnergia.CodCPFL, db.ContasEnergia.Mes, db.ContasEnergia.Kwh)

    if session.selectgraf == 'Energia':
        rows = dbentidades(((dbentidades.ContasEnergia.CodCPFL == db.Predios.CodEnergia) & (db.Predios.Id == session.IdPredio)) & (dbentidades.ContasEnergia.Mes >= session.slcAno+'/01/01') & (dbentidades.ContasEnergia.Mes <= session.slcAno+'/12/01' ) ).iterselect(dbentidades.ContasEnergia.CodCPFL, dbentidades.ContasEnergia.Mes, dbentidades.ContasEnergia.Kwh)
        data = [['Mes', 'Kwh']]
        rlist = []
        for row in rows:
            #cod = row.CodCPFL
            mes = row.Mes
            kw = row.Kwh
            #rlist.append((cod))
            mesext = mes_ext[mes.month]
            rlist.append((mesext))
            rlist.append((kw))
            data.append(rlist)
            rlist = []   
    elif session.selectgraf == 'Água' :
        rows = dbentidades(((dbentidades.ContasAgua.CodSemae == db.Predios.CodAgua) & (db.Predios.Id == session.IdPredio)) & (dbentidades.ContasAgua.Data >= session.slcAno+'/01/01' ) & (dbentidades.ContasAgua.Data <= session.slcAno+'/12/01' )  ).iterselect(dbentidades.ContasAgua.CodSemae, dbentidades.ContasAgua.Data, dbentidades.ContasAgua.Consumo)
        data = [['Mes', 'Consumo']]
        rlist = []
        for row in rows:
            mes = row.Data
            Cons = row.Consumo
            mesext = mes_ext[mes.month]
            rlist.append((mesext))
            rlist.append((Cons))
            data.append(rlist)
            rlist = [] 
    elif session.selectgraf == 'Resíduo' :
        r1 = dbentidades((dbentidades.A3pLixos.IdPredio == session.IdPredio) & (dbentidades.A3pLixos.Data >= session.slcAno+'/01/01' ) & (dbentidades.A3pLixos.Data <= session.slcAno+'/12/01' )& (dbentidades.A3pLixos.Tipo == 'Org')).select(dbentidades.A3pLixos.Tipo, dbentidades.A3pLixos.Data, dbentidades.A3pLixos.Qtd.sum().with_alias('Geracao'), groupby=dbentidades.A3pLixos.Data.month())
        r2 = dbentidades((dbentidades.A3pLixos.IdPredio == session.IdPredio) & (dbentidades.A3pLixos.Data >= session.slcAno+'/01/01' ) & (dbentidades.A3pLixos.Data <= session.slcAno+'/12/01' ) & (dbentidades.A3pLixos.Tipo == 'Rec') ).select(dbentidades.A3pLixos.Tipo, dbentidades.A3pLixos.Data, dbentidades.A3pLixos.Qtd.sum().with_alias('Geracao'), groupby=dbentidades.A3pLixos.Data.month())
        rows = r1+r2
        data = [['Data',r1[0]['A3pLixos.Tipo'], r2[0]['A3pLixos.Tipo']]]
        rlist = []
        for row in range(len(r1)-1):
            mes = r1[row]['A3pLixos.Data']            
            res2 = r2[row]['Geracao']
            res1 = r1[row]['Geracao']
            mesext = mes_ext[mes.month]
            rlist.append(str(mes))
            rlist.append(int(res2))
            rlist.append(int(res1))
            data.append(rlist)
            rlist = []

    #grid=SQLFORM.grid(data)

    return dict(data=data)

@auth.requires_login()
def plotA3P():
    ano = session.slcAno
    #if session.IdPredio ==
    if session.selectgraf == 'Energia':
        rdata = dbentidades(((dbentidades.ContasEnergia.CodCPFL == db.Predios.CodEnergia) & (db.Predios.Id == session.IdPredio)) & (dbentidades.ContasEnergia.Mes >= session.slcAno+'/01/01') & (dbentidades.ContasEnergia.Mes <= session.slcAno+'/12/01' ) )
        ramo = 'Consumo de Energia '
        tipograf = 'line'
        fields = [dbentidades.ContasEnergia.Mes, dbentidades.ContasEnergia.Kwh, dbentidades.ContasEnergia.Valor]
        
    elif session.selectgraf == 'Água':
        rdata = dbentidades(((dbentidades.ContasAgua.CodSemae == db.Predios.CodAgua) & (db.Predios.Id == session.IdPredio)) & (dbentidades.ContasAgua.Data >= session.slcAno+'/01/01' ) & (dbentidades.ContasAgua.Data <= session.slcAno+'/12/01' )  )
        ramo = 'Consumo de Água '
        tipograf = 'line'
        fields = [dbentidades.ContasAgua.Data, dbentidades.ContasAgua.Consumo, dbentidades.ContasAgua.Valor]
        
    elif session.selectgraf == 'Resíduo':
        rdata = dbentidades((dbentidades.A3pLixos.IdPredio == session.IdPredio) & (dbentidades.A3pLixos.Data >= '2018/01/01' ) & (dbentidades.A3pLixos.Data <= '2018/12/01'))
        ramo = 'Produção de Resíduos'
        tipograf = 'area'
        fields = [dbentidades.A3pLixos.Data, dbentidades.A3pLixos.Tipo, dbentidades.A3pLixos.Qtd]
    else:        
        ramo = 'Consumo de Recursos'
        tipograf = 'bar'
   

    predio_p_cod = dbentidades((db.Predios.Id == session.IdPredio)).select(db.Predios.Predio)
    predio = predio_p_cod[0]['Predio']
    return dict(predio=predio, ramo=ramo, tipograf=tipograf, ano=ano, grade=SQLFORM.grid(rdata, deletable=False,
            editable=False, fields=fields))



