import numpy as np
import random
from msa import score_sp, remove_empty_columns


def random_individual(sekw):
    maxd = max(len(s) for s in sekw)
    szer = maxd + max(2, maxd // 4)
    wiersze = []
    for s in sekw:
        w = np.array([1] * len(s) + [0] * (szer - len(s)))
        np.random.shuffle(w)
        wiersze.append(w)
    return remove_empty_columns(np.array(wiersze))


def initial_population(sekw, ile):
    return [random_individual(sekw) for _ in range(ile)]


def tournament_pick(pop, oceny, k=3):
    kand = random.sample(range(len(pop)), k)
    naj = max(kand, key=lambda i: oceny[i])
    return pop[naj].copy()


def _suffix_after(w, n_liter):
    if n_liter == 0:
        return w.copy()
    licz = 0
    for j in range(len(w)):
        if w[j] == 1:
            licz += 1
            if licz == n_liter:
                return w[j + 1:].copy()
    return np.array([], dtype=int)


def _make_child(lewy, prawy):
    ile = lewy.shape[0]
    ciecie = random.randint(1, lewy.shape[1] - 1)
    wiersze = []
    for i in range(ile):
        lewa = lewy[i, :ciecie]
        ile_lit = int(lewa.sum())
        prawa = _suffix_after(prawy[i], ile_lit)
        wiersze.append(np.concatenate([lewa, prawa]))
    szer = max(len(w) for w in wiersze)
    mac = np.array([
        np.concatenate([w, np.zeros(szer - len(w), dtype=int)])
        for w in wiersze
    ])
    return remove_empty_columns(mac)


def crossover(r1, r2):
    if r1.shape[1] < 2 or r2.shape[1] < 2:
        return r1.copy(), r2.copy()
    return _make_child(r1, r2), _make_child(r2, r1)


def mutate_shift(osob, rate=0.3):
    kopia = osob.copy()
    if random.random() > rate:
        return kopia
    wierszy, kolumn = kopia.shape
    w = random.randint(0, wierszy - 1)
    luki = list(np.where(kopia[w] == 0)[0])
    if not luki:
        return kopia
    poz = random.choice(luki)
    sasiad = poz + random.choice([-1, 1])
    if 0 <= sasiad < kolumn:
        kopia[w, poz], kopia[w, sasiad] = kopia[w, sasiad], kopia[w, poz]
    return remove_empty_columns(kopia)


def run_ga(sekw, pop_size=30, n_generations=120,
           crossover_prob=0.8, mutation_rate=0.3,
           tournament_k=3, elitism=2):

    pop = initial_population(sekw, pop_size)
    oceny = [score_sp(o, sekw) for o in pop]

    naj_i = int(np.argmax(oceny))
    najlepszy = pop[naj_i].copy()
    naj_ocena = oceny[naj_i]
    historia = [naj_ocena]

    for _ in range(n_generations):
        ranking = sorted(range(len(oceny)), key=lambda i: oceny[i], reverse=True)
        nowa = [pop[i].copy() for i in ranking[:elitism]]

        while len(nowa) < pop_size:
            r1 = tournament_pick(pop, oceny, tournament_k)
            r2 = tournament_pick(pop, oceny, tournament_k)
            if random.random() < crossover_prob:
                dz1, dz2 = crossover(r1, r2)
            else:
                dz1, dz2 = r1.copy(), r2.copy()
            nowa.append(mutate_shift(dz1, mutation_rate))
            if len(nowa) < pop_size:
                nowa.append(mutate_shift(dz2, mutation_rate))

        pop = nowa
        oceny = [score_sp(o, sekw) for o in pop]

        i_gen = int(np.argmax(oceny))
        if oceny[i_gen] > naj_ocena:
            naj_ocena = oceny[i_gen]
            najlepszy = pop[i_gen].copy()
        historia.append(naj_ocena)

    return najlepszy, naj_ocena, historia
