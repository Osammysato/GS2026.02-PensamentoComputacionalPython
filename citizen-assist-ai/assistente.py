# ---------------------------------------------------------------------------
# PASSO 3.1 - Imports
# ---------------------------------------------------------------------------
import datetime, time
import json, csv
import base_conhecimento


# ---------------------------------------------------------------------------
# PASSO 3.2 - Classe e __init__()
# ---------------------------------------------------------------------------
class Assistente:
    def __init__(self, nome, base):
        self.nome = nome
        self.base = base
        self.historico = []
        self.caminho_historico = "data/historico.json"


# ---------------------------------------------------------------------------
# PASSO 3.3 - tem_dado_pessoal()
# ---------------------------------------------------------------------------
    def tem_dado_pessoal(self, texto):
        contador = 0

        for caractere in texto:
            if caractere.isdigit():
                contador += 1

        if contador >= 8 or "@" in texto:
            return True

        else:
            return False


# ---------------------------------------------------------------------------
# PASSO 3.4 - ler_opcao()
# ---------------------------------------------------------------------------
    def ler_opcao(self, mensagem, minimo, maximo):
        while True:
            try:
                opcao = int(input(mensagem))
                if opcao >= minimo and opcao <= maximo:
                    return opcao
                else:
                    print(f"Opção inválida. Digite um número de {minimo} a {maximo}.")
            except ValueError:
                print(f"Digite apenas números, de {minimo} a {maximo}.")


# ---------------------------------------------------------------------------
# PASSO 3.5 - ler_sim_nao()
# ---------------------------------------------------------------------------
    def ler_sim_nao(self, mensagem):
        while True:
            try:
                resposta = input(mensagem).strip().lower()

                if resposta == "s":
                    return True
                elif resposta == "n":
                    return False
                else:
                    print("Digite apenas 's' (Sim) ou 'n' (Não)!!")
            except ValueError:
                print("Digite apenas as letrar s/n")


# ---------------------------------------------------------------------------
# PASSO 3.6 - perguntar()
# ---------------------------------------------------------------------------



# ---------------------------------------------------------------------------
# PASSO 3.7 - navegar()
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# PASSO 3.8 - carregar_historico() e salvar_historico()
# ---------------------------------------------------------------------------



# ---------------------------------------------------------------------------
# PASSO 3.9 - registrar()
# ---------------------------------------------------------------------------



# ---------------------------------------------------------------------------
# PASSO 3.10 - pedir_nota()
# ---------------------------------------------------------------------------



# ---------------------------------------------------------------------------
# PASSO 3.11 - indicadores()
# ---------------------------------------------------------------------------



# ---------------------------------------------------------------------------
# PASSO 3.12 - exportar_csv()
# ---------------------------------------------------------------------------



# ---------------------------------------------------------------------------
# PASSO 3.13 - Testes neste arquivo
# ---------------------------------------------------------------------------







