# Przypomnienia (zaplanowane zadania) — okno meczowe RTS

Zaplanowane zadania uruchamiają nową sesję Claude o zadanej porze; wysyłają Bartkowi powiadomienie push i wykonują opisaną czynność. Ustawione 10.10.2026 (decyzja Bartka). Zasady faz: `obieg-komunikacji.md`; wysyłka na Discord: `integracje.md`; **twarde zasady paczek (link do audycji w treści, karta razem z postem): `zasady-paczek.md` — każde zadanie czyta je przed przygotowaniem lub wysyłką paczki.**

## Aktywne
| Zadanie | Kiedy | Co robi |
| --- | --- | --- |
| RTS #376: skład przed meczem | niedz. 11.10, 13:30 (CEST) | pyta o skład (post ze składem na ok. 13:45), przypomina o „faza 3" po meczu |
| RTS #376: faza 3 po meczu | niedz. 11.10, 16:40 | prosi o wynik i strzelców; po wyniku wykonuje fazę 3 i wysyła paczkę 3 (z linkiem i kartą „Mecz") |
| RTS #376: faza 4 po live i plan kolejnego meczu | niedz. 11.10, 21:45 | prosi o „faza 4" i klipy; wysyła paczkę 4; **dopilnowuje, że w harmonogramie są zadania dla następnego meczu** (D−3 wt ok. 9:00 i D−1 czw — faza 1; M−3h — paczka 2/skład; M+2h — „faza 3"; L+2,5h — „faza 4"), tworzy brakujące |
| RTS: faza 1 następnego meczu (wt/czw) | co wtorek i czwartek, 8:47 (Europe/Warsaw), cyklicznie | sprawdza, czy paczka fazy 1 najbliższego meczu poszła; jeśli nie i do meczu ≤ 6 dni — pyta o brakujące dane i wysyła paczkę 1 |

## Zasada ciągłości
Po każdej fazie 4 (koniec okna jednego meczu) trzeba mieć w harmonogramie przypomnienia dla następnego meczu (patrz zadanie „faza 4"). Jeśli ich brakuje — utworzyć je od razu i dopisać tu.

## Uwaga
Treści zadań (prompty) odsyłają do dokumentów projektu; nowe zasady dopisujemy do `zasady-paczek.md`, żeby nie trzeba było zmieniać każdego zadania osobno.

## Do zrobienia po przeniesieniu do Claude Code (17.10.2026)
- Sprawdzenie danych 30 min po meczu Widzewa (ponawiaj co godzinę do skutku) i odświeżenie Firestore `data/stats` (metoda delta, `statystyki-odswiezenie-k10.md`).

## Zadania zaplanowane ustawione 17.10.2026 (chmura, bez komputera)
| Zadanie | Kiedy | Co robi |
| --- | --- | --- |
| RTS: kolejka 11 kompletna, odświeżenie Studio | wt. 20.10, 09:00 (CEST) | sprawdza, czy wszystkie 9 meczów K11 jest FT w bazie; push do Bartka; ponawia co 3 h (maks. 4 próby). Na 17.10 w bazie są tylko 2 mecze K11 (Wieczysta–Raków, Widzew–Wisła 0:0) |
| RTS: sprawdzenie bazy po meczu z Górnikiem | pt. 23.10, 23:00 (CEST) | sprawdza, czy Widzew–Górnik jest FT; push z wynikiem; ponawia co godzinę (maks. 6 prób). Godzina meczu 23.10 niepotwierdzona (zakładane 20:30) |
Zadania nic nie publikują i nie wysyłają na Discorda. Wpis do Firestore `data/stats` nadal wymaga sesji z Chrome Bartka.
