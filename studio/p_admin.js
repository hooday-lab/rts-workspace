/* ---------- admin ---------- */
const fs=ctx.fs;
function siteUrl(){return location.origin+location.pathname}
async function renderAdmin(){
  const v=$('#view');
  v.innerHTML=`<div class="admin">
  <div class="card-box"><h3>Ekipa (adresy Google)</h3><p class="msg">Tylko adresy z tej listy zobaczą dane i zrobią karty. Wpisz adres, którego dziennikarz używa do logowania przez Google (najczęściej @gmail.com).</p>
   <div class="actions"><input type="text" id="m-email" placeholder="adres@gmail.com" style="max-width:260px"><select id="m-role" style="max-width:140px"><option value="member">dziennikarz</option><option value="admin">admin</option></select><button class="btn pri" id="m-add">Dodaj</button></div><div class="msg" id="m-msg"></div>
   <div class="scroll"><table class="t"><thead><tr><th>Adres</th><th>Rola</th><th></th></tr></thead><tbody id="m-list"></tbody></table></div>
   <button class="btn sm" id="m-copy">Kopiuj zaproszenie na WhatsApp</button><span class="msg" id="m-copymsg"></span></div>
  <div class="card-box"><h3>Tło kart</h3><p class="msg">Obraz 1920×1080 w stylu RTS: logo w prawym górnym rogu, wolny lewy panel. Zostanie przeskalowany i zapisany jako JPEG.</p>
   <img class="mini" id="bgp" alt="Aktualne tło"><div class="actions"><input type="file" id="bgf" accept="image/png,image/jpeg,image/webp"><button class="btn" id="bgr">Przywróć domyślne</button></div><div class="msg" id="bg-msg"></div></div>
  <div class="card-box"><h3>Dostępne typy kart</h3><div class="checks" id="cards-box"></div><div class="msg" id="k-msg"></div></div>
  <div class="card-box"><h3>Dane</h3><p class="msg">Aktualne dane: z dnia <b>${esc(D.meta.generatedAt)}</b>, rozegrane kolejki 1–${lastRound}, sezon ${esc(D.meta.season)}.</p>
   <p class="msg">Po kolejce wgraj tu nowy plik <code>rtsstat-data.json</code> (dostajesz go od Claude'a), a potem odśwież stronę.</p>
   <div class="actions"><input type="file" id="df" accept="application/json,.json"></div><div class="msg" id="d-msg"></div></div></div>`;
  $('#bgp').src=bgData;
  const cb=$('#cards-box');cb.innerHTML=TKEYS.map(k=>`<label><input type="checkbox" data-k="${k}" ${SET.cards[k]!==false?'checked':''}> ${esc(TYPES[k].name)}</label>`).join('');
  cb.querySelectorAll('input').forEach(i=>i.onchange=async()=>{
    SET.cards[i.dataset.k]=i.checked;
    try{await fs.doc('settings/cards').set({...SET.cards});$('#k-msg').textContent='Zapisano.';$('#k-msg').className='msg ok'}catch(e){$('#k-msg').textContent='Nie udało się zapisać ('+(e.code||e.message)+')';$('#k-msg').className='msg err'}
  });
  $('#m-add').onclick=async()=>{
    const em=$('#m-email').value.trim().toLowerCase(),m=$('#m-msg');m.className='msg';
    if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em)){m.textContent='To nie wygląda na adres e-mail.';m.className='msg err';return}
    try{await fs.doc('members/'+em).set({role:$('#m-role').value,addedBy:ctx.email,addedAt:new Date().toISOString()});$('#m-email').value='';m.textContent='Dodano '+em;m.className='msg ok';loadMembers()}
    catch(e){m.textContent='Błąd zapisu ('+(e.code||e.message)+')';m.className='msg err'}
  };
  $('#m-copy').onclick=async()=>{const t=`Cześć! Mamy w Rozmowach Tylko Sportowych narzędzie do robienia kart ze statystykami (#RTSstats): ${siteUrl()}\nWejdź, kliknij „Zaloguj przez Google" i wybierz konto, którego adres mi podałeś/aś. Jeśli nie wpuszcza, napisz do mnie.`;
    try{await navigator.clipboard.writeText(t);$('#m-copymsg').textContent=' Skopiowano'}catch(e){$('#m-copymsg').textContent=' Nie udało się skopiować – zaznacz ręcznie'}};
  $('#bgf').onchange=async e=>{
    const f=e.target.files[0];if(!f)return;const m=$('#bg-msg');m.className='msg';
    try{
      m.textContent='Przetwarzam…';
      const im=new Image();const u=URL.createObjectURL(f);im.src=u;await im.decode();
      const cv=document.createElement('canvas');cv.width=1920;cv.height=1080;cv.getContext('2d').drawImage(im,0,0,1920,1080);URL.revokeObjectURL(u);
      let q=.85,url=cv.toDataURL('image/jpeg',q);while(url.length>900000&&q>.4){q-=.1;url=cv.toDataURL('image/jpeg',q)}
      if(url.length>900000)throw new Error('za duży plik');
      await fs.doc('data/bg').set({dataUrl:url,name:f.name,at:new Date().toISOString()});
      bgData=url;$('#bgp').src=bgData;m.textContent='Tło zmienione.';m.className='msg ok';
    }catch(err){m.textContent='Nie udało się ('+(err.code||err.message)+')';m.className='msg err'}
  };
  $('#bgr').onclick=async()=>{const m=$('#bg-msg');try{await fs.doc('data/bg').delete();bgData=BG_DEFAULT;$('#bgp').src=bgData;m.textContent='Przywrócono domyślne tło.';m.className='msg ok'}catch(err){m.textContent='Błąd ('+(err.code||err.message)+')';m.className='msg err'}};
  $('#df').onchange=async e=>{
    const f=e.target.files[0];if(!f)return;const m=$('#d-msg');m.className='msg';
    try{const txt=await f.text();const d=JSON.parse(txt);
      for(const k of ['fx','teams','tstats','upcoming','goals','players','meta'])if(!d[k])throw new Error('brak pola '+k);
      await fs.doc('data/stats').set({json:JSON.stringify(d),uploadedAt:new Date().toISOString(),by:ctx.email});
      m.textContent='Dane zapisane (kolejki do '+d.meta.lastRound+'). Odśwież stronę, żeby je zobaczyć.';m.className='msg ok';
    }catch(err){m.textContent='Nie udało się: '+(err.code||err.message);m.className='msg err'}
  };
  loadMembers();
}
async function loadMembers(){
  const tb=$('#m-list');if(!tb)return;
  try{
    const snap=await fs.collection('members').get();
    const rows=snap.docs.map(d=>({id:d.id,...d.data()})).sort((a,b)=>a.id.localeCompare(b.id));
    tb.innerHTML=rows.length?'':'<tr><td colspan="3" class="msg">Na razie nikogo – dodaj pierwszy adres.</td></tr>';
    rows.forEach(r=>{
      const tr=el(`<tr><td>${esc(r.id)}</td><td>${r.role==='admin'?'admin':'dziennikarz'}</td><td class="actions"></td></tr>`);
      const ac=tr.querySelector('.actions');
      const tg=el(`<button class="btn sm">${r.role==='admin'?'Zrób dziennikarzem':'Zrób adminem'}</button>`);
      tg.onclick=async()=>{await fs.doc('members/'+r.id).update({role:r.role==='admin'?'member':'admin'});loadMembers()};
      const del=el(`<button class="btn sm">Usuń</button>`);
      del.onclick=async()=>{if(del.dataset.s!=='1'){del.dataset.s='1';del.textContent='Na pewno?';return}await fs.doc('members/'+r.id).delete();loadMembers()};
      ac.append(tg,del);tb.appendChild(tr);
    });
  }catch(e){tb.innerHTML=`<tr><td colspan="3" class="msg err">Nie udało się wczytać listy (${esc(e.code||e.message)})</td></tr>`}
}
function showStudio(who){
  $('#gate').hidden=true;$('#boot').hidden=true;$('#deny').hidden=true;$('#studio').hidden=false;
  if(!TKEYS.includes(S.type)||(!isAdmin&&SET.cards[S.type]===false))S.type=TKEYS.find(k=>SET.cards[k]!==false)||'rival';
  renderTabs();renderWork();
}
await loadFonts();
showStudio();
}
