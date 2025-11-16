import random

linhas = 6
colunas = 6
energiaInicial = 100
paredes = 6
armadilhas = 5
visao = 1
ranking_file = "ranking.txt"

JOGADOR = "🤠"
PAREDE = "🧱"
SAIDA = "🚪"
VAZIO = "·"

def criarLabirinto():
    labirinto = [[VAZIO for _ in range(colunas)] for _ in range(linhas)]
    
    def pos_valida(x, y):
        return (0 <= x < linhas) and (0 <= y < colunas) and (x, y) != (0, 0)

    for _ in range(paredes):
        while True:
            x, y = random.randint(0, linhas-1), random.randint(0, colunas-1)
            if pos_valida(x, y) and labirinto[x][y] == VAZIO:
                labirinto[x][y] = PAREDE
                break

    for _ in range(armadilhas):
        while True:
            x, y = random.randint(0, linhas-1), random.randint(0, colunas-1)
            if pos_valida(x, y) and labirinto[x][y] == VAZIO:
                labirinto[x][y] = 'A'
                break

    while True:
        x, y = random.randint(0, linhas-1), random.randint(0, colunas-1)
        if pos_valida(x, y) and labirinto[x][y] == VAZIO:
            labirinto[x][y] = SAIDA
            break

    labirinto[0][0] = JOGADOR
    return labirinto

def mostrarLabirinto(labirinto, jogador):
    jx, jy = jogador
    for x in range(linhas):
        linha = []
        for y in range(colunas):

            dist = abs(x - jx) + abs(y - jy)

            if dist <= visao:
                cel = labirinto[x][y]

                if cel == 'A':
                    linha.append('?')
                else:
                    if cel == VAZIO and random.random() < 0.20:
                        linha.append('?')
                    else:
                        linha.append(cel)
            else:
                linha.append(' ')
        print(" ".join(linha))
    print()

def moverJogador(labirinto, posicao, energia):
    x, y = posicao
    movimento = input("Movimento (W/A/S/D): ").upper()

    if movimento == 'W': x -= 1
    elif movimento == 'S': x += 1
    elif movimento == 'A': y -= 1
    elif movimento == 'D': y += 1
    else:
        print("Comando inválido!")
        return posicao, energia, False

    if x < 0 or x >= linhas or y < 0 or y >= colunas:
        print("🚧 Você bateu na parede!")
        return posicao, energia, False

    if labirinto[x][y] == PAREDE:
        print("🧱 Parede bloqueia o caminho!")
        return posicao, energia, False

    energia -= 1

    if labirinto[x][y] == 'A':
        print("💀 Armadilha! (-10 energia)")
        energia -= 10
        labirinto[x][y] = VAZIO

    if labirinto[x][y] == SAIDA:
        print("🎉 Você encontrou a saída!")
        labirinto[posicao[0]][posicao[1]] = VAZIO
        labirinto[x][y] = JOGADOR
        return (x, y), energia, True

    labirinto[posicao[0]][posicao[1]] = VAZIO
    labirinto[x][y] = JOGADOR
    return (x, y), energia, False

def salvarRanking(nome, pontuacao):
    with open(ranking_file, 'a') as f:
        f.write(f"{nome}:{pontuacao}\n")

def mostrarRanking():
    print("\n=== 📊 RANKING ===")

    try:
        with open(ranking_file, "r") as f:
            dados = f.readlines()

        if not dados:
            print("Nenhum jogador registrado ainda.\n")
            return

        lista = [d.strip().split(":") for d in dados]
        lista = sorted(lista, key=lambda x: int(x[1]), reverse=True)

        for pos, (nome, energia) in enumerate(lista, start=1):
            print(f"{pos}. {nome} — {energia} energia")

    except FileNotFoundError:
        print("Ranking ainda não existe.\n")

def jogar():
    nome = input("Digite seu nome: ")
    labirinto = criarLabirinto()
    posicao = (0, 0)
    energia = energiaInicial
    vitoria = False

    print("\n=== 🏰 FUGA DA MASMORRA ===")
    mostrarLabirinto(labirinto, posicao)

    while energia > 0 and not vitoria:
        posicao, energia, vitoria = moverJogador(labirinto, posicao, energia)
        print(f"⚡ Energia: {energia}")
        mostrarLabirinto(labirinto, posicao)

    if energia <= 0:
        print("💀 Você ficou sem energia e perdeu!")
    elif vitoria:
        print(f"🏆 Parabéns! Você escapou com {energia} de energia!")

    salvarRanking(nome, energia)

while True:
    print("=== MENU PRINCIPAL ===")
    print("1 - Iniciar Jogo")
    print("2 - Ver Ranking")
    print("3 - Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == '1':
        jogar()
    elif opcao == '2':
        mostrarRanking()
    elif opcao == '3':
        print("👋 Saindo do jogo...")
        break
    else:
        print("❌ Opção inválida! Tente novamente.\n")