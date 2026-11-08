# VovóSabeAI — Citizen Assist AI para pessoas idosas

Global Solution 2026.2 (desafio CitizenTech) — **Pensamento Computacional e Automação com Python (PCP)** — FIAP

Assistente executado no **terminal**, em **Python puro** (só biblioteca padrão), que responde dúvidas de **idosos** com base em informações verificadas em fontes oficiais. Toda resposta mostra a fonte, a data de verificação e o aviso de que **este assistente NÃO é um canal oficial**. O assistente não pede e não registra dados pessoais.

---

## 👥 Integrantes

| Nome | RM |
|---|---|
| Sammy Sato | RM 569182 |
| Gabriel Pedro de Souza | RM 571995 |

---

## 🎯 Público e problema

**Público:** pessoas idosas.

**Problema:** muitas pessoas idosas perdem tempo tentando descobrir onde fazer o Cartão SUS, como conseguir a gratuidade no transporte ou quais documentos levar para um serviço público. A informação existe, mas está espalhada, em linguagem técnica e, muitas vezes, misturada com páginas que parecem oficiais e não são.

**Solução:** o VovóSabeAI reúne orientações verificadas em uma **base de conhecimento** e, a partir de uma pergunta em texto livre ou da navegação por categorias, informa:

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
git clone https://github.com/Osammysato/GS2026.02-PensamentoComputacionalPython.git
cd GS2026.02-PensamentoComputacionalPython/citizen-assist-ai
python main.py
```

> No macOS/Linux, use `python3 main.py` caso `python` não esteja disponível.
> O `main.py` muda a pasta de trabalho para a pasta do projeto (`os.chdir`), então os caminhos `data/...` funcionam mesmo se o programa for chamado de outra pasta.

### Menu principal

```
1 - Digitar minha dúvida        → perguntar()
2 - Procurar por categorias     → navegar()
3 - Ver indicadores             → indicadores()
4 - Exportar atendimentos (CSV) → exportar_csv()
0 - Sair                        → pede a nota de facilidade (1 a 5)
```

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
assistente = Assistente("VovóSabeAI", base)       # o Assistente TEM uma BaseConhecimento
assistente.perguntar()                            # usa base.buscar() e orientacao.exibir()
```

Além dos métodos mínimos, o `Assistente` tem métodos de apoio: `ler_opcao()` e `ler_sim_nao()` (validação de entradas), `tem_dado_pessoal()` (bloqueio de CPF/telefone/e-mail), `confianca()` (ALTA/MÉDIA), `carregar_historico()`, `salvar_historico()` e `pedir_nota()`.

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

**Exemplo:** em *"Como faço o cartão do SUS?"*, a orientação 1 (Cartão SUS) recebe +3 por `cartao do sus`, +3 por `sus` e +1 porque "cartao" está no título: **7 pontos → confiança ALTA**.

**Ajustes de pesos/limites:** nenhum. Usamos os pesos e limites do enunciado. As alternativas só aparecem se também tiverem 3 pontos ou mais.

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

Cada atendimento é salvo em `data/historico.json` como um dicionário com: `data`, `origem` (pergunta ou categoria), `pergunta`, `id_orientacao`, `encontrou`, `ajudou`, `tentativas`, `tempo_segundos` (medido com `time.time()`) e `nota_facilidade` (preenchida quando a pessoa sai). O histórico é salvo a cada atendimento e carregado ao abrir o programa, então os testes de várias sessões se acumulam.

**Dúvida sem solução:** consideramos tanto a pergunta que não foi encontrada quanto a orientação que foi exibida mas não ajudou (resposta "n").

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

Não houve integração com outras disciplinas. Toda a "inteligência" do assistente é a busca por pontuação descrita acima, em Python puro.

---

## 📚 Fontes consultadas

Todas as orientações da base usam fonte oficial e têm a data em que a equipe conferiu a informação (campo `verificado_em`).

