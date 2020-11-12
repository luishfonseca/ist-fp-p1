# 99266 Luis Fonseca

def eh_tabuleiro(var):
    """Devolve se o seu argumento corresponde a um tabuleiro.

    eh_tabuleiro: universal -> booleano
    """

    if not (type(var) == tuple and len(var) == 3):
        return False

    for linha in var:
        if not (type(linha) == tuple and len(linha) == 3):
            return False

        for cell in linha:
            if not (type(cell) == int and -1 <= cell <= 1):
                return False

    return True


def eh_posicao(var):
    """Devolve se o seu argumento corresponde a uma posicao.

    eh_posicao: universal -> booleano
    """

    return type(var) == int and 1 <= var <= 9


def obter_coluna(tab, n):
    """Devolve um tuplo com os valores da coluna correspondente ao inteiro
    dado.

    obter_coluna: tabuleiro x inteiro -> tuplo
    """

    if not (eh_tabuleiro(tab) and type(n) == int and 1 <= n <= 3):
        raise ValueError('obter_coluna: algum dos argumentos e invalido')

    vect = ()
    for linha in tab:
        vect += (linha[n-1],)

    return vect


def obter_linha(tab, n):
    """Devolve um tuplo com os valores da linha correspondente ao inteiro dado.

    obter_linha: tabuleiro x inteiro -> tuplo
    """

    if not (eh_tabuleiro(tab) and type(n) == int and 1 <= n <= 3):
        raise ValueError('obter_linha: algum dos argumentos e invalido')

    return tab[n-1]


def obter_diagonal(tab, n):
    """Devolve um tuplo com os valores da diagonal correspondente ao inteiro
    dado.

    obter_diagonal: tabuleiro x inteiro -> tuplo
    """

    if not (eh_tabuleiro(tab) and type(n) == int and 1 <= n <= 2):
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
    """Devolve a cadeia de caracteres que representa o tabuleiro dado.

    tabuleiro_str: tabuleiro -> cad. caracteres
    """

    if not eh_tabuleiro(tab):
        raise ValueError('tabuleiro_str: o argumento e invalido')

    tab_str = ''
    for n in range(3):
        tab_str += linha_str(obter_linha(tab, n + 1))
        if n <= 1:
            tab_str += '\n-----------\n'

    return tab_str


def linha_str(linha):
    """Devolve a cadeia de caracteres que representa a linha dada.

    lin_str: tuplo -> cad. caracteres
    """

    if not (type(linha) == tuple and len(linha) == 3):
        raise ValueError('linha_str: o argumento e invalido')

    symbols = { -1: 'O', 0: ' ', 1: 'X'}

    lin_str = ''
    for n in range(3):
        lin_str += ' ' + symbols[linha[n]] + ' '
        if n <= 1:
            lin_str += '|'

    return lin_str


