
tamanhos = {'p': 4, 'm': 6, 'g': 8}

blocos = {'casa': '| |', 'vazio': '  ', 'p1casa': '[X]', 'p2casa': '[@]'}

while True:
    tam = int(input('Tamanho do seu tabuleiro: '))
    
    if tam >= 1000:
        print("Para que eu não vou aguentar!")
        
    def tabuleiro(tam):
        mapa = [(n, blocos['casa']) if n <= tam or n % tam == 1 or n % tam == 0 or n > (tam*tam)-tam else (n, '   ')
                for n, v in enumerate(range(tam**2), 1)]                                 
        for l in range(tam):
            linha = (x[1] for x in mapa[l * tam : l * tam + tam])
            print(''.join(linha))          
    tabuleiro(tam)
