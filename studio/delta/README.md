# Delta `data/stats` (Firestore)
1. `python3 -I fs.py <katalog>/stats_k10.json` — odczyt bieżącego dokumentu (nazwa pliku wejściowego stała w `delta.py`).
2. Z Supabase (`api_fixtures_raw`, MCP, tylko SELECT) zapisać `<katalog>/k11_raw.json` z kluczami `fx`, `st`, `ev`, `pl` (zapytanie w historii sesji 17.10; układ: `docs/statystyki-odswiezenie-k10.md`).
3. `python3 -I delta.py <katalog> <lastRound>` → `<katalog>/stats_k11.json` + podsumowanie liczności.
4. `python3 -I write.py <katalog>` — kopia poprzedniego stanu do `data/stats_backup_k10`, zapis `data/stats`. Wymaga `FIREBASE_SERVICE_ACCOUNT`.
Przy następnej kolejce zmienić nazwy plików/backupu w skryptach.
