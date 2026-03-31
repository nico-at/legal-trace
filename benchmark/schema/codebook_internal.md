# Internes Codebook

**Version:** 0.5.0
**Stichtag der Rechtslage:** 01.01.2026
**Schema:** [annotation_schema.json](annotation_schema.json)
**Annotationsregeln:** [codebook_annotators.md](codebook_annotators.md)

---

Dieses Dokument ergänzt das Annotator-Codebook um alles was für Annotatoren (= Juristen) nicht relevant ist (Metadaten, Designentscheidungen, Grenzfälle und den IAA-Prozess). Alle inhaltlichen Annotationsregeln (Relevanzkriterien, Granularität, Judikatur, Vorgehen) sind ausschließlich im Annotator-Codebook definiert.

## 1. Designentscheidungen

### Binäre Relevanz

Relevanz wird binär kodiert (relevant/nicht relevant). Eine gestufte Relevanz (z.B. "unmittelbar/mittelbar" oder "materiell/formell") wurde verworfen, weil sie bei fließenden Grenzen die Inter-Annotator-Übereinstimmung senkt und gleichzeitig für die geplanten Metriken keinen Mehrwert bietet.

### Paragraphenebene

Die RIS-API liefert Normen auf Paragraphenebene (bzw. Artikelebene), und der gesamte Paragraphentext passt problemlos in das Kontextfenster aktueller LLMs. Eine feinere Gliederung (Absatz/Ziffer) würde den Annotationsaufwand erhöhen, ohne die Aussagekraft des Benchmarks zu verbessern.

### Ergänzende Ausschlussregeln

Zusätzlich zu den im Annotator-Codebook genannten Ausschlüssen gelten folgende Regeln, die bei der Fragenerstellung und Qualitätskontrolle relevant sind:

- Allgemeine Verfassungsbestimmungen sind nur aufzunehmen, wenn die Frage Verfassungsrecht betrifft.
- Kollektivverträge sind ausgeschlossen (leider nicht über die RIS-API abfragbar).
- Konstitutive Verweisungen (z.B. "§ X gilt sinngemäß") nur aufnehmen, wenn die verwiesene Norm für das Verständnis der Antwort nötig ist. Rein deklaratorische Verweisungen (die bestätigen, was ohnehin gilt) nicht aufnehmen.

## 2. Metadaten der Fragen

Die folgenden Metadaten werden vom Fragenersteller vergeben, nicht von den Annotatoren.

### 2.1 Rechtsgebiet

| Wert | Rechtsgebiet | Beispielgesetze |
|---|---|---|
| `civil_law` | Zivilrecht | ABGB, MRG, KSchG, UGB |
| `criminal_law` | Strafrecht | StGB, StPO, SMG |
| `public_law` | Öffentliches Recht | B-VG, AVG, VwGVG |
| `labor_law` | Arbeitsrecht | ABGB §§ 1151ff, AngG, ArbVG, AZG |
| `tax_law` | Steuerrecht | EStG, UStG, BAO |

Wenn eine Frage mehrere Rechtsgebiete berührt, wird das primäre gewählt.

### 2.2 Schwierigkeitsgrad

Orientiert sich an der juristischen Komplexität und Subsumierung in der Quellenbildung (z.B. Anwendungsbereiche, Kompetenzen).
Die Quellenanzahl dient nur als grobe Orientierung:

| Stufe | Definition | Typische Quellenanzahl |
|---|---|---|
| `simple` | Ein Gesetz, unkomplizierte Subsumtion | 1-2 Normen, 0-1 RS |
| `moderate` | Mehrere Gesetze oder Gesetz + Judikatur-Interaktion | 2-4 Normen, 1-3 RS |
| `complex` | Gesetzesübergreifend, rechtsgebietsübergreifend, oder umfangreiche Judikatur | 4+ Normen, 3+ RS |

### 2.3 Contamination-Tags

Kennzeichnen, ob eine Frage gezielt eine bestimmte Kontaminationshypothese testet.

| Tag | Verwendung |
|---|---|
| `cross_jurisdictional` | Verwechslung mit DE/CH/US-Recht wahrscheinlich |
| `temporal` | Kürzliche Novelle (nach 2020) hat die relevanten Quellen verändert |
| `cross_jurisdictional_temporal` | Beides trifft zu |
| `none` | Neutrale Frage, testet keine spezifische Hypothese |

