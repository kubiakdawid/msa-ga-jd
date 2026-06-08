<p align="center">
  <img src="logo.png" alt="logo" width="480"/>
</p>

# MSA — algorytm genetyczny

Projekt zaliczeniowy. Implementacja GA dla problemu Multiple Sequence Alignment.

![Status](https://img.shields.io/badge/Status-W_fazie_test%C3%B3w-orange?style=flat-square)
![Wersja](https://img.shields.io/badge/wersja-v0.1.0-blue?style=flat-square)
> [!NOTE]
> **Wydanie v0.1.0** — Pierwsza publiczna wersja projektu. Prosimy o zgłaszanie ewentualnych problemów ;)

> [!WARNING]
> **Harmonogram projektu:** Obecny kod jest w fazie testów. Ostateczna, zoptymalizowana wersja kodu zostanie opublikowana **08.06.2026 r.**

## Co robi

Bierze zestaw sekwencji DNA i stara się je jak najlepiej dopasować do siebie - tzn. ustawić tak, żeby podobne fragmenty trafiły w te same kolumny. Tam gdzie sekwencje mają różne długości, wstawiane są gapy (`-`). Jakość dopasowania mierzona jest funkcją sum-of-pairs (SP-score), którą GA stara się zmaksymalizować.

## Struktura

```
msa_ga/
├── msa.py         # reprezentacja + funkcja celu SP
├── ga.py          # algorytm genetyczny
├── generator.py   # generator instancji + wczytywanie sekwencji z pliku
├── main.py        # eksperymenty podstawowe + tabela wyników
├── tuning.py      # testy parametrów, klasy trudności, wykresy zbieżności
├── example.txt    # przykładowe sekwencje wejściowe
└── report/        # generowane automatycznie (wykresy, tabela)
```

## Uruchomienie

```bash
pip install numpy matplotlib
```

Eksperymenty podstawowe (tabela wyników w `report/`):

```bash
python main.py
```

Dopasowanie własnych sekwencji z pliku (jedna sekwencja na linię):

```bash
python main.py example.txt
```

Testy parametrów, klasy trudności i uśrednione wykresy zbieżności:

```bash
python tuning.py
```

## Wersje

### v0.1.0
- Pierwsza publiczna wersja
- GA dla MSA (DNA), funkcja celu sum-of-pairs
- Testy parametrów i klasy trudności
