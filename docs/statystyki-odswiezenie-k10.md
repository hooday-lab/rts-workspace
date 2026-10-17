# Odświeżenie danych Studio po K10 (12.10.2026)
Właściciel: czat „Statystyki". Uzupełnia `statystyki-studio-strona.md` i `statystyki-render-kart.md`.

## Co zrobiono (12.10.2026)
- K10 jest w bazie ClubFantasy (`api_fixtures_raw`: 8 meczów FT, pobrane 11.10 ok. 22:20–22:55 UTC). Wcześniej 11.10 wszystkie wywołania live kończyły się błędem HTTP 500 (m.in. brak kolumny `goals` w `live_meta`); później dane dotarły, a `auto_close` zwraca `{"setting":"all"}`.
- Firestore `data/stats` odświeżone metodą delta (dopisanie K10 do istniejącego JSON): fx 81→89, tstats 156→172, goals 229→257, players 424→426 (28 kolumn), meta lastRound=10, generatedAt 2026-10-12; z `upcoming` usunięto mecze K10 sprzed 12.10.
- `starts` liczone z `raw->lineups` (startXI, 176 zawodników), bo flaga zmiennika w surowych danych jest niewiarygodna. Średnia ocen: ((stara × apps) + ocena K10) / (apps+1), zaokrąglenie do 0,01.
- Weryfikacja: liczności jak wyżej, suma id zawodników 78939132; strona ładuje się z zakładkami po twardym odświeżeniu (`?v=`). Odświeżenie danych nie wymaga wdrożenia strony (dane czytane w runtime z Firestore).

## Nowa funkcja Studio (12.10.2026, commit 5d17ab3)
- Przy każdej karcie sekcja „Pakiet dla komunikacji (prompt do posta)" z przyciskiem „Kopiuj pakiet": zadanie dla czatu komunikacji, typ i teksty karty, stan danych (sezon, kolejka, data), szkic tekstu ze Studio, zasady głosu RTS (fakt, deadpan, pytanie; #RTSstat; bez wymyślonych liczb), link do live (pole opcjonalne). Dołącza się do tego PNG 4:5.
- Wysyłka na Discord nadal przez Claude (webhook jest sekretem, strona jest publiczna). Możliwy dalszy krok: zapis pakietu w Firestore i odczyt przez Claude albo Cloudflare Worker z przyciskiem „Wyślij do Patryka".

## Uwagi
- Radomiak–Motor (12.10, 16:00 UTC) należy do K10 i nie był rozegrany: po nim odświeżyć dane ponownie (delta).
- Gol Świderskiego (71') po rożnym: brak w danych, nie używane.
- Widzew–Wisła Kr.: piątek 16.10, 20:30 (czas polski; z `upcoming` w Studio).

## Wymuszanie aktualizacji po meczach Widzewa
Claude ma w bazie tylko SELECT. Bartek wybrał (12.10): sprawdzenie ok. 30 min po meczu Widzewa. Uwaga: po K10 dane dotarły do bazy dopiero kilka godzin po meczu, więc sprawdzenia powtarzać co godzinę do skutku (do potwierdzenia przez Bartka). Zaplanowane zadania jeszcze nie ustawione.

---

## Układ danych `data/stats` (odtworzony 17.10.2026 z dokumentu i kodu Studio)
Dokument Firestore: `{json: "<JSON jako tekst>", uploadedAt, by}`. Pola JSON:
- `fx`: `[id, kolejka, data UTC "YYYY-MM-DDTHH:MM", gosp_id, gość_id, gole_g, gole_go, ht_g, ht_go, status]`
- `teams`: `[id, pełna nazwa, skrót]`
- `tstats` (na drużynę w meczu): `[fid, team, posiadanie %, strzały, celne, rożne, faule, żółte, czerwone, obrony bramkarza, podania, % celnych podań (round(accurate/total*100)), xG]`
- `goals`: `[fid, minuta (elapsed, bez doliczonego), team (beneficjent, jak w API), strzelec, asystent, typ N/P/O]` (Missed Penalty pomijany)
- `players` (28 kolumn, sumy sezonu): `[pid, nazwa, team, poz G/D/M/F, apps, starts, minuty, ocena śr., gole, asysty, strzały, celne, kluczowe podania, żółte, czerwone, podania, spalone, odbiory, bloki, przechwyty, pojedynki, wygrane pojedynki, dryblingi próby, dryblingi udane, faule wymuszone, faule popełnione, obrony, stracone]`
- `upcoming`: `[kolejka, data UTC, gospodarz (pełna nazwa), gość]`; `meta`: `{generatedAt, lastRound, season}`

Źródło delty: `api_fixtures_raw.raw` (`players`, `statistics`, `events`, `lineups`). `goals.conceded` u bramkarzy bywa null: wtedy gole rywala (bramkarz grał 90').
Ocena „0” (1–3 minuty gry) nie wchodzi do średniej.
Zapis: konto serwisowe `FIREBASE_SERVICE_ACCOUNT` (Firestore REST, `PATCH documents/data/stats`).

## Odświeżenie częściowe po K11 (17.10.2026, 05:27 UTC, Claude Code)
- Delta 4 meczów: Widzew 0:0 Wisła Kr. (K11), Wieczysta 1:2 Raków (K11) oraz zaległe po 12.10: Radomiak 2:3 Motor (K10), GKS 2:1 Wieczysta (K3, wcześniej NS).
- fx 89→92 (90 FT, 2 NS z K4), tstats 172→180, goals 257→268, players 426→429 (nowi: Steve Kingue, Ioan Vermeșan, N. Zätterström), upcoming 19→16, meta lastRound=11 (decyzja Bartka mimo 2/9 meczów K11), generatedAt 2026-10-17.
- Weryfikacja: Widzew 11 meczów, 1W-7R-3P, 10 pkt, dom 0-4-2 (zgodne z tablicą); suma id zawodników 79838393.
- Kopia stanu po K10: Firestore `data/stats_backup_k10`. Skrypty: `studio/delta/`.
- Do zrobienia: druga delta po pozostałych 7 meczach K11 (17–19.10).
