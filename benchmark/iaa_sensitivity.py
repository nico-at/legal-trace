from itertools import combinations


def krippendorff_alpha(units: list[tuple[int, ...]]) -> float:
    if not units:
        return 1.0

    m = len(units[0])
    categories = set(v for unit in units for v in unit)
    if len(categories) < 2:
        return 1.0

    o: dict[tuple[int, int], float] = {}
    for unit in units:
        for j in range(m):
            for k in range(m):
                if j != k:
                    pair = (unit[j], unit[k])
                    o[pair] = o.get(pair, 0) + 1 / (m - 1)

    n_c = {c: sum(o.get((c, c2), 0) for c2 in categories) for c in categories}
    n = sum(n_c.values())

    D_o = 1 - sum(o.get((c, c), 0) for c in categories) / n
    D_e = 1 - sum(nc * (nc - 1) for nc in n_c.values()) / (n * (n - 1))

    if D_e == 0:
        return 1.0
    return 1 - D_o / D_e


def f1(set_a: set[str], set_b: set[str]) -> float:
    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 0.0
    overlap = len(set_a & set_b)
    precision = overlap / len(set_a)
    recall = overlap / len(set_b)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def mean_pairwise_f1(annotations: list[list[set[str]]]) -> float:
    scores = []
    for question_sets in annotations:
        for a, b in combinations(range(len(question_sets)), 2):
            scores.append(f1(question_sets[a], question_sets[b]))
    return sum(scores) / len(scores) if scores else 1.0


def build_scenario(
    n_questions: int,
    core_per_q: int,
    missed_per_q: int,
    extras_per_q: int,
) -> tuple[list[tuple[int, ...]], list[list[set[str]]]]:
    alpha_units = []
    f1_annotations = []

    for q in range(n_questions):
        sets: list[set[str]] = [set(), set(), set()]
        source_id = 0

        # Alle einig
        for _ in range(core_per_q):
            name = f"Q{q}_S{source_id}"
            source_id += 1
            alpha_units.append((1, 1, 1))
            for a in range(3):
                sets[a].add(name)

        # Fehler (einer fehlt)
        for i in range(missed_per_q):
            name = f"Q{q}_S{source_id}"
            source_id += 1
            missing_annotator = i % 3
            coding = [1, 1, 1]
            coding[missing_annotator] = 0
            alpha_units.append(tuple(coding))
            for a in range(3):
                if a != missing_annotator:
                    sets[a].add(name)

        # Extras (nur einer hat sie)
        for i in range(extras_per_q):
            name = f"Q{q}_X{i}"
            extra_annotator = i % 3
            coding = [0, 0, 0]
            coding[extra_annotator] = 1
            alpha_units.append(tuple(coding))
            sets[extra_annotator].add(name)

        f1_annotations.append(sets)

    return alpha_units, f1_annotations


def label_alpha(a: float) -> str:
    if a >= 0.80:
        return "reliabel"
    if a >= 0.67:
        return "tentativ"
    return "problematic"


def label_f1(f: float) -> str:
    if f >= 0.90:
        return "sehr gut"
    if f >= 0.80:
        return "gut"
    if f >= 0.70:
        return "akzeptabel"
    return "problematisch"


def run():
    scenarios = [
        ("Perfekt: alle einig", 4, 0, 0),
        ("Minimal: 1 Quelle/Frage übersehen", 4, 1, 0),
        ("Leicht: 1 übersehen + 1 Extra/Frage", 4, 1, 1),
        ("Moderat: 1 übersehen + 1 Extra/Frage", 3, 1, 1),
        ("Grenzwertig: 2 übersehen + 1 Extra", 3, 2, 1),
        ("Problematisch: 2 übersehen + 2 Extras", 3, 2, 2),
        ("Schlecht: 2 übersehen + 3 Extras", 2, 2, 3),
    ]

    print("IAA-Sensitivitaet: Krippendorffs Alpha vs. Pairwise F1")
    print("Setting: 10 Fragen, 3 Annotatoren")
    print("=" * 78)
    print()
    print(f"  {'Szenario':<42} {'Alpha':>7} {'':>14} {'F1':>7} {'':>1}")
    print(f"  {'':<42} {'':>7} {'':>14} {'':>7}")

    for desc, core, missed, extras in scenarios:
        alpha_units, f1_data = build_scenario(10, core, missed, extras)
        a = krippendorff_alpha(alpha_units)
        f = mean_pairwise_f1(f1_data)
        print(f"  {desc:<42} {a:>7.3f} {label_alpha(a):<14} {f:>7.3f} {label_f1(f)}")


if __name__ == "__main__":
    run()