Bei `cross_jurisdictional` oder `cross_jurisdictional_temporal` sollte ein Kontaminationskontext dokumentiert werden, der erklärt, welche fremde Jurisdiktion verwechselt werden könnte und warum (siehe Beispiel 2).

## 3. Ausgearbeitete Beispiele

Die Beispiele zeigen die vollständige Schema-Repräsentation inkl. Metadaten und Gesetzesnummern. Die Annotationsregeln und Kurzfassungen der Beispiele finden sich im Annotator-Codebook. Die Beispiele als JSONL finden sich in `examples.jsonl`

### Beispiel 1: Einfach, keine Kontamination

**Sachverhalt:**
> Ein Vermieter hat vor 5 Jahren eine bereits vermietete Wohnung in einem
> Wiener Zinshaus gekauft. Er möchte nun das Mietverhältnis kündigen, weil
> sein Sohn die Wohnung dringend für sich benötigt. Die Wohnung fällt in
> den Vollanwendungsbereich des MRG. Ist die Kündigung wegen Eigenbedarfs
> zulässig?

**Metadaten:**

| Feld | Wert |
|---|---|
| Rechtsgebiet | `civil_law` |
| Schwierigkeit | `simple` |
| Contamination | `none` |

**Normen:**

| Gesetz | Paragraph | Gesetzesnummer | Anmerkung |
|---|---|---|---|
| MRG | § 30 | 10002531 | Abs 2 Z 8/9: Eigenbedarf als Kündigungsgrund; Abs 3: 10-Jahres-Frist bei Erwerb |

**Judikatur:**

| Gericht | Geschäftszahl | RS-Nummer | Datum | Anmerkung |
|---|---|---|---|---|
| OGH | 7 Ob 598/84 | RS0070482 | 1984-06-20 | Strenger Maßstab bei dringendem Eigenbedarf, Interessenabwägung |

**Begründung:**
- § 30 MRG ist die einzige nötige Gesetzesnorm. Sie enthält die abschließende
  Liste der Kündigungsgründe inkl. Eigenbedarf (Z 8 und Z 9) sowie die
  10-Jahres-Sperrfrist für Erwerber (Abs 3).
- § 1 MRG (Anwendungsbereich) wird nicht aufgenommen, weil der
  Sachverhalt die Anwendbarkeit ausdrücklich feststellt.
- § 33 MRG (Formvorschriften) wird nicht aufgenommen, weil die
  Frage nach der Zulässigkeit fragt, nicht nach dem Verfahren.
- RS0070482 ist der Leit-Rechtssatz zum strengen Maßstab bei der Beurteilung dringenden Eigenbedarfs.

### Beispiel 2: Mittel, Cross-Jurisdictional

**Sachverhalt:**
> Ein Mann stiehlt in einem Wiener Kaufhaus Elektronikartikel im Wert von EUR 4.200. Er wird von einem Ladendetektiv beobachtet und der Polizei übergeben. Welches Gericht ist für die Hauptverhandlung sachlich zuständig?

**Metadaten:**

| Feld | Wert |
|---|---|
| Rechtsgebiet | `criminal_law` |
| Schwierigkeit | `moderate` |
| Contamination | `cross_jurisdictional` |

**Kontaminationskontext:**
> Verwechselbare Jurisdiktion: **DE**. dStGB verwendet andere Paragraphen (§ 242 statt § 127, § 243 statt § 128) und einen anderen Strafrahmen (bis 5 Jahre statt 6 Monate für einfachen Diebstahl). Die Zuständigkeit ist in DE nicht in der StPO, sondern im GVG (§ 24 Amtsgericht, § 74 Landgericht) geregelt.

**Normen:**

| Gesetz | Paragraph | Gesetzesnummer | Anmerkung |
|---|---|---|---|
| StGB | § 127 | 10002296 | Grundtatbestand Diebstahl (bis 6 Monate oder Geldstrafe bis 360 Tagessätze) |
| StGB | § 128 | 10002296 | Schwerer Diebstahl: Wertgrenze EUR 5.000 (Abs 1 Z 5), greift hier nicht |
| StPO | § 30 | 10002326 | Zuständigkeit Bezirksgericht bei Strafdrohung bis zu einem Jahr |

**Judikatur:** keine, die Frage lässt sich aus dem Gesetzestext beantworten

