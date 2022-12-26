import sys
sys.path.append("..")

from api.link_tab import Casa, Tabuleiro

print(sys.path[0])

def Tabuleiro_correto():
    return '[1]'
#print(Tabuleiro_correto())



def test_link_tab():
    tab = Tabuleiro()
    assert repr(tab) == Tabuleiro_correto(), 'Não bate'

def test_link_tab_add_casa():
    tab = Tabuleiro()
    dois = 2
    casa2 = Casa(f'[{dois}]')
    tab.proxim = casa2
    print(tab)
    assert repr(tab) != '[1][2]' , 'Tabuleiro com 2ª casa adicionada não bate com o teste'

test_link_tab()
test_link_tab_add_casa()
