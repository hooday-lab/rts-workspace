# Obieg komunikacji odcinka — playbook RTS

> **STATUS: OBOWIĄZUJE od 27.09.2026 do odwołania. Od 10.10.2026 model 4 FAZ (zastępuje model 3 posiedzeń) i KARTY GOTOWE W PACZKACH (zastępuje „Patryk robi plansze sam"). Paczki na Discord wysyła Claude (webhook), nie Bartek.** Wszystkie sesje przygotowują materiały zgodnie z tym obiegiem.

Playbook komunikacji wokół odcinka: co, kiedy i gdzie publikować — w formie checklisty do odhaczania.

**Wykonanie:** Patryk (publikacja i planowanie postów) · Bartek (dane i decyzje) · Claude (teksty, karty, wysyłka paczek).
**Powiązane dokumenty:** `rejestr-odcinkow.md` (numer, tytuł, opis, gość, termin, link) · `wpisy.md` (pełne treści wpisów) · `statystyki.md` (format RTS Stats + baza liczb) · `plan-okno-piast-wisla-gornik.md` (plan bieżącego okna) · `integracje.md` (wysyłka na Discord) · `przypomnienia.md` (przypomnienia).
**Placeholdery w szkicach roboczych:** `[nr]`, `[gość]`, `[dzień]`, `[godz.]`. **Patryk nie dostaje żadnych placeholderów** — każda paczka jest gotowa do publikacji.

---

## Model pracy: 4 FAZY (ustalone 10.10.2026, Bartek)

Patryk dostaje na Discordzie **cztery osobne paczki**, nie jedną. Każda paczka jest **w całości gotowa do publikacji** (zero [WYNIK], [LINK], [GODZ.], [GOŚĆ]) i **uwzględnia całą wiedzę, którą mamy w danej fazie**. Terminy publikacji **liczymy od daty i godziny meczu** (D = dzień meczu, M = gwizdek, L = start live), nie od dni tygodnia — mecze są w różne dni, więc kalendarz zawsze wyliczamy na nowo.

**Karty w paczkach (decyzja Bartka 10.10, późniejsza):** do każdej paczki dołączone są **gotowe karty RTS Stats w formacie 4:5 (1080×1350 PNG)**, wygenerowane tym samym kodem co RTS Stats Studio (te same typy kart, to samo tło RTS) na aktualnych danych z bazy. Karta jest **dobrana do kontekstu posta i do sytuacji sportowej Widzewa** (kto gra, jaka forma, jaki rywal, co jest najbardziej interesujące w danym momencie) — nie z góry ustalonej listy. Każdy post w paczce ma przypisaną swoją kartę (nazwa pliku = faza + numer posta). Patryk nie robi kart sam; Studio zostaje narzędziem ekipy i awaryjnym (np. korekta karty). **Każda wysyłka, także korekta tekstu, zawiera te same karty co oryginał.**

**Link do live znamy przed fazą 1** (live jest tworzony na YouTube od razu, gdy ustalimy termin). Link jest więc w każdej paczce, w formie `youtu.be/...` bez końcówki `?feature=share` / `?is=...`.

| Faza | Kiedy Patryk dostaje paczkę | Co wiemy | Co zawiera paczka |
| --- | --- | --- | --- |
| **1. Przed meczem** | gdy znamy mecz (zwykle zaraz po poprzednim meczu), najpóźniej D−5 | przeciwnik, data i godzina meczu, gość, godzina live, link live; **nie** wiemy wyniku ani składów | cały zestaw postów do wyjścia przed dniem meczu i rano w dniu meczu **z gotowymi kartami 4:5**: zapowiedź live z gościem + collab IG, karty RTS Stats dobrane do kontekstu (np. „Liczba przed rywalem" D−1, karta kontekstowa rano D), pytanie „o co zapytać gościa?". Każdy post z konkretną datą i godziną publikacji |
| **2. Bliska przedmeczowa** | ok. M−3h (publikacje od M−2h) | stan na dzień meczu: wiadomości drużynowe; skład tylko jeśli Bartek poda (ok. M−1h) | „dziś gramy" + przypomnienie o live wieczorem (M−2h), pytanie do kibiców, opcjonalnie post ze składem (M−1h); karta dobrana do sytuacji (np. forma rywala, bilans wyjazdowy) |
| **3. Pomeczowa** | zaraz po gwizdku — Bartek podaje wynik, strzelców, 1–2 zdania o meczu | wynik, przebieg | post po meczu (reakcja + zaproszenie) **z kartą „Mecz"** (dane odświeżone po meczu), tytuł YT z wynikiem, opis YT, posty L−1h i L (start), stories z odliczaniem; licznik po meczu domowym; live dzień później → też poranne przypomnienie |
| **4. Po podcaście** | do godziny po live | odcinek nagrany; Bartek podaje temat/cytat klipów | podziękowanie + link do nagrania, opisy 2–3 klipów (X, FB, Reels, Shorts), pytanie do kibiców po live, **pierwszy post zapowiadający następny mecz z kartą** (przejście do fazy 1 kolejnego okna) |

Faza 4 jednego meczu przechodzi w fazę 1 następnego. Wariant „live tego samego wieczoru co mecz" (np. #376): faza 3 obejmuje posty od razu po meczu aż do startu live (zaplanowane po meczu), poranne przypomnienie odpada.

**Kto uruchamia fazę:** Bartek pisze w czacie „faza 2" / „faza 3 + wynik" / „faza 4" (i podaje brakujące dane). Faza 1 przygotowywana jest z wyprzedzeniem — po ustaleniu terminu meczu, gościa i godziny live. **Po każdej kolejce dane do kart odświeża Claude z bazy ClubFantasy (SELECT) przed przygotowaniem fazy 3 i kolejnej fazy 1.**

**Podział ról (10.10.2026, korekta)**

| Kto | Odpowiada za |
| --- | --- |
| **Patryk** | Publikacja i planowanie postów (X, Facebook, Instagram), stories, obsługa 4 faz. **Dostaje na Discordzie 4 osobne paczki: teksty + gotowe karty 4:5.** Nie generuje kart sam (Studio awaryjnie) |
| **Bartek** | Uruchamia fazy 2–4 danymi (wynik, skład, temat klipów), klipy, tytuły i opisy na YouTube, rejestr odcinków, decyzje redakcyjne; administrator RTS Stats Studio. **Niczego nie wkleja Patrykowi** |
| **Claude** | Teksty i karty 4:5 do każdej paczki, **wysyłka paczek na Discord przez webhook** (`integracje.md`), aktualizacja dokumentów, przypomnienia (`przypomnienia.md`) |
| **Prowadzący** | W trakcie live: wyświetlanie komentarzy z czatu StreamYard na ekranie |

Zasada przekazania: Claude przygotowuje paczkę (po jednej wiadomości na post: godzina publikacji, tekst w bloku do skopiowania, karta 4:5 w załączniku) i sam wysyła ją na Discord. Zmiany w tekstach po drodze Patryk zgłasza Bartkowi.

**Cele na najbliższe 2–3 miesiące:** więcej widzów na live, więcej subskrypcji YouTube, mocniejsza marka i zasięg na X.

**Rola kanałów**
- **YouTube** — dom podcastu: nagrania, Shorts. Każdy link prowadzi tu.
- **X + Facebook** — główna komunikacja, posty równolegle. Transmisja live równolegle (StreamYard).
- **Instagram** — to samo co Facebook, plus: post collab z gościem (faza 1), stories z odliczaniem w dniu live, karuzele z kartami, Reels.
- **TikTok** — poza obiegiem (decyzja 2026-09-27).

**Transmisja i czat (StreamYard)**
- Live leci równolegle na **YouTube, X i Facebook** przez StreamYard.
- Czat jest **jeden** — StreamYard łączy komentarze z trzech platform.
- **Prowadzący sam** wyświetla komentarze na ekranie (z imieniem kibica i platformą) — w naturalnych przerwach.
- Każdy post zaplanowany na dzień live zawiera zdanie o pytaniu do gościa na czacie (np. „Masz pytanie do gościa? Napisz na czacie na YouTube, X albo Facebooku, przeczytamy na antenie.").
- Pomysły odłożone: stały blok „Pytania od kibiców" o ustalonej porze, post „Najlepszy komentarz z czatu" po live, liczby widzów per platforma w rejestrze.

**Warianty**
- **Live tego samego wieczoru co mecz:** faza 3 obejmuje wszystkie posty do startu live.
- **Live następnego dnia lub później:** faza 3 zawiera też poranne przypomnienie (lista „czego się spodziewać") w dniu live.
- **Odcinek Extra (bez meczu):** zostają fazy 1 (zapowiedź, collab IG, przypomnienia zaplanowane z góry) i 4. Tytuł kończy się na „| EXTRA".

---

## Checklista odcinka #[nr] — [gość], [dzień] [godz.]

### FAZA 1 — Przed meczem
- [ ] Odcinek wpisany do `rejestr-odcinkow.md`: numer, tytuł roboczy, gość, termin, **link live**
- [ ] YouTube: live zaplanowany, tytuł roboczy (+ wersja krótka „do okna"), opis (z hasztagami X: 2–3)
- [ ] Link w formie `youtu.be/...`
- [ ] Zapowiedź główna z gościem (kto, kiedy, jeden powód, pytanie „o co zapytać gościa?") — X + Facebook + Instagram
- [ ] Instagram: post collab z gościem
- [ ] Karty RTS Stats 4:5 wg kalendarza liczonego od D, dobrane do kontekstu, dane z bazy aktualne po ostatniej kolejce (PNG w paczce)
- [ ] Wszystkie posty zaplanowane z konkretnymi datami i godzinami

### FAZA 2 — Bliska przedmeczowa (M−3h … M)
- [ ] Post „dziś gramy" + przypomnienie o live (M−2h) + karta
- [ ] (jeśli Bartek poda skład) post ze składem (M−1h)
- [ ] Uwaga: od 16.10 bez próśb o typowanie i zgadywanie (`zasady-paczek.md` pkt 5)

### FAZA 3 — Pomeczowa
- [ ] Post po meczu: reakcja na wynik (fakt → reakcja → pytanie) + zaproszenie na live z godziną i linkiem + karta „Mecz" — X + Facebook + Instagram
- [ ] YouTube: tytuł live z wynikiem (`#[nr] [Drużyna1] - [Drużyna2] [wynik] | [hook]`), opis pomeczowy
- [ ] `rejestr-odcinkow.md`: tytuł, opis, godzina live
- [ ] Karta „Licznik" (jeśli aktywny; po meczu domowym)
- [ ] Zaplanowane: L−1h, L (start), stories z odliczaniem; (live dzień później: poranne przypomnienie)

### DZIEŃ LIVE — nic ręcznie
- [ ] Posty wychodzą z planu (kontrola: czy wyszły)
- [ ] StreamYard: live równolegle na YouTube, X i Facebook
- [ ] Prowadzący wyświetla komentarze z czatu w naturalnych przerwach

### FAZA 4 — Po podcaście
- [ ] Podziękowanie + link do nagrania (X + Facebook + Instagram)
- [ ] 1 klip jakościowy (montaż ręczny) — X, Facebook, Instagram Reels, YouTube Shorts
- [ ] 2 klipy szybkie (automat) — kolejne 1–3 dni, te same platformy; każdy klip odsyła do pełnego odcinka
- [ ] Pytanie do kibiców po live
- [ ] Pierwszy post zapowiadający następny mecz + karta (start fazy 1 kolejnego okna)
- [ ] `rejestr-odcinkow.md`: status → „opublikowany" + link + post promocyjny; `wpisy.md`: statusy
- [ ] Upewnić się, że przypomnienia na następny mecz są ustawione (`przypomnienia.md`)

---

## Ściągawka czasowa (D = dzień meczu, M = gwizdek, L = start live)

| Kiedy | Faza | Co |
| --- | --- | --- |
| D−5 … D−4 | 1 (paczka u Patryka) | cały zestaw z kartami na okno przed meczem, zaplanowany |
| D−3 / D−2 | 1 | zapowiedź live z gościem + collab IG |
| D−1 (ok. 12:00) | 1 | „Liczba przed rywalem" (RTS Stats) |
| D rano | 1 | karta kontekstowa RTS Stats (np. „Dom na opak") |
| M−2h | 2 | „dziś gramy" + przypomnienie o live + karta |
| M−1h | 2 | skład (gdy Bartek poda) |
| po M | 3 | post po meczu + zaproszenie + karta „Mecz", tytuł z wynikiem |
| L−1h, L | 3 (zaplanowane po meczu) | „za godzinę wchodzimy", „jesteśmy na żywo" |
| do 1h po L | 4 | podziękowanie + nagranie, klipy, pytanie, zapowiedź następnego meczu |

Gdy odstęp między ostatnim meczem a następnym jest krótki (np. piątek po niedzieli), karty układamy w dostępnych slotach i pomijamy te, których nie da się zrobić na świeżych danych.

---

## Okno meczowe — karty RTS Stats w paczkach (dot. odcinków pomeczowych)

W oknie meczowym karta **RTS Stats** jest stałym elementem każdej paczki — niezależnie od promocji samego odcinka. Hasztag **#RTSstat**. Karty przygotowuje Claude i dołącza do paczek jako gotowe PNG 4:5 (1080×1350), generowane kodem Studio (https://hooday-lab.github.io/rtsstat/) na danych z bazy ClubFantasy (SELECT); dobór typu karty zależy od kontekstu sportowego i od posta. Typy: Liczba przed rywalem, Mecz, Zawodnik, Porównanie, Dom i wyjazd, Własna liczba (+ Porównanie klubów, Mapa ligi, Własna liczba/fakt). Studio zostaje narzędziem ekipy i awaryjnym.

- [ ] **Faza 1 — „Liczba przed rywalem"** (D−1): jedno porównanie Widzew vs rywal (bez pytania o typ)
- [ ] **Faza 1, rano D — karta kontekstowa** (np. „Dom na opak")
- [ ] **Faza 3 — „Mecz"** i **„Licznik"** (po meczu domowym, jeśli aktywny)
- [ ] Liczby zweryfikowane z bazy; #RTSstat; w podtytule karty tylko twierdzenia sprawdzone na danych

---

## Zasady i standardy (referencja)

**Platformy**
- YouTube = dom podcastu (nagrania, Shorts); live równolegle na YouTube, X i Facebook (StreamYard).
- X + Facebook = główna komunikacja, równolegle.
- Instagram = to samo co Facebook + collab, stories, karuzele, Reels.
- Transmisja wyjątkowo tylko na YouTube → zaznaczyć wyraźnie.

**Styl „ostatniego przypomnienia"**
hook → lista „czego się spodziewać" (2–4 punkty, emoji dopasowane znaczeniowo) → ew. „tylko YouTube" → cel/CTA → linia startu z godziną i skróconym linkiem.

**Linki**
- Zawsze skrót `youtu.be/...` — bez końcówki śledzącej (`?is=...`, `?feature=share`).
- Na Instagramie link nie klika się w opisie → „Link w bio".

**Tytuł odcinka (YouTube)**
- `#[nr] [temat/hook z nazwiskiem gościa] | Rozmowy Tylko Sportowe` (Extra: + „ | EXTRA").
- Pomeczówka: `#[nr] [Drużyna1] - [Drużyna2] [wynik] | [hook]`.
- Numeracja wspólna (pomeczowe + EXTRA w jednym ciągu), inkrementować o 1.
- Warto mieć wersję krótką „do okna".

**Hasztagi**
- X: 2–3 (np. #Widzew #Ekstraklasa). Facebook: 1–2. Instagram: ~10 na końcu lub w pierwszym komentarzu.
- RTS Stats: **#RTSstat** (+ #Widzew i ew. 1 tematyczny).
- Na X/IG tagi z diakrytykami i bez to różne tagi.

**Zasady redakcyjne (głos „my" kibiców)**
- Fakt → reakcja (suchy humor) → pytanie do kibiców (bez próśb o typ/liczbę). Pisać tak, jak pisze kibic, nie jak komunikat prasowy: krótkie zdania, bez patosu, bez zwrotów typu „w tym artykule", „warto zauważyć", „podsumowując", bez długich myślników jako ozdobnika.
- Unikać „dziś/jutro" w postach publikowanych wcześniej — nazywać konkretny dzień (wyjątek: same-day, gdy „dziś" jest jednoznaczne).
- „sparing" w cudzysłowie, gdy odcinek jest metaforycznym „sparingiem".
- Sygnatura „Od kibiców dla kibiców" (+ 🔴⚪🔴) rzadko, przy ważnych momentach — jeden mocny post z sygnaturą w danym oknie.
- Poza Widzewem (np. gość MMA) — rozważyć samą frazę bez serc.
- Liczb nie podajemy, jeśli nie mamy ich w bazie — żadnych „rekord ligi" bez danych. Każde twierdzenie „pierwszy raz / jedyny / najwięcej" sprawdzamy na danych (w tym remisy i drużyny z tym samym wynikiem), zanim trafi do posta.
- **Dwa przejścia przed wysyłką:** (1) fakty i liczby względem bazy, (2) literówki, spójność z tym stylem i brzmienie „jak człowiek".

**Gotowce do skopiowania (WAŻNE)**
- Treść do skopiowania = wyłącznie czysty, gotowy do wklejenia tekst posta. Zero elementów zdradzających AI: żadnych etykiet „Wariant A/B", nagłówków, komentarzy w nawiasach, uwag, podpowiedzi, meta-opisów wewnątrz kopiowanego bloku.
- Każdy post = osobny gotowiec (osobna wiadomość na Discordzie z blokiem kodu do skopiowania). Wskazówki i uwagi Claude umieszcza POZA blokiem do skopiowania.
- Paczki dla Patryka: **jedna faza = jedna paczka** (wiadomość-nagłówek + po jednej wiadomości na post z kartą 4:5), wysyłana przez Claude na Discord.

---

## Do ustalenia
- [ ] Stała godzina live: 19:10 (potwierdzone dla #376 i #377), czy zależnie od odcinka?
- [ ] Czy Facebook dostaje dłuższe wersje postów niż X, czy wystarczą te same?
- [ ] Narzędzie do szybkich klipów z automatu
- [ ] Czy RTS wspomina o żałobie Piastu po Sługockim (decyzja Bartka, #376; domyślnie nie)
