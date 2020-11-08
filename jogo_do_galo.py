# 99266 Luis Fonseca

def eh_tabuleiro(univ):
    """Verifica se o argumento e um tabuleiro 3x3 valido"""

    if not (
            type(univ) == tuple and
            len(univ) == 3
    ):
        return False

    for linha in univ:
        if not (
                type(linha) == tuple and
                len(linha) == 3
        ):
            return False

        for cell in linha:
            if not (
                    type(cell) == int and
                    -1 <= cell <= 1
            ):
                return False

    return True

def eh_posicao(univ):
    """Verifica se o argumento e uma posicao valida"""

    return type(univ) == int and 1 <= univ <= 9

def obter_coluna(tab, n):
    """Retorna um tuplo com os valores da coluna n de um tabuleiro tab"""

    if not (
        eh_tabuleiro(tab) and
        type(n) == int and
        1 <= n <= 3
    ):
        raise ValueError('obter_coluna: algum dos argumentos e invalido')

    vect = ()
    for linha in tab:
        vect += (linha[n-1],)

    return vect

def obter_linha(tab, n):
    """Retorna um tuplo com os valores da linha n de um tabuleiro tab"""

    if not (
       eh_tabuleiro(tab) and
       type(n) == int and
       1 <= n <= 3
    ):
        raise ValueError('obter_linha: algum dos argumentos e invalido')

    return tab[n-1]

def obter_diagonal(tab, n):
    """Retorna um tuplo com os valores de uma das diagonais de um tabuleiro tab

    Quando n == 1 e retornada a diagonal descendente com origem na posicao 1
    Quando n == 2 e retornada a diagonal ascendente com origem na posicao 7
    """

    if not (
        eh_tabuleiro(tab) and
        type(n) == int and
        1 <= n <= 2
    ):
        raise ValueError('obter_diagonal: algum dos argumentos e invalido')

    if n == 1:
        step = 1
    elif n == 2:
        n = 3
        step = -1

    vect = ()
    for c in range(3):
        vect += ( obter_coluna(tab, c + 1)[n-1], )
        n += step

    return vect

def tabuleiro_str(tab):
    """Retorna a cadeia de carateres formatada do tabuleiro tab"""

    if not eh_tabuleiro(tab):
        raise ValueError('tabuleiro_str: o argumento e invalido')

    out_str = ''
    for n in range(3):
        out_str += linha_str(obter_linha(tab, n + 1))
        if n <= 1:
            out_str += '\n-----------\n'

    return out_str

def linha_str(linha):
    """Retorna a cadeia de carateres formatada da linha de um tabuleiro"""

    out_str = ''

    symbols = {
        -1: 'O',
         0: ' ',
         1: 'X'
    }

    for n in range(3):
        out_str += ' ' + symbols[linha[n]] + ' '
        if n <= 1:
            out_str += '|'

    return out_str

