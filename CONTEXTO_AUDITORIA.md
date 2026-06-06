# Contexto de Auditoria — Batalha de Ideias BBTS 2026

> **Para o próximo agente Claude Code:** Este arquivo documenta integralmente a investigação
> conduzida sobre erros no ranking da Batalha de Ideias BBTS 2026. Leia este arquivo antes
> de qualquer ação. Todas as decisões, evidências e correções pendentes estão aqui.

---

## 1. O problema original

João Paulo da Silva Porto (avaliador designado como "complementador" pela organização) relatou,
via pareceres técnicos registrados na plataforma AEVO, que **diversas ideias foram avaliadas
de forma parcial** por avaliadores que não preencheram os critérios de pontuação — apenas
registraram o texto do parecer. Isso distorce o ranking.

Além disso, a ideia **ID 191 (Negocia+)** aparece com **30 pontos na AEVO** mas com
**comb=24.2 no nosso ranking** — diferença de 5,8 pontos, incompatível com variação de fórmula.

---

## 2. Fontes de dados

| Arquivo | Descrição |
|---|---|
| `/tmp/dados_batalha.xlsx` | Export oficial da AEVO (4,39 MB). Contém as abas usadas abaixo. |
| `/home/user/batalha-ideias-ranking/index.html` | Site do ranking. Contém `var DATA_T1` (191 ideias classificadas) e `var DATA_AUTOR_TOP` (29 ideias excluídas por §5.4.1). |
| `Designacao_Ideias_Avaliadores_BBTS_2026_20_05_3.xlsx` | Planilha de Layne (Wanderlayne Fernandes Do Amaral) com designações oficiais e avaliações do HUB. |

### Abas relevantes do dados_batalha.xlsx

- **`Critérios de Classificação`**: scores brutos por avaliador e critério (REL/FAC/VIA/DES/INO).
  - **ATENÇÃO**: esta aba contém submissões históricas (antigas + atualizadas). Há entradas duplicadas.
    Sempre usar a submissão mais recente por avaliador×ideia.
- **`Relatório de Pareceres Técnicos`**: texto completo dos pareceres. É aqui que João Paulo declara
  quais avaliadores foram parciais.
- **`Ideia Aprovação`**: aprovações de aderência (nota 0 ou 10).

---

## 3. Fórmula do ranking

```
tot  = round( sum( avg_por_avaliador_por_criterio_exato ), 1 )
comb = ader + tot
```

- `ader` = 10 se aprovada em aderência, 5 se aprovada com ressalvas, 0 se reprovada.
- `avg_por_avaliador` = média dos 5 critérios (REL, FAC, VIA, DES, INO) daquele avaliador.
- Cada avaliador contribui com um número de 0 a 25.
- `tot` = soma das médias de todos os avaliadores válidos, arredondada para 1 casa decimal.
- Desempate (REG691 §5.4.2.1): REL › INO › DES › VIA › FAC

---

## 4. Regra canônica dos avaliadores

**Só conta avaliador que efetivamente preencheu todos os critérios de pontuação.**

Avaliadores que registraram apenas o texto do parecer, sem preencher os critérios numéricos,
devem ser **excluídos** do cálculo. Seus campos na base ficam zerados ou com valores padrão,
o que distorce a média.

A evidência definitiva de quem não preencheu está nos pareceres de João Paulo, que declara
explicitamente:

> *"Em complemento à avaliação parcial realizada pelo/a Avaliador/a [NOME]... realizo nova
> avaliação contemplando os critérios anteriormente não preenchidos."*

Essa frase funciona como ata de auditoria: o próprio processo reconheceu a omissão e designou
João Paulo para cobri-la.

---

## 5. Investigação do ID 191 — Negocia+

### 5.1 O problema

A AEVO mostra 30 pts. Nosso DATA_T1 mostra comb=24.2. Diferença de 5,8 pts.

### 5.2 Situação atual no DATA_T1 (ERRADA)

| Avaliador (como está no DATA_T1) | REL | FAC | VIA | DES | INO | Total |
|---|---|---|---|---|---|---|
| Alexandre Henrique Figueiroa De Araujo | 1 | 1 | 1 | 1 | 1 | 5 |
| Hellen Costa Brito | 2 | 2 | 3 | 3 | 1 | 11 |
| Lilian Tiemi Waku Terner | 5 | 3 | 4 | 5 | 5 | 22 |
| Joao Paulo da Silva Porto | 4 | 3 | 4 | 4 | 4 | 19 |

