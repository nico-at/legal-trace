# Annotationsanleitung

**Version:** 0.5.0

**Stichtag der Rechtslage:** 01.01.2026

---

## 1. Ziel

Wir erstellen einen Datensatz, der dokumentiert, **welche Rechtsquellen ein Jurist zu einer österreichischen Rechtsfrage zitieren würde**. Es geht ausschließlich um die Quellenidentifikation, nicht darum, wie die Frage inhaltlich zu beantworten ist.

## 2. Aufgabe

Gegeben ist ein Sachverhalt mit einer konkreten Rechtsfrage.

1. Identifizieren Sie alle **Normen des Bundesrechts** (Gesetze und Verordnungen), die für die Beantwortung der Frage nach österreichischem Recht (Rechtslage 01.01.2026) relevant sind.
2. Identifizieren Sie alle **Leitentscheidungen** (über deren Rechtssatznummer im RIS), die für die Frage relevant sind.

Jeder Annotator arbeitet **unabhängig**, d.h. ohne Einsicht in die Ergebnisse anderer Annotatoren.

## 3. Was gilt als „relevant"?

### 3.1 Normen des Bundesrechts

Eine Norm ist relevant, wenn ein Jurist sie in einem **Kurzgutachten** (praxistypisch wenige Seiten), das ausschließlich die gestellte Frage beantwortet, **zitieren** würde.

**Einschließen:**
- Anspruchsgrundlage bzw. einschlägiger Tatbestand
- Legaldefinitionen, die zentrale Begriffe der Hauptnorm definieren
- Bundesverordnungen, die das Gesetz konkretisieren und für die Beantwortung nötig sind
- Anwendungsbereichsnormen, sofern die Anwendbarkeit nicht offensichtlich aus dem Sachverhalt hervorgeht

**Ausschließen:**
- EU-Verordnungen und EU-Richtlinien (auch wenn unmittelbar anwendbar, z.B. DSGVO)
- Landesrecht
- Fremde Rechtsordnungen (Rechtsvergleiche)
- Gesetzesmaterialien, Erläuterungen und Literatur
- Normen, die nur allgemeines Hintergrundwissen darstellen, ohne für die konkrete Frage nötig zu sein
- Verfahrensrechtliche Normen (außer die Frage ist ausdrücklich verfahrensrechtlicher Natur)

Gesetzlichen Verweisungen ist nur zu folgen, wenn die verwiesene Norm den materiellen Gehalt der Antwort verändert.

Jede Frage muss **mindestens eine Norm** enthalten. Judikatur ist hingegen optional.

### 3.2 Granularität

Annotieren Sie auf **Paragraphenebene**: § 30 MRG, nicht § 30 Abs 1 Z 8 MRG. Bei langen Sammel-Paragraphen die relevante Stelle im Anmerkungsfeld vermerken.

### 3.3 Judikatur

Aufgenommen werden ausschließlich **Leitentscheidungen** der drei Höchstgerichte (OGH, VfGH, VwGH), identifiziert über ihre RS-Nummer im RIS. Eine Leitentscheidung ist eine Entscheidung, in der ein Höchstgericht erstmals einen für die Frage relevanten Rechtsgrundsatz aufgestellt hat.

Suchen Sie pro relevanter Norm im RIS nach Rechtssätzen (z.B. Suche nach Norm MRG § 30). Betrifft ein Rechtssatz die konkrete Frage, nehmen Sie ihn auf (RS-Nummer + Geschäftszahl); andernfalls überspringen.

Mehrere zutreffende Rechtssätze pro Norm sind alle aufzunehmen. Folgeentscheidungen und Entscheidungen unterer Instanzen werden **nicht** aufgenommen.

### 3.4 Vorgehen

1. Sachverhalt lesen und Rechtsfragen identifizieren
2. Im RIS (Stichtag 01.01.2026) einschlägige Normen suchen
3. Gesetzestext lesen und Relevanz bestätigen
4. Judikatur nach obiger Anleitung suchen
5. Bei Bedarf mit Kommentarliteratur gegenprüfen

Bei Unsicherheit: **Aufnehmen** und Zweifel im Anmerkungsfeld vermerken. Eine kurze Begründung der Quellenauswahl ist empfohlen, besonders wenn die Quellenauswahl nicht offensichtlich ist.

## 4. Beispiele

### Beispiel 1: Einfach

**Sachverhalt:**
> Ein Vermieter hat vor 5 Jahren eine bereits vermietete Wohnung in einem Wiener Zinshaus gekauft. Er möchte nun das Mietverhältnis kündigen, weil sein Sohn die Wohnung dringend für sich benötigt. Die Wohnung fällt in den Vollanwendungsbereich des MRG. Ist die Kündigung wegen Eigenbedarfs zulässig?

**Normen:**

| Gesetz | Paragraph | Anmerkung |
|---|---|---|
| MRG | § 30 | Abs 2 Z 8/9: Eigenbedarf als Kündigungsgrund; Abs 3: 10-Jahres-Frist bei Erwerb |

**Judikatur:**

| Gericht | Geschäftszahl | RS-Nummer | Datum | Anmerkung |
|---|---|---|---|---|
| OGH | 7 Ob 598/84 | RS0070482 | 1984-06-20 | Strenger Maßstab bei dringendem Eigenbedarf, Interessenabwägung |

**Begründung:**
- § 30 MRG enthält die abschließende Liste der Kündigungsgründe inkl. Eigenbedarf und die 10-Jahres-Sperrfrist für Erwerber.
- § 1 MRG (Anwendungsbereich) und § 33 MRG (Formvorschriften) werden nicht aufgenommen, weil der Sachverhalt die Anwendbarkeit feststellt und die Frage nicht verfahrensrechtlicher Natur ist.

### Beispiel 2: Mittel

**Sachverhalt:**
> Ein Mann stiehlt in einem Wiener Kaufhaus Elektronikartikel im Wert von EUR 4.200. Er wird von einem Ladendetektiv beobachtet und der Polizei übergeben. Welches Gericht ist für die Hauptverhandlung sachlich zuständig?

**Normen:**

| Gesetz | Paragraph | Anmerkung |
|---|---|---|
| StGB | § 127 | Grundtatbestand Diebstahl (Strafdrohung bis 6 Monate oder Geldstrafe bis 360 Tagessätze) |
| StGB | § 128 | Schwerer Diebstahl: Wertgrenze EUR 5.000 (Abs 1 Z 5), greift hier nicht |
| StPO | § 30 | Zuständigkeit Bezirksgericht bei Strafdrohung bis zu einem Jahr |

**Judikatur:** keine, die Frage lässt sich aus dem Gesetzestext beantworten

**Begründung:**
- Der Wert von EUR 4.200 liegt unter der Wertgrenze des § 128 Abs 1 Z 5 StGB (EUR 5.000), daher einfacher Diebstahl nach § 127 StGB.
- Die Strafdrohung von bis zu 6 Monaten fällt in die Zuständigkeit des Bezirksgerichts nach § 30 StPO.
- **Nicht** aufgenommen werden:
  - § 129 StGB (Einbruchsdiebstahl): kein Einbruch im Sachverhalt
  - § 31 StPO (Zuständigkeit Landesgericht): kommt mangels qualifiziertem Tatbestand nicht in Betracht
