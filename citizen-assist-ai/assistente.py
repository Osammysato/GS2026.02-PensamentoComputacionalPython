# Imports
import csv
import json
import time
from datetime import datetime


class Assistente:
    def __init__(self, nome, base):
        self.nome = nome
        self.base = base            # o Assistente TEM uma BaseConhecimento
        self.historico = []         # lista de dicionários, um por atendimento
        self.caminho_historico = "data/historico.json"

        # Já começa lendo o que foi salvo antes, senão cada execução
        # sobrescreveria o histórico dos testes anteriores.
        self.carregar_historico()

    # ------------------------------------------------------------------ entradas

    def tem_dado_pessoal(self, texto):
        # Somamos todos os dígitos do texto, e não só os que estão juntos:
        # "123.456.789-00" tem pontos e traço no meio, mas continua sendo um CPF.
        contador = 0
        for caractere in texto:
            if caractere.isdigit():
                contador += 1

        # 8 dígitos ou mais já parece CPF/telefone; "@" denuncia um e-mail.
        if contador >= 8 or "@" in texto:
            return True
        else:
            return False

    def ler_opcao(self, mensagem, minimo, maximo):
        # Usado em toda tela que pede número (menus e nota). Só sai daqui
        # quando a pessoa digitar um número entre minimo e maximo.
        while True:
            try:
                opcao = int(input(mensagem))
                if opcao >= minimo and opcao <= maximo:
                    return opcao
                else:
                    print(f"Opção inválida. Digite um número de {minimo} a {maximo}.")
            except ValueError:
                # int() falha com letras ou com a resposta vazia
                print(f"Digite apenas números, de {minimo} a {maximo}.")

    def ler_sim_nao(self, mensagem):
        # Mesma ideia do ler_opcao, mas para respostas s/n.
        # O .strip().lower() faz " S " valer o mesmo que "s".
        while True:
            resposta = input(mensagem).strip().lower()

            if resposta == "s":
                return True
            elif resposta == "n":
                return False
            else:
                print("Resposta inválida. Digite s para sim ou n para não.")

    # ------------------------------------------------------------- atendimento

    def confianca(self, pontos):
        # Regra do enunciado: 6 ou mais é ALTA, de 3 a 5 é MÉDIA.
        # Abaixo de 3 a orientação nem é mostrada, por isso devolve None.
        if pontos >= 6:
            return "ALTA"
        elif pontos >= 3:
            return "MÉDIA"
        else:
            return None

    def perguntar(self):
        # Esses três valores valem para o atendimento inteiro, então ficam fora
        # do laço. Se ficassem dentro, voltariam a zero a cada pergunta.
        inicio = time.time()
        tentativas = 0
        ultima_pergunta = ""

        while True:
            duvida = input("\nDigite sua dúvida (0 para voltar): ")
            pergunta = duvida.strip().lower()

            if pergunta == "0":
                # Só registra se a pessoa tentou e desistiu sem achar resposta.
                # Se ela saiu logo de cara, não houve atendimento.
                if tentativas > 0:
                    tempo = round(time.time() - inicio, 1)
                    self.registrar("pergunta", ultima_pergunta, None, False, False,
                                   tentativas, tempo)
                return

            if pergunta == "":
                print("Você não digitou nada. Escreva sua dúvida.")
                continue

            # A checagem de dado pessoal vem ANTES de contar a tentativa e de buscar:
            # assim o CPF ou e-mail nunca chega ao histórico.
            if self.tem_dado_pessoal(pergunta):
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
                continue

            tentativas += 1
            resultados = self.base.buscar(pergunta)   # lista de (pontos, orientacao)

            # Lista vazia (o JSON não abriu) ou melhor nota abaixo de 3:
            # melhor dizer que não achou do que inventar uma resposta.
            if len(resultados) == 0 or resultados[0][0] < 3:
                print("Não encontrei uma orientação para essa dúvida.")
                print("Tente outras palavras ou procure pelas categorias:",
                      ", ".join(self.base.categorias()))
                ultima_pergunta = pergunta
                continue

            # O buscar() já devolve ordenado, então a primeira tupla é a melhor.
            pontos, melhor = resultados[0]
            print(f"\nConfiança da resposta: {self.confianca(pontos)} ({pontos} pontos)")
            melhor.exibir()

            # Até 2 alternativas: as posições 1 e 2 da lista, mas só se também
            # tiverem 3 pontos ou mais.
            alternativas = []
            for nota, orientacao in resultados[1:3]:
                if nota >= 3:
                    alternativas.append((nota, orientacao))

            if len(alternativas) > 0:
                print("\nOutras orientações que podem ajudar:")
                for nota, orientacao in alternativas:
                    print(f" - {orientacao.titulo} [{orientacao.categoria}] "
                          f"(confiança {self.confianca(nota)}, {nota} pontos)")

            ajudou = self.ler_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
            tempo = round(time.time() - inicio, 1)
            self.registrar("pergunta", pergunta, melhor.id, True, ajudou, tentativas, tempo)
            return

    def navegar(self):
        # Caminho para quem prefere escolher numa lista em vez de digitar a dúvida.
        categorias = self.base.categorias()

        if len(categorias) == 0:
            print("Não há categorias disponíveis no momento.")
            return

        # Laço de fora: lista de categorias. Laço de dentro: orientações da categoria.
        while True:
            print("\n========== CATEGORIAS ==========")
            for numero, categoria in enumerate(categorias, 1):
                print(f"{numero} - {categoria}")
            print("0 - Voltar")

            opcao = self.ler_opcao("Escolha uma categoria (0 para voltar): ", 0, len(categorias))
            if opcao == 0:
                return    # sai do navegar e volta para o menu principal

            # A tela começa no 1, mas a lista começa no índice 0, daí o "- 1".
            categoria = categorias[opcao - 1]
            orientacoes = self.base.por_categoria(categoria)
            inicio = time.time()

            while True:
                print(f"\n========== {categoria.upper()} ==========")
                for numero, orientacao in enumerate(orientacoes, 1):
                    print(f"{numero} - {orientacao.titulo}")
                print("0 - Voltar")

                escolha = self.ler_opcao("Escolha uma orientação (0 para voltar): ", 0,
                                         len(orientacoes))
                if escolha == 0:
                    break    # volta para a lista de categorias

                orientacao = orientacoes[escolha - 1]
                orientacao.exibir()
                ajudou = self.ler_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
                tempo = round(time.time() - inicio, 1)

                # Pela categoria a pessoa sempre chega numa orientação na primeira
                # escolha, por isso conta como 1 tentativa e encontrou=True.
                self.registrar("categoria", orientacao.titulo, orientacao.id, True, ajudou, 1,
                               tempo)
                break    # depois de registrar, volta para a lista de categorias

    # --------------------------------------------------------------- histórico

    def carregar_historico(self):
        try:
            with open(self.caminho_historico, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            # Um JSON pode ser válido e mesmo assim não ser uma lista (ex.: {}).
            if type(dados) == list:
                self.historico = dados
            else:
                print("Aviso: o histórico está em formato inválido. Começando um novo.")
                self.historico = []

        except FileNotFoundError:
            # Normal na primeira execução: o arquivo ainda não existe.
            self.historico = []
        except json.JSONDecodeError:
            print("Aviso: o histórico está corrompido. Começando um novo.")
            self.historico = []

    def salvar_historico(self):
        # ensure_ascii=False mantém os acentos legíveis; indent=4 deixa um campo por linha.
        with open(self.caminho_historico, "w", encoding="utf-8") as arquivo:
            json.dump(self.historico, arquivo, ensure_ascii=False, indent=4)

    def registrar(self, origem, pergunta, id_orientacao, encontrou, ajudou, tentativas, tempo_segundos):
        # Cada atendimento vira um dicionário. A data é pega na hora, e a nota de
        # facilidade fica vazia (None) até a pessoa sair e dar a nota.
        registro = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": tempo_segundos,
            "nota_facilidade": None,
        }

        self.historico.append(registro)
        self.salvar_historico()    # salva na hora, para não perder nada se o programa fechar

    def pedir_nota(self):
        # Chamado quando a pessoa sai do programa.
        nota = self.ler_opcao("De 1 a 5, quão fácil foi usar o assistente? ", 1, 5)

        # Os atendimentos desta sessão são os que ainda estão sem nota.
        # Os de sessões anteriores já têm a nota da sua própria sessão.
        for registro in self.historico:
            if registro["nota_facilidade"] is None:
                registro["nota_facilidade"] = nota

        self.salvar_historico()
        print("Obrigado pela avaliação!")

    # -------------------------------------------------------------- indicadores

    def indicadores(self):
        total = len(self.historico)
        if total == 0:
            # Sem esse retorno, as contas abaixo dividiriam por zero.
            print("Ainda não há atendimentos registrados.")
            return

        encontrados = 0
        ajudaram = 0
        soma_tempo = 0
        soma_tentativas = 0
        soma_notas = 0
        qtd_notas = 0
        sem_solucao = []

        # Uma passada só pelo histórico, juntando tudo o que os indicadores precisam.
        for registro in self.historico:
            soma_tentativas += registro["tentativas"]

            if registro["encontrou"]:
                encontrados += 1
                soma_tempo += registro["tempo_segundos"]

            if registro["ajudou"]:
                ajudaram += 1
            else:
                # Consideramos sem solução tanto o "não encontrei" quanto a
                # orientação que foi mostrada mas não ajudou.
                sem_solucao.append(registro["pergunta"])

            if registro["nota_facilidade"] is not None:
                soma_notas += registro["nota_facilidade"]
                qtd_notas += 1

        print("\n========== INDICADORES ==========")
        print(f"Atendimentos: {total}")
        print(f"Resposta encontrada: {encontrados / total * 100:.1f}%")
        print(f"Taxa de acerto (ajudou): {ajudaram / total * 100:.1f}%")

        # Esses dois só podem ser calculados se houver algo para dividir.
        if encontrados > 0:
            print(f"Tempo médio para encontrar: {soma_tempo / encontrados:.1f} s")
        else:
            print("Tempo médio para encontrar: sem dados")

        print(f"Tentativas por atendimento: {soma_tentativas / total:.1f}")

        if qtd_notas > 0:
            print(f"Facilidade de uso (1 a 5): {soma_notas / qtd_notas:.1f}")
        else:
            print("Facilidade de uso (1 a 5): sem dados")

        print("Dúvidas sem solução:")
        if len(sem_solucao) == 0:
            print(" (nenhuma)")
        for pergunta in sem_solucao:
            print(f" - {pergunta}")

    def exportar_csv(self):
        if len(self.historico) == 0:
            print("Ainda não há atendimentos para exportar.")
            return

        # As colunas são as mesmas chaves do dicionário montado no registrar().
        campos = ["data", "origem", "pergunta", "id_orientacao", "encontrou", "ajudou",
                  "tentativas", "tempo_segundos", "nota_facilidade"]

        # newline="" evita uma linha em branco entre os registros no Windows.
        with open("data/atendimentos.csv", "w", encoding="utf-8", newline="") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(self.historico)

        print("Atendimentos exportados para data/atendimentos.csv")