// Annotationsanleitung - Print version
// Source of truth: codebook_annotators.md
// Build: typst compile codebook_annotators.typ

// ── Page ──
#set document(title: "Annotationsanleitung", date: datetime(year: 2026, month: 3, day: 31))
#set page(
  paper: "a4",
  margin: (top: 2cm, bottom: 2cm, left: 2.5cm, right: 2.5cm),
  header: context {
    if counter(page).get().first() > 1 {
      set text(8pt)
      [Annotationsanleitung #h(1fr) #counter(page).display("1")]
      v(-4pt)
      line(length: 100%, stroke: 0.3pt)
    }
  }, 
  footer: [],
)

// ── Typography ──
#set text(font: "Palatino Linotype", size: 10pt, lang: "de")
#set par(justify: true, leading: 0.58em, first-line-indent: 0em)
#set heading(numbering: "1.1")
#show heading.where(level: 1): it => { v(0.5em); text(11.5pt, weight: "bold")[#it]; v(0.15em) }
#show heading.where(level: 2): it => { v(0.4em); text(10pt, weight: "bold")[#it]; v(0.1em) }
#set list(indent: 0.5em, body-indent: 0.5em, spacing: auto)
#set enum(indent: 0.5em, body-indent: 0.5em, spacing: auto)

// ── Helpers ──
#let note-block(body) = block(
  width: 100%,
  inset: (left: 1.2em, top: 0.3em, bottom: 0.3em),
  stroke: (left: 0.5pt),
)[#text(size: 9.5pt, style: "italic")[#body]]

#let ruled-table(columns: (), header: (), ..rows) = {
  let data = rows.pos()
  block(width: 100%, above: 0.4em, below: 0.4em)[#table(
    columns: columns,
    stroke: none,
    inset: (x: 5pt, y: 3.5pt),
    align: left,
    table.hline(stroke: 0.7pt),
    ..header.map(h => text(weight: "bold", size: 9pt)[#h]),
    table.hline(stroke: 0.35pt),
    ..data.flatten().map(c => text(size: 9pt)[#c]),
    table.hline(stroke: 0.7pt),
  )]
}

// ══════════════════════════════════════════
// Title - compact, left-aligned
// ══════════════════════════════════════════

#text(14pt, weight: "bold")[Annotationsanleitung] #h(1fr) #text(9pt)[v0.5.0]
#v(-2pt)
#text(9pt)[Legal-Trace Benchmark #sym.dot.c Stichtag der Rechtslage: 01.01.2026]
#v(1pt)
#line(length: 100%, stroke: 0.5pt)
#v(0.3em)

Wir erstellen einen Datensatz, der dokumentiert, *welche Rechtsquellen ein Jurist zu einer österreichischen Rechtsfrage zitieren würde.* Es geht ausschließlich um die Quellenidentifikation, nicht darum, wie die Frage inhaltlich zu beantworten ist.

= Aufgabe

Gegeben ist ein Sachverhalt mit einer konkreten Rechtsfrage.

+ Identifizieren Sie alle *Normen des Bundesrechts* (Gesetze und Verordnungen), die für die Beantwortung der Frage nach österreichischem Recht (Rechtslage 01.01.2026) relevant sind.
+ Identifizieren Sie alle *Leitentscheidungen* (über deren Rechtssatznummer im RIS), die für die Frage relevant sind.

Jeder Annotator arbeitet *unabhängig*, d.h. ohne Einsicht in die Ergebnisse anderer Annotatoren.

= Was gilt als #[\u{201E}relevant\u{201C}]?

== Normen des Bundesrechts

Eine Norm ist relevant, wenn ein Jurist sie in einem *Kurzgutachten* (praxistypisch wenige Seiten), das ausschließlich die gestellte Frage beantwortet, *zitieren* würde.

#grid(
  columns: (1fr, 1fr),
  column-gutter: 1.5em,
  [
    #set par(justify: false)
    *Einschließen:*
    - Anspruchsgrundlage bzw. einschlägiger Tatbestand
    - Legaldefinitionen zentraler Begriffe der Hauptnorm
    - Bundesverordnungen, die das Gesetz konkretisieren
    - Anwendungsbereichsnormen, sofern Anwendbarkeit nicht offensichtlich
  ],
  [
    #set par(justify: false)
    *Ausschließen:*
    - EU-Recht, auch wenn unmittelbar anwendbar (z.B. DSGVO)
    - Landesrecht
    - Fremde Rechtsordnungen (Rechtsvergleiche)
    - Gesetzesmaterialien, Erläuterungen, Literatur
    - Normen, die nur allgemeines Hintergrundwissen darstellen
    - Verfahrensrecht (außer ausdrücklich gefragt)
  ],
)

_Gesetzlichen Verweisungen ist nur zu folgen, wenn die verwiesene Norm den materiellen Gehalt der Antwort verändert._

== Granularität

Annotieren Sie auf *Paragraphenebene*: § 30 MRG, nicht § 30 Abs 1 Z 8 MRG. Bei langen Sammel-Paragraphen die relevante Stelle im Anmerkungsfeld vermerken.

== Judikatur

Aufgenommen werden ausschließlich *Leitentscheidungen* der drei Höchstgerichte (OGH, VfGH, VwGH), identifiziert über ihre RS-Nummer im RIS. Eine Leitentscheidung ist eine Entscheidung, in der ein Höchstgericht erstmals einen für die Frage relevanten Rechtsgrundsatz aufgestellt hat.

Pro relevanter Norm im RIS nach Rechtssätzen suchen (z.B. Norm: MRG § 30). Betrifft ein Rechtssatz die konkrete Frage: aufnehmen (RS-Nummer + Geschäftszahl). Betrifft er sie nicht: überspringen.

Mehrere zutreffende Rechtssätze sind alle aufzunehmen. Folgeentscheidungen und untere Instanzen werden *nicht* aufgenommen.

== Vorgehen

#block(breakable: false)[
+ Sachverhalt lesen und Rechtsfragen identifizieren
+ Im RIS (Stichtag 01.01.2026) einschlägige Normen suchen
+ Gesetzestext lesen und Relevanz bestätigen
+ Judikatur nach obiger Anleitung suchen
+ Bei Bedarf mit Kommentarliteratur gegenprüfen

Bei Unsicherheit: *Aufnehmen* und Zweifel im Anmerkungsfeld vermerken. Eine kurze Begründung ist empfohlen, besonders bei nicht-trivialen Entscheidungen.
]

= Beispiele

*Beispiel 1: Einfach*

#note-block[Ein Vermieter hat vor 5 Jahren eine bereits vermietete Wohnung in einem Wiener Zinshaus gekauft. Er möchte nun das Mietverhältnis kündigen, weil sein Sohn die Wohnung dringend für sich benötigt. Die Wohnung fällt in den Vollanwendungsbereich des MRG. Ist die Kündigung wegen Eigenbedarfs zulässig?]

*Normen:*
#ruled-table(
  columns: (auto, auto, 1fr),
  header: ("Gesetz", "§", "Anmerkung"),
  [MRG], [§ 30], [Abs 2 Z 8/9: Eigenbedarf als Kündigungsgrund; Abs 3: 10-Jahres-Frist bei Erwerb],
)

#v(0.3em)

*Judikatur:*
#ruled-table(
  columns: (auto, auto, auto, auto, 1fr),
  header: ("Gericht", "GZ", "RS-Nr.", "Datum", "Anmerkung"),
  [OGH], [7 Ob 598/84], [RS0070482], [1984-06-20], [Strenger Maßstab bei dringendem Eigenbedarf],
)

#v(0.3em)

*Begründung:* § 30 MRG enthält die abschließende Liste der Kündigungsgründe inkl. Eigenbedarf und die 10-Jahres-Sperrfrist für Erwerber. § 1 MRG (Anwendungsbereich) und § 33 MRG (Formvorschriften) werden nicht aufgenommen, weil der Sachverhalt die Anwendbarkeit feststellt und die Frage nicht verfahrensrechtlicher Natur ist.

#v(0.9em)
*Beispiel 2: Mittel (gesetzesübergreifend)*

#note-block[Ein Mann stiehlt in einem Wiener Kaufhaus Elektronikartikel im Wert von EUR 4.200. Er wird von einem Ladendetektiv beobachtet und der Polizei übergeben. Welches Gericht ist für die Hauptverhandlung sachlich zuständig?]

*Normen:*
#ruled-table(
  columns: (auto, auto, 1fr),
  header: ("Gesetz", "§", "Anmerkung"),
  [StGB], [§ 127], [Grundtatbestand Diebstahl (bis 6 Monate oder Geldstrafe bis 360 Tagessätze)],
  [StGB], [§ 128], [Schwerer Diebstahl: Wertgrenze EUR 5.000 (Abs 1 Z 5), greift hier nicht],
  [StPO], [§ 30], [Zuständigkeit Bezirksgericht bei Strafdrohung bis zu einem Jahr],
)

#v(0.3em)
*Judikatur:* keine, die Frage lässt sich aus dem Gesetzestext beantworten

#v(0.3em)
*Begründung:* Der Wert liegt unter EUR 5.000 (§ 128 StGB), daher einfacher Diebstahl nach § 127 StGB. Die Strafdrohung von bis zu 6 Monaten fällt in die Zuständigkeit des Bezirksgerichts (§ 30 StPO). § 129 StGB (Einbruchsdiebstahl) und § 31 StPO (Zuständigkeit Landesgericht) werden nicht aufgenommen.
