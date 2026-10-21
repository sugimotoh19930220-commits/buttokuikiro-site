// Regression checks for customer measurement and staff collection suppression.
import {readFileSync, readdirSync} from 'node:fs';
import {resolve, join} from 'node:path';
import {fileURLToPath} from 'node:url';
import vm from 'node:vm';
import assert from 'node:assert/strict';

const root=resolve(fileURLToPath(new URL('..',import.meta.url)));
const publicDir=join(root,'public');
const key='buttoku-analytics-opt-out', flag='ga-disable-G-BLYH7L3V1X';
function pages(dir){return readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?pages(join(dir,e.name)):e.name.endsWith('.html')?[join(dir,e.name)]:[]);}
const html=readFileSync(join(publicDir,'index.html'),'utf8');
const bootstrap=html.match(/<script>\n\(function\(\)\{[\s\S]*?<\/script>/)[0];
let count=0;
for(const path of pages(publicDir)){
  const s=readFileSync(path,'utf8');
  if(path.endsWith('/staff-check/index.html')){
    assert(s.includes('noindex,nofollow'));
    assert(!s.includes('googletagmanager.com'));
    continue;
  }
  assert(s.includes(bootstrap),path);
  assert(!/<script[^>]+src="https:\/\/www\.googletagmanager/.test(s),path);
  count++;
}
assert(!readFileSync(join(publicDir,'sitemap.xml'),'utf8').includes('/staff-check/'));
function context(value,broken=false,bodyReady=true){
  const listeners={},domEvents={},scripts=[],badges=[];
  const storage=new Map(value?[ [key,value] ]:[]);
  const body={appendChild:a=>badges.push(a)};
  const document={body:bodyReady?body:null,head:{appendChild:s=>scripts.push(s)},createElement:()=>({style:{}}),getElementById:id=>badges.find(b=>b.id===id),addEventListener:(n,f)=>domEvents[n]=f};
  const window={addEventListener:(n,f)=>listeners[n]=f};
  const localStorage={getItem:k=>{if(broken)throw Error('blocked');return storage.get(k)??null;}};
  const env=vm.createContext({window,document,localStorage,Date});
  vm.runInContext(bootstrap.replace(/^<script>\s*|<\/script>$/g,''),env);
  return {window,document,body,listeners,domEvents,scripts,badges,storage};
}
const normal=context(null);
assert.equal(normal.scripts.length,1);
assert.equal(normal.scripts[0].async,true);
assert.equal(normal.window.dataLayer[1][0],'config');
assert.equal(normal.window.dataLayer[1][1],'G-BLYH7L3V1X');
normal.window.gtag('event','tap_map');
assert.equal(normal.window.dataLayer.length,3);
assert.equal(normal.badges.length,0);
const staff=context('1');
assert.equal(staff.scripts.length,0,'staff must not request the Google loader');
assert.equal(staff.window[flag],true);
staff.window.gtag('event','tap_map');staff.window.gtag('event','tap_phone');staff.window.gtag('event','tap_form');
assert.equal(staff.window.dataLayer,undefined,'custom events must not be queued');
assert.equal(staff.badges[0].textContent,'確認用アクセス：集計対象外');
const early=context('1',false,false);
early.document.body=early.body;early.domEvents.DOMContentLoaded();
assert.equal(early.badges.length,1,'status waits for the DOM');
normal.storage.set(key,'1');normal.listeners.storage({key});
assert.equal(normal.window[flag],true,'other open pages stop on opt-out');
normal.window.gtag('event','tap_map');assert.equal(normal.window.dataLayer.length,3);
const restored=context(null);restored.storage.set(key,'1');restored.listeners.pageshow();
assert.equal(restored.window[flag],true,'back/forward cached pages recheck exclusion');
assert.equal(context(null,true).scripts.length,1,'blocked storage must not disable all customer analytics');
console.log(JSON.stringify({pages:count,customer_loader_and_events:'pass',staff_loader_and_events_suppressed:'pass',early_dom:'pass',cross_tab:'pass',back_forward:'pass',blocked_storage:'pass'}));
