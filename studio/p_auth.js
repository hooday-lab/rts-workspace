/* ---------- logowanie (Firebase) ---------- */
const ADMIN_EMAIL='hooday@gmail.com';
function show(id){for(const x of ['boot','gate','deny','setup','first','studio'])$('#'+x).hidden=(x!==id)}
function renderWho(email,admin){
  $('#who').innerHTML=`<span>${esc(email)}</span>${admin?'<span class="badge">admin</span>':''} <button class="btn sm" id="so">Wyloguj</button>`;
  $('#so').onclick=()=>firebase.auth().signOut().then(()=>location.reload());
}
async function startApp(){
  const cfg=window.RTS_FIREBASE;
  if(!cfg||!cfg.apiKey||/WKLEJ/.test(cfg.apiKey)||typeof firebase==='undefined'){show('setup');return}
  firebase.initializeApp(cfg);
  const auth=firebase.auth(),fs=firebase.firestore();
  let started=false;
  $('#g-go').onclick=async()=>{
    const m=$('#g-msg');m.className='msg';m.textContent='';
    const pr=new firebase.auth.GoogleAuthProvider();pr.setCustomParameters({prompt:'select_account'});
    try{await auth.signInWithPopup(pr)}catch(e){
      if(e.code==='auth/popup-blocked'||e.code==='auth/operation-not-supported-in-this-environment'){try{await auth.signInWithRedirect(pr);return}catch(e2){e=e2}}
      if(e.code==='auth/popup-closed-by-user'||e.code==='auth/cancelled-popup-request')return;
      m.textContent='Nie udało się zalogować ('+(e.code||e.message)+').';m.className='msg err';
    }
  };
  auth.onAuthStateChanged(async u=>{
    if(!u){show('gate');return}
    if(started)return;
    const email=(u.email||'').toLowerCase();
    $('#d-email').textContent=email;
    $('#d-out').onclick=()=>auth.signOut().then(()=>location.reload());
    let snap;
    try{snap=await fs.doc('data/stats').get()}
    catch(e){
      if(e.code==='permission-denied'){renderWho(email,false);show('deny');return}
      $('#boot').textContent='Błąd połączenia z bazą ('+(e.code||e.message)+')';show('boot');return;
    }
    started=true;
    const isAdmin=email===ADMIN_EMAIL||await fs.doc('members/'+email).get().then(d=>d.exists&&d.data().role==='admin').catch(()=>false);
    renderWho(email,isAdmin);
    if(!snap.exists){
      if(!isAdmin){$('#boot').textContent='Dane nie zostały jeszcze wgrane. Napisz do admina.';show('boot');return}
      show('first');
      $('#first-f').onchange=async e=>{const f=e.target.files[0];if(!f)return;const m=$('#first-msg');
        try{const d=JSON.parse(await f.text());for(const k of ['fx','teams','tstats','upcoming','goals','players','meta'])if(!d[k])throw new Error('brak pola '+k);
          await fs.doc('data/stats').set({json:JSON.stringify(d),uploadedAt:new Date().toISOString(),by:email});location.reload()}
        catch(err){m.textContent='Nie udało się: '+(err.code||err.message);m.className='msg err'}};
      return;
    }
    let d;try{d=JSON.parse(snap.data().json)}catch(e){$('#boot').textContent='Plik danych jest uszkodzony.';show('boot');return}
    let bg=null,cards={};
    try{const b=await fs.doc('data/bg').get();if(b.exists)bg=b.data().dataUrl}catch(e){}
    try{const c=await fs.doc('settings/cards').get();if(c.exists)cards=c.data()}catch(e){}
    show('studio');
    runApp(d,{fs,email,isAdmin,bg,cards});
  });
}
startApp();