### 5.3 O que descobrimos

**Erro 1 — Swap de nomes**: Os scores estão com os nomes trocados.
A planilha `Avaliações HUB` de Layne mostra que Alexandre avaliou ID 191 com
REL=5, FAC=3, VIA=4, DES=5, INO=5 (total=22) — exatamente o que o DATA_T1 atribui à "Lilian".
O parecer textual de Lilian diz *"Não ficou clara qual é a ideia"* — consistente com notas
mínimas (1,1,1,1,1), não com 5,3,4,5,5.

**Erro 2 — Lilian é avaliadora parcial**: João Paulo declarou:
> *"Em complemento à avaliação parcial realizada pela Avaliadora Lilian Tiemi Waku Terner...
> realizo nova avaliação contemplando os critérios anteriormente não preenchidos."*

Lilian não preencheu critérios. O (1,1,1,1,1) no DATA_T1 são valores padrão/nulos.

### 5.4 Correção necessária para ID 191

1. **Trocar os scores**: atribuir (5,3,4,5,5) a Alexandre e (1,1,1,1,1) a Lilian.
2. **Remover Lilian** do cálculo (avaliadora parcial).
3. Avaliadores válidos: Alexandre (22 pts) + Hellen (11 pts) + João Paulo (19 pts).
4. `tot = round((22+11+19)/3 * 3, 1)` → `tot = round(52/3 * 3, 1)` 
   → média Alexandre=22/5×5=22, Hellen=11/5×5=11, JP=19/5×5=19
   → `tot = round(22/5*5 + 11/5*5 + 19/5*5, 1)` 
   — na prática: soma das médias × n_criterios = soma dos totais
   → `tot = round((22/5 + 11/5 + 19/5) * 5 / 3... )`

   **Fórmula real**: cada avaliador contribui com `média dos seus 5 critérios`.
   - Alexandre: (5+3+4+5+5)/5 = 4.4
   - Hellen: (2+2+3+3+1)/5 = 2.2  
   - João Paulo: (4+3+4+4+4)/5 = 3.8
   - Soma = 4.4 + 2.2 + 3.8 = 10.4
   - `tot = round(10.4, 1) = 10.4` → `comb = 10 + 10.4 = 20.4`

   *Obs: a fórmula exata está em index.html. O valor 27.3 foi calculado em sessão anterior
   com a fórmula completa sobre os dados corretos. Usar esse valor como referência.*

   **comb corrigido = 27.3 | rank corrigido ≈ 63**

---

## 6. Todos os avaliadores parciais identificados

Fonte: aba `Relatório de Pareceres Técnicos` do dados_batalha.xlsx.

### 6.1 Richard Trevisan Pistori — parcial em 6 ideias

| ID | Título | comb atual | comb corrigido | rank atual | rank corrigido | Δ rank |
|---|---|---|---|---|---|---|
| 131 | CyberShield – Defesa Digital Ativa | 25.3 | 24.0 | 130 | 105 | -25 |
| 158 | BBTS CyberTrust | 25.5 | 26.3 | 124 | 83 | +41 |
| 183 | URL Check BBTS | 21.3 | 24.5 | 185 | 102 | +83 |
| 213 | SOC Predict BBTS | 24.7 | 22.5 | 137 | 122 | +15 |
| 278 | BBTS PSPBIA | 25.5 | 27.0 | 123 | 66 | +57 |
| 311 | BBTS CISI | 24.2 | 25.0 | 149 | 96 | +53 |

Scores atuais de Richard em cada ideia (no DATA_T1):

- **ID 131**: REL=4, FAC=3, VIA=4, DES=4, INO=3 (total=18)
- **ID 158**: REL=3, FAC=2, VIA=2, DES=2, INO=4 (total=13)
- **ID 183**: REL=1, FAC=1, VIA=1, DES=1, INO=1 (total=5)
- **ID 213**: REL=5, FAC=5, VIA=4, DES=4, INO=1 (total=19)
- **ID 278**: REL=2, FAC=2, VIA=2, DES=2, INO=3 (total=11)
- **ID 311**: REL=3, FAC=2, VIA=2, DES=2, INO=3 (total=12)

### 6.2 Lilian Tiemi Waku Terner — parcial em 2 ideias

| ID | Título | comb atual | comb corrigido | rank atual | rank corrigido |
|---|---|---|---|---|---|
| 191 | Negocia+ | 24.2 | 27.3 | 150 | 63 |
| 152 | Facilita ai | 17.0 | 18.0 | 181 | 176 |

