# Render kart 4:5 w sesji Claude — procedura (sprawdzona 11.10.2026)

Uzupełnia `statystyki-studio-strona.md` i skrzynkę Statystyki w `tablica.md`.

1. **Dane z bazy ClubFantasy** (Supabase, projekt `psaplnrfderixnunxshu`, tylko SELECT):
   - `api_fixtures_raw`: `api_fixture_id, round, kickoff, home_id, away_id, goals_home, goals_away, ht_home, ht_away, status, events (jsonb)`; mecz K10 nie był w bazie, wpisany ręcznie.
   - `api_team_stats`: `possession, shots_total, shots_on, corners, fouls, yellow, red, saves, passes_total, pass_pct, xg`.
   - Format Studio: `fx` = [id, kolejka, kickoff UTC „YYYY-MM-DDTHH:MM", home, away, gh, ga, ht_h, ht_a, „FT"]; `goals` = [fid, minuta, id drużyny (beneficjent, także przy samobóju), zawodnik, asystent, „P"/„O"/""]; `tstats` = [fid, team, poss, shots, on, corners, fouls, yellow, red, saves, passes, pass%, xg]; `teams` = [id, pełna nazwa, skrót].
2. **Strona:** `index.html` z repo `hooday-lab/rtsstat`, kopia lokalna. Ładowanie bez Firebase: usunąć tagi `<script src="https://www.gstatic...">`, w Playwright `page.evaluate(()=>{show('studio');return runApp(data,{fs:null,email:'x',isAdmin:false,bg:null,cards:{}})})`.
3. **Playwright** (`NODE_PATH=$(npm root -g)`, `executablePath:'/opt/pw-browsers/chromium'`): klik zakładki typu, „Pionowo 4:5", wypełnienie pól `#f-...`, klik `#dl` i przechwycenie pobrania (PNG 1080×1350).
4. **Obejścia przy minimalnym zestawie danych (tylko w lokalnej kopii, nie w repo):**
   - minuta „90+1": sortowanie goli po `parseInt(x[1])`, a w danych minuta jako tekst „90+1";
   - przy pustych `players`/`tstats` karta „Własna liczba" wywala podpowiedzi (`facts()`), więc w kopii `sugg(){return []}`;
   - mecz bez statystyk w `tstats`: karta „Mecz" pomija słupki (puste dolne pole).
5. **Liczby o końcówkach (SQL na `events`):** gole po `minute>=75` z podziałem na drużynę (team_id = beneficjent), stan z 74' z minut ≤74; punkty = różnica wyniku meczowego względem stanu z 74'.
6. **Pełne odświeżenie `data/stats` w Firestore po K10** zrobione 12.10 (szczegóły: `statystyki-odswiezenie-k10.md`). Po każdej kolejce powtarzać metodą delta.

Uwaga (17.10.2026): po zmianie nazwy na RTS Stats Studio nagłówek karty brzmi „RTS Stats · …", pobrany plik `RTS-Stats-….png`.