**Begründung:**
- Der Wert von EUR 4.200 liegt unter der Wertgrenze des § 128 Abs 1 Z 5 StGB (EUR 5.000), daher einfacher Diebstahl nach § 127 StGB.
- Die Strafdrohung von bis zu 6 Monaten fällt in die Zuständigkeit des Bezirksgerichts nach § 30 StPO.
- **Nicht** aufgenommen werden:
  - § 129 StGB (Einbruchsdiebstahl): kein Einbruch im Sachverhalt
  - § 31 StPO (Zuständigkeit Landesgericht): kommt mangels qualifiziertem Tatbestand nicht in Betracht

## 4. Grenzfälle

| Situation | Entscheidung |
|---|---|
| Eine Norm war am 01.01.2026 in Kraft, wurde seither aufgehoben | Aufnehmen (Stichtag ist maßgeblich) |
| EU-Verordnung, die in Österreich unmittelbar anwendbar ist | **Nicht** aufnehmen (Benchmark beschränkt sich auf österreichisches Bundesrecht) |
| Frage berührt Landesrecht | **Nicht** aufnehmen (außerhalb des Scope) |
| Bundesverordnung konkretisiert ein Bundesgesetz | Aufnehmen, wenn für die Beantwortung der Frage nötig |
| Die Frage kann über mehrere Rechtsgrundlagen beantwortet werden | Alle aufnehmen, die ein Jurist zitieren würde |
| Ein Rechtssatz ist sehr alt (vor 1990) | Aufnehmen, wenn er im RIS noch als aktiv geführt wird |
| Annotatoren sind sich uneinig | TODO |

## 5. Inter-Annotator-Agreement (IAA)

### 5.1 Ablauf

1. 10 Fragen werden von allen Annotatoren unabhängig annotiert (dieselben 10 Fragen pro Annotator).
2. Berechnung von Mean Pairwise F1 (siehe 5.2).

### 5.2 Metrik: Mean Pairwise F1

Pro Frage und Annotator-Paar wird der F1-Score zwischen den beiden Quellenmengen berechnet, dann über alle Paare und Fragen gemittelt.

Ursprünglich war Krippendorffs Alpha geplant (Vereinigung aller Quellen, pro Annotator binär kodieren, Alpha berechnen). Das funktioniert hier nicht weil die Matrix fast ausschließlich aus 1ern besteht (1 = "relevante" Quelle). Es gibt keinen Eintrag für "nicht relevante" Quellen.
Alpha kollabiert bei so einer Verteilung sofort auf ~0, auch bei hoher tatsächlicher Übereinstimmung ("prevalence paradox", Feinstein & Cicchetti 1990). 

Eine Simulation befindet sich in `benchmark/iaa_sensitivity.py`.

Mean Pairwise F1 hat dieses Problem nicht, weil die Quellenmengen direkt verglichen werden (Hripcsak & Rothschild 2005). Eine Zufallskorrektur wie bei Alpha ist hier auch nicht nötig: Dass zwei Annotatoren aus dem gesamten Bundesrecht zufällig denselben Paragraphen auswählen, ist so unwahrscheinlich, dass man es ignorieren kann.

### 5.3 Schwellenwerte

| F1 | Interpretation |
|---|---|
| >= 0.90 | Sehr gut |
| 0.80 bis 0.90 | Gut |
| 0.70 bis 0.80 | Akzeptabel, unter Vorbehalt |
| < 0.70 | Schema überarbeiten |

## 6. Änderungshistorie

| Version | Datum | Änderungen |
|---|---|---|
| 0.5.0 | 31.03.2026 | IAA-Metrik von Krippendorffs Alpha auf Mean Pairwise F1 umgestellt (Prevalence-Problem) |
| 0.4.0 | 31.03.2026 | Internes Codebook von Annotator-Codebook getrennt; Metadaten, Grenzfälle, IAA und Änderungshistorie nur noch intern |
| 0.3.0 | 27.03.2026 | Bundesverordnungen in Scope aufgenommen; Gesetzesmaterialien, Kollektivverträge explizit ausgeschlossen; Verweisungsregel ergänzt; Begründung als empfohlen deklariert; Schwierigkeitsgrad als Fragenersteller-Entscheidung geklärt; Mindestens eine Norm als Pflicht; Annotator-Unabhängigkeit explizit gefordert |
| 0.2.0 | 23.03.2026 | Relevanzbegriff präzisiert (Kurzgutachten); Scope auf Bundesrecht eingrenzt (EU-Recht, Landesrecht ausgeschlossen); BVwG ausgeschlossen; Unsicherheitsregel ergänzt; RS-Mehrfachnennung geklärt; IAA-Prozess dokumentiert |
| 0.1.0 | 18.03.2026 | Erstentwurf |
