# Procedura po odcinku: transkrypcja, klipy, opis z rozdziałami, YouTube

Ustalone z Bartkiem 14.10.2026. Obowiązuje po każdym nagranym odcinku (pomeczówki i Extra). Wykonuje ją Claude w czacie, kiedy Bartek poda komendę.

## Zasada nadrzędna: informacje podajemy w czacie
**Bartek nie otwiera plików .md w projekcie (decyzja 14.10).** Wszystko, co mu przekazujemy (tytuł, opis z rozdziałami, lista klipów, wnioski, decyzje do podjęcia), Claude podaje **bezpośrednio w odpowiedzi w czacie**, gotowe do skopiowania (karta kopiowania). Pliki w repo nadal aktualizujemy, ale tylko jako pamięć dla innych sesji. Nigdy nie odsyłamy Bartka do pliku zamiast podać treść.

## Dwie różne rzeczy: ROZDZIAŁY w opisie vs KLIPY do wycięcia (decyzja Bartka 14.10)
Nie mieszać ich ani w tekstach, ani w rozmowie.

| | **Rozdziały w opisie odcinka na YouTube** | **Klipy (fragmenty) do wycięcia w DaVinci** |
| --- | --- | --- |
| Po co | nawigacja widza po całym odcinku (oś czasu YT) | krótkie materiały na X, FB, IG Reels, YT Shorts |
| Ile | **maks. 10** (5–10) | tyle, ile jest mocnych fragmentów (zwykle 10–12 do głosowania, 4 do cięcia) |
| Długość | cały odcinek podzielony na tematy, każdy min. 10 s | **zwykle 30 s do 2 min** (dłuższe tylko wyjątkowo; krótsze niż 30 s słabo działają) |
| Wybór | tematy w kolejności chronologicznej | **najmocniejsze i najlepsze wypowiedzi**, nie chronologicznie |
| Gdzie trafia | opis YT (karta kopiowania w czacie, zmiana przez `/NNN_zmien`) | Discord #fragmenty-do-wycięcia (ankieta), a po wyborze `/NNN_fragmenty` (tabela + plik EDL) |

Przy wyborze klipów Claude pilnuje długości 30 s – 2 min; jeśli fragment wychodzi dłuższy, skraca okno albo dzieli.

## Gdzie co trafia (webhooki w `integracje.md`)
- **Rekomendacje klipów** → Discord **#fragmenty-do-wycięcia** (webhook „RTS Klipy"), zakończone **ankietą i `@everyone`** (patrz krok 2).
- **Wszystko inne z procedury** (tytuł i opis do ręcznej zmiany po błędzie na YouTube, komunikaty o błędach, wyniki analizy) → webhook **„Analizator odcinka"**.
- Gotowe posty dla Patryka → webhook „RTS Gotowiec", dopiero po wyborze klipów przez ekipę.
- **Tytuł i opis z rozdziałami zawsze także w czacie** (karta kopiowania), niezależnie od wysyłki na Discord.

## Komendy (ustalone 14.10)
- **`/NNN`** (np. `/377`): kroki 1–3 (transkrypcja, klipy z ankietą, tytuł i opis w czacie). **Bez** zmiany na YouTube.
- **`/NNN_zmien`** (np. `/377_zmien`): kroki 1–4, czyli to samo plus **samodzielna zmiana tytułu i opisu na YouTube**. Ta komenda jest jednoznaczną zgodą Bartka na zmianę publicznej treści, więc Claude nie pyta o nią jeszcze raz.
- **`/NNN_fragmenty`** (np. `/376_fragmenty`): Claude podaje **w czacie tabelę z podsumowaniem fragmentów do wycięcia** i dołącza **plik EDL ze znacznikami** do DaVinci (SendUserFile). Szczegóły niżej.
- Nic nie obserwuje w tle, więc samo wrzucenie nagrania na YouTube niczego nie uruchamia.
- Odcinek musi być już na YouTube (napisy automatyczne powstają po publikacji, zwykle po kilkunastu minutach). Claude nie transkrybuje samego pliku audio.
- Przed pracą: sprawdź `rejestr-odcinkow.md` (numer, tytuł, gość, prowadzący, link do live).

### `/NNN_fragmenty`: co dokładnie
- **Które klipy:** te, które Bartek poda w tej samej wiadomości (np. `/376_fragmenty 1,2,4,7`, numery z listy). Gdy nie poda numerów, Claude bierze klipy z `klipy-NNN.md` oznaczone jako wybrane; jeśli takich nie ma, pyta, które (Claude nie widzi wyniku ankiety na Discordzie).
- **Tabela w czacie:** # klipu, okno (wejście – wyjście), długość, temat, fraza wejścia i wyjścia, gdzie publikujemy (X, FB, IG Reels, YT Shorts), uwagi (wypikać słowa, karta RTS Stats). Klipy 30 s – 2 min; za długie Claude skraca i zaznacza zmianę.
- **Plik EDL:** znaczniki w formacie Resolve (`|C:ResolveColorBlue |M:Klip N nazwa |D:długość w klatkach`), po jednym na klip, chronologicznie. Wymaga fps i początkowego TC timeline'u. **Domyślnie 25 fps i start 01:00:00:00**, dopóki Bartek nie poda swoich wartości (wtedy zapisać je tutaj). Nazwy znaczników bez polskich znaków.
- Instrukcja importu: File → Import → Timeline → Markers from EDL; potem `I`/`O` na znaczniku i File → Quick Export.
- Po wysłaniu zaktualizować `klipy-NNN.md` (status: wybrane) i `tablica.md`.

