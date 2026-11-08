# GS2026.02-PensamentoComputacionalPython
# Citizen Assist AI — Assistente Digital de Orientação ao Cidadão

Global Solution 2026.2 (desafio CitizenTech) — **Pensamento Computacional e Automação com Python (PCP)** — FIAP

Assistente executado no **terminal**, em **Python puro** (só biblioteca padrão), que responde dúvidas de **idosos** com base em informações verificadas em fontes oficiais. Toda resposta mostra a fonte, a data de verificação e o aviso de que **este assistente NÃO é um canal oficial**. O assistente não pede e não registra dados pessoais.

---

## 👥 Integrantes

| Nome | RM |
|---|---|
| `PREENCHER` | `RMxxxxxx` |
| `PREENCHER` | `RMxxxxxx` |

---

## 🎯 Público e problema

**Público:** pessoas idosas.

**Problema:** muitas pessoas idosas perdem tempo tentando descobrir onde fazer o Cartão SUS, como conseguir a gratuidade no transporte ou quais documentos levar para um serviço público. A informação existe, mas está espalhada, em linguagem técnica e, muitas vezes, misturada com páginas que parecem oficiais e não são.

**Solução:** o Citizen Assist AI reúne orientações verificadas em uma **base de conhecimento** e, a partir de uma pergunta em texto livre ou da navegação por categorias, informa:

1. se existe uma orientação para a dúvida;
2. com que nível de confiança ela foi encontrada (ALTA / MÉDIA);
3. quais documentos são necessários e onde a pessoa deve ir;
4. de onde veio a informação e quando ela foi verificada;
5. se a pessoa resolveu a dúvida e quanto tempo levou.

---

## 🌍 ODS relacionados

- **ODS 3 — Saúde e Bem-Estar:** facilita o acesso a serviços de saúde (Cartão SUS, vacinação, medicamentos).
- **ODS 10 — Redução das Desigualdades:** traduz informação pública para linguagem simples, reduzindo a barreira de acesso para pessoas idosas.
- **ODS 16 — Paz, Justiça e Instituições Eficazes:** direciona o cidadão para canais e fontes oficiais, combatendo páginas falsas.

---

## ▶️ Como executar

Pré-requisito: **Python 3** instalado. Não há bibliotecas externas (nada de `pip install`).

```bash
git clone PREENCHER_LINK_DO_REPOSITORIO
cd citizen-assist-ai
python main.py
```

> No macOS/Linux, use `python3 main.py` caso `python` não esteja disponível.
> O programa deve ser executado **de dentro da pasta do projeto**, porque os caminhos `data/...` são relativos a ela.

---

## 📁 Estrutura do projeto

```
citizen-assist-ai/
├── README.md
├── main.py                  # ponto de entrada: cria a base, carrega o JSON e inicia o assistente
├── orientacao.py            # classe Orientacao
├── base_conhecimento.py     # classe BaseConhecimento (carregar, categorias, busca por pontuação)
├── assistente.py            # classe Assistente (atendimento, histórico, indicadores, CSV)
└── data/
    ├── base_conhecimento.json   # orientações verificadas
    ├── historico.json           # atendimentos registrados (gerado pelo programa)
    └── atendimentos.csv         # exportação dos atendimentos (gerado por exportar_csv())
```

---

## 🧱 Orientação a Objetos (composição)

O sistema é dividido em três classes, ligadas por **composição** (como na Aula 10, em que um `Aluno` tinha uma lista de objetos `Disciplina`):

```
Assistente
└── base: BaseConhecimento
    └── orientacoes: [Orientacao, Orientacao, Orientacao, ...]
```

| Classe | Representa | Atributos | Métodos |
|---|---|---|---|
| `Orientacao` | Uma orientação da base (um registro do JSON) | `id`, `categoria`, `titulo`, `palavras_chave`, `resposta`, `documentos`, `onde`, `fonte`, `verificado_em` | `exibir()` |
| `BaseConhecimento` | O conjunto de todas as orientações | `caminho`, `orientacoes` | `carregar()`, `categorias()`, `por_categoria()`, `pontuar()`, `buscar()` |
| `Assistente` | Quem conversa com o cidadão | `nome`, `base`, `historico` | `perguntar()`, `navegar()`, `registrar()`, `indicadores()`, `exportar_csv()` |

Uso no `main.py`:

```python
base = BaseConhecimento("data/base_conhecimento.json")
base.carregar()                                   # lê o JSON e cria os objetos Orientacao
assistente = Assistente("Citizen Assist AI", base)
assistente.perguntar()                            # usa base.buscar() e orientacao.exibir()
```

---

## 🔎 Regra de pontuação usada (busca inteligente por regras)

### 1. Normalização
Pergunta, palavras-chave e título são comparados **sem acentos, sem pontuação e em minúsculas** pela função `normalizar()`. O texto normalizado recebe um espaço no início e no fim, para que a comparação seja feita por **palavra inteira** (ex.: `" sus "` não casa dentro de `"suspensão"`).

### 2. Pontuação
| Regra | Resultado |
|---|---|
| Palavra-chave da orientação que aparece na pergunta | **+3 pontos** |
| Palavra da pergunta (4 letras ou mais) que aparece no título | **+1 ponto** |

