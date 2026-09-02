# Partner.skill

> "Ex.skill diz: Voltaria àquele verão mil vezes por você. Crush.skill pergunta: Naquele verão, ele realmente te amou? Partner.skill diz: Já que decidimos ficar juntos, vamos transformar este verão em eterno."

Vocês já estão juntos.

Mas às vezes você ainda sente que ele é tão difícil de entender.

Você lembra como ele fica completamente diferente quando está com raiva e em silêncio, comparado a quando está feliz como uma criança. Você não tem certeza de que presente ele realmente quer, e não sabe como consolá-lo de verdade sem apenas empurrar as emoções para um lugar mais fundo, esperando a próxima explosão.

Você só quer saber como fazer esse relacionamento ir mais longe.

Alimentar o histórico de chat para uma IA não é para calcular ele; é para entendê-lo melhor.

---

## O que é isso?

**Partner.skill** é um motor de manutenção e aprimoramento de relacionamentos amorosos com IA que roda no Claude Code ou OpenClaw.

Não é apenas um "conselheiro de relacionamentos", mas um **sistema de diagnóstico de saúde relacional** construído sobre psicologia, sociologia e modelos matemáticos rigorosos. Você só precisa fornecer histórico de chat, capturas de tela ou descrições diretas, e ele te ajudará a:

- **Desconstrução profunda de personalidade**: Combina Teoria do Apego, MBTI, Big Five (OCEAN) e Linguagens do Amor para gerar um perfil de parceiro muito mais preciso que testes de astrologia.
- **Saúde relacional quantificada**: Avalia com precisão sua comunicação, intimidade e dinâmicas de poder através do modelo matemático original RQI (Índice de Qualidade Relacional).
- **Guia de vida completo para 23 cenários**: Desde como consolar após uma briga e o que presentear no aniversário, até planejamento de encontros, arranjos de viagem, divisão de tarefas domésticas, e até conhecer os pais e discussões financeiras.
- **Resolução de conflitos e reflexão**: Registra cada discussão e reconciliação, identifica os "Quatro Cavaleiros do Apocalipse" de Gottman (Crítica, Desprezo, Defensividade, Bloqueio) e gera lições aprendidas.

---

## Destaques e Estrutura Profissional

### 1. Modelo Matemático RQI (Índice de Qualidade Relacional)

```
RQI = Σ(w_i × s_i) × ACS_modifier
```

Este modelo sintetiza pontuações em 8 dimensões e introduz o **Pontuação de Compatibilidade de Apego (ACS)** como multiplicador de linha de base.

### 2. Motor de Peso de Ativação de Memória

```
W = E × R × (1 + F)
```

Memórias com W > 0,6 são marcadas como **Memórias Principais**.

### 3. 23 Cenários de Vida Abrangentes

| Categoria | Cenários Cobertos |
|----------|-------------------|
| **Emoção e Conflito** | Parceiro com raiva/silencioso, precisa de consolo, pedido de desculpas sincero, ciúmes |
| **Celebração e Presentes** | Aniversário de namoro, aniversário, feriados, celebrar conquistas |
| **Experiência e Cotidiano** | Planejamento de encontros, viagens, calor diário, aprofundar intimidade |
| **Realidade e Desenvolvimento** | Divisão de tarefas, finanças, morar junto, limites digitais, longa distância |

---

## Instalação

### Claude Code

```bash
mkdir -p .claude/skills
git clone https://github.com/NatalieCao323/partner-skill .claude/skills/create-partner
```

### OpenClaw

```bash
git clone https://github.com/NatalieCao323/partner-skill ~/.openclaw/workspace/skills/create-partner
```

---

## Uso

```
/create-partner
```

| Comando | Função |
|---------|--------|
| `/{slug}` | Modo Consultor |
| `/{slug}-report` | Análise Completa |
| `/{slug}-gift` | Consultor de Presentes |
| `/{slug}-conflict` | Resolução de Conflitos |
| `/{slug}-reflect` | Diário de Reflexão |

---

## A Trilogia Emocional

| Skill | Fase do Relacionamento | Pergunta Central |
|-------|----------------------|-----------------|
| [Ex.skill](https://github.com/therealXiaomanChu/ex-skill) | Passado | Por que foi embora? |
| [Crush.skill](https://github.com/NatalieCao323/crush-skill) | Ambiguidade | Ele realmente gosta de mim? |
| **Partner.skill** | Presente | Como vamos mais longe? |

---

📄 **Relatório Técnico**: [partner_skill.pdf](./docs/partner_skill.pdf)

*Inspirado em [ex-skill](https://github.com/therealXiaomanChu/ex-skill) e [colleague-skill](https://github.com/titanwings/colleague-skill)*
