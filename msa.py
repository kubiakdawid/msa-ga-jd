import numpy as np
from itertools import combinations


MATCH = 1
MISMATCH = -1
GOPEN = -2
GEXT = -1


def decode(mac, sekw):
    wynik = []
    for i, s in enumerate(sekw):
        wiersz = mac[i]
        k = 0
        linia = ""
        for v in wiersz:
            if v == 1:
                linia += s[k]
                k += 1
            else:
                linia += "-"
        wynik.append(linia)
    return wynik


def is_valid(mac, sekw):
    kolumny = mac.shape[1]
    for i, s in enumerate(sekw):
        if np.sum(mac[i]) != len(s):
            return False
    for j in range(kolumny):
        if np.sum(mac[:, j]) == 0:
            return False
    return True


def remove_empty_columns(mac):
    sumy = np.sum(mac, axis=0)
    return mac[:, sumy > 0]


def score_pair(w1, w2, s1, s2):
    n = len(w1)
    suma = 0
    i1 = 0
    i2 = 0
    luka1 = False
    luka2 = False

    for j in range(n):
        gap1 = (w1[j] == 0)
        gap2 = (w2[j] == 0)

        if not gap1 and not gap2:
            suma += MATCH if s1[i1] == s2[i2] else MISMATCH
            i1 += 1
            i2 += 1
            luka1 = False
            luka2 = False
        elif gap1 and not gap2:
            suma += GEXT if luka1 else GOPEN
            i2 += 1
            luka1 = True
            luka2 = False
        elif not gap1 and gap2:
            suma += GEXT if luka2 else GOPEN
            i1 += 1
            luka1 = False
            luka2 = True
        else:
            luka1 = False
            luka2 = False

    return suma


def score_sp(mac, sekw):
    n = len(sekw)
    suma = 0
    for i, j in combinations(range(n), 2):
        suma += score_pair(mac[i], mac[j], sekw[i], sekw[j])
    return suma