### 3. Confiança
| Melhor pontuação | Resultado |
|---|---|
| 6 pontos ou mais | Confiança **ALTA** |
| 3 a 5 pontos | Confiança **MÉDIA** |
| Menos de 3 pontos | **"Não encontrei"** — o assistente sugere outras palavras ou as categorias. Nunca inventa uma resposta. |

`buscar()` devolve uma **lista de tuplas `(pontos, orientacao)`**, ordenada da maior para a menor pontuação. O assistente mostra a melhor orientação e até **duas alternativas**.

**Exemplo:** em *"Como faço o cartão do SUS?"*, a orientação do Cartão SUS recebe +3 por `cartao do sus`, +3 por `sus` e +1 porque "cartao" está no título: **7 pontos → confiança ALTA**.

**Ajustes de pesos/limites:** `PREENCHER — "nenhum, usamos os pesos do enunciado" ou descrever o ajuste e o motivo`.

---

## 🛡️ Regras de atendimento

- **Navegação por categorias:** categorias e orientações numeradas, com **"0 para voltar"** em todas as telas.
- **Entradas inválidas:** opção fora da faixa, letras, resposta vazia ou s/n inválido **não encerram o programa**.
- **Dados pessoais:** o assistente nunca pede nome, CPF, telefone ou e-mail. Pergunta com **8 ou mais dígitos** ou com **`@`** é recusada (`Atenção: não digite CPF, telefone ou e-mail. Reescreva.`) e **não é registrada** no histórico.
- **Transparência:** toda resposta mostra fonte, data de verificação e o aviso **"este assistente NÃO é um canal oficial"**.
- **Arquivos:** JSON ausente ou corrompido não trava o programa (tratamento com `try/except`).
- **Ao sair:** o assistente pede uma **nota de facilidade de 1 a 5**.

---

## 📊 Histórico, indicadores e CSV

Cada atendimento é salvo em `data/historico.json` como um dicionário com: `data`, `origem` (pergunta ou categoria), `pergunta`, `id` da orientação, `encontrou`, `ajudou`, `tentativas` e `tempo` em segundos (medido com `time.time()`).

Indicadores calculados por `indicadores()`:
- Resposta encontrada (%)
- Taxa de acerto: ajudou (%)
- Tempo médio para encontrar
- Tentativas por atendimento
- Facilidade de uso (1 a 5)
- Lista de dúvidas sem solução

Os atendimentos são exportados para `data/atendimentos.csv` com `csv.DictWriter` (Aula 09).

---

## 🔗 Integrações com outras disciplinas

`PREENCHER — "Não houve integração com outras disciplinas." ou descrever a integração (ex.: COA, DSA, IA) e como ela se conecta à busca por pontuação.`

---

## 📚 Fontes consultadas

Todas as orientações da base usam fonte oficial e têm a data em que a equipe conferiu a informação (campo `verificado_em`).

| Orientação | Fonte oficial | Verificado em |
|---|---|---|
| `PREENCHER (título)` | `PREENCHER (link)` | `AAAA-MM-DD` |
| `PREENCHER` | `PREENCHER` | `AAAA-MM-DD` |
| `...` (uma linha por orientação do JSON) | | |

---

## 🧪 Teste com usuários

Teste realizado com **`PREENCHER` pessoas** de fora da equipe, somando **`PREENCHER` atendimentos**. Nenhum nome ou dado pessoal dos participantes foi registrado.

### Indicadores obtidos

| Indicador | Resultado |
|---|---|
| Resposta encontrada (%) | `PREENCHER` |
| Taxa de acerto: ajudou (%) | `PREENCHER` |
| Tempo médio para encontrar | `PREENCHER` s |
| Tentativas por atendimento | `PREENCHER` |
| Facilidade de uso (1 a 5) | `PREENCHER` |

### Dúvidas sem solução

- `PREENCHER (copiar da lista gerada pelos indicadores)`

### Melhoria feita a partir do teste

`PREENCHER — ex.: "A pergunta 'ônibus de graça' não era encontrada; incluímos a palavra-chave 'onibus de graca' na orientação de gratuidade no transporte e ela passou a ser encontrada com confiança MÉDIA."`

---

## ⚠️ Limitações

- A busca é **por regras** (palavras-chave), não entende o sentido da frase: perguntas com palavras que não estão na base não são encontradas.
- **Erros de digitação** e sinônimos não cadastrados reduzem a pontuação.
- O assistente só responde com o que está na base: tem cobertura limitada às orientações cadastradas.
- As informações podem **ficar desatualizadas**; por isso cada orientação mostra a data de verificação e o link da fonte oficial.
- Funciona apenas no **terminal**, o que pode ser uma barreira para parte do público idoso.
- O bloqueio de dados pessoais é por regra (8+ dígitos ou `@`): pode recusar perguntas legítimas com números longos e não detecta, por exemplo, um nome digitado.

---

## 🎥 Vídeo técnico

`PREENCHER — link do YouTube (não listado)`

---

> **Aviso:** este assistente NÃO é um canal oficial. Sempre confirme as informações na fonte oficial indicada.
