# Integracje — Rozmowy Tylko Sportowe

Techniczne wpisy integracji projektu. Nie jest to plik treści — tylko konfiguracja połączeń. **Adresy webhooków NIE są w repo.** Leżą w zmiennych środowiska (patrz `../ZMIENNE.md`): `DISCORD_WEBHOOK_GOTOWIEC`, `DISCORD_WEBHOOK_KLIPY`, `DISCORD_WEBHOOK_ANALIZATOR`. Stare adresy z projektu claude.ai trzeba unieważnić i wygenerować nowe (były zapisane otwartym tekstem).

## Mapa webhooków Discorda (stan 14.10.2026)
| Webhook | Zmienna | Kanał | Co tam wysyłam |
| --- | --- | --- | --- |
| „RTS Gotowiec" | DISCORD_WEBHOOK_GOTOWIEC | kanał Patryka (`1549891505613705347`, serwer `1549270230340210748`) | gotowe paczki postów 1–4 do publikacji |
| „RTS Klipy" | DISCORD_WEBHOOK_KLIPY | #fragmenty-do-wycięcia (`1549891704474181652`) | **rekomendacje klipów do wycięcia** (do głosowania ekipy), na końcu ankieta z `@everyone` |
| „Analizator odcinka" | DISCORD_WEBHOOK_ANALIZATOR | kanał `1549270231162167370` | **wszystko inne z procedury po odcinku**: m.in. tytuł i opis z rozdziałami do ręcznej zmiany, gdy zmiana na YouTube się nie uda, komunikaty o błędach |

## Discord — webhook na gotowce (kanał Patryka)
**Status: DZIAŁA (potwierdzone testem 10.10.2026, użyte 11.10, 13.10, 16.10).**
- **Cel:** automatyczna wysyłka gotowych pakietów treści (zapowiedzi, karty RTS Stats, posty pomeczowe itd.) na kanał Patryka, gdy w danym oknie odcinka nie zostają żadne placeholdery do uzupełnienia (gość, wynik, link, bio).
- **Wymóg sieciowy:** `discord.com` musi być na liście dozwolonych domen środowiska. `cdn.discordapp.com` (linki do załączników) bywa blokowany — obrazki od Bartka muszą przyjść jako załącznik w czacie.
- **Jak wysyłam:** POST `multipart/form-data` na URL ze zmiennej: pole `payload_json` = `{"content": "<tekst>", "username": "RTS · paczki dla Patryka", "allowed_mentions": {"parse": []}}` oraz `files[0]=@plik.png` (karta 4:5). **W curl używać `--form-string payload_json=...`** (cudzysłowy w treści psuły `-F`; nagłówek dostał 400). Discord limituje wiadomość do 2000 znaków — **jeden post = jedna wiadomość**: nagłówek (nazwa posta), godzina publikacji, tekst w bloku kodu (łatwe kopiowanie), karta jako załącznik. Każda paczka zaczyna się wiadomością-nagłówkiem (faza, mecz, link live) i nagłówek wysyłamy PRZED postami.
- **Twarde zasady paczek (`zasady-paczek.md`):** (1) każdy post odsyłający do podcastu ma w treści link do audycji na YouTube; (2) post z elementem z RTS Stats Studio wysyłamy razem z kartą 4:5, także w korektach. Przed wysyłką sprawdzam: czy każdy post z kartą ma załącznik (HTTP 200 przy pliku, 204 bez pliku) i czy każdy post o live/odcinku ma link.
- **Zasada automatycznej wysyłki (10.10.2026):** gdy w oknie odcinka wszystkie placeholdery zostają uzupełnione, wysyłam kompletny gotowiec bez dodatkowego pytania o zgodę. Bartek niczego nie wkleja; paczki 3 i 4 po komendzie Bartka („faza 3 + wynik", „faza 4").
- **Poza obiegiem Patryka:** posty o ClubFantasy (`wpisy-clubfantasy.md`) nie idą na ten webhook (decyzja Bartka 12.10).

## Discord — webhook „RTS Klipy" (#fragmenty-do-wycięcia)
**Status: DZIAŁA (utworzony i użyty 14.10.2026).**
- **Cel (decyzja Bartka 14.10):** fragmenty (klipy) do wycięcia z odcinków ustalamy z ekipą na tym kanale. Propozycje klipów, głosowania i dyskusje idą tutaj, **nie** na kanał Patryka.
- **Jak wysyłam:** jak wyżej, z `?wait=true` w adresie, żeby odpowiedź zwracała numer wiadomości (`id`), i **zapisywać wszystkie numery** (w pętli!) w logu: `DELETE <webhook>/messages/<id>`. Nazwa nadawcy: „RTS · klipy #NNN (do głosowania)".
- **Ankieta i @everyone (decyzja Bartka 14.10):** po rekomendacjach wysyłam JSON-em wiadomość z polem `poll` (`question.text`, do 10 `answers[].poll_media.text` po max 55 znaków, `allow_multiselect: true`, `duration` 24 h) i `allowed_mentions: {"parse": ["everyone"]}` oraz `@everyone` w treści. Sprawdzone 14.10 (HTTP 200).
- **Zaproszenie na serwer:** https://discord.gg/dgqvpPXpK (Claude nie czyta Discorda; webhook tylko pisze).

## Discord — webhook „Analizator odcinka"
**Status: DZIAŁA (przekazany 14.10.2026; sprawdzone tylko metadane).**
- **Cel (decyzja Bartka 14.10):** wszystko z `procedura-po-odcinku.md` poza rekomendacjami klipów. Nazwa nadawcy „RTS · analizator #NNN", z `?wait=true`.

## Log
- **10.10.2026:** webhook otrzymany od Bartka. Test z kontenera zablokowany (403, `discord.com` nie na liście), po dodaniu domeny — sukces (HTTP 204).
- **10.10.2026:** wysłane paczki 1 i 2 dla #376 (7 wiadomości z postami + 3 karty 4:5 + 3 nagłówki; HTTP 200/204). Pierwsza korekta poszła bez kart — błąd; wysłana wersja ostateczna z kartami; post 2b ponownie z linkiem do live.
- **11.10.2026 (~16:55):** paczka 3 dla #376 (Piast 2:1 Widzew): nagłówek (204) + 3a z kartą „Mecz" (200) + 3b z kartą „Końcówki" (200) + 3c L−1h (204) + 3d start live (204).
- **13.10.2026:** paczka 1 przed Wisłą Kraków (K11): nagłówek (204) + 1a (200) + 1b (200) + 1c (200) + 1d (200). Teksty: `wpisy-wisla-faza1.md`.
- **14.10.2026 (pomyłka kanału):** propozycje klipów #376 poszły przez webhook kanału Patryka (zły kanał; numerów nie zapisano, Bartek kasuje ręcznie). Utworzony webhook „RTS Klipy"; te same propozycje wysłane na właściwy kanał (4 wiadomości, HTTP 200). Ankieta klipów #376 z @everyone (10 klipów, 24 h, HTTP 200).
- **14.10.2026:** Bartek przekazał webhook „Analizator odcinka".
- **16.10.2026:** zapowiedź live #377 + faza 2 Wisły (4 posty; nagłówek po postach przez błąd 400) oraz faza 3 #377 po 0:0 (nagłówek + 4 posty, HTTP 200). Szczegóły: `wpisy-377-zapowiedz-faza2.md`, `wpisy-377-faza3.md`.
- **17.10.2026:** przeniesienie projektu do Claude Code; webhooki wyjęte z dokumentów, trafiają do zmiennych środowiska.