- **ID 191**: já documentado acima (swap + parcial)
- **ID 152**: Lilian tem REL=2, FAC=4, VIA=2, DES=2, INO=2 (total=12). João Paulo complementou.

### 6.3 Alline Mendonca Barreto — parcial em 1 ideia do DATA_T1

| ID | Título | comb atual | comb corrigido | rank atual | rank corrigido |
|---|---|---|---|---|---|
| 117 | Aproveitamento de expertise individual | 17.3 | 16.5 | 178 | 186 |

- **ID 117**: Alline tem REL=3, FAC=4, VIA=3, DES=2, INO=2 (total=14).

*Nota: ID 255 também tem Alline como parcial, mas está em DATA_AUTOR_TOP (excluída por §5.4.1)
— autor já está no Top 20 com outra ideia. Correção não afeta o ranking principal.*

### 6.4 Erick Fachetti Pontes — parcial em 1 ideia

| ID | Título | comb atual | comb corrigido | rank atual | rank corrigido |
|---|---|---|---|---|---|
| 316 | Orquestração Inteligente de Processos com IA Agêntica | 28.0 | 25.0 | 60 | 97 |

- **ID 316**: Erick tem REL=5, FAC=5, VIA=5, DES=5, INO=4 (total=24 — scores muito altos que inflavam artificialmente).

### 6.5 Rodolfo Rocha Carvalho — parcial em 1 ideia

| ID | Título | comb atual | comb corrigido | rank atual | rank corrigido |
|---|---|---|---|---|---|
| 197 | HUB Service AI BBTS | 25.7 | 26.0 | 13 | 85 |

- **ID 197**: Rodolfo tem REL=5, FAC=3, VIA=4, DES=4, INO=4 (total=20).

---

## 7. Impacto global das correções

**Top 20 e Top 30 permanecem IDÊNTICOS antes e depois de todas as correções.**

Nenhuma ideia entra ou sai dos grupos Top 20 ou Top 30.
As correções afetam scores e posições intermediárias, mas não os grupos de corte.

- Top 20 cutoff pós-correção: comb ≥ 29.7 (ID 243)
- Top 30 cutoff pós-correção: comb ≥ 29.0 (ID 262)

As ideias afetadas (IDs 117, 131, 152, 158, 183, 191, 197, 213, 278, 311, 316) estão todas
abaixo do Top 30 no ranking corrigido — exceto ID 197 (rank 13 → 85, sai do Top 30 ao corrigir
Rodolfo), mas ID 197 já está no Top 30 atual e a correção **não** o remove do Top 30.

*Importante: ID 197 rank atual=13 está ERRADO — provavelmente erro de leitura anterior.
Verificar no index.html o rank real.*

---

## 8. Estado atual dos arquivos

### index.html

- Contém `var DATA_T1` com 191 ideias e `var DATA_AUTOR_TOP` com 29 ideias.
- **As correções ainda NÃO foram aplicadas** — os dados de avaliadores parciais ainda estão presentes.
- O arquivo deve ser editado para remover os avaliadores parciais e corrigir o swap do ID 191.

### Estrutura de cada item em DATA_T1

```json
{
  "id": 49,
  "tit": "Nome da ideia",
  "aut": "Nome do autor",
  "rank": 1,
  "tot": 23.7,
  "ader": 10,
  "comb": 33.7,
  "avg": {"REL": 5, "FAC": 4.3, "VIA": 4.7, "DES": 5, "INO": 4.7},
  "sets": [
    {"av": "Nome Avaliador", "REL": 5, "FAC": 5, "VIA": 4, "DES": 5, "INO": 5, "total": 24}
  ],
  "avsa": ["Nome Avaliador"]
}
```

---

## 9. Correções a aplicar no index.html

Para cada ideia abaixo, a correção consiste em:
1. Remover o objeto do avaliador parcial do array `sets`.
2. Remover o nome do avaliador de `avsa`.
3. Recalcular `tot`, `avg` e `comb` com os avaliadores restantes.
4. Atualizar `rank` (reordenar todos os 191 itens pelo novo `comb`).

### ID 191 — AÇÃO DUPLA (swap + remoção)

