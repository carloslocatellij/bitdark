# -*- coding: utf-8 -*-


def Campanha():
    campanha = Campanhas(request.args(0, cast=int)) or redirect(URL('index'))

    return dict(campanha = campanha)