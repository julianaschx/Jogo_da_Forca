import pygame
import random
import sys
import json
import time
import textwrap

pygame.init()
largura, altura = 600, 400
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo da Forca - Lógica Matemática")

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA_CLARO = (200, 200, 200)

fonte_titulo = pygame.font.Font("PressStart2P.ttf", 20)
fonte_palavra = pygame.font.Font("PressStart2P.ttf", 25)
fonte_mensagem = pygame.font.Font("PressStart2P.ttf", 15)
fonte_pergunta = pygame.font.Font("PressStart2P.ttf", 12)
fonte_dicas = pygame.font.Font("PressStart2P.ttf", 12)
fonte_dicas.set_bold(True)

nickname = ""
pontuacao = 0
ranking_file = "ranking.json"
tempo_inicial = 0
letras_adivinhadas = set()
letras_erradas = set()

som_clique = pygame.mixer.Sound("clique.wav")
som_acerto = pygame.mixer.Sound("acerto.wav")
som_erro = pygame.mixer.Sound("erro.wav")
pygame.mixer.music.load("musica_fundo.mp3")
pygame.mixer.music.play(-1)

fundo_tematica = pygame.image.load("fundo_tematica.jpg")
fundo_tematica = pygame.transform.scale(fundo_tematica, (largura, altura))


palavras = {
    "LogicaMatematica": {
        "PROPOSICAO": ("O que representa uma sentença que pode ser verdadeira ou falsa?",
                       ["É a base da lógica", "Pode ser afirmativa ou negativa", "Tem valor lógico"]),
        "CONJUNCAO": ("Qual operação lógica retorna verdadeiro se ambas as proposições forem verdadeiras?",
                      ["Combina duas proposições", "Ligada pela palavra 'e'", "Usada em lógica formal"]),
        "DISJUNCAO": ("Qual operação lógica retorna verdadeiro se pelo menos uma proposição for verdadeira?",
                      ["Ligada pela palavra 'ou'", "É verdadeira em múltiplas condições", "Usada em lógica formal"]),
        "NEGACAO": ("Qual operação lógica inverte o valor lógico de uma proposição?",
                    ["Transforma verdadeiro em falso e vice-versa", "Usa-se a palavra 'não'",
                     "Usada para inverter proposições"]),
        "TAUTOLOGIA": ("Qual proposição é sempre verdadeira?",
                       ["É verdadeira em todos os casos", "Não depende das proposições", "É uma verdade lógica"]),
        "CONTRADICAO": ("Qual proposição é sempre falsa?",
                        ["É falsa em todos os casos", "Não depende das proposições", "Representa um absurdo lógico"]),
        "IMPLICACAO": ("Qual operação lógica indica que uma proposição implica outra?",
                       ["Relaciona duas proposições", "Usa-se a expressão 'se... então'",
                        "É a base do raciocínio dedutivo"]),
        "BICONDICIONAL": ("Qual operação lógica é verdadeira se ambas as proposições tiverem o mesmo valor lógico?",
                          ["Relaciona duas proposições", "Usa-se a expressão 'se e somente se'", "É simétrica"]),
        "VERDADE": ("Qual é o valor lógico de uma proposição verdadeira?",
                    ["Um dos dois valores possíveis", "O oposto de falso", "Representa uma afirmação correta"]),
        "FALSO": ("Qual é o valor lógico de uma proposição falsa?",
                  ["Um dos dois valores possíveis", "O oposto de verdadeiro", "Representa uma afirmação incorreta"]),
        "DEDUCAO": ("Qual é o processo lógico que parte de premissas para uma conclusão?",
                    ["Usa-se para chegar a conclusões", "Base do raciocínio lógico", "Parte de premissas"]),
        "INDUCAO": ("Qual é o processo lógico que parte de casos específicos para uma generalização?",
                    ["Base do raciocínio experimental", "Usa-se para gerar hipóteses", "Parte do particular"]),
        "INFERENCIA": ("Qual é o processo de derivar uma conclusão a partir de premissas?",
                       ["Base para deduções", "Relaciona proposições", "Conduz a uma conclusão"]),
        "AXIOMA": ("Qual é uma proposição aceita como verdadeira sem prova?",
                   ["Base de sistemas lógicos", "Não precisa de demonstração", "É uma verdade inicial"]),
        "PARADOXO": ("Qual é uma afirmação que contradiz a lógica tradicional?",
                     ["Desafia a lógica", "Pode ser verdadeiro e falso", "Exemplo: Paradoxo do mentiroso"]),
        "SILOGISMO": ("Qual é uma forma de argumento dedutivo com duas premissas e uma conclusão?",
                      ["Base da lógica aristotélica", "Duas premissas levam a uma conclusão", "Usado em deduções"]),
        "PREMISSA": ("Qual é uma afirmação que serve de base para um argumento?",
                     ["Fundamento de uma conclusão", "Base das inferências", "Utilizada em raciocínio lógico"]),
        "PROVA": ("Qual é o processo de demonstração da verdade de uma proposição?",
                  ["Base da lógica formal", "Usa-se para validar proposições", "Demonstra a validade"]),
        "ARGUMENTO": ("Qual é uma sequência de proposições que levam a uma conclusão?",
                      ["Usado em raciocínio dedutivo", "Leva a uma conclusão lógica", "Base para raciocínio lógico"]),
        "VALIDADE": ("Qual é a propriedade de um argumento onde a conclusão segue logicamente das premissas?",
                     ["Base da lógica formal", "Indica coerência lógica", "Essencial em deduções"]),
        "CONTINGENCIA": ("Qual é uma proposição que pode ser verdadeira ou falsa dependendo das circunstâncias?",
                         ["Não é sempre verdadeira", "Não é sempre falsa", "Depende do contexto"]),
        "INCONSISTENCIA": ("Qual é uma situação onde premissas levam a conclusões contraditórias?",
                           ["Contradição lógica", "Dificulta a validação", "Inviabiliza conclusões"]),
        "EQUIVALENCIA": (
        "Qual é a relação lógica entre proposições com o mesmo valor lógico em todas as circunstâncias?",
        ["Lógica simétrica", "Usada em bicondicionais", "Valores idênticos"]),
        "CONDICAO": ("Qual é uma proposição que liga duas proposições usando 'se... então'?",
                     ["Base para inferência", "Condição necessária", "Implica uma relação"]),
        "REFLEXIVIDADE": ("Qual é a propriedade de uma relação onde todo elemento está relacionado consigo mesmo?",
                          ["Propriedade relacional", "Usado em lógica de conjuntos", "Simetria reflexiva"]),
        "TRANSITIVIDADE": (
        "Qual é a propriedade de uma relação onde se A está relacionado com B e B com C, então A está com C?",
        ["Propriedade relacional", "Base em lógica matemática", "É transitiva"]),
        "LEI_DE_MORGAN": ("Qual lei afirma que a negação de uma conjunção é a disjunção das negações?",
                          ["Usada em lógica proposicional", "Inverte operadores", "Simplifica expressões"]),
        "QUANTIFICADOR_UNIVERSAL": ("Qual quantificador indica que uma propriedade é válida para todos os elementos?",
                                    ["Representado por ∀", "Afirma validade geral", "Usado em lógica matemática"]),
        "QUANTIFICADOR_EXISTENCIAL": (
        "Qual quantificador indica que existe pelo menos um elemento com uma propriedade?",
        ["Representado por ∃", "Afirma existência", "Usado em lógica matemática"]),
        "CONTRAPOSICAO": ("Qual é a afirmação inversa de uma implicação?",
                          ["Inverte e nega", "Relacionada à implicação", "É logicamente equivalente"]),
        "CONTRARRECIPROCA": ("Qual é a forma inversa e negada de uma proposição condicional?",
                             ["Inverte e nega proposições", "Relacionada à implicação", "Equivalente lógica"]),
        "SIMETRIA": ("Qual é a propriedade de uma relação que se mantém inalterada ao inverter seus elementos?",
                     ["Propriedade reflexiva", "Usada em relações binárias", "Simetria lógica"]),
        "IMPLICACAO_LOGICA": (
        "Qual operação lógica é verdadeira quando uma proposição verdadeira implica outra verdadeira?",
        ["Relaciona proposições", "Forma 'se... então'", "É uma dedução"]),
        "COMUTATIVIDADE": ("Qual propriedade lógica permite trocar a ordem dos elementos sem alterar o resultado?",
                           ["Ordem não importa", "Usada em soma e multiplicação", "Simetria lógica"]),
        "ASSOCIATIVIDADE": ("Qual propriedade permite agrupar proposições de forma diferente sem alterar o valor?",
                            ["Não altera resultado", "Usada em operações", "Agrupamento de elementos"]),
        "NECESSIDADE": ("Qual termo indica uma condição que deve estar presente para algo ser verdadeiro?",
                        ["Condição essencial", "Sem ela, o resultado falha", "É obrigatório"]),
        "SUFICIENCIA": ("Qual termo indica que uma condição basta para tornar algo verdadeiro?",
                        ["Condição completa", "Torna o evento certo", "É suficiente para a conclusão"]),
        "IMPROPRIEDADE": ("Qual termo descreve uma proposição que não é relevante para o resultado?",
                          ["Não afeta o resultado", "Irrelevância lógica", "Desconexa"]),
        "PREDICADO": ("Qual termo descreve a propriedade atribuída aos elementos em uma proposição?",
                      ["Atribuição de valor", "Relaciona com elementos", "Usado em proposições"]),
        "CONSISTENCIA": ("Qual propriedade lógica indica ausência de contradições?",
                         ["Sem conflito", "Fundamental para lógica", "Indica harmonia"]),
        "NECESSIDADE_E_SUFICIENCIA": ("Qual condição é simultaneamente necessária e suficiente?",
                                      ["As duas condições juntas", "Garante o resultado", "Não depende de outra"]),
        "BIVALENCIA": ("Qual princípio lógico afirma que proposições são verdadeiras ou falsas, mas não ambas?",
                       ["Dois valores lógicos", "A lógica clássica depende", "É ou verdadeiro ou falso"]),
        "DISJUNCAO_EXCLUSIVA": ("Qual operação lógica indica que apenas uma das proposições pode ser verdadeira?",
                                ["Ligada por 'ou exclusivo'", "Só uma é verdadeira", "Usada para alternativas únicas"]),
        "UNIVERSALIDADE": ("Qual conceito abrange todos os elementos de um conjunto?",
                           ["Abrangência total", "Representa todos", "Afirma validade para todos"]),
        "IMPLICA_CONTRA": ("Qual proposição negativa reflete uma implicação inversa?",
                           ["Inversão e negação", "Equivalente inversa", "Relação de contrários"])
    }
}


def salvar_ranking(nickname, pontuacao, tempo_jogo):
    try:
        with open(ranking_file, 'r') as f:
            ranking = json.load(f)
    except FileNotFoundError:
        ranking = []
    ranking.append({"nickname": nickname, "pontuacao": pontuacao, "tempo": round(tempo_jogo, 2)})
    ranking = sorted(ranking, key=lambda x: (-x['pontuacao'], x['tempo']))[:10]
    with open(ranking_file, 'w') as f:
        json.dump(ranking, f)


def carregar_ranking():
    try:
        with open(ranking_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def escolher_palavra():
    global categoria, palavra, pergunta, dicas, letras_adivinhadas, letras_erradas
    categoria, palavras_categ = random.choice(list(palavras.items()))
    palavra, (pergunta, dicas) = random.choice(list(palavras_categ.items()))
    letras_adivinhadas = set()
    letras_erradas = set()


def desenhar_balao_dica(texto, x, y, largura_maxima):
    linhas = textwrap.wrap(texto, width=largura_maxima)
    largura_balao = max(fonte_dicas.size(linha)[0] for linha in linhas) + 20
    altura_balao = len(linhas) * 20 + 20
    balao_rect = pygame.Rect(x - 10, y - 10, largura_balao, altura_balao)

    pygame.draw.rect(tela, BRANCO, balao_rect)
    pygame.draw.rect(tela, PRETO, balao_rect, 2)

    for i, linha in enumerate(linhas):
        texto_surface = fonte_dicas.render(linha, True, PRETO)
        tela.blit(texto_surface, (x, y + i * 20))


def mostrar_pergunta_e_dicas():
    rodando = True
    while rodando:
        tela.blit(fundo_tematica, (0, 0))

        desenhar_balao_dica(pergunta.upper(), 50, 40, 35)
        for i, dica in enumerate(dicas):
            desenhar_balao_dica(f"DICA {i + 1}: {dica.upper()}", 50, 100 + i * 50, 35)

        botao_proximo = pygame.Rect(largura // 2 - 70, altura - 60, 140, 30)
        pygame.draw.rect(tela, CINZA_CLARO, botao_proximo)
        tela.blit(fonte_mensagem.render("PRÓXIMO", True, PRETO), (botao_proximo.x + 10, botao_proximo.y + 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if botao_proximo.collidepoint(event.pos):
                    som_clique.play()
                    rodando = False
                    iniciar_jogo_forca()
        pygame.display.flip()


def mostrar_ranking():
    rodando = True
    ranking = carregar_ranking()
    while rodando:
        tela.blit(fundo_tematica, (0, 0))
        titulo = fonte_titulo.render("Ranking", True, PRETO)
        tela.blit(titulo, (largura // 2 - titulo.get_width() // 2, 20))

        tabela_rect = pygame.Rect(50, 60, 500, 260)
        pygame.draw.rect(tela, BRANCO, tabela_rect)
        pygame.draw.rect(tela, PRETO, tabela_rect, 2)

        cabecalho = ["Pos", "Nickname", "Pts", "Tempo"]
        colunas_largura = [50, 150, 100, 100]
        for i, col in enumerate(cabecalho):
            coluna_texto = fonte_mensagem.render(col, True, PRETO)
            tela.blit(coluna_texto, (tabela_rect.x + sum(colunas_largura[:i]), tabela_rect.y + 10))

        for i, entry in enumerate(ranking):
            texto_ranking = [
                f"{i + 1}", entry['nickname'],
                str(entry['pontuacao']), f"{entry['tempo']}s"
            ]
            for j, texto in enumerate(texto_ranking):
                texto_render = fonte_mensagem.render(texto, True, PRETO)
                tela.blit(texto_render, (tabela_rect.x + sum(colunas_largura[:j]), tabela_rect.y + 40 + i * 20))

            pygame.draw.line(tela, PRETO, (tabela_rect.x, tabela_rect.y + 35 + i * 20),
                             (tabela_rect.x + tabela_rect.width, tabela_rect.y + 35 + i * 20), 1)

        botao_voltar = pygame.Rect(largura // 2 - 60, altura - 50, 120, 30)
        pygame.draw.rect(tela, CINZA_CLARO, botao_voltar)
        tela.blit(fonte_mensagem.render("VOLTAR", True, PRETO), (botao_voltar.x + 10, botao_voltar.y + 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if botao_voltar.collidepoint(event.pos):
                    som_clique.play()
                    rodando = False
                    tela_inicial()
        pygame.display.flip()


def iniciar_jogo_forca():
    global pontuacao, tempo_inicial, letras_adivinhadas, letras_erradas
    pontuacao = 0
    tempo_inicial = time.time()
    jogo_forca()


def desenhar_forca(erros):
    # Desenho da estrutura da forca
    pygame.draw.rect(tela, PRETO, (100, 100, 8, 200))
    pygame.draw.rect(tela, PRETO, (100, 100, 80, 8))
    pygame.draw.rect(tela, PRETO, (180, 100, 8, 40))
    pygame.draw.rect(tela, PRETO, (60, 300, 80, 8))


def desenhar_boneco(erros):
    # Desenho do boneco dependendo da quantidade de erros
    if erros > 0:
        pygame.draw.circle(tela, PRETO, (185, 145), 10)  # cabeça
    if erros > 1:
        pygame.draw.line(tela, PRETO, (185, 155), (185, 185), 2)  # tronco
    if erros > 2:
        pygame.draw.line(tela, PRETO, (185, 160), (170, 170), 2)  # braço esquerdo
    if erros > 3:
        pygame.draw.line(tela, PRETO, (185, 160), (200, 170), 2)  # braço direito
    if erros > 4:
        pygame.draw.line(tela, PRETO, (185, 185), (175, 200), 2)  # perna esquerda
    if erros > 5:
        pygame.draw.line(tela, PRETO, (185, 185), (195, 200), 2)  # perna direita


def desenhar_tracos():
    espaco_entre_tracos = 20
    x = 220
    y = 300
    for letra in palavra:
        if letra in letras_adivinhadas:
            letra_texto = fonte_palavra.render(letra, True, PRETO)
            tela.blit(letra_texto, (x, y - 30))
        else:
            pygame.draw.line(tela, PRETO, (x, y), (x + 15, y), 2)
        x += espaco_entre_tracos


def jogo_forca():
    global pontuacao
    rodando = True
    erros = 0
    while rodando:
        tela.blit(fundo_tematica, (0, 0))
        desenhar_forca(erros)
        desenhar_boneco(erros)
        desenhar_tracos()

        # Mostrar o tempo de jogo e pontuação
        tempo_jogo = time.time() - tempo_inicial
        tempo_texto = fonte_mensagem.render(f"Tempo: {round(tempo_jogo, 2)}s", True, PRETO)
        pontuacao_texto = fonte_mensagem.render(f"Pontuação: {pontuacao}", True, PRETO)
        letras_erradas_texto = fonte_mensagem.render(f"Letras erradas: {', '.join(sorted(letras_erradas))}", True,
                                                     PRETO)

        tela.blit(tempo_texto, (10, 10))
        tela.blit(pontuacao_texto, (10, 30))
        tela.blit(letras_erradas_texto, (10, altura - 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                letra = pygame.key.name(event.key).upper()
                if letra.isalpha() and letra not in letras_adivinhadas and letra not in letras_erradas:
                    if letra in palavra:
                        letras_adivinhadas.add(letra)
                        som_acerto.play()
                        pontuacao += 10
                    else:
                        letras_erradas.add(letra)
                        erros += 1
                        som_erro.play()

        if erros >= 6:
            salvar_ranking(nickname, pontuacao, tempo_jogo)
            rodando = False
            mostrar_ranking()
        elif set(palavra) <= letras_adivinhadas:
            pontuacao += 10
            salvar_ranking(nickname, pontuacao, tempo_jogo)
            rodando = False
            mostrar_ranking()

        pygame.display.flip()


def tela_inicial():
    global nickname
    entrada_ativa = False
    rodando = True
    while rodando:
        input_rect, botao_iniciar, botao_ranking = desenhar_tela_inicial()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    entrada_ativa = True
                else:
                    entrada_ativa = False
                if botao_iniciar.collidepoint(event.pos) and nickname:
                    som_clique.play()
                    rodando = False
                    escolher_palavra()
                    mostrar_pergunta_e_dicas()
                elif botao_ranking.collidepoint(event.pos):
                    som_clique.play()
                    rodando = False
                    mostrar_ranking()
            elif event.type == pygame.KEYDOWN and entrada_ativa:
                if event.key == pygame.K_BACKSPACE:
                    nickname = nickname[:-1]
                elif len(nickname) < 10:
                    nickname += event.unicode
        pygame.display.flip()


def desenhar_tela_inicial():
    tela.blit(fundo_tematica, (0, 0))
    titulo = fonte_titulo.render("Jogo da Forca", True, PRETO)
    tela.blit(titulo, (largura // 2 - titulo.get_width() // 2, 30))
    texto_nickname = fonte_mensagem.render("Nickname:", True, PRETO)
    tela.blit(texto_nickname, (largura // 2 - 70, altura // 2 - 100))

    input_rect = pygame.Rect(largura // 2 - 60, altura // 2 - 70, 120, 30)
    pygame.draw.rect(tela, BRANCO, input_rect)
    pygame.draw.rect(tela, PRETO, input_rect, 2)

    text_surface = fonte_mensagem.render(nickname, True, PRETO)
    tela.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

    botao_iniciar = pygame.Rect(largura // 2 - 60, altura // 2, 120, 40)
    botao_ranking = pygame.Rect(largura // 2 - 60, altura // 2 + 60, 120, 40)

    pygame.draw.rect(tela, CINZA_CLARO, botao_iniciar)
    pygame.draw.rect(tela, CINZA_CLARO, botao_ranking)

    tela.blit(fonte_mensagem.render("INICIAR", True, PRETO), (botao_iniciar.x + 10, botao_iniciar.y + 10))
    tela.blit(fonte_mensagem.render("RANKING", True, PRETO), (botao_ranking.x + 10, botao_ranking.y + 10))

    return input_rect, botao_iniciar, botao_ranking


def main():
    try:
        tela_inicial()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()