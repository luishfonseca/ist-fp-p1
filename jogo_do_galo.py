# 99266 Luis Fonseca

# univ -> bool
def eh_tabuleiro(univ):
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

# univ -> bool
def eh_posicao(univ):
    return type(univ) == int and 1 <= univ <= 9

# tab x int -> vect
def obter_coluna(tab, n):
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

# tab x int -> vect
def obter_linha(tab, n):
    if not (
       eh_tabuleiro(tab) and
       type(n) == int and
       1 <= n <= 3
    ):
        raise ValueError('obter_linha: algum dos argumentos e invalido')

    return tab[n-1]

# tab x int -> vect
def obter_diagonal(tab, n):
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

# tab -> str
def tabuleiro_str(tab):
    if not eh_tabuleiro(tab):
        raise ValueError('tabuleiro_str: o argumento e invalido')

    out_str = ''
    for n in range(3):
        out_str += linha_str(obter_linha(tab, n + 1))
        if n <= 1:
            out_str += '\n-----------\n'

    return out_str

# vect -> str
def linha_str(linha):
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

# tab x pos -> int
def obter_valor_posicao(tab, pos):
    if not (
        eh_tabuleiro(tab) and
        eh_posicao(pos)
    ):
        raise ValueError('obter_valor_posicao: algum dos argumentos e invalido')

    pos -= 1
    return obter_linha(tab, (pos//3)+1)[(pos%3)]

# tab x pos -> bool
def eh_posicao_livre(tab, pos):
    if not (
        eh_tabuleiro(tab) and
        eh_posicao(pos)
    ):
        raise ValueError('eh_posicao_livre: algum dos argumentos e invalido')

    return obter_valor_posicao(tab,pos) == 0

# tab -> vect
def obter_posicoes_livres(tab):
    if not eh_tabuleiro(tab):
        raise ValueError('obter_posicoes_livres: o argumento é invalido')

    vect = ()
    for n in range(1,10):
        if eh_posicao_livre(tab,n):
            vect += (n,)

    return vect

# tab x int -> vect
def obter_linhas_colunas_diagonais(tab, n):
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

# tab -> int
def jogador_ganhador(tab):
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

# vect -> bool
def eh_vitoria(vect):
    if not len(vect) == 3:
        raise ValueError('eh_vitoria: o argumento e invalido')

    return vect[0] != 0 and vect[0] == vect[1] == vect[2]

# tab x int x pos -> tab
def marcar_posicao(tab, v, pos):
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

# vect x int x pos -> vect
def marcar_linha(vect, v, pos):
    new_linha = ()
    for n in range(3):
        if n == (pos-1)%3:
            new_linha += (v,)
        else:
            new_linha += (vect[n], )

    return new_linha

# tab -> pos
def escolher_posicao_manual(tab):
    if not eh_tabuleiro(tab):
        raise ValueError('escolher_posicao_manual: o argumento e invalido')

    pos = int(input('Turno do jogador. Escolha uma posicao livre: '))

    if not (
        eh_posicao(pos) and
        eh_posicao_livre(tab, pos)
    ):
        raise ValueError('escolher_posicao_manual: a posicao introduzida e invalida')

    return pos

# tab x int x str -> pos
def escolher_posicao_auto(tab, p, strat):
    if not (
        eh_tabuleiro(tab) and
        type(p) == int and
        p in (-1, 1) and
        strat in ('basico', 'normal', 'perfeito')
    ):
        raise ValueError('escolher_posicao_auto: algum dos argumentos e invalido')

    niveis = {
        'basico': 0,
        'normal': 1,
        'perfeito': 2
    }
    nivel = niveis[strat]

    if nivel >= 1 and vitoria(tab, p):
        return vitoria(tab, p)
    elif nivel >= 1 and bloqueio(tab, p):
        return bloqueio(tab, p)
    elif nivel == 2 and bifurcacao(tab, p):
        return bifurcacao(tab, p)
    elif nivel == 2 and bloqueio_bifurcacao(tab, p):
        return bloqueio_bifurcacao(tab, p)
    elif centro(tab):
        return centro(tab)
    elif nivel >= 1 and canto_oposto(tab, p):
        return canto_oposto(tab, p)
    elif canto_vazio(tab):
        return canto_vazio(tab)
    elif lateral_vazio(tab):
        return lateral_vazio(tab)

# tab x int -> pos (or None)
# x - -
# - x -
# - - +
def vitoria(tab, p):
    for pos in obter_posicoes_livres(tab):
        for lcd in obter_linhas_colunas_diagonais(tab, pos):
            if lcd.count(p) == 2:
                return pos

    return None

# tab x int -> pos (or None)
# o - -
# o - -
# + - -
def bloqueio(tab, p):
    return vitoria(tab, -p)

# tab x int -> pos (or None)
# x - -
# - - -
# * x -
def bifurcacao(tab, p):
    for pos in obter_posicoes_livres(tab):
        if eh_intersecao(tab, pos, p):
            return pos

    return None

# tab x pos x int -> bool
def eh_intersecao(tab,pos,p):
    total = 0
    for lcd in obter_linhas_colunas_diagonais(tab, pos):
        if lcd.count(0) == 2:
            total += lcd.count(p)

    return total >= 2

# tab x int -> pos (or None)
# o - o  o * -
# - * -  - x -
# - - -  - - o
def bloqueio_bifurcacao(tab, p):
    posicoes_livres = obter_posicoes_livres(tab)
    intersecoes = ()
    for pos in posicoes_livres:
        if eh_intersecao(tab, pos, -p):
            intersecoes += (pos, )

    if len(intersecoes) == 0:
        return None
    elif len(intersecoes) == 1:
        return intersecoes[0]
    else:
        for pos in posicoes_livres:
            if pos not in intersecoes:
                return pos

        return None

# tab x int -> pos (or None)
# - - -
# - * -
# - - -
def centro(tab):
    if eh_posicao_livre(tab, 5):
        return 5

    return None

# tab x int -> pos (or None)
# - - o
# - - -
# * - -
def canto_oposto(tab, p):
    for pos in (1,3,7,9):
        if (
            eh_posicao_livre(tab, pos) and
            obter_valor_posicao(tab, 10-pos) == -p
        ):
            return pos

    return None

# tab x int -> pos (or None)
# * - -
# - - -
# - - -
def canto_vazio(tab):
    for pos in (1,3,7,9):
        if eh_posicao_livre(tab, pos):
            return pos

    return None

# tab x int -> pos (or None)
# - - -
# - - *
# - - -
def lateral_vazio(tab):
    for pos in (2,4,6,8):
        if eh_posicao_livre(tab, pos):
            return pos

    return None

# str x str -> str
def jogo_do_galo(p, strat):
    if not (
        p in ('X','O') and
        strat in ('basico','normal','perfeito')
    ):
        raise ValueError('jogo_do_galo: algum dos argumentos e invalido')

    print('Bem-vindo ao JOGO DO GALO.')
    print('O jogador joga com \'{}\'.'.format(p))

    turnos = {
        'X': 1,
        'O': -1
    }
    p = turnos[p]

    tab = ((0,)*3,)*3
    turno = 1
    while jogador_ganhador(tab) == 0 and len(obter_posicoes_livres(tab)) > 0:
        if p == turno:
            pos = escolher_posicao_manual(tab)
        else:
            print('Turno do computador ({}):'.format(strat))
            pos = escolher_posicao_auto(tab, turno, strat)

        tab = marcar_posicao(tab, turno, pos)

        print(tabuleiro_str(tab))

        turno *= -1

    resultados = {
        1: 'X',
        0: 'EMPATE',
        -1: 'O'
    }
    return resultados[jogador_ganhador(tab)]

