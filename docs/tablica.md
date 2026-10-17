# Tablica projektu RTS — komunikacja między sesjami

**Każda sesja czyta ten plik na początku** i (1) wykonuje zadania ze swojej skrzynki, (2) po wykonaniu zmienia status na „zrobione" z datą, (3) gdy ustali coś, co dotyczy innego obszaru — dopisuje zadanie do jego skrzynki, (4) każde ustalenie wpisuje też do właściwego pliku tematycznego i jedną linią do logu poniżej.

> Kopia z projektu claude.ai z 17.10.2026 (przeniesienie do Claude Code). Pełny stary log jest w `claude/tablica.md` w projekcie; tutaj stan bieżący i skrócony log.

## Mapa obszarów i plików
| Obszar | Co obejmuje | Pliki |
| --- | --- | --- |
| Statystyki | seria RTS Stats (format, mechaniki, baza liczb, karty PNG, dane z API-Football, strona Studio) | `statystyki.md`, `statystyki-karty.md`, `statystyki-studio.md`, `statystyki-studio-strona.md`, `statystyki-render-kart.md`, `sklady-i-absencje.md`, `statystyki-odswiezenie-k10.md`, `brand-rtsstat.md` |
| Wpisy | treści postów X/FB/IG, plan publikacji, wzorce copy | `wpisy.md`, `wpisy-376-faza3.md`, `wpisy-wisla-faza1.md`, `wpisy-377-zapowiedz-faza2.md`, `wpisy-377-faza3.md`, `wpisy-clubfantasy.md` |
| Odcinki | numer, tytuł, opis, gość, termin; transkrypcje i klipy | `rejestr-odcinkow.md`, `transkrypcja-376.md`, `klipy-376.md`, `procedura-po-odcinku.md` |
| Obieg komunikacji | standard komunikacji odcinka, plan okna meczowego, przypomnienia, zasady paczek | `obieg-komunikacji.md`, `plan-okno-piast-wisla-gornik.md`, `przypomnienia.md`, `integracje.md`, `zasady-paczek.md` |

Uwaga: nie wszystkie pliki z tej mapy są już skopiowane do `docs/`; brakujące (np. `wpisy.md`, `transkrypcja-376.md`) leżą w projekcie claude.ai i są dokopiowywane w miarę potrzeb.

## Zasady wspólne
- **Obieg odcinka wg `obieg-komunikacji.md`: model 4 FAZ** (przed meczem / bliska przedmeczowa / pomeczowa / po podcaście). Patryk dostaje na Discordzie 4 osobne paczki na mecz, każda w całości gotowa do publikacji i z kartami 4:5. Link do live znamy przed fazą 1. Wyjątek: faza 4 #376 odwołana (Bartek 15.10).
- **Twarde zasady paczek** (`zasady-paczek.md`): link do audycji, karta razem z postem, dwa przejścia, log po wysyłce, bez próśb o typowanie.
- Głos RTS: fakt → reakcja deadpan → pytanie do kibiców, pisane jak człowiek. Liczby tylko z bazy. Hasztag serii **#RTSstat**. Nazwa narzędzia: **RTS Stats Studio** (RSS).
- Posty zaproszeniowe (ClubFantasy): luźniej, najpierw konkret, bez hard sellu (`wpisy-clubfantasy.md`).
- **Procedura po odcinku** (`procedura-po-odcinku.md`): komendy `/NNN`, `/NNN_zmien`, `/NNN_fragmenty`.

