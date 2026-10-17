/**
 * RTSstat v2 — pobieranie danych Ekstraklasy z API-Football do Google Drive.
 * Układ folderów: RTSstat-data/<sezon>/ standings.json, fixtures.json, teams.json,
 *   players.json (WSZYSCY zawodnicy ligi), fixtures/<id>.json (szczegóły meczów), widzew-team-stats.json
 *
 * Script Properties:
 *   API_KEY   — klucz z dashboard.api-football.com (wymagane)
 *   LEAGUE_ID — domyślnie 106
 *   SEASONS   — lista sezonów, domyślnie "2026,2025,2024,2023" (pierwszy = bieżący; reszta pobierana raz)
 *   FOLDER    — domyślnie "RTSstat-data"
 * Uruchom: testApi -> syncRTSstat (kilka razy, jeśli pracuje długo) -> installTrigger
 */
const BASE = 'https://v3.football.api-sports.io';
const T0 = Date.now();
const TIME_BUDGET_MS = 5 * 60 * 1000;           // Apps Script przerywa po 6 min

function cfg_() {
  const p = PropertiesService.getScriptProperties();
  const key = p.getProperty('API_KEY');
  if (!key) throw new Error('Brak API_KEY we Właściwościach skryptu.');
  return { key: key, league: Number(p.getProperty('LEAGUE_ID') || 106),
           seasons: (p.getProperty('SEASONS') || '2026,2025,2024,2023').split(',').map(s => Number(s.trim())),
           folder: p.getProperty('FOLDER') || 'RTSstat-data' };
}
function api_(path, params) {
  const c = cfg_();
  const qs = Object.keys(params || {}).map(k => k + '=' + encodeURIComponent(params[k])).join('&');
  const url = BASE + path + (qs ? '?' + qs : '');
  const res = UrlFetchApp.fetch(url, { headers: { 'x-apisports-key': c.key }, muteHttpExceptions: true });
  if (res.getResponseCode() !== 200) throw new Error('API ' + res.getResponseCode() + ' ' + url + ': ' + res.getContentText().slice(0, 200));
  const body = JSON.parse(res.getContentText());
  if (body.errors && Object.keys(body.errors).length) throw new Error('API błąd: ' + JSON.stringify(body.errors));
  return body;
}
function sub_(parent, name) { const f = parent.getFoldersByName(name); return f.hasNext() ? f.next() : parent.createFolder(name); }
function root_() { return sub_(DriveApp.getRootFolder(), cfg_().folder); }
function save_(folder, name, obj) {
  const ex = folder.getFilesByName(name), txt = JSON.stringify(obj);
  if (ex.hasNext()) ex.next().setContent(txt); else folder.createFile(name, txt, MimeType.PLAIN_TEXT);
}
function has_(folder, name) { return folder.getFilesByName(name).hasNext(); }
function read_(folder, name) { const f = folder.getFilesByName(name); return f.hasNext() ? JSON.parse(f.next().getBlob().getDataAsString()) : null; }
function timeLeft_() { return Date.now() - T0 < TIME_BUDGET_MS; }

function syncSeason_(season, isCurrent, log) {
  const c = cfg_(), dir = sub_(root_(), String(season)), fxDir = sub_(dir, 'fixtures');
  const league = { league: c.league, season: season };
  // 1. tabela i terminarz — zawsze dla bieżącego, raz dla przeszłych
  if (isCurrent || !has_(dir, 'standings.json')) { save_(dir, 'standings.json', api_('/standings', league).response); log.requests++; }
  let fx = null;
  if (isCurrent || !has_(dir, 'fixtures.json')) { fx = api_('/fixtures', league).response; save_(dir, 'fixtures.json', fx); log.requests++; }
  else fx = read_(dir, 'fixtures.json');
  if (!has_(dir, 'teams.json')) { save_(dir, 'teams.json', api_('/teams', league).response); log.requests++; }
  // 2. WSZYSCY zawodnicy ligi (potrzebne do percentyli) — stronicowane, wznawiane między uruchomieniami
  if (isCurrent || !has_(dir, 'players.json')) {
    const partial = read_(dir, 'players.partial.json') || { page: 1, items: [] };
    let page = partial.page, items = partial.items, total = 99;
    while (page <= total && timeLeft_()) {
      const r = api_('/players', { league: c.league, season: season, page: page }); log.requests++;
      items = items.concat(r.response); total = (r.paging && r.paging.total) || 1; page++;
    }
    if (page > total) { save_(dir, 'players.json', items); const p = dir.getFilesByName('players.partial.json'); while (p.hasNext()) p.next().setTrashed(true); }
    else { save_(dir, 'players.partial.json', { page: page, items: items }); log.errors.push('players ' + season + ': wznów przy następnym uruchomieniu (strona ' + page + '/' + total + ')'); }
  }
  // 3. szczegóły zakończonych meczów (tylko bieżący sezon): events, statistics, players, lineups
  if (isCurrent && fx) {
    const done = fx.filter(f => ['FT', 'AET', 'PEN'].includes(f.fixture.status.short));
    let budget = 12;
    for (const f of done) {
      const name = f.fixture.id + '.json';
      if (has_(fxDir, name) || budget <= 0 || !timeLeft_()) continue;
      try {
        const id = f.fixture.id;
        save_(fxDir, name, { fixture: f, events: api_('/fixtures/events', { fixture: id }).response,
          statistics: api_('/fixtures/statistics', { fixture: id }).response,
          players: api_('/fixtures/players', { fixture: id }).response,
          lineups: api_('/fixtures/lineups', { fixture: id }).response, fetched_at: new Date().toISOString() });
        log.requests += 4; log.new_fixtures.push(id); budget--;
      } catch (e) { log.errors.push('fixture ' + f.fixture.id + ': ' + e.message); }
    }
    // 4. statystyki sezonowe Widzewa
    const tm = read_(dir, 'teams.json') || [];
    const w = tm.find(t => /widzew/i.test(t.team.name));
    if (w) { save_(dir, 'widzew-team-stats.json', api_('/teams/statistics', { league: c.league, season: season, team: w.team.id }).response); log.requests++; }
  }
}

/** GŁÓWNA FUNKCJA — wyzwalacz czasowy. */
function syncRTSstat() {
  const c = cfg_(), log = { run_at: new Date().toISOString(), requests: 0, new_fixtures: [], errors: [] };
  c.seasons.forEach((s, i) => { try { if (timeLeft_()) syncSeason_(s, i === 0, log); } catch (e) { log.errors.push('sezon ' + s + ': ' + e.message); } });
  save_(root_(), '_log.json', log); Logger.log(JSON.stringify(log));
}
function installTrigger() {
  ScriptApp.getProjectTriggers().forEach(t => { if (t.getHandlerFunction() === 'syncRTSstat') ScriptApp.deleteTrigger(t); });
  ScriptApp.newTrigger('syncRTSstat').timeBased().everyDays(1).atHour(4).create();
}
function testApi() { Logger.log(JSON.stringify(api_('/status', {}).response)); }
