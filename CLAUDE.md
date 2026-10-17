# RTS — Rozmowy Tylko Sportowe (podcast kibiców Widzewa Łódź, "od kibiców dla kibiców")

Repo prywatne. Źródło prawdy projektu. Czytaj na początku KAŻDEJ sesji: `docs/tablica.md`, `docs/zasady-paczek.md`, `docs/rejestr-odcinkow.md`.

## Kim pracujesz
- Właściciel: Bartek (PL). Komunikacja po polsku. Daj opcje do wyboru, numeruj odpowiedzi, kończ sekcją "TWOJE KROKI" (albo napisz, że nic nie musi robić).
- Testy opisuj: Krok #1, Krok #2 z rolą [Admin] / [Gracz] / [Gracz Rzeczywisty].
- Po ostatniej odpowiedzi na pytania zapytaj: "czy chcesz coś dodać?", dopiero potem działaj.
- Konta: X https://x.com/rozmowysportowe, YouTube @RozmowyTylkoSportowe, FB. Głównie X + FB, dom podcastu = YouTube.
- Patryk publikuje posty. Dostaje gotowe paczki (bez placeholderów) na Discordzie. Bartek niczego mu nie wkleja.

## Marka
- Pełna nazwa narzędzia: **RTS Stats Studio** (skrót RSS). Seria na kartach: "RTS Stats". Hasztag: #RTSstat.
- Studio: repo `hooday-lab/rtsstat` (publiczne, GitHub Pages), Firebase `rtsstat-55616`. Kod = `index.html`.

## Zasady (szczegóły w docs/)
- `zasady-paczek.md`: link youtu.be w każdym poście odsyłającym do podcastu; post ze Studio = karta 4:5; dwa przejścia (fakty, styl); log po wysyłce; BEZ próśb o typowanie/zgadywanie.
- `obieg-komunikacji.md`: model 4 faz (przed meczem / M−3h / po meczu / po podcaście).
- `procedura-po-odcinku.md`: komendy /NNN, /NNN_zmien, /NNN_fragmenty.
- `editorial-voice`: głos "my", fakt → reakcja → pytanie, pisane jak człowiek.
- Nie komunikujemy newsów (nie jesteśmy kontem newsowym). Liczby tylko z bazy.

## Sekrety (NIGDY w repo, tylko zmienne środowiska)
DISCORD_WEBHOOK_GOTOWIEC, DISCORD_WEBHOOK_KLIPY, DISCORD_WEBHOOK_ANALIZATOR, SUPABASE_URL, SUPABASE_ANON_KEY (SELECT), FIREBASE_SERVICE_ACCOUNT (zapis do data/stats).
Domeny do odblokowania w środowisku: discord.com, *.supabase.co, firestore.googleapis.com, github.com.

## Zadania zaplanowane
Sprawdzenie danych 30 min po meczu Widzewa (ponawiaj co godzinę do skutku) → odśwież Firestore `data/stats` (metoda delta, `docs/statystyki-odswiezenie-k10.md`).

## Co jest w repo, a co jeszcze w projekcie claude.ai
- `docs/`: tablica, zasady-paczek, obieg-komunikacji, procedura-po-odcinku, rejestr-odcinkow (skrócony), integracje (bez webhooków), przypomnienia, statystyki-render-kart.
- `studio/`: kod generatora kart (Python/Playwright), szablon i skrypty strony.
- Jeszcze w projekcie claude.ai (dokopiować w miarę potrzeby, odczyt przez narzędzie Projects): `wpisy*.md`, `statystyki*.md`, `transkrypcja-376.md`, `klipy-376.md`, `statystyki-odswiezenie-k10.md`, `sklady-i-absencje.md`, `plan-okno-piast-wisla-gornik.md`, `brand-rtsstat.md`.
