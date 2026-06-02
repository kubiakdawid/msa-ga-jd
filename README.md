<p align="center">
  <img src="logo.png" alt="logo" width="480"/>
</p>

# MSA  algorytm genetyczny

Projekt zaliczeniowy. Implementacja GA dla problemu Multiple Sequence Alignment.

![Status](https://img.shields.io/badge/Status-W_fazie_test%C3%B3w-orange?style=flat-square)

> [!WARNING]
> **Harmonogram projektu:** Obecny kod jest w fazie testów. Ostateczna, zoptymalizowana wersja kodu zostanie opublikowana **08.06.2026 r.**

## Co robi

Bierze zestaw sekwencji DNA i stara się je jak najlepiej dopasować do siebie - tzn. ustawić tak, żeby podobne fragmenty trafiły w te same kolumny. Tam gdzie sekwencje mają różne długości, wstawiane są gapy (`-`). Jakość dopasowania mierzona jest funkcją sum-of-pairs (SP-score), którą GA stara się zmaksymalizować.

## Struktura

```
msa_ga/
├── msa.py        # reprezentacja + funkcja celu SP
├── ga.py         # algorytm genetyczny
├── generator.py  # generator instancji testowych
├── main.py       # eksperymenty i wykresy
└── report/       # generowane automatycznie
```

## Uruchomienie

```bash
pip install numpy matplotlib
python main.py
```

Generuje wykresy zbieżności i tabelę wyników w `report/`.