## Kroki
1. **Transkrypcja z napisów automatycznych YouTube** (decyzja Bartka 14.10; środowisko Claude nie ma silnika rozpoznawania mowy, a modele są zablokowane). Czyta je Claude w przeglądarce Chrome (rozszerzenie Claude) z panelu „Pokaż transkrypcję" albo Bartek wkleja plik. Zapis: `docs/transkrypcja-NNN.md`. Uwaga: czasy ±20 s, nazwiska bywają przekręcone.
2. **Rekomendacje klipów na Discord #fragmenty-do-wycięcia** (webhook „RTS Klipy", z `?wait=true`, **numery wszystkich wiadomości zapisać w logu**). Klipy **30 s – 2 min**, wybrane jako najmocniejsze wypowiedzi (patrz tabela wyżej). Format: nagłówek z linkiem do odcinka i prośbą o reakcje 🔥 👍 👎, potem klipy od najmocniejszych (okno czasowe, długość, cytat, o czym, uwagi), typ Claude na 4 klipy i lista fragmentów, których nie wycinać. Maks. 2000 znaków na wiadomość. Zapis tabeli: `docs/klipy-NNN.md`. **Nie** na kanał Patryka. Lista klipów trafia też do Bartka w czacie.
   **Zakończenie (decyzja Bartka 14.10): ostatnia wiadomość to ankieta z `@everyone`**, żeby ekipa dostała powiadomienie i szybko odpowiedziała. Ankieta: pole `poll` w JSON-ie webhooka (`question.text`, `answers[].poll_media.text` do 55 znaków, maks. 10 odpowiedzi, `allow_multiselect: true`, `duration` w godzinach, domyślnie 24), a w `allowed_mentions` `{"parse": ["everyone"]}`. Gdy klipów jest więcej niż 10, odpadają najsłabsze lub dyskusyjne (wyjaśnić w opisie). Sprawdzone 14.10: webhook przyjmuje ankietę (HTTP 200). Po wyborze ekipy Bartek wydaje `/NNN_fragmenty`.
3. **Tytuł i opis odcinka z rozdziałami.** **Maks. 5–10 rozdziałów** (decyzja Bartka 14.10: więcej jest nieużyteczne dla człowieka). Zasady YouTube: pierwszy znacznik `0:00`, min. 3, każdy rozdział min. 10 s, każdy w osobnej linii, format `m:ss` lub `h:mm:ss`, zwykłe spacje (bez twardych). Tytuł wg wzoru `#NNN Drużyna1 - Drużyna2 wynik | hook` (wynik zawsze po nazwach drużyn). W opisie link do ClubFantasy (pokój, jeśli aktualny) i sygnatura. Bez niezweryfikowanych zarzutów ani tez z czatu. **Podajemy w czacie jako kartę kopiowania**; zapis także w `rejestr-odcinkow.md`.
4. **Samodzielna zmiana tytułu i opisu na YouTube przez Claude** (tylko po `/NNN_zmien`). Rozszerzenie Claude w Chrome jest podłączone (sprawdzone 14.10: przeglądarka Windows, YouTube Studio zalogowane na koncie kanału; tytuł #376 zmieniony tą drogą). Wymaga: włączony Chrome z rozszerzeniem i zalogowane YouTube Studio. Claude nie wpisuje haseł. Ścieżka: `https://studio.youtube.com/video/<ID>/edit`, pole tytułu i opisu, przycisk „Zapisz" (komunikat „Zapisano zmiany"). **Poczekać na załadowanie strony przed wpisywaniem** (14.10 pierwsze wpisanie zdarzyło się za wcześnie i przepadło; Studio bywa wolne i pokazuje stare wartości). Po zapisaniu sprawdzić publiczną stronę (pasek postępu z podziałami, nazwa rozdziału w odtwarzaczu) i zamknąć kartę. Po wykonaniu krótko potwierdzić Bartkowi, co zmieniono. **Przy każdym błędzie** (brak przeglądarki, brak logowania, brak zgody) wyślij tytuł i opis w bloku kodu na webhook **„Analizator odcinka"**, a Bartek zmienia ręcznie.
   Uwaga: system może mimo komendy poprosić o zgodę na działanie w Chrome (zabezpieczenia poza kontrolą Claude); wtedy krótko zapytać Bartka albo wysłać wersję awaryjną na Discord.

## Zasady
- Posty o klipach dla Patryka dopiero po wyborze ekipy, z linkiem do odcinka (`zasady-paczek.md`).
- Każdą wysyłkę wpisz do `integracje.md`, a stan do `tablica.md`.
- Pierwsze użycie `/NNN_zmien` na realnym nowym odcinku traktuj jako test i opisz wynik Bartkowi.
