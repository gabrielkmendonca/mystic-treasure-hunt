import random 

tesouro = "🏆"
armadilha = "💣"
pista = "🔎"
vazio = " _"
escondido = " X"

def configurar_tabuleiro (mensagem): #função para configurar a dimensão do tabuleiro
    try:
        valor = int(input(mensagem))
        return valor
    except ValueError:
        print("Entrada inválida. Insira um número inteiro.")
    
def criar_tabuleiro(tamanho): #função para criar o tabuleiro
    tabuleiro = []
    for i in range (tamanho):
        linha = []
        for j in range (tamanho):
            linha.append(vazio)
        tabuleiro.append(linha)
    tabuleiro[0][0] = vazio
    return tabuleiro

def distribuir_elementos(tabuleiro, tamanho, quantidade_armadilhas, quantidade_pistas): #função para distribuir os itens pelo tabuleiro
    todas_posicoes = []
    for i in range (tamanho):
        for j in range (tamanho):
            if not (i == 0 and j == 0):
                todas_posicoes.append((i,j))
    random.shuffle(todas_posicoes)

    #posição do tesouro
    x, y = todas_posicoes.pop()
    tabuleiro[x][y] = tesouro
    pos_tesouro = (x, y)

    #posição das armadilhas
    for i in range (quantidade_armadilhas):
        x, y = todas_posicoes.pop()
        tabuleiro[x][y] = armadilha

    #posição das pistas
    for i in range (quantidade_pistas):
        x, y = todas_posicoes.pop()
        tabuleiro[x][y] = pista

    return pos_tesouro

def exibir_tabuleiro(tamanho_tabuleiro, tabuleiro, pos_reveladas): #função pra exibir o tabuleiro ao longo do jogo
    print("\nTabuleiro Atual:")
    print("    " + " ".join(f"{i:2d}" for i in range(1, tamanho_tabuleiro + 1)))
    print("   " + "———" * tamanho_tabuleiro)
    for i in range(tamanho_tabuleiro):
        linha = []
        for j in range (tamanho_tabuleiro):
            if (i, j) in pos_reveladas:
                if tabuleiro[i][j] == vazio:
                    linha.append(f"{tabuleiro[i][j]:2s}")
                else:
                    linha.append(f"{tabuleiro[i][j]}")
            else:
                linha.append(f"{escondido:2s}")
        print(f"{i + 1} | " + " ".join(linha))

def obter_jogada(tamanho_tabuleiro, pos_reveladas): #função para solicitar uma jogada
    while True:
        x = int(input(f"\nInforme a linha (1 a {tamanho_tabuleiro}): ")) - 1
        y = int(input(f"Informe a coluna (1 a {tamanho_tabuleiro}): ")) - 1
        if (x, y) in pos_reveladas:
            print("Essa posição já foi revelada... Escolha outra.")
            continue
        return x, y
    
def conteudo_pistas(posicao, pos_tesouro): #função para informar a dica contida na pista
    x, y = posicao
    X, Y = pos_tesouro
    dica = []

    if X < x:
        dica.append("para Cima")
    elif X > x:
        dica.append("para Baixo")

    if Y < y:
        dica.append("para a Esquerda")
    elif Y > y:
        dica.append("para a Direita")

    if len(dica) == 2:
        return f"O tesouro está mais para {dica[0]} e {dica[1]}."
    return f"O tesouro está mais {dica[0]}."

def processar_jogada(tabuleiro, posicao): #processar e armazenar as jogadas já realizadas
    x, y = posicao
    conteudo_casa = tabuleiro[x][y]
    if conteudo_casa == tesouro:
        return tesouro
    elif conteudo_casa == armadilha:
        return armadilha
    elif conteudo_casa == pista:
        return pista
    else:
        return vazio
        

print("======= Caça ao Tesouro Místico =======")

tamanho_tabuleiro = configurar_tabuleiro("Insira o tamanho do tabuleiro (NxN): ")
tabuleiro = criar_tabuleiro(tamanho_tabuleiro)
quantidade_armadilhas = random.randint(3, 6)
quantidade_pistas = random.randint(5, 8)
pos_tesouro = distribuir_elementos(tabuleiro, tamanho_tabuleiro, quantidade_armadilhas, quantidade_pistas)
pos_reveladas = set()
vidas = 3

exibir_tabuleiro(tamanho_tabuleiro, tabuleiro, pos_reveladas)

while True:
    print(f"\nVocê possui {vidas} vidas restantes.")
    x, y = obter_jogada(tamanho_tabuleiro, pos_reveladas)
    pos_reveladas.add((x, y))
    resultado = processar_jogada(tabuleiro,(x, y))

    if resultado == tesouro:
        exibir_tabuleiro(tamanho_tabuleiro, tabuleiro, pos_reveladas)
        print("\nVocê encontrou o TESOURO MÍSTICO! PARABÉNS!")
        break
    elif resultado == armadilha:
        exibir_tabuleiro(tamanho_tabuleiro, tabuleiro, pos_reveladas)
        print("\nVocê caiu em uma ARMADILHA!")
        vidas -= 1
        if vidas == 0:
            print("Suas vidas acabaram!")
            break
    elif resultado == pista:
        dica = conteudo_pistas((x, y), pos_tesouro)
        print(f"\nVocê descobriu uma PISTA: {dica}")
        exibir_tabuleiro(tamanho_tabuleiro, tabuleiro, pos_reveladas)
    elif resultado == vazio:
        print("\nPosição vazia... nada aqui")
        exibir_tabuleiro(tamanho_tabuleiro, tabuleiro, pos_reveladas)