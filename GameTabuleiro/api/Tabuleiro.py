
from collections import OrderedDict

tamanhos = {'p': 4, 'm': 6, 'g': 8}


class Tabuleiro():
    blocos = {'casa': '[{}]', 'vazio': ' '}
    jogador_1 = '[+]'
    jogador_2 = '[O]'
    
    def __init__(self, tamanho='p', casas=OrderedDict()) -> None:
        self.tamanho = tamanhos[tamanho]
        self.casas = OrderedDict()
        tam = self.tamanho
        casa = 0
        qtd_blocos = self.tamanho**2
        qtd_casas = self.tamanho * 4-4
        casa_b = qtd_casas - (tam - 1)
        espacos_casa = len(str(qtd_casas))
        def casa_formatada(casa): return self.blocos['casa'].format(
            str(casa).center(espacos_casa)) if len(str(casa)) < espacos_casa else self.blocos['casa'].format(
            str(casa))
            
        for n in range(1, qtd_blocos+1):
            if n <= tam or n % tam == 0:
                casa += 1
                self.casas[n] = casa_formatada(casa)

            elif n % tam == 1:
                self.casas[n] = casa_formatada(qtd_casas)
                qtd_casas -= 1

            elif n > (tam*tam)-tam and n < tam*tam:
                self.casas[n] = casa_formatada(casa_b) 
                casa_b -= 1
            else:
                self.casas[n] =  self.blocos['vazio']*4

    # def __setattr__(self, __name: str, __value: Any) -> None:
    #     self.


    def __repr__(self) -> str:
        print('')
        k=1
        plinha = ''''''
        for y in range(1, self.tamanho +1):
            linha = []
            plinha = plinha.join('<tr>')
            #k = y * self.tamanho
            for x in range(1, self.tamanho +1):
                linha.append(self.casas[k])
                k += 1
                plinha = plinha.join(['<td>', str(linha), '</td>'])
            plinha = plinha.join('</tr>')

        return plinha

