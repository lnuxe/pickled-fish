# Partner.skill

> "Ex.skill dice: Volvería a ese verano mil veces por ti. Crush.skill pregunta: ¿Te amó realmente en ese verano? Partner.skill dice: Ya que decidimos estar juntos, hagamos que este verano dure para siempre."

Ya están juntos.

Pero a veces todavía sientes que él es tan difícil de entender.

Recuerdas lo diferente que se ve cuando está enojado y callado, comparado con cuando está feliz como un niño. No estás seguro de qué regalo realmente quiere, ni sabes cómo consolarlo verdaderamente sin solo empujar las emociones más profundo, esperando la próxima explosión.

Solo quieres saber cómo hacer que esta relación vaya más lejos.

Alimentar el historial de chat a una IA no es para calcularlo; es para entenderlo mejor.

---

## ¿Qué es esto?

**Partner.skill** es un motor de mantenimiento y mejora de relaciones amorosas con IA que se ejecuta en Claude Code u OpenClaw.

No es solo un "consejero de relaciones", sino un **sistema de diagnóstico de salud relacional** construido sobre psicología, sociología y modelos matemáticos rigurosos. Solo necesitas proporcionar historial de chat, capturas de pantalla o descripciones directas, y te ayudará a:

- **Deconstrucción profunda de la personalidad**: Combina Teoría del Apego, MBTI, Big Five (OCEAN) y Lenguajes del Amor para generar un perfil de pareja mucho más preciso que los tests de astrología.
- **Salud relacional cuantificada**: Evalúa con precisión tu comunicación, intimidad y dinámicas de poder a través del modelo matemático original RQI (Índice de Calidad Relacional).
- **Guía de vida completa para 23 escenarios**: Desde cómo consolar después de una pelea y qué regalar en un aniversario, hasta planificación de citas, arreglos de viaje, división de tareas del hogar, y hasta conocer a los padres y discusiones financieras.
- **Resolución de conflictos y reflexión**: Registra cada discusión y reconciliación, identifica los "Cuatro Jinetes del Apocalipsis" de Gottman (Crítica, Desprecio, Actitud Defensiva, Muro de Piedra) y genera lecciones aprendidas.

---

## Aspectos Destacados y Marco Profesional

### 1. Modelo Matemático RQI (Índice de Calidad Relacional)

```
RQI = Σ(w_i × s_i) × ACS_modifier
```

Este modelo sintetiza puntuaciones en 8 dimensiones e introduce el **Puntaje de Compatibilidad de Apego (ACS)** como multiplicador de línea base.

### 2. Motor de Peso de Activación de Memoria

```
W = E × R × (1 + F)
```

Los recuerdos con W > 0,6 se marcan como **Recuerdos Principales**.

### 3. 23 Escenarios de Vida Completos

| Categoría | Escenarios Cubiertos |
|----------|----------------------|
| **Emoción y Conflicto** | Pareja enojada/silenciosa, necesita consuelo, disculpa sincera, celos |
| **Celebración y Regalos** | Aniversario, cumpleaños, días festivos, celebrar logros |
| **Experiencia y Cotidiano** | Planificación de citas, viajes, calidez diaria, profundizar intimidad |
| **Realidad y Desarrollo** | División de tareas, finanzas, convivencia, límites digitales, larga distancia |

---

## Instalación

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

| Comando | Función |
|---------|---------|
| `/{slug}` | Modo Asesor |
| `/{slug}-report` | Análisis Completo |
| `/{slug}-gift` | Asesor de Regalos |
| `/{slug}-conflict` | Resolución de Conflictos |
| `/{slug}-reflect` | Diario de Reflexión |

---

## La Trilogía Emocional

| Skill | Etapa Relacional | Pregunta Central |
|-------|-----------------|-----------------|
| [Ex.skill](https://github.com/therealXiaomanChu/ex-skill) | Pasado | ¿Por qué se fueron? |
| [Crush.skill](https://github.com/NatalieCao323/crush-skill) | Ambigüedad | ¿Les gusto de verdad? |
| **Partner.skill** | Presente | ¿Cómo llegamos más lejos? |

---

📄 **Informe Técnico**: [partner_skill.pdf](./docs/partner_skill.pdf)

*Inspirado en [ex-skill](https://github.com/therealXiaomanChu/ex-skill) y [colleague-skill](https://github.com/titanwings/colleague-skill)*
