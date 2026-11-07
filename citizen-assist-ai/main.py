import os

from base_conhecimento import BaseConhecimento
from assistente import Assistente


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    base = BaseConhecimento("data/base_conhecimento.json")
    base.carregar()

    assistente = Assistente("VovóSabeAI", base)

    print(f"\nOlá! Eu sou o {assistente.nome}.")
    print("Eu ajudo a encontrar orientações sobre saúde, benefícios, transporte e direitos.")
    print("Não digite nome, CPF, telefone ou e-mail: eu não preciso desses dados.")

    while True:
        print("\n========== MENU ==========")
        print("1 - Digitar minha dúvida")
        print("2 - Procurar por categorias")
        print("3 - Ver indicadores")
        print("4 - Exportar atendimentos (CSV)")
        print("0 - Sair")

        opcao = assistente.ler_opcao("Escolha uma opção: ", 0, 4)

        if opcao == 1:
            assistente.perguntar()
        elif opcao == 2:
            assistente.navegar()
        elif opcao == 3:
            assistente.indicadores()
        elif opcao == 4:
            assistente.exportar_csv()
        else:
            assistente.pedir_nota()
            print("Até logo! Lembre-se: este assistente NÃO é um canal oficial.")
            break

if __name__ == "__main__":
    main()

