# ---------------------------------------------------------------------------
# PASSO 2.1 - Imports
# ---------------------------------------------------------------------------
import json
import os
from orientacao import Orientacao


# ---------------------------------------------------------------------------
# PASSO 2.2 - Função normalizar()
# ---------------------------------------------------------------------------
ACENTOS = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e",
           "í": "i", "ó": "o", "õ": "o", "ô": "o", "ú": "u", "ç": "c"}


def normalizar(texto):
    # Deixa tudo em minúsculas e tira os espaços das pontas
    texto = texto.lower().strip()

    # Tira acentos
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)

    # Tira pontuação
    for sinal in "?!.,;:()":
        texto = texto.replace(sinal, " ")

    # Deixa um espaço entre as palavras e um espaço em cada ponta
    return " " + " ".join(texto.split()) + " "


# Recebe uma tupla (pontos, orientacao) e devolve só os pontos.
# O buscar() usa esta função para ordenar olhando apenas para a nota.
def pegar_nota(tupla):
    return tupla[0]


# ---------------------------------------------------------------------------
# PASSO 2.3 - Classe e __init__()
# ---------------------------------------------------------------------------
class BaseConhecimento:
    def __init__(self, caminho):
        self.orientacoes = []
        self.caminho = caminho


# ---------------------------------------------------------------------------
# PASSO 2.4 - carregar()
# ---------------------------------------------------------------------------
    def carregar(self):
        self.orientacoes = []

        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            for item in dados:
                orientacao = Orientacao(
                    id=item["id"],
                    categoria=item["categoria"],
                    titulo=item["titulo"],
                    palavras_chave=item["palavras_chave"],
                    resposta=item["resposta"],
                    documentos=item["documentos"],
                    onde=item["onde"],
                    fonte=item["fonte"],
                    verificado_em=item["verificado_em"],
                )

                self.orientacoes.append(orientacao)

        except FileNotFoundError:
            print("O arquivo json não foi encontrado!!")
            self.orientacoes = []

        except json.JSONDecodeError:
            print("O arquivo json está corrompido!!")
            self.orientacoes = []

        except KeyError:
            print("Campo faltando no json")
            self.orientacoes = []

        except TypeError:
            print("O json não está no formato esperado")
            self.orientacoes = []


# ---------------------------------------------------------------------------
# PASSO 2.5 - categorias()
# ---------------------------------------------------------------------------
    def categorias(self):
        lista_categoria = []
        for orientacao in self.orientacoes:
            if orientacao.categoria not in lista_categoria:
                lista_categoria.append(orientacao.categoria)

        return lista_categoria


# ---------------------------------------------------------------------------
# PASSO 2.6 - por_categoria()
# ---------------------------------------------------------------------------
    def por_categoria(self, categoria_recebida):
        resultado = []
        for orientacao in self.orientacoes:
            if orientacao.categoria == categoria_recebida:
                resultado.append(orientacao)

        return resultado


# ---------------------------------------------------------------------------
# PASSO 2.7 - pontuar()
# ---------------------------------------------------------------------------
    def pontuar(self, pergunta, orientacao):
        pontos = 0
        pergunta_normalizada = normalizar(pergunta)
        titulo_normalizado = normalizar(orientacao.titulo)

        for palavra_chave in orientacao.palavras_chave:
            palavra_chave_normalizada = normalizar(palavra_chave)
            if palavra_chave_normalizada in pergunta_normalizada:
                pontos += 3

        palavras_pergunta = pergunta_normalizada.split()
        for palavra in palavras_pergunta:
            if len(palavra) >= 4 and " " + palavra + " " in titulo_normalizado:
                pontos += 1

        return pontos


# ---------------------------------------------------------------------------
# PASSO 2.8 - buscar()
# ---------------------------------------------------------------------------
    def buscar(self, pergunta):
        resultados = []

        for orientacao in self.orientacoes:
            nota_orien = self.pontuar(pergunta, orientacao)
            tupla_notas = (nota_orien, orientacao)
            resultados.append(tupla_notas)

        resultados.sort(key=pegar_nota, reverse=True)
        return resultados


# ---------------------------------------------------------------------------
# PASSO 2.9 - Testes neste arquivo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    base = BaseConhecimento("data/base_conhecimento.json")
    base.carregar()
    print("Orientações:", len(base.orientacoes))
    print("Categorias:", base.categorias())
    print("Em Saúde:", len(base.por_categoria("Saúde")))

    # Cada item do buscar() é uma tupla, separada aqui em pontos e orientacao.
    for pergunta in ["cartão do SUS", "bpc", "pizza", "cita"]:
        print("\nPergunta:", pergunta)
        for pontos, orientacao in base.buscar(pergunta):
            print(f"  {pontos} pontos - {orientacao.titulo}")

    print("\nJSON ausente:")
    base_ausente = BaseConhecimento("data/nao_existe.json")
    base_ausente.carregar()
    print("Orientações:", len(base_ausente.orientacoes))

    # Cada defeito é testado em um arquivo temporário, sem mexer no JSON original.
    caminho_teste = "data/teste_defeito.json"
    defeitos = [
        ("JSON corrompido", '[{"id": 1'),
        ("Campo faltando", '[{"id": 1}]'),
        ("Formato errado", "[1]"),
    ]

    for nome, conteudo in defeitos:
        print(f"\n{nome}:")
        with open(caminho_teste, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)

        base_defeito = BaseConhecimento(caminho_teste)
        base_defeito.carregar()
        print("Orientações:", len(base_defeito.orientacoes))
        os.remove(caminho_teste)