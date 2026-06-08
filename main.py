import time
import sys
import numpy as np
import matplotlib.pyplot as plt
import os

from msa import score_sp, decode, is_valid
from ga import run_ga
from generator import SMALL_INSTANCES, MEDIUM_INSTANCES, load_sequences

os.makedirs("report", exist_ok=True)


def verify_document_example():
    sekw = ["AGTCGTAG", "ATCGTCG", "GTAG", "GTAGAG"]

    mac = np.array([
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 0, 1, 1],
    ])

    sp = score_sp(mac, sekw)

    print("=*[ Weryfikacja przykładu z doku ]*=")
    for w in decode(mac, sekw):
        print(w)
    print(f"SP-score: {sp}  (oczekiwane: -9)")
    print(f"Dopasowanie dopuszczalne: {is_valid(mac, sekw)}")
    print()


def run_experiment(instancje, label, n_runs=10, pop_size=30, n_generations=120):
    print(f"=*[ Eksperymenty: {label} ]*=")
    rzedy = []

    for idx, sekw in enumerate(instancje):
        starty = []
        konce = []
        czasy = []

        for _ in range(n_runs):
            t0 = time.time()
            najlepszy, wynik, historia = run_ga(sekw, pop_size=pop_size, n_generations=n_generations)
            czasy.append(time.time() - t0)
            starty.append(historia[0])
            konce.append(wynik)

        sr_start = np.mean(starty)
        sr_koniec = np.mean(konce)
        naj_koniec = max(konce)
        odch = np.std(konce)
        sr_czas = np.mean(czasy)
        poprawa = sr_koniec - sr_start

        print(f"  Instancja {idx+1}: start={sr_start:.1f} | koniec śr={sr_koniec:.1f} "
              f"| najlepszy={naj_koniec} | std={odch:.1f} | poprawa={poprawa:.1f} | czas={sr_czas:.1f}s")

        rzedy.append({
            "instancja": idx + 1,
            "start": sr_start,
            "koniec": sr_koniec,
            "naj": naj_koniec,
            "odch": odch,
            "poprawa": poprawa,
            "czas": sr_czas,
        })

    print()
    return rzedy


def plot_summary_table(male, srednie):
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.axis("off")

    naglowki = ["Klasa", "Inst.", "Start (śr.)", "Koniec (śr.)", "Najlepszy", "Std", "Poprawa", "Czas [s]"]
    dane = []

    for r in male:
        dane.append([
            "Mała", r["instancja"],
            f"{r['start']:.1f}", f"{r['koniec']:.1f}",
            r["naj"], f"{r['odch']:.1f}",
            f"{r['poprawa']:.1f}", f"{r['czas']:.1f}"
        ])
    for r in srednie:
        dane.append([
            "Średnia", r["instancja"],
            f"{r['start']:.1f}", f"{r['koniec']:.1f}",
            r["naj"], f"{r['odch']:.1f}",
            f"{r['poprawa']:.1f}", f"{r['czas']:.1f}"
        ])

    tab = ax.table(cellText=dane, colLabels=naglowki, loc="center", cellLoc="center")
    tab.auto_set_font_size(False)
    tab.set_fontsize(9)
    tab.scale(1, 1.5)
    plt.title("Wyniki eksperymentów... podsumowanie", pad=20)
    plt.tight_layout()
    plt.savefig("report/summary_table.png")
    plt.close()
    print("Tabela zapisana: report/summary_table.png")


def run_on_file(path):
    sekw = load_sequences(path)
    print(f"=*[ Dopasowanie sekwencji z pliku: {path} ]*=")
    print(f"Wczytano sekwencji: {len(sekw)}")
    najlepszy, wynik, historia = run_ga(sekw)
    for w in decode(najlepszy, sekw):
        print(w)
    print(f"SP-score: {wynik}  (start: {historia[0]})")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_on_file(sys.argv[1])
    else:
        verify_document_example()

        male = run_experiment(SMALL_INSTANCES, label="Małe instancje", n_runs=10)
        srednie = run_experiment(MEDIUM_INSTANCES, label="Średnie instancje", n_runs=10)

        plot_summary_table(male, srednie)

        print("Gotowe ;)")