def obter_valor_posicao(tab, pos):
    """Devolve um inteiro com o valor da marca na posicao dada.

    obter_valor_posicao: tabuleiro x posicao -> inteiro
    """

    if not (eh_tabuleiro(tab) and eh_posicao(pos)):
        raise ValueError('obter_valor_posicao: algum dos argumentos e invalido')

    pos -= 1

    return obter_linha(tab, (pos//3)+1)[(pos%3)]


def eh_posicao_livre(tab, pos):
    """Devolve se a dada posicao se encontra livre.

    eh_posicao_livre: tabuleiro x posicao -> booleano
    """

    if not (eh_tabuleiro(tab) and eh_posicao(pos)):
        raise ValueError('eh_posicao_livre: algum dos argumentos e invalido')

    return obter_valor_posicao(tab,pos) == 0


def obter_posicoes_livres(tab):
    """Devolve o tuplo ordenado com todas as posicoes livres do tabuleiro dado.

    obter_posicoes_livres: tabuleiro -> tuplo
    """

    if not eh_tabuleiro(tab):
        raise ValueError('obter_posicoes_livres: o argumento e invalido')

    vect = ()
    for n in range(1,10):
        if eh_posicao_livre(tab,n):
            vect += (n,)

    return vect


def obter_linhas_colunas_diagonais(tab, pos):
    """Devolve um tuplo com os tuplos correspondentes a todas as linhas,
    colunas e diagonais a que essa posicao pertence.

    obter_linhas_colunas_diagonais: tabuleiro x posicao -> tuplo
    """

    if not (eh_tabuleiro(tab) and eh_posicao(pos)):
        raise ValueError('obter_linhas_colunas_diagonais: algum dos argumentos e invalido')

    lcds = ()

    linha = ((pos-1)//3)+1
    lcds += (obter_linha(tab, linha), )

    coluna = ((pos-1)%3)+1
    lcds += (obter_coluna(tab, coluna), )

    if pos in (1,5,9):
        lcds += (obter_diagonal(tab, 1), )

    if pos in (3,5,7):
        lcds += (obter_diagonal(tab, 2), )

    return lcds


def jogador_ganhador(tab):
    """Devolve o inteiro a correspondente ao jogador que ganhou a partida.

    jogador_ganhador: tabuleiro -> inteiro
    """

    if not eh_tabuleiro(tab):
        raise ValueError('jogador_ganhador: o argumento e invalido')

    def eh_vitoria(vect):
        return vect[0] != 0 and vect[0] == vect[1] == vect[2]

    for obter_fila in (obter_linha, obter_coluna, obter_diagonal):
        for n in range(3):
            if not (n == 2 and obter_fila == obter_diagonal):
                fila = obter_fila(tab, n+1)
                if eh_vitoria(fila):
                    return fila[0]

    return 0


def marcar_posicao(tab, j, pos):
    """Devolve um tabuleiro com a marca do jogador na posicao dada.

    marcar_posicao: tabuleiro x inteiro x posicao -> tabuleiro
    """

    if not (
        eh_tabuleiro(tab) and
        type(j) == int and j in (-1, 1) and
        eh_posicao(pos) and eh_posicao_livre(tab,pos)
    ):
        raise ValueError('marcar_posicao: algum dos argumentos e invalido')

    new_tab = ()
    for n in range(3):
        linha = obter_linha(tab, n + 1)
        if n == (pos-1)//3:
            new_tab += (marcar_linha(linha , j, pos), )
        else:
            new_tab += (linha, )

    return new_tab


def marcar_linha(vect, j, pos):
    """Devolve um tuplo representante de uma linha com a marca do jogador na
    posicao dada.

    marcar_linha: tuplo x inteiro x posicao -> tuplo
    """

    new_linha = ()
    for n in range(3):
        if n == (pos-1)%3:
            new_linha += (j,)
        else:
            new_linha += (vect[n], )

    return new_linha


def escolher_posicao_manual(tab):
    """Esta funcao realiza a leitura de uma posicao introduzida manualmente por
    um jogador e devolve esta posicao escolhida.

    escolher_posicao_manual: tabuleiro -> posicao
    """

    if not eh_tabuleiro(tab):
        raise ValueError('escolher_posicao_manual: o argumento e invalido')

    pos = int(input('Turno do jogador. Escolha uma posicao livre: '))

    if not (eh_posicao(pos) and eh_posicao_livre(tab, pos)):
        raise ValueError('escolher_posicao_manual: a posicao introduzida e invalida')

    return pos


def escolher_posicao_auto(tab, j, strat):
    """Devolve a posicao escolhida automaticamente de acordo com a estrategia
    selecionada.

    escolher_posicao_auto: tabuleiro x inteiro x cad. caracteres -> posicao
    """

    if not (
        eh_tabuleiro(tab) and
        type(j) == int and j in (-1, 1) and
        strat in ('basico', 'normal', 'perfeito')
    ):
        raise ValueError('escolher_posicao_auto: algum dos argumentos e invalido')

    acoes = (
        (vitoria, 'normal'),
        (bloqueio, 'normal'),
        (bifurcacao, 'perfeito'),
        (bloqueio_bifurcacao, 'perfeito'),
        (centro, 'basico'),
        (canto_oposto, 'normal'),
        (canto_vazio, 'basico'),
        (lateral_vazio, 'basico')
    )

    pos = None
    for acao in acoes:
        if eh_mais_avancada(strat, acao[1]):
            pos = acao[0](tab, j)

        if pos:
            return pos


def eh_mais_avancada(strat, outra_strat):
    """Devolve se a primeira estrategia e mais ou igualmente avancada em
    comparacao a segunda.

    eh_mais_avancada: cad. caracteres x cad. caracteres -> booleano
    """

    strats = { 'basico': 0, 'normal': 1, 'perfeito': 2 }
    return strats[strat] >= strats[outra_strat]


def vitoria(tab, j):
    """Se o jogador tiver um dois em linha devolve a posicao livre restante.

    vitoria: tabuleiro x inteiro -> posicao
    """

    for pos in obter_posicoes_livres(tab):
        for lcd in obter_linhas_colunas_diagonais(tab, pos):
            if lcd.count(j) == 2:
                return pos

    return None


def bloqueio(tab, j):
    """Se o adversario tiver um dois em linha devolve a posicao livre restante.

    bloqueio: tabuleiro x inteiro -> posicao
    """

    # bloqueio utiliza a mesma logica que vitoria sendo assim possivel
    # reutilizar o codigo -j e o oponente de j
    return vitoria(tab, -j)


def bifurcacao(tab, j):
    """Se o jogador tiver uma posicao de bifurcacao devolve essa posicao.

    bifurcacao: tabuleiro x inteiro -> posicao
    """

    for pos in obter_posicoes_livres(tab):
        if eh_intersecao(tab, pos, j):
            return pos

    return None


def eh_intersecao(tab,pos,j):
    """Verifica se a posicao se encontra em duas ou mais linhas, colunas ou
    diagonais com pecas do jogador.

    eh_intersecao: tabuleiro x posicao x inteiro -> booleano
    """

    total = 0
    for lcd in obter_linhas_colunas_diagonais(tab, pos):
        if lcd.count(0) == 2:
            total += lcd.count(j)

    return total >= 2


def bloqueio_bifurcacao(tab, j):
    """Se o oponente tiver apenas uma posicao de bifurcacao devolve essa
    posicao. Caso exista mais do que uma bifurcacao devolve a primeira
    posicao que impede o oponente de tirar partido da situacao.

    bloqueio_bifurcacao: tabuleiro x inteiro -> posicao
    """

    intersecoes = ()
    for pos in obter_posicoes_livres(tab):
        if eh_intersecao(tab, pos, -j):
            intersecoes += (pos, )

    if len(intersecoes) == 0:
        return None
    elif len(intersecoes) == 1:
        return intersecoes[0]
    else:
        return bloqueio_bifurcacoes(intersecoes, tab, j)

def bloqueio_bifurcacoes(intersecoes, tab, j):
    """Devolve a posicao que impede a criacao de uma bifurcacao quando existem
    mais do que uma posicao que a crie.

    bloqueio_bifurcacoes: tuplo x tabuleiro x inteiro -> posicao
    """

    posicoes_livres = obter_posicoes_livres(tab)

    possibilidades = ()
    for pos in posicoes_livres:
        if pos not in intersecoes:

            # Forca o oponente a jogar numa posicao que nao seja intersecao
            acao = forcar_jogada_lc(tab, j, pos)
            if acao:
                possibilidades += (acao, )

    # Escolhe a primeira posicao que satisfaz o pretendido
    for pos in posicoes_livres:
        if pos in possibilidades:
            return pos

    return None


def forcar_jogada_lc(tab, j, pos):
    """Devolve a posicao que forca o oponente a jogar na dada posicao no turno
    seguinte. Apenas se aplica a linhas e colunas.

    forcar_jogada_lc: tabuleiro x inteiro x posicao -> posicao
    """

    linha = (pos-1)//3
    coluna = (pos-1)%3

    # Caso a linha tenha uma peca do jogador e dois vazios
    # jogasse na posicao vazia que nao e a que se deseja forcar
    lin_vect = obter_linha(tab, linha+1)
    if j in lin_vect:
        for c in range(3):
            if c != coluna and lin_vect[c] == 0:
                return (linha*3+c)+1

    # Mesma logica para colunas
    col_vect = obter_coluna(tab, coluna+1)
    if j in col_vect:
        for l in range(3):
            if l != linha and col_vect[l] == 0:
                return (l*3+coluna)+1

    return None


def centro(tab, _):
    """Devolve a posicao central se esta estiver livre.

    centro: tabuleiro -> posicao
    """

    if eh_posicao_livre(tab, 5):
        return 5

    return None


def canto_oposto(tab, j):
    """Se o oponente tiver uma marca num canto do tabuleiro diagonalmente
    oposto a uma posicao livre devolve essa posicao.

    canto_oposto: tabuleiro x inteiro -> posicao
    """

    for pos in (1,3,7,9):
        if (
            eh_posicao_livre(tab, pos) and
            obter_valor_posicao(tab, 10-pos) == -j
        ):
            return pos

    return None


def canto_vazio(tab, _):
    """Devolve o primeiro canto que e uma posicao livre caso exista.

    canto_vazio: tabuleiro -> posicao
    """

    for pos in (1,3,7,9):
        if eh_posicao_livre(tab, pos):
            return pos

    return None


def lateral_vazio(tab, _):
    """Devolve a primeira lateral que e uma posicao livre caso exista.

    lateral_vazio: tabuleiro -> posicao
    """

    for pos in (2,4,6,8):
        if eh_posicao_livre(tab, pos):
            return pos

    return None


def jogo_do_galo(j, strat):
    """Esta funcao corresponde a funcao principal que permite jogar um jogo
    completo de Jogo do Galo de uma jogador contra o computador.

    jogo_do_galo: cad. caracteres x cad. caracteres -> cad. caracteres
    """

    if not (j in ('X','O') and strat in ('basico','normal','perfeito')):
        raise ValueError('jogo_do_galo: algum dos argumentos e invalido')

    print('Bem-vindo ao JOGO DO GALO.')
    print('O jogador joga com \'{}\'.'.format(j))

    turnos = {'X': 1, 'O': -1}
    j = turnos[j]

    tab = ((0,)*3,)*3
    turno = 1

    while jogador_ganhador(tab) == 0 and len(obter_posicoes_livres(tab)) > 0:
        tab = jogar_turno(turno, strat, tab, j)
        print(tabuleiro_str(tab))
        turno *= -1

    resultados = {1: 'X', 0: 'EMPATE', -1: 'O'}
    return resultados[jogador_ganhador(tab)]


def jogar_turno(turno, strat, tab, j):
    """Devolve o tabuleiro modificado apos o turno.

    jogar_turno: inteiro x cad. caracteres x tabuleiro x inteiro -> tabuleiro
    """

    if j == turno:
        pos = escolher_posicao_manual(tab)
    else:
        print('Turno do computador ({}):'.format(strat))
        pos = escolher_posicao_auto(tab, turno, strat)

    return marcar_posicao(tab, turno, pos)

