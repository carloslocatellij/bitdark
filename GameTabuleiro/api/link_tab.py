#Lista linkada 

class Casa:
    def __init__(self, info):
        self.info = info
        self.next = None

    def __repr__(self):
        return self.info


class Tabuleiro:
    def __init__(self, lado=3):
        self.lado = lado
        self.inicio = Casa(f'[{1}]')
        self.num_casas = lado * 4 - 4
        casa = self.inicio
        self.casas = [casa]
        for c in range(2, self.num_casas +1):
            casa.next = Casa(f'[{c}]')
            casa = casa.next
            self.casas.append(casa)
        casa.next = self.inicio

    def __repr__(self):
        casa, casas = self.inicio ,[]
        forma_de_saida = ''''''
        while casa != self.casas[-1]:
            casas.append(casa)
            casa = casa.next
            forma_de_saida += str(casa)
            if int(casa.info[1:].replace(']','')) % self.lado == 0:
                forma_de_saida += '\n'
        return forma_de_saida


if __name__ == '__main__':
    t = Tabuleiro(6)
    print(t)



