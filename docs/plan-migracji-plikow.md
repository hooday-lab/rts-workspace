# Plan przeniesienia plików z projektu claude.ai do repo (17.10.2026)

Z sesji Claude Code nie ma dostępu do plików projektu claude.ai. Każdy plik trzeba raz wkleić do czatu (albo wgrać), a Claude zapisuje go w `docs/` i wypycha na gałąź. Kolejność wg ważności:

| # | Plik | Po co | Priorytet |
| --- | --- | --- | --- |
| 1 | `statystyki-odswiezenie-k10.md` | instrukcja metody delta dla zadania „sprawdzenie bazy po meczu”; **bez niego zadanie zaplanowane nie ma instrukcji** | wysoki (przed 20.10) |
| 2 | `wpisy.md` | wzorce postów RTS Stats, typy kart; potrzebne do każdej paczki | wysoki |
| 3 | `statystyki.md`, `sklady-i-absencje.md` | format serii, baza liczb, składy do faz 1–2 (Górnik 23.10) | wysoki (przed 18.10, faza 1 Górnika) |
| 4 | `brand-rtsstat.md` | marka; zaktualizować hasztag na #RTSstats | średni |
| 5 | `plan-okno-piast-wisla-gornik.md` | okno meczowe; tylko Górnik jeszcze aktualny | średni |
| 6 | `wpisy-377-zapowiedz-faza2.md`, `wpisy-377-faza3.md`, `wpisy-wisla-faza1.md`, `wpisy-376-faza3.md`, `wpisy-clubfantasy.md` | archiwum wysłanych paczek | niski (kandydaci do archiwum) |
| 7 | `transkrypcja-376.md`, `klipy-376.md` | odcinek #376 zamknięty; zostawić w claude.ai | archiwum, nie przenosić |
| 8 | `statystyki*.md` pozostałe (karty, studio, studio-strona) | opis Studio; kod i tak jest w `studio/` | niski |

## Zasady przy przenoszeniu
- Przy kopiowaniu zamieniamy stary hasztag `#RTSstat` na `#RTSstats`.
- Nie przenosimy webhooków ani kluczy (trafiają do zmiennych środowiska, `ZMIENNE.md`).
- Pliki archiwalne (pkt 6–7) przenosimy do `docs/archiwum/` dopiero na prośbę.
- Po przeniesieniu pliku skreślamy go z tabeli i dopisujemy linię do logu w `tablica.md`.