## Stan bieżący (17.10.2026)
- #377 (Widzew 0:0 Wisła Kraków): live niedziela 19.10, 19:10, link https://youtu.be/K8Vz0AFqbZc. Faza 1, 2 i 3 wysłane. Do zrobienia: Bartek ustawia tytuł i opis na YT; po live `/377`; faza 4 #377 do decyzji Bartka.
- **Górnik (K12, 23.10, dom): faza 1 do przygotowania po odświeżeniu danych po K11, najpóźniej D−5 (18.10).**
- Dane Studio: Firestore `data/stats` odświeżone 17.10 częściowo po K11 (2/9 meczów + zaległe Radomiak–Motor i GKS–Wieczysta; lastRound=11). Druga delta po meczach K11 z 17–19.10 (Górnik–Piast 18.10). Metoda i skrypty: `statystyki-odswiezenie-k10.md`, `studio/delta/`.
- Zadanie zaplanowane do ustawienia: sprawdzenie bazy 30 min po meczu Widzewa (ponawiać co godzinę).
- Przeniesienie do Claude Code (17.10): prywatne repo `rts-workspace` (ten), środowisko `RTS`, sekrety w zmiennych (`../ZMIENNE.md`). Webhooki Discorda do unieważnienia i wygenerowania na nowo.
- Rename brandu na RTS Stats Studio (RSS) wdrożony 17.10 (commit `4f5dbb3` w `hooday-lab/rtsstat`).

## Skrzynki (otwarte)
- **Wpisy:** wzorce RTS Stats w `wpisy.md`; dopisać typy „Forma przed meczem", „0 kontra 0", wzorzec posta po remisie bez goli; typy „Zgadnij liczbę" i „Typowanie" wycofane (16.10). Priorytet niski.
- **Statystyki:** karta #13 (Górnik) i licznik domowy po K11 (0W-4R-2P, nie wysłany); etap 2 automatycznego importu Supabase → Firestore czeka na rolę read-only; historia sezonów z Dysku (Apps Script v2) czeka na Bartka.
- **Odcinki:** tytuł i opis #377 na YT; opis z rozdziałami po live; wiersz #376 zaktualizowany.
- **Obieg:** paczka 1 Górnika; decyzja o fazie 4 #377.

## Log ustaleń (najnowsze na górze)
- **17.10.2026 (rano):** `data/stats` częściowo po K11 (fx 92, tstats 180, goals 268, players 429, lastRound=11); kopia K10 w `data/stats_backup_k10`; zapis kontem serwisowym z Claude Code (bez Chrome).
- **17.10.2026:** przeniesienie do Claude Code; nazwa RTS Stats Studio (RSS); dokumenty kopiowane do prywatnego repo bez webhooków.
- **16.10.2026:** faza 3 #377 po 0:0 (wysłana ok. 22:50): karta „Mecz" z posiadaniem, strzałami, rożnymi i xG; Wisła nie wykorzystała karnego w 66. min; Widzew po K11: 1W-7R-3P, 10 pkt, u siebie 0-4-2, ósmy mecz bez wygranej. Zasada 5: bez próśb o typowanie. Zapowiedź live + faza 2 wysłane ok. 12:50. Poprawka: curl z `--form-string payload_json=...`.
- **15.10.2026:** live #377 w niedzielę 19.10 o 19:10 (1910); faza 4 #376 odwołana.
- **14.10.2026:** procedura po odcinku; tytuł #376 wariant A; klipy #376 na #fragmenty-do-wycięcia + ankieta.
- **13.10.2026:** faza 1 przed Wisłą wysłana (4 posty z kartami).
- **12.10.2026:** K10 w bazie; Studio `data/stats` odświeżone (89 meczów, 426 zawodników, lastRound=10).
- **11.10.2026:** faza 3 #376 (Piast 2:1 Widzew): karty „Mecz" i „Końcówki"; paczka 3 wysłana.
- **10.10.2026:** model 4 faz, karty 4:5 w paczkach, dwie twarde zasady paczek, korekta tekstów, typ karty „Dom i wyjazd".
- **09.10.2026:** Studio online (GitHub Pages + Firebase `rtsstat-55616`); plan okna Piast–Wisła–Górnik.
- **29.09–27.09.2026:** źródło danych, nazwa serii, podział ról, TikTok poza obiegiem.
