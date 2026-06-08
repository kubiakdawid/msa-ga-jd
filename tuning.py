import os
import numpy as np
import matplotlib.pyplot as plt

from ga import run_ga
from generator import TUNING_SET, LATWE, SREDNIE, TRUDNE, SMALL_INSTANCES, MEDIUM_INSTANCES

os.makedirs("report", exist_ok=True)

DEFAULTS = dict(pop_size=30, n_generations=120, crossover_prob=0.8,
                mutation_rate=0.3, tournament_k=3, elitism=2)


def sweep(nazwa, klucz, wartosci, zbior, n_runs=10):
    print(f"=*= test parametru: {nazwa} =*=")
    srednie = []
    odchylenia = []
    for v in wartosci:
        wyniki = []
        for sekw in zbior:
            params = dict(DEFAULTS)
            params[klucz] = v
            for _ in range(n_runs):
                _, w, _ = run_ga(sekw, **params)
                wyniki.append(w)
        srednie.append(np.mean(wyniki))
        odchylenia.append(np.std(wyniki))
        print(f"  {nazwa} = {v}: SP śr={np.mean(wyniki):.1f}  std={np.std(wyniki):.1f}")

    plt.figure()
    plt.errorbar(range(len(wartosci)), srednie, yerr=odchylenia, marker="o", capsize=4)
    plt.xticks(range(len(wartosci)), [str(x) for x in wartosci])
    plt.xlabel(nazwa)
    plt.ylabel("Średni SP-score")
    plt.title(f"Wpływ parametru: {nazwa}")
    plt.tight_layout()
    plt.savefig(f"report/param_{klucz}.png")
    plt.close()
    print(f"Wykres zapisany: report/param_{klucz}.png\n")
    return srednie, odchylenia


def klasy_trudnosci(n_runs=10):
    print("=*= Klasy trudności (podobieństwo sekwencji) =*=")
    nazwy = ["łatwe", "średnie", "trudne"]
    zbiory = [LATWE, SREDNIE, TRUDNE]
    srednie = []
    for nazwa, zbior in zip(nazwy, zbiory):
        konce = []
        for sekw in zbior:
            for _ in range(n_runs):
                _, w, _ = run_ga(sekw, **DEFAULTS)
                konce.append(w)
        srednie.append(np.mean(konce))
        print(f"  {nazwa}: SP śr={np.mean(konce):.1f}  std={np.std(konce):.1f}")

    plt.figure()
    plt.bar(nazwy, srednie, color=["#4c72b0", "#dd8452", "#c44e52"])
    plt.ylabel("Średni końcowy SP-score")
    plt.title("Jakość dopasowania wg klasy trudności")
    plt.tight_layout()
    plt.savefig("report/classes.png")
    plt.close()
    print("Zapisuje.. report/classes.png\n")


def avg_convergence(sekw, label, fname, n_runs=10):
    historie = []
    for _ in range(n_runs):
        _, _, h = run_ga(sekw, **DEFAULTS)
        historie.append(h)
    historie = np.array(historie)
    srednia = historie.mean(axis=0)
    odch = historie.std(axis=0)
    x = np.arange(len(srednia))

    plt.figure()
    plt.plot(x, srednia, label="średnia z 10 uruchomień")
    plt.fill_between(x, srednia - odch, srednia + odch, alpha=0.2, label="+- odchylenie std")
    plt.xlabel("Generacja")
    plt.ylabel("Najlepszy SP-score")
    plt.title(f"Zbieżność GA {label}")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"report/{fname}")
    plt.close()
    print(f"Wykres zapisuje do.. report/{fname}")


if __name__ == "__main__":
    sweep("rozmiar populacji", "pop_size", [10, 20, 30, 50, 80], TUNING_SET)
    sweep("prawdop. mutacji", "mutation_rate", [0.0, 0.1, 0.3, 0.5, 0.8], TUNING_SET)
    sweep("prawdop. krzyżowania", "crossover_prob", [0.0, 0.4, 0.6, 0.8, 1.0], TUNING_SET)
    klasy_trudnosci()
    avg_convergence(SMALL_INSTANCES[0], "mała instancja", "convergence_mala.png")
    avg_convergence(MEDIUM_INSTANCES[0], "średnia instancja", "convergence_srednia.png")
    print("Mamy to!")