# teste
if __name__ == "__main__":
    import builtins
    import os
    from base_conhecimento import BaseConhecimento

    base = BaseConhecimento("data/base_conhecimento.json")
    base.carregar()

    CAMINHO_TESTE = "data/teste_historico.json"
    CAMINHO_CSV = "data/atendimentos.csv"
    CHAVES = ["data", "origem", "pergunta", "id_orientacao", "encontrou", "ajudou",
              "tentativas", "tempo_segundos", "nota_facilidade"]
    input_original = builtins.input
    resumo = {"ok": 0, "falhou": 0}

    def conferir(descricao, obtido, esperado):
        if obtido == esperado:
            print(f"  OK      {descricao}")
            resumo["ok"] += 1
        else:
            print(f"  FALHOU  {descricao}: esperado {esperado!r}, veio {obtido!r}")
            resumo["falhou"] += 1

    def simular_digitacao(entradas):
        fila = list(entradas)

        def input_falso(mensagem=""):
            if len(fila) == 0:
                raise RuntimeError("o método pediu mais entradas do que o teste previa "
                                   "(aceitou algo errado ou ficou em laço infinito)")
            valor = fila.pop(0)
            print(f"{mensagem}{valor}")
            return valor

        builtins.input = input_falso

    def novo_assistente(base_usada=None):
        if base_usada is None:
            base_usada = base
        assistente = Assistente("Teste", base_usada)
        assistente.caminho_historico = CAMINHO_TESTE
        assistente.historico = []
        return assistente

    def registro_falso(pergunta, id_orientacao, encontrou, ajudou, tentativas, tempo, nota):
        return {"data": "2026-11-10 14:32", "origem": "pergunta", "pergunta": pergunta,
                "id_orientacao": id_orientacao, "encontrou": encontrou, "ajudou": ajudou,
                "tentativas": tentativas, "tempo_segundos": tempo, "nota_facilidade": nota}

    def apagar_historico_teste():
        if os.path.exists(CAMINHO_TESTE):
            os.remove(CAMINHO_TESTE)

    # ---------------------------------------------------------------- 3.3
    def testar_tem_dado_pessoal():
        a = novo_assistente()
        casos = [("meu cpf é 123.456.789-00", True), ("meu email é ana@gmail.com", True),
                 ("12345678", True), ("1234567", False), ("tenho 70 anos", False)]
        for texto, esperado in casos:
            conferir(repr(texto), a.tem_dado_pessoal(texto), esperado)

    # ---------------------------------------------------------------- 3.4
    def testar_ler_opcao():
        a = novo_assistente()
        simular_digitacao(["abc", "", "9", "-1", "2"])
        conferir("abc, vazio, 9 e -1 recusados; 2 aceito (faixa 0 a 3)",
                 a.ler_opcao("Teste: ", 0, 3), 2)
        simular_digitacao(["0"])
        conferir("limite mínimo 0 aceito", a.ler_opcao("Teste: ", 0, 3), 0)
        simular_digitacao(["3"])
        conferir("limite máximo 3 aceito", a.ler_opcao("Teste: ", 0, 3), 3)

    # ---------------------------------------------------------------- 3.5
    def testar_ler_sim_nao():
        a = novo_assistente()
        simular_digitacao(["talvez", "", " S "])
        conferir("talvez e vazio recusados; ' S ' vira True",
                 a.ler_sim_nao("Ajudou? (s/n): "), True)
        simular_digitacao(["N"])
        conferir("'N' vira False", a.ler_sim_nao("Ajudou? (s/n): "), False)

    # ---------------------------------------------------------------- 3.8
    def testar_carregar_e_salvar():
        apagar_historico_teste()
        a = novo_assistente()
        a.carregar_historico()
        conferir("sem arquivo: histórico vazio", a.historico, [])

        a.historico = [{"pergunta": "vacinação"}]
        a.salvar_historico()
        b = novo_assistente()
        b.carregar_historico()
        conferir("salvar e carregar de novo", b.historico, [{"pergunta": "vacinação"}])
        with open(CAMINHO_TESTE, "r", encoding="utf-8") as arquivo:
            conferir("acentos legíveis no arquivo", "vacinação" in arquivo.read(), True)

        for descricao, conteudo in [("corrompido", "[{"), ("que não é lista", "{}")]:
            with open(CAMINHO_TESTE, "w", encoding="utf-8") as arquivo:
                arquivo.write(conteudo)
            c = novo_assistente()
            c.historico = ["lixo"]
            c.carregar_historico()
            conferir(f"arquivo {descricao}: histórico vazio, sem travar", c.historico, [])
        apagar_historico_teste()

    # ---------------------------------------------------------------- 3.9
    def testar_registrar():
        apagar_historico_teste()
        a = novo_assistente()
        a.registrar("pergunta", "como faço o cartão do sus", 1, True, True, 2, 12.4)
        conferir("1 registro no histórico", len(a.historico), 1)
        registro = a.historico[-1]
        conferir("chaves, na ordem", list(registro.keys()), CHAVES)
        conferir("id_orientacao", registro["id_orientacao"], 1)
        conferir("tentativas", registro["tentativas"], 2)
        conferir("tempo_segundos", registro["tempo_segundos"], 12.4)
        conferir("nota_facilidade começa None", registro["nota_facilidade"], None)
        conferir("data no formato AAAA-MM-DD HH:MM (16 caracteres)", len(registro["data"]), 16)
        conferir("historico.json foi salvo", os.path.exists(CAMINHO_TESTE), True)
        apagar_historico_teste()

    # ---------------------------------------------------------------- 3.6
    def testar_perguntar():
        a = novo_assistente()

        simular_digitacao(["Como faço o cartão do SUS?", "s"])
        a.perguntar()
        conferir("cartão do SUS: 1 registro", len(a.historico), 1)
        if len(a.historico) == 1:
            r = a.historico[-1]
            conferir("origem", r["origem"], "pergunta")
            conferir("id_orientacao", r["id_orientacao"], 1)
            conferir("encontrou", r["encontrou"], True)
            conferir("ajudou", r["ajudou"], True)
            conferir("tentativas", r["tentativas"], 1)

        total = len(a.historico)
        simular_digitacao(["meu cpf é 123.456.789-00", "0"])
        a.perguntar()
        conferir("CPF recusado e NÃO registrado", len(a.historico), total)

        simular_digitacao(["", "0"])
        a.perguntar()
        conferir("vazio e depois 0: nada registrado", len(a.historico), total)

        simular_digitacao(["0"])
        a.perguntar()
        conferir("0 logo de início: nada registrado", len(a.historico), total)

        simular_digitacao(["pizza", "bolo", "0"])
        a.perguntar()
        conferir("pizza, bolo e 0: 1 registro novo", len(a.historico), total + 1)
        if len(a.historico) == total + 1:
            r = a.historico[-1]
            conferir("pergunta guardada é a última (bolo)", "bolo" in r["pergunta"], True)
            conferir("id_orientacao", r["id_orientacao"], None)
            conferir("encontrou", r["encontrou"], False)
            conferir("ajudou", r["ajudou"], False)
            conferir("tentativas", r["tentativas"], 2)

        simular_digitacao(["como peço o loas", "n"])
        a.perguntar()
        conferir("loas encontrado (id 2)", a.historico[-1]["id_orientacao"], 2)
        conferir("loas com resposta n: ajudou False", a.historico[-1]["ajudou"], False)

        print("  (base vazia: o próximo aviso de JSON não encontrado é esperado)")
        vazia = BaseConhecimento("data/nao_existe.json")
        vazia.carregar()
        d = novo_assistente(vazia)
        simular_digitacao(["cartão do sus", "0"])
        d.perguntar()
        conferir("base vazia não trava", True, True)
        apagar_historico_teste()

    # ---------------------------------------------------------------- 3.7
    def testar_navegar():
        a = novo_assistente()
        primeira = base.por_categoria(base.categorias()[0])[0]

        simular_digitacao(["1", "1", "s", "0"])
        a.navegar()
        conferir("categoria 1 > orientação 1: 1 registro", len(a.historico), 1)
        if len(a.historico) == 1:
            r = a.historico[-1]
            conferir("origem", r["origem"], "categoria")
            conferir("id_orientacao", r["id_orientacao"], primeira.id)
            conferir("encontrou", r["encontrou"], True)
            conferir("ajudou", r["ajudou"], True)
            conferir("tentativas", r["tentativas"], 1)

        total = len(a.historico)
        simular_digitacao(["1", "0", "0"])
        a.navegar()
        conferir("entrar e voltar com 0: nada registrado", len(a.historico), total)

        simular_digitacao(["x", "99", "0"])
        a.navegar()
        conferir("x e 99 recusados sem travar", len(a.historico), total)
        apagar_historico_teste()

    # ---------------------------------------------------------------- 3.10
    def testar_pedir_nota():
        a = novo_assistente()
        a.historico = [{"nota_facilidade": None}, {"nota_facilidade": 5},
                       {"nota_facilidade": None}]
        simular_digitacao(["9", "0", "4"])
        a.pedir_nota()
        notas = []
        for registro in a.historico:
            notas.append(registro["nota_facilidade"])
        conferir("9 e 0 recusados; 4 só onde era None", notas, [4, 5, 4])
        apagar_historico_teste()

    # ---------------------------------------------------------------- 3.11
    def testar_indicadores():
        a = novo_assistente()
        print("  -- histórico vazio:")
        a.indicadores()
        conferir("histórico vazio não trava", True, True)

        print("  -- ninguém achou resposta nem deu nota:")
        a.historico = [registro_falso("pizza", None, False, False, 2, 8.0, None)]
        a.indicadores()
        conferir("sem encontrados e sem notas não trava (divisão por zero)", True, True)

        print("  -- 4 atendimentos:")
        a.historico = [
            registro_falso("cartão do sus", 1, True, True, 1, 10.0, 5),
            registro_falso("loas", 2, True, False, 2, 20.0, 3),
            registro_falso("pizza", None, False, False, 3, 30.0, None),
            registro_falso("vacina da gripe", 6, True, True, 2, 30.0, 4),
        ]
        a.indicadores()
        print("  CONFIRA NA TELA ACIMA (estes não dá para conferir automaticamente):")
        print("    Resposta encontrada ........ 75%")
        print("    Ajudou ..................... 50% sobre o total, ou 66.7% sobre os encontrados")
        print("    Tempo médio para encontrar . 20.0 s")
        print("    Tentativas por atendimento . 2.0")
        print("    Facilidade de uso .......... 4.0")
        print("    Sem solução ................ pizza (e loas, se contar ajudou=False)")

    # ---------------------------------------------------------------- 3.12
    def testar_exportar_csv():
        backup = None
        if os.path.exists(CAMINHO_CSV):
            with open(CAMINHO_CSV, "r", encoding="utf-8") as arquivo:
                backup = arquivo.read()

        a = novo_assistente()
        a.historico = [registro_falso("cartão do sus", 1, True, True, 1, 10.0, 5),
                       registro_falso("pizza", None, False, False, 3, 30.0, None)]
        a.exportar_csv()
        with open(CAMINHO_CSV, "r", encoding="utf-8", newline="") as arquivo:
            leitor = csv.DictReader(arquivo)
            linhas = list(leitor)
            conferir("cabeçalho = chaves do histórico", leitor.fieldnames, CHAVES)
        conferir("2 linhas de dados (sem linhas em branco)", len(linhas), 2)
        if len(linhas) == 2:
            conferir("acentos preservados", linhas[0]["pergunta"], "cartão do sus")

        a.historico = []
        a.exportar_csv()
        conferir("histórico vazio não trava", True, True)

        if backup is None:
            if os.path.exists(CAMINHO_CSV):
                os.remove(CAMINHO_CSV)
        else:
            with open(CAMINHO_CSV, "w", encoding="utf-8", newline="") as arquivo:
                arquivo.write(backup)

    # ------------------------------------------------- execução dos testes
    # (nome do teste, função de teste, métodos que precisam existir)
    testes = [
        ("3.3 tem_dado_pessoal()", testar_tem_dado_pessoal, ["tem_dado_pessoal"]),
        ("3.4 ler_opcao()", testar_ler_opcao, ["ler_opcao"]),
        ("3.5 ler_sim_nao()", testar_ler_sim_nao, ["ler_sim_nao"]),
        ("3.8 carregar_historico() e salvar_historico()", testar_carregar_e_salvar,
         ["carregar_historico", "salvar_historico"]),
        ("3.9 registrar()", testar_registrar, ["registrar", "salvar_historico"]),
        ("3.6 perguntar()", testar_perguntar,
         ["perguntar", "tem_dado_pessoal", "ler_sim_nao", "registrar", "salvar_historico"]),
        ("3.7 navegar()", testar_navegar,
         ["navegar", "ler_opcao", "ler_sim_nao", "registrar", "salvar_historico"]),
        ("3.10 pedir_nota()", testar_pedir_nota,
         ["pedir_nota", "ler_opcao", "salvar_historico"]),
        ("3.11 indicadores()", testar_indicadores, ["indicadores"]),
        ("3.12 exportar_csv()", testar_exportar_csv, ["exportar_csv"]),
    ]

    for nome, funcao, metodos in testes:
        print(f"\n=== {nome}")
        faltando = []
        for metodo in metodos:
            if not hasattr(Assistente, metodo):
                faltando.append(metodo)
        if len(faltando) > 0:
            print(f"  PULADO  falta escrever: {', '.join(faltando)}")
            continue
        try:
            funcao()
        except Exception as erro:
            print(f"  FALHOU  o teste parou com erro: {type(erro).__name__}: {erro}")
            resumo["falhou"] += 1
        finally:
            builtins.input = input_original

    apagar_historico_teste()
    print(f"\nResumo: {resumo['ok']} OK, {resumo['falhou']} FALHOU")
