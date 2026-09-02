# Partner.skill

> „Ex.skill sagt: Ich würde für dich tausendmal in diesen Sommer zurückkehren. Crush.skill fragt: Hat er dich in diesem Sommer wirklich geliebt? Partner.skill sagt: Da wir uns entschieden haben, zusammen zu sein, lass uns diesen Sommer für immer dauern."

Ihr seid bereits zusammen.

Aber manchmal hast du das Gefühl, dass er so schwer zu verstehen ist.

Du erinnerst dich, wie unterschiedlich er aussieht, wenn er wütend und still ist, verglichen mit wenn er glücklich wie ein Kind ist. Du bist dir nicht sicher, was für ein Geschenk er wirklich möchte, und du weißt nicht, wie du ihn wirklich trösten kannst, ohne die Emotionen nur tiefer zu drücken und auf die nächste Explosion zu warten.

Du möchtest einfach wissen, wie du diese Beziehung weiter bringen kannst.

Chatverläufe an eine KI zu füttern bedeutet nicht, ihn zu berechnen – es geht darum, ihn besser zu verstehen.

---

## Was ist das?

**Partner.skill** ist eine KI-gestützte Beziehungspflege- und -verbesserungsmaschine, die in Claude Code oder OpenClaw läuft.

Es ist nicht nur ein „Beziehungsberater", sondern ein **Beziehungsgesundheits-Diagnosesystem**, das auf Psychologie, Soziologie und strengen mathematischen Modellen basiert. Du musst nur Chatverläufe, Screenshots oder direkte Beschreibungen bereitstellen, und es hilft dir dabei:

- **Tiefgreifende Persönlichkeitsanalyse**: Kombiniert Bindungstheorie, MBTI, Big Five (OCEAN) und Liebessprachen, um ein Partnerprofil zu erstellen, das präziser ist als Horoskoptests.
- **Quantifizierte Beziehungsgesundheit**: Bewertet präzise deine Kommunikation, Intimität und Machtdynamiken durch das originale RQI (Relationship Quality Index) Mathematikmodell.
- **Vollständiger Lebensratgeber für 23 Szenarien**: Von Streitschlichtung und Geburtstagsgeschenken bis hin zu Verabredungsplanung, Reisearrangements, Haushaltsaufteilung und sogar Elterntreffen und Finanzgesprächen.
- **Konfliktlösung und Reflexion**: Zeichnet jeden Streit und jede Versöhnung auf, identifiziert Gottmans „Vier Apokalyptische Reiter" (Kritik, Verachtung, Defensivität, Mauern) und generiert Lektionen, um Fehler nicht zu wiederholen.

---

## Kernhighlights und professioneller Rahmen

### 1. Relationship Quality Index (RQI) Mathematikmodell

```
RQI = Σ(w_i × s_i) × ACS_modifier
```

Dieses Modell synthetisiert Bewertungen in 8 Dimensionen und führt den **Attachment Compatibility Score (ACS)** als Basismultiplikator ein.

### 2. Speicheraktivierungsgewichts-Engine

```
W = E × R × (1 + F)
```

Erinnerungen mit W > 0,6 werden als **Kernerinnerungen** markiert.

### 3. 23 umfassende Lebensszenarien

| Kategorie | Abgedeckte Szenarien |
|----------|----------------------|
| **Emotion & Konflikt** | Partner wütend/still, Trost benötigt, aufrichtige Entschuldigung, Eifersucht |
| **Feier & Geschenke** | Jahrestag, Geburtstag, Feiertage, Erfolge feiern |
| **Erlebnis & Alltag** | Verabredungsplanung, Reiseplanung, tägliche Wärme, Intimität vertiefen |
| **Realität & Entwicklung** | Haushaltsaufteilung, Finanzen, Zusammenziehen, digitale Grenzen, Fernbeziehung |

---

## Installation

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

## Verwendung

```
/create-partner
```

| Befehl | Funktion |
|--------|----------|
| `/{slug}` | Beratungsmodus |
| `/{slug}-report` | Vollständige Analyse |
| `/{slug}-gift` | Geschenkberater |
| `/{slug}-conflict` | Konfliktlösung |
| `/{slug}-reflect` | Reflexionsprotokoll |

---

## Die Beziehungstrilogie

| Skill | Beziehungsphase | Kernfrage |
|-------|----------------|-----------|
| [Ex.skill](https://github.com/therealXiaomanChu/ex-skill) | Vergangenheit | Warum haben sie mich verlassen? |
| [Crush.skill](https://github.com/NatalieCao323/crush-skill) | Unklarheit | Mögen sie mich wirklich? |
| **Partner.skill** | Gegenwart | Wie gehen wir weiter? |

---

📄 **Technischer Bericht**: [partner_skill.pdf](./docs/partner_skill.pdf)

*Inspiriert von [ex-skill](https://github.com/therealXiaomanChu/ex-skill) und [colleague-skill](https://github.com/titanwings/colleague-skill)*
