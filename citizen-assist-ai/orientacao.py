class Orientacao:
    def __init__(self, id, categoria, titulo, palavras_chave, resposta, documentos, onde, fonte, verificado_em):
        self.id = id
        self.categoria = categoria
        self.titulo = titulo
        self.palavras_chave = palavras_chave
        self.resposta = resposta
        self.documentos = documentos
        self.onde = onde
        self.fonte = fonte
        self.verificado_em = verificado_em

    def exibir(self):
        print(f"Título: {self.titulo}")
        print(f"Resposta: {self.resposta}")
        print("Documentos necessários:")
        for doc in self.documentos:
            print(f"- {doc}")
        print(f"Onde: {self.onde}")
        print(f"Fonte: {self.fonte}")
        print(f"Verificado em: {self.verificado_em}")
        print("Aviso: este assistente NÃO é um canal oficial.")

if __name__ == "__main__":
    # criar uma orientação de teste
    orientacao_teste = Orientacao(
        id=1,
        categoria="Saude",
        titulo="Marcar consulta no posto de saúde",
        palavras_chave=["consulta", "posto", "saúde"],
        resposta="Para marcar uma consulta, vá ao posto de saúde mais próximo com seu Cartão SUS e documento de identidade.",
        documentos=["Cartão SUS", "Documento de identidade"],
        onde="Posto de saúde mais próximo",
        fonte="https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/c/consultas",
        verificado_em="2023-06-15"
    )

    # exibir a orientação de teste
    orientacao_teste.exibir()