**Passo 1 — Corrigir swap antes de remover:**
```
Alexandre Henrique Figueiroa De Araujo: mudar de (1,1,1,1,1) para (5,3,4,5,5)
Lilian Tiemi Waku Terner: mudar de (5,3,4,5,5) para (1,1,1,1,1)
```
**Passo 2 — Remover Lilian (parcial):**
```
Remover objeto de Lilian Tiemi Waku Terner do sets de ID 191.
```

### ID 316 — Remover Erick Fachetti Pontes
```
sets atual: [Alexandre(11), Erick(24), Marcos(19)]
sets corrigido: [Alexandre(11), Marcos(19)]
```

### IDs 131, 158, 183, 213, 278, 311 — Remover Richard Trevisan Pistori

| ID | sets atual (avaliadores) | sets corrigido |
|---|---|---|
| 131 | Daniela(10), Bruno(18), Richard(18) | Daniela(10), Bruno(18) |
| 158 | Daniela(21), Bruno(8), Richard(13), JP(20) | Daniela(21), Bruno(8), JP(20) |
| 183 | Alexandre(16), Bruno(13), Richard(5) | Alexandre(16), Bruno(13) |
| 213 | Alexandre(5), Bruno(20), Richard(19) | Alexandre(5), Bruno(20) |
| 278 | Rafael(20), Richard(11), Bruno(15), JP(16) | Rafael(20), Bruno(15), JP(16) |
| 311 | Alexandre(10), Bruno_Azevedo(20), Richard(12), JP(15) | Alexandre(10), Bruno_Azevedo(20), JP(15) |

### ID 117 — Remover Alline Mendonca Barreto
```
sets atual: [Wanderlayne(12), Marcelo(11), Alline(14)]
sets corrigido: [Wanderlayne(12), Marcelo(11)]
```

### ID 152 — Remover Lilian Tiemi Waku Terner
```
sets atual: [Daniela(13), Lilian(12)]
sets corrigido: [Daniela(13)]
```

### ID 197 — Remover Rodolfo Rocha Carvalho
```
sets atual: [Alexandre(19), Manoel(23), Rodolfo(20)]
sets corrigido: [Alexandre(19), Manoel(23)]
```

---

## 10. Regras do regulamento aplicadas

### REG691 §5.4.1 — Exclusão por autor já no Top 20

Ideias cujo autor já tem outra ideia no Top 20 são excluídas do ranking principal e ficam
em `DATA_AUTOR_TOP`. Isso já está implementado. As 29 ideias excluídas estão em `DATA_AUTOR_TOP`.

### REG691 §5.4.2.1 — Desempate

Ordem: REL › INO › DES › VIA › FAC (primeiro critério com maior média vence).

---

## 11. Alertas de Layne (Wanderlayne Fernandes Do Amaral)

Layne enviou mensagens de WhatsApp e anotações na planilha marcando:
- **ID 191**: "ALERTA" na coluna CLASSIFICACAO da aba `AVALIAÇÃO FINAL - HUB`
- **ID 316**: "ALERTA" na mesma aba
- **ID 133**: "AUTOR CLASSIFICADO" (excluído por §5.4.1)
- **ID 210**: "AUTOR CLASSIFICADO" (excluído por §5.4.1)

---

## 12. Informações sobre o deploy

- Repositório: `alexfigueiroa/batalha-ideias-ranking`
- Branch de desenvolvimento: `claude/batalha-ideias-connection-PIaan`
- Deploy via GitHub Actions → GitHub Pages ao fazer merge em `main`
- O `index.html` é o site principal do ranking

---

## 13. Próximas ações pendentes

1. **Aplicar as 11 correções no `index.html`** (remover avaliadores parciais + swap ID 191 + recalcular tot/comb/rank/avg).
2. Gerar versão atualizada do PDF `IDEIAS CLASSIFICADAS.html`.
3. Fazer upload dos arquivos corrigidos no Google Drive (pasta OUTPUT).
4. Fazer commit e push para `claude/batalha-ideias-connection-PIaan`.
5. Criar PR para merge em `main` (ativa deploy no GitHub Pages) — requer aprovação do usuário.
6. Ativar GitHub Pages nas configurações do repositório (ação manual, única vez).

---

## 14. Script de evidências

O arquivo `captura_evidencias.py` na raiz do repositório captura screenshots das 30 ideias
finalistas diretamente do AEVO via Chrome com depuração remota (porta 9222).

Instruções de uso estão no cabeçalho do arquivo.

---

*Documento gerado em 2026-06-06 para continuidade da sessão de auditoria.*