def obter_valor_posicao(tab, pos):
    """Retorna o valor na posicao pos de um tabuleiro tab"""

    if not (
        eh_tabuleiro(tab) and
        eh_posicao(pos)
    ):
        raise ValueError('obter_valor_posicao: algum dos argumentos e invalido')

    pos -= 1
    return obter_linha(tab, (pos//3)+1)[(pos%3)]

def eh_posicao_livre(tab, pos):
    """Verifica se o tabuleiro tab tem a posicao pos livre"""

    if not (
        eh_tabuleiro(tab) and
        eh_posicao(pos)
    ):
        raise ValueError('eh_posicao_livre: algum dos argumentos e invalido')

    return obter_valor_posicao(tab,pos) == 0

def obter_posicoes_livres(tab):
    """Retorna um tuplo com todas as posicoes livres num tabuleiro tab"""

    if not eh_tabuleiro(tab):
        raise ValueError('obter_posicoes_livres: o argumento e invalido')

    vect = ()
    for n in range(1,10):
        if eh_posicao_livre(tab,n):
            vect += (n,)

    return vect

def obter_linhas_colunas_diagonais(tab, n):
    """Retorna um tuplo com todas as linhas, colunas e diagonais de um
    tabuleiro tab que passam pela posicao n
    """

    lcds = ()

    pos_l = ((n-1)//3)+1
    lcds += (obter_linha(tab, pos_l), )

    pos_c = ((n-1)%3)+1
    lcds += (obter_coluna(tab, pos_c), )

    if n in (1,5,9):
        lcds += (obter_diagonal(tab, 1), )

    if n in (3,5,7):
        lcds += (obter_diagonal(tab, 2), )

    return lcds

def jogador_ganhador(tab):
    """Retorna o jogador ganhador caso este exista para um tabuleiro tab

    Se o tabuleiro nao estiver numa condicao de vitoria e retornado 0
    """

    if not eh_tabuleiro(tab):
        raise ValueError('jogador_ganhador: o argumento e invalido')

    for n in range(1,4):
        if eh_vitoria(obter_coluna(tab, n)):
            return obter_coluna(tab, n)[0]
        if eh_vitoria(obter_linha(tab, n)):
            return obter_linha(tab, n)[0]
        if n != 3 and eh_vitoria(obter_diagonal(tab, n)):
            return obter_diagonal(tab, n)[0]

    return 0

def eh_vitoria(vect):
    """Verifica se uma dada linha/coluna/diagonal esta numa condicao de vitoria"""

    if not len(vect) == 3:
        raise ValueError('eh_vitoria: o argumento e invalido')

    return vect[0] != 0 and vect[0] == vect[1] == vect[2]

def marcar_posicao(tab, v, pos):
    """Retorna o tabuleiro tab com o valor na posicao pos mudado para v"""

    if not (
        eh_tabuleiro(tab) and
        type(v) == int and
        v in (-1, 1) and
        eh_posicao(pos) and
        eh_posicao_livre(tab,pos)
    ):
        raise ValueError('marcar_posicao: algum dos argumentos e invalido')

    new_tab = ()
    for n in range(3):
        if n == (pos-1)//3:
            new_tab += (marcar_linha(obter_linha(tab, n + 1), v, pos), )
        else:
            new_tab += (obter_linha(tab, n + 1), )

    return new_tab

def marcar_linha(vect, v, pos):
    """Retorna a linha vect com o valor na posicao pos mudado para v"""

    new_linha = ()
    for n in range(3):
        if n == (pos-1)%3:
            new_linha += (v,)
        else:
            new_linha += (vect[n], )

    return new_linha

def escolher_posicao_manual(tab):
    """Pede ao utilizador que escolha a jogada seguinte

    Pede ao utilizador que insira uma posicao valida no tabuleiro tab
    Caso valida essa posicao sera a jogada seguinte
    """

    if not eh_tabuleiro(tab):
        raise ValueError('escolher_posicao_manual: o argumento e invalido')

    pos = int(input('Turno do jogador. Escolha uma posicao livre: '))

    if not (
        eh_posicao(pos) and
        eh_posicao_livre(tab, pos)
    ):
        raise ValueError('escolher_posicao_manual: a posicao introduzida e invalida')

    return pos

def escolher_posicao_auto(tab, j, strat):
    """Dependendo da estrategia, determina automaticamente a jogada seguinte

    A funcao chama funcoes auxiliares para cada uma das acoes quando esta se aplica
    Dependendo da estrategia certas acoes sao ignoradas
    """
    if not (
        eh_tabuleiro(tab) and
        type(j) == int and
        j in (-1, 1) and
        strat in ('basico', 'normal', 'perfeito')
    ):
        raise ValueError('escolher_posicao_auto: algum dos argumentos e invalido')

    niveis = {
        'basico': 0,
        'normal': 1,
        'perfeito': 2
    }
    nivel = niveis[strat]

    if nivel >= 1 and vitoria(tab, j):
        return vitoria(tab, j)
    elif nivel >= 1 and bloqueio(tab, j):
        return bloqueio(tab, j)
    elif nivel == 2 and bifurcacao(tab, j):
        return bifurcacao(tab, j)
    elif nivel == 2 and bloqueio_bifurcacao(tab, j):
        return bloqueio_bifurcacao(tab, j)
    elif centro(tab):
        return centro(tab)
    elif nivel >= 1 and canto_oposto(tab, j):
        return canto_oposto(tab, j)
    elif canto_vazio(tab):
        return canto_vazio(tab)
    elif lateral_vazio(tab):
        return lateral_vazio(tab)

def vitoria(tab, j):
    """Executa a estrategia vitoria"""

    # Uma das linhas/colunas/diagonais tem 2 pecas do jogador j e um espaco vazio

    for pos in obter_posicoes_livres(tab):
        for lcd in obter_linhas_colunas_diagonais(tab, pos):
            if lcd.count(j) == 2:
                return pos

    return None

def bloqueio(tab, j):
    """Executa a estrategia bloqueio"""

    # Se uma das linhas/colunas/diagonais tem 2 pecas do oponente do jogador j e um espaco livre
    # Retornar o espaco livre


    # bloqueio utiliza a mesma logica que vitoria sendo assim possivel reutilizar o codigo
    # -j e o oponente de j
    return vitoria(tab, -j)

def bifurcacao(tab, j):
    """Executa a estrategia bifurcacao"""

    # Se existir um espaco livre numa intersecao de pecas do jogador j
    # Retornar o espaco livre

    for pos in obter_posicoes_livres(tab):
        if eh_intersecao(tab, pos, j):
            return pos

    return None

def eh_intersecao(tab,pos,j):
    """Verifica se a posicao pos de encontra numa intersecao de pecas do jogador j"""

    # Caso a posicao pos se encontre em duas ou mais linhas/colunas/diagonais
    # com pecas do jogador j tem-se que a pos se encontra numa intersecao

    total = 0
    for lcd in obter_linhas_colunas_diagonais(tab, pos):
        if lcd.count(0) == 2:
            total += lcd.count(j)

    return total >= 2

def bloqueio_bifurcacao(tab, j):
    """Executa a estrategia bloqueio de bifurcacao"""

    # Impede o oponente do jogador j de realizar um bifurcacao

    posicoes_livres = obter_posicoes_livres(tab)
    intersecoes = ()
    for pos in posicoes_livres:
        if eh_intersecao(tab, pos, -j):
            intersecoes += (pos, )

    if len(intersecoes) == 0:
        return None
    elif len(intersecoes) == 1:
        # Se existir apenas um espaco livre numa intersecao de pecas do oponente do jogador j
        # Retorna esse espaco
        return intersecoes[0]
    else:
        # Caso exista mais que um espaco livre
        # O jogado j forca o oponente a jogar numa posicao que nao crie uma bifurcacao.

        # Esta inversao e desnecessaria mas remove a simetria em comparacao ao exemplo do enunciado
        for pos in posicoes_livres[::-1]:
            if pos not in intersecoes:

                # Impedir a criacao de uma bifurcacao implica impedir o oponente de jogar numa intersecao
                acao = forcar_jogada_lc(tab, j, pos)
                if acao:
                    return acao

def forcar_jogada_lc(tab, j, pos):
    """Retorna a posicao que forca o oponente de j a jogar na posicao pos no turno seguinte

    Apenas se aplica a linhas e colunas
    """

    pos_l = (pos-1)//3
    pos_c = (pos-1)%3

    lin = obter_linha(tab, pos_l+1)
    col = obter_coluna(tab, pos_c+1)
    # A verificacao das diagonais e desnecessaria uma vez que as posicoes
    # livres que nao sao intersecoes nunca se encontram nos cantos

    # Caso a linha tenha uma peca do jogador e dois vazios
    # jogasse na posicao vazia que nao e a que se deseja forcar
    if j in lin:
        for c in range(3):
            if c != pos_c and lin[c] == 0:
                return (pos_l*3+c)+1

    # Mesma logica para colunas
    if j in col:
        for l in range(3):
            if l != pos_l and col[l] == 0:
                return (l*3+pos_c)+1

    return None

def centro(tab):
    """Executa a estrategia centro"""

    # Se o centro esta livre
    # Retornar a posicao central

    if eh_posicao_livre(tab, 5):
        return 5

    return None

def canto_oposto(tab, j):
    """Executa a estrategia canto oposto"""

    # Se dos cantos (posicoes 1,3,7,9) tiver uma peca do oponente do jogador j
    # Retornar o canto oposto caso estaja livre

    for pos in (1,3,7,9):
        if (
            eh_posicao_livre(tab, pos) and
            obter_valor_posicao(tab, 10-pos) == -j
        ):
            return pos

    return None

def canto_vazio(tab):
    """Executa a estrategia canto vazio"""

    # Retornar um dos cantos caso estejam livres

    for pos in (1,3,7,9):
        if eh_posicao_livre(tab, pos):
            return pos

    return None

def lateral_vazio(tab):
    """Executa a estrategia lateral vazio"""

    # Retornar uma das laterais (posicoes 2,4,6,8) caso estejam livres

    for pos in (2,4,6,8):
        if eh_posicao_livre(tab, pos):
            return pos

    return None

def jogo_do_galo(j, strat):
    """Ponto de entrada do programa. Retorna o vencedor do jogo

    Pede o simbolo do jogador humano e a estrategia para o algoritmo
    Esta funcao repete ate um vencedor ser determinado
    """

    if not (
        j in ('X','O') and
        strat in ('basico','normal','perfeito')
    ):
        raise ValueError('jogo_do_galo: algum dos argumentos e invalido')

    print('Bem-vindo ao JOGO DO GALO.')
    print('O jogador joga com \'{}\'.'.format(j))

    turnos = {
        'X': 1,
        'O': -1
    }
    j = turnos[j]

    tab = ((0,)*3,)*3
    turno = 1
    while jogador_ganhador(tab) == 0 and len(obter_posicoes_livres(tab)) > 0:

        if j == turno:
            pos = escolher_posicao_manual(tab)
        else:
            print('Turno do computador ({}):'.format(strat))
            pos = escolher_posicao_auto(tab, turno, strat)

        tab = marcar_posicao(tab, turno, pos)

        print(tabuleiro_str(tab))

        # no proximo turno joga o oponente do jogador do turno atual
        turno *= -1

    resultados = {
        1: 'X',
        0: 'EMPATE',
        -1: 'O'
    }
    return resultados[jogador_ganhador(tab)]

