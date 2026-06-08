import random

ALPHABET = ['A', 'C', 'G', 'T']


def random_sequence(dl):
    return ''.join(random.choices(ALPHABET, k=dl))


def descend_from(przodek, sub_rate, indel_rate):
    wynik = []
    for lit in przodek:
        r = random.random()
        if r < indel_rate:
            continue
        if r < indel_rate + sub_rate:
            wynik.append(random.choice(ALPHABET))
        else:
            wynik.append(lit)
        if random.random() < indel_rate:
            wynik.append(random.choice(ALPHABET))
    return ''.join(wynik) if wynik else przodek[:1]


def make_family(n_seqs, dl, sub_rate, indel_rate, seed):
    random.seed(seed)
    przodek = random_sequence(dl)
    return [descend_from(przodek, sub_rate, indel_rate) for _ in range(n_seqs)]


def make_class(n_inst, n_seqs, dl, sub_rate, indel_rate, base_seed):
    return [make_family(n_seqs, dl, sub_rate, indel_rate, base_seed + i)
            for i in range(n_inst)]


SMALL_INSTANCES  = make_class(5, 5, 30, sub_rate=0.12, indel_rate=0.04, base_seed=42)
MEDIUM_INSTANCES = make_class(5, 6, 60, sub_rate=0.12, indel_rate=0.04, base_seed=43)

LATWE  = make_class(5, 6, 50, sub_rate=0.05, indel_rate=0.02, base_seed=100)
SREDNIE = make_class(5, 6, 50, sub_rate=0.15, indel_rate=0.05, base_seed=200)
TRUDNE = make_class(5, 6, 50, sub_rate=0.30, indel_rate=0.08, base_seed=300)

TUNING_SET = (make_class(2, 5, 30, sub_rate=0.05, indel_rate=0.02, base_seed=500)
              + make_class(2, 5, 30, sub_rate=0.15, indel_rate=0.05, base_seed=510)
              + make_class(2, 5, 30, sub_rate=0.30, indel_rate=0.08, base_seed=520))


def load_sequences(path):
    with open(path, encoding="utf-8") as f:
        return [linia.strip().upper() for linia in f if linia.strip()]