| # | Orientação | Categoria | Fonte oficial | Verificado em |
|---|---|---|---|---|
| 1 | Cartão SUS (Cartão Nacional de Saúde) | Saúde | [gov.br/saude](https://www.gov.br/saude/pt-br/assuntos/noticias/2025/setembro/ministerio-da-saude-comeca-a-emitir-cartao-sus-com-base-no-cpf) | 2026-11-07 |
| 2 | BPC/LOAS | Benefícios | [gov.br — Benefício assistencial ao idoso](https://www.gov.br/pt-br/servicos/solicitar-beneficio-assistencial-ao-idoso) | 2026-11-07 |
| 3 | Prova de vida do INSS | Benefícios | [INSS — FAQ Prova de Vida](https://www.gov.br/inss/pt-br/noticias/prova-de-vida/FAQProvadeVida.pdf) | 2026-11-07 |
| 4 | Cadastro Único (CadÚnico) | Benefícios | [gov.br — Cadastro Único](https://www.gov.br/pt-br/servicos/inscrever-se-no-cadastro-unico-para-programas-sociais-do-governo-federal) | 2026-11-07 |
| 5 | Farmácia Popular | Saúde | [gov.br — Farmácia Popular](https://www.gov.br/saude/pt-br/assuntos/farmaciapopular) | 2026-11-07 |
| 6 | Vacina da gripe (influenza) | Saúde | [Ministério da Saúde — Campanha contra a influenza](https://www.gov.br/saude/pt-br/assuntos/noticias/2026/marco/dia-d-campanha-nacional-de-vacinacao-contra-a-influenza-comeca-neste-sabado-28) | 2026-11-07 |
| 7 | Carteira da Pessoa Idosa | Transporte | [gov.br — Carteira da Pessoa Idosa](https://www.gov.br/pt-br/servicos/adquirir-carteira-do-idoso) | 2026-11-07 |
| 8 | Ônibus de graça (65+) | Transporte | [Estatuto da Pessoa Idosa — Lei 10.741/2003](https://www.planalto.gov.br/ccivil_03/leis/2003/l10.741.htm) | 2026-11-07 |
| 9 | Atendimento prioritário (60+) | Direitos | [Estatuto da Pessoa Idosa — Lei 10.741/2003](https://www.planalto.gov.br/ccivil_03/leis/2003/l10.741.htm) | 2026-11-07 |
| 10 | Denúncia de violência (Disque 100) | Direitos | [gov.br — Denunciar violação de direitos humanos](https://www.gov.br/pt-br/servicos/denunciar-violacao-de-direitos-humanos) | 2026-11-07 |

---

## 🧪 Teste com usuários

Teste realizado em 08/11/2026 com **3 pessoas** de fora da equipe, somando **12 atendimentos**: 8 por pergunta digitada e 4 pela navegação por categorias. Nenhum nome ou dado pessoal dos participantes foi registrado. Os registros estão em `data/historico.json` e `data/atendimentos.csv`.

### Indicadores obtidos

| Indicador | Resultado |
|---|---|
| Resposta encontrada (%) | 83,3% (10 de 12) |
| Taxa de acerto: ajudou (%) | 83,3% (10 de 12) |
| Tempo médio para encontrar | 44,6 s |
| Tentativas por atendimento | 1,3 |
| Facilidade de uso (1 a 5) | 3,8 |

### Dúvidas sem solução

- **"onde pego rémedio para pressão?"**: não foi encontrada (1 ponto, abaixo do mínimo de 3). Corrigida com a melhoria abaixo.
- **"2"**: a pessoa digitou o número de uma opção do menu na tela de dúvida, achando que estava escolhendo "Procurar por categorias". Não é uma dúvida da base: mostra que a diferença entre a tela do menu e a tela de pergunta não ficou clara para todos.

### Observações do teste

- Na pergunta **"com quantos nos posso entrar na fila de idoso?"**, a pessoa precisou de **4 tentativas** (233,7 s) até chegar à orientação 9 (atendimento prioritário), e deu nota de facilidade 1. Na última tentativa a palavra-chave `fila de idoso` foi encontrada (4 pontos, confiança MÉDIA).
- Pela **navegação por categorias**, os 4 atendimentos encontraram a orientação na primeira escolha, em 6,9 s a 15,9 s.

### Melhoria feita a partir do teste

A pergunta **"onde pego rémedio para pressão?"** somava só **1 ponto** (a palavra "remedio" no título da orientação 5), e o assistente respondia "Não encontrei". O motivo: nenhuma palavra-chave da orientação 5 (Farmácia Popular) aparecia do jeito que a pessoa perguntou.

Incluímos duas palavras-chave na orientação 5: `"remedios para pressao"` e `"pego remedio"`. Depois disso:

| Pergunta | Antes | Depois |
|---|---|---|
| "onde pego rémedio para pressão?" | 1 ponto — Não encontrei | **4 pontos — confiança MÉDIA** (+3 `pego remedio`, +1 "remedio" no título) |
| "onde pego remedios para pressão?" | 1 ponto — Não encontrei | **3 pontos — confiança MÉDIA** (+3 `remedios para pressao`) |

---

## 🎥 Vídeo técnico

`PREENCHER — link do YouTube (não listado)`

---

> **Aviso:** este assistente NÃO é um canal oficial. Sempre confirme as informações na fonte oficial indicada.
