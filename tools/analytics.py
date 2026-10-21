"""Shared, synchronous GA4 bootstrap used by every generated site page."""

ANALYTICS_TAG = '''<script>
(function(){
  var id='G-BLYH7L3V1X',key='buttoku-analytics-opt-out',stopped=false;
  function excluded(){try{return localStorage.getItem(key)==='1';}catch(e){return false;}}
  function showStatus(){
    if(!document.body){document.addEventListener('DOMContentLoaded',showStatus,{once:true});return;}
    if(document.getElementById('analytics-check-status'))return;
    var a=document.createElement('a');
    a.id='analytics-check-status';a.href='/staff-check/';
    a.textContent='確認用アクセス：集計対象外';
    a.style.cssText='position:fixed;right:12px;bottom:82px;z-index:2147483647;max-width:calc(100vw - 24px);padding:8px 12px;border:1px solid #dad2c4;border-radius:6px;background:#fff;color:#25211b;font:13px/1.5 system-ui,sans-serif;text-decoration:none;box-shadow:0 2px 10px #0003';
    document.body.appendChild(a);
  }
  function stop(){
    stopped=true;window['ga-disable-'+id]=true;
    window.gtag=function(){};
    showStatus();
  }
  if(excluded())stop();
  else{
    window.dataLayer=window.dataLayer||[];
    window.gtag=function(){window.dataLayer.push(arguments);};
    window.gtag('js',new Date());window.gtag('config',id);
    var s=document.createElement('script');s.async=true;
    s.src='https://www.googletagmanager.com/gtag/js?id='+id;
    document.head.appendChild(s);
  }
  window.addEventListener('storage',function(e){if(e.key===key&&excluded())stop();});
  window.addEventListener('pageshow',function(){if(!stopped&&excluded())stop();});
})();
</script>'''
