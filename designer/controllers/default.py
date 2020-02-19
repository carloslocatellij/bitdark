# coding: utf8                                                       

#########################################################################
## This is a samples controller                                          
## - index is the default action of any application                      
## - user is required for authentication and authorization                                                                                                                              
## - download is for downloading files uploaded in the db (does streaming)                                                                                                              
## - call exposes all registered services (none by default)                                                                                                                             
#########################################################################                                                                                                               
                                                                                                                                                                                       
def index():                                                                                                                                                                            
    redirect(URL(r=request,c='static',f='designer/index.html',vars=request.vars))  

def user():
    return dict(form=auth())                                    


def download():
    return response.download(request,db)         


def call():
    session.forget()
    return service()

def backend():
    import re
    if request.vars.action == "save": # api is URL?action=save&keyword=schemaname
        if re.compile('[^0-9a-zA-Z]').findall(request.vars.keyword):
            raise HTTP(503, 'NOT SAVED! use [0-9a-zA-Z] for project names only... ')
        name = db(db.tbldata.tblname == request.vars.keyword).select(db.tbldata.tblname)
        if len(name) != 0:
            db(db.tbldata.tblname==request.vars.keyword).update(
                              tblname=request.vars.keyword,
                              changed=request.now,
                              xmldata=request.body.read()
                          )
        else:
            db.tbldata.insert(tblname=request.vars.keyword,
                              changed=request.now,
                              xmldata=request.body.read()
                          )
        raise HTTP(201, "Model has been saved...")
       #request.body.read()
    elif request.vars.action == "list": # api is URL?action=list
        rows = db().select(db.tbldata.ALL)
        names = ""
        for row in rows:
            if names == "":
                names = row.tblname
                continue
            names = names + "\n" + row.tblname
            response.headers['Content-Type'] = 'text/plain'
        return names
    elif request.vars.action == "load":               # api is URL?action=load&keyword=schemaname
        row = db(db.tbldata.tblname == request.get_vars.keyword).select(db.tbldata.xmldata)
        if len(row) != 0 :
            response.headers['Content-Type'] = 'application/xml'
            #return row[0].xmldata        # without cast it errors out with Blob does not have items attribute????
            return "%s" % row[0].xmldata  # when casted to string it works on GAE....
        else:
            raise HTTP(404,T('Model Not found...'))
    elif request.vars.action == "import":     # api is URL?action=import&database=somedatabasename
        raise HTTP(501,T("Not implemented"))
