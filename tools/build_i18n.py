# -*- coding: utf-8 -*-
"""
麺屋 ぶっとく生きろ。 多言語トップページ生成スクリプト

使い方:  python3 tools/build_i18n.py
出力:    public/en/index.html, public/ko/index.html,
         public/zh-hans/index.html, public/zh-hant/index.html

文言を直すときは、このファイル下部の LANGS を編集して再実行する。
日本語版（public/index.html）はこのスクリプトの対象外。手で編集する。
"""
import os

BASE = 'https://buttokuikiro.com'
GA = 'G-BLYH7L3V1X'
ORDER = ['ja', 'en', 'ko', 'zh-hans', 'zh-hant']
PATHS = {'ja': '/', 'en': '/en/', 'ko': '/ko/', 'zh-hans': '/zh-hans/', 'zh-hant': '/zh-hant/'}
HREFLANG = {'ja': 'ja', 'en': 'en', 'ko': 'ko', 'zh-hans': 'zh-Hans', 'zh-hant': 'zh-Hant'}
SWITCH = {'ja': '日本語', 'en': 'English', 'ko': '한국어', 'zh-hans': '简体中文', 'zh-hant': '繁體中文'}

CSS = """
*{box-sizing:border-box}
body{margin:0;background:#0a0908;color:#f5f1e8;font-family:var(--fb);-webkit-font-smoothing:antialiased;padding-bottom:64px;line-height:1.7}
a{color:#e0391f;text-decoration:none}
img{display:block;max-width:100%}
dl,dd{margin:0}
.wrap{max-width:880px;margin:0 auto}
.sec{padding:clamp(40px,6.5vw,84px) clamp(20px,5vw,52px)}
.lab{display:block;font:400 clamp(11px,1.2vw,13px)/1 var(--fb);letter-spacing:.22em;text-transform:uppercase;color:#e0391f}
.lab.d{color:#a2321f}
h1,h2{font-family:var(--fd);font-weight:var(--fw);line-height:1.2;margin:14px 0 0;letter-spacing:.01em}
h1{font-size:clamp(30px,5.6vw,62px)}
h2{font-size:clamp(23px,3.4vw,40px)}
p{font-size:clamp(14px,1.5vw,16px);text-wrap:pretty}
.light{background:#efe9dc;color:#141210}
.red{background:#e0391f;color:#0a0908}
.top{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;padding:16px clamp(20px,5vw,52px);border-bottom:1px solid rgba(245,241,232,.14)}
.top img{height:30px;width:auto;filter:invert(1)}
.langs{display:flex;flex-wrap:wrap;gap:6px}
.langs a{padding:5px 11px;border:1px solid rgba(245,241,232,.3);border-radius:999px;font-size:12px;color:rgba(245,241,232,.78);white-space:nowrap}
.langs a[aria-current]{background:#e0391f;border-color:#e0391f;color:#0a0908}
.langs.on-light a{border-color:rgba(20,18,16,.3);color:rgba(20,18,16,.75)}
.hero img{width:100%;height:min(56vh,460px);object-fit:cover}
.badge{display:inline-block;margin-top:20px;padding:9px 16px;background:#e0391f;color:#0a0908;font-size:clamp(12px,1.4vw,15px);font-weight:700}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:clamp(14px,2.4vw,28px);margin-top:26px}
.card{border-top:2px solid #e0391f;padding-top:14px}
.card b{display:block;font-family:var(--fd);font-weight:var(--fw);font-size:clamp(17px,2vw,21px);line-height:1.3}
.card span{display:block;margin-top:8px;font-size:clamp(12px,1.35vw,14px);color:rgba(245,241,232,.72)}
.mgrp{margin-top:30px}
.mgrp h3{margin:0 0 4px;font-family:var(--fd);font-weight:var(--fw);font-size:clamp(16px,1.9vw,20px);color:#e0391f}
.mrow{display:flex;justify-content:space-between;align-items:baseline;gap:14px;padding:11px 0;border-top:1px solid rgba(245,241,232,.16);font-size:clamp(13px,1.45vw,15px)}
.mrow s{flex:1 1 auto;text-decoration:none}
.mrow em{flex:0 0 auto;font-style:normal;font-family:'Shippori Mincho B1',serif;font-size:1.06em;white-space:nowrap}
.note{margin-top:14px;font-size:clamp(11px,1.2vw,13px);color:rgba(245,241,232,.55)}
.step{display:flex;gap:16px;padding:16px 0;border-top:1px solid rgba(20,18,16,.2)}
.step i{flex:0 0 auto;font-style:normal;font-family:'Shippori Mincho B1',serif;font-size:clamp(21px,2.5vw,27px);line-height:1.3;color:#a2321f}
.step b{display:block;font-family:var(--fd);font-weight:var(--fw);font-size:clamp(16px,1.8vw,19px)}
.step span{display:block;margin-top:5px;font-size:clamp(13px,1.4vw,15px);color:#3b3631}
.irow{display:flex;gap:14px;padding:13px 0;border-top:1px solid rgba(245,241,232,.16);font-size:clamp(13px,1.4vw,15px)}
.irow dt{flex:0 0 9em;color:rgba(245,241,232,.5)}
.irow dd{flex:1 1 auto}
.ul{margin:24px 0 0;padding:0;list-style:none}
.ul li{padding:12px 0;border-top:1px solid rgba(20,18,16,.2);font-size:clamp(13px,1.4vw,15px)}
.btns{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px}
.btns a{flex:1 1 180px;padding:16px 0;text-align:center;background:#0a0908;color:#f5f1e8;font-size:clamp(14px,1.5vw,16px)}
.vid{max-width:440px;margin:0 auto}
.bar{position:fixed;left:0;right:0;bottom:0;z-index:30;display:flex;background:#0a0908;border-top:1px solid rgba(255,255,255,.18)}
.bar a{flex:1;padding:19px 0;text-align:center;font-size:clamp(13px,1.4vw,15px)}
.bar .c{color:#f5f1e8}
.bar .m{background:#e0391f;color:#0a0908}
.end{border-top:1px solid rgba(245,241,232,.16)}
.end.d{border-color:rgba(20,18,16,.2)}
"""

def langs_nav(cur, on_light=False):
    cls = 'langs on-light' if on_light else 'langs'
    out = ['<nav class="%s" aria-label="Language">' % cls]
    for k in ORDER:
        cu = ' aria-current="true"' if k == cur else ''
        out.append('<a href="%s" hreflang="%s"%s>%s</a>' % (PATHS[k], HREFLANG[k], cu, SWITCH[k]))
    out.append('</nav>')
    return ''.join(out)

def hreflangs():
    out = []
    for k in ORDER:
        out.append('<link rel="alternate" hreflang="%s" href="%s%s">' % (HREFLANG[k], BASE, PATHS[k]))
    out.append('<link rel="alternate" hreflang="x-default" href="%s/">' % BASE)
    return '\n'.join(out)

def build(code, L):
    p = PATHS[code]
    menu = []
    for gname, items in L['menu_groups']:
        menu.append('<div class="mgrp"><h3>%s</h3>' % gname)
        for name, price in items:
            menu.append('<div class="mrow"><s>%s</s><em>%s</em></div>' % (name, price))
        menu.append('<div class="end"></div></div>')
    steps = []
    for n, t, d in L['how_items']:
        steps.append('<div class="step"><i>%s</i><div><b>%s</b><span>%s</span></div></div>' % (n, t, d))
    info = []
    for k, v in L['info_rows']:
        info.append('<div class="irow"><dt>%s</dt><dd>%s</dd></div>' % (k, v))
    notes = ''.join('<li>%s</li>' % x for x in L['notes_items'])
    cards = ''.join('<div class="card"><b>%s</b><span>%s</span></div>' % (a, b) for a, b in L['about_cards'])

    return """<!DOCTYPE html>
<html lang="%(htmllang)s">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(base)s%(path)s">
%(hreflangs)s
<meta property="og:type" content="website">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(base)s%(path)s">
<meta property="og:image" content="%(base)s/ogp.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="%(base)s/ogp.jpg">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<script async src="https://www.googletagmanager.com/gtag/js?id=%(ga)s"></script>
<script>
window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}
gtag('js',new Date());
gtag('config','%(ga)s');
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="%(fonthref)s" rel="stylesheet">
<style>
:root{%(fontvars)s}
%(css)s
</style>
</head>
<body>

<header class="top">
<a href="/"><img src="/logo-brush-trim.png" alt="麺屋 ぶっとく生きろ。" width="1200" height="323"></a>
%(nav)s
</header>

<div class="hero"><img src="/photo-men-lift.jpg" alt="%(alt_hero)s" width="1600" height="1067" fetchpriority="high"></div>

<section class="sec">
<div class="wrap">
<span class="lab">MENYA BUTTOKUIKIRO</span>
<h1>%(h1)s</h1>
<p style="margin:18px 0 0;color:rgba(245,241,232,.85)">%(hero_sub)s</p>
<p style="margin:14px 0 0;font-size:clamp(12px,1.3vw,14px);color:rgba(245,241,232,.55)">%(hero_meta)s</p>
<div class="badge">%(promo)s</div>
</div>
</section>

<section class="sec">
<div class="wrap">
<span class="lab">%(about_lab)s</span>
<h2>%(about_h2)s</h2>
<p style="margin:16px 0 0;color:rgba(245,241,232,.85)">%(about_body)s</p>
<div class="cards">%(cards)s</div>
</div>
</section>

<section class="sec">
<div class="wrap">
<span class="lab">%(menu_lab)s</span>
<h2>%(menu_h2)s</h2>
%(menu)s
<p class="note">%(menu_note)s</p>
</div>
</section>

<section class="sec light">
<div class="wrap">
<span class="lab d">%(how_lab)s</span>
<h2>%(how_h2)s</h2>
<div style="margin-top:24px">%(steps)s<div class="end d"></div></div>
</div>
</section>

<section class="sec">
<div class="wrap vid">
<video src="/video-reel.mp4" poster="/video-poster.jpg" autoplay muted loop playsinline preload="metadata" width="720" height="1108" aria-label="%(alt_video)s" style="width:100%%;height:auto;background:#141210"></video>
<p class="note" style="text-align:center">%(video_cap)s</p>
</div>
</section>

<section class="sec">
<div class="wrap">
<span class="lab">%(info_lab)s</span>
<h2>%(info_h2)s</h2>
<dl style="margin-top:24px">%(info)s<div class="end"></div></dl>
<div class="btns">
<a href="https://www.google.com/maps/search/?api=1&amp;query=%(mapq)s" target="_blank" rel="noopener">%(cta_map)s</a>
<a href="tel:0665637763">%(cta_call)s</a>
<a href="https://www.instagram.com/buttoi_men/" target="_blank" rel="noopener">Instagram</a>
</div>
</div>
</section>

<section class="sec light">
<div class="wrap">
<span class="lab d">%(notes_lab)s</span>
<h2>%(notes_h2)s</h2>
<ul class="ul">%(notes)s<li style="padding:0"></li></ul>
</div>
</section>

<footer style="padding:clamp(30px,5vw,60px) clamp(20px,5vw,52px);border-top:1px solid rgba(255,255,255,.12)">
<div class="wrap">
%(nav_footer)s
<p style="margin:20px 0 0;font-size:clamp(11px,1.15vw,13px);color:rgba(245,241,232,.42)">%(ga_note)s</p>
<p style="margin:14px 0 0;font-size:clamp(10px,1.1vw,12px);color:rgba(245,241,232,.42);font-family:ui-monospace,Menlo,monospace">MENYA BUTTOKUIKIRO / (c) 2026</p>
</div>
</footer>

<div class="bar">
<a class="c" href="tel:0665637763">%(bar_call)s</a>
<a class="m" href="https://www.google.com/maps/search/?api=1&amp;query=%(mapq)s" target="_blank" rel="noopener">%(bar_map)s</a>
</div>

<script>
(function(){
  if(typeof gtag!=='function')return;
  document.addEventListener('click',function(e){
    var a=e.target.closest && e.target.closest('a');
    if(!a||!a.href)return;
    var h=a.href,n=null;
    if(h.indexOf('tel:')===0)n='tap_phone';
    else if(h.indexOf('google.com/maps')>-1)n='tap_map';
    else if(h.indexOf('instagram.com')>-1)n='tap_instagram';
    if(n)gtag('event',n,{link_url:h,page_lang:'%(htmllang)s'});
  },true);
})();
</script>

</body>
</html>
""" % dict(
        htmllang=L['htmllang'], title=L['title'], desc=L['desc'], base=BASE, path=p,
        hreflangs=hreflangs(), ga=GA, fonthref=L['fonthref'], fontvars=L['fontvars'], css=CSS,
        nav=langs_nav(code), nav_footer=langs_nav(code),
        alt_hero=L['alt_hero'], alt_video=L['alt_video'], video_cap=L['video_cap'],
        h1=L['h1'], hero_sub=L['hero_sub'], hero_meta=L['hero_meta'], promo=L['promo'],
        about_lab=L['about_lab'], about_h2=L['about_h2'], about_body=L['about_body'], cards=cards,
        menu_lab=L['menu_lab'], menu_h2=L['menu_h2'], menu=''.join(menu), menu_note=L['menu_note'],
        how_lab=L['how_lab'], how_h2=L['how_h2'], steps=''.join(steps),
        info_lab=L['info_lab'], info_h2=L['info_h2'], info=''.join(info),
        notes_lab=L['notes_lab'], notes_h2=L['notes_h2'], notes=notes,
        cta_map=L['cta_map'], cta_call=L['cta_call'], bar_call=L['bar_call'], bar_map=L['bar_map'],
        ga_note=L['ga_note'],
        mapq='%E9%BA%BA%E5%B1%8B%20%E3%81%B6%E3%81%A3%E3%81%A8%E3%81%8F%E7%94%9F%E3%81%8D%E3%82%8D%E3%80%82%20%E5%A4%A7%E9%98%AA%E5%B8%82%E4%B8%AD%E5%A4%AE%E5%8C%BA%E5%8D%97%E6%9C%AC%E7%94%BA3%E4%B8%81%E7%9B%AE3-17%20%E4%B8%B8%E6%9D%BE%E3%83%93%E3%83%ABB1',
    )

LANGS = {}

LANGS['en'] = dict(
    htmllang='en',
    fonthref='https://fonts.googleapis.com/css2?family=Anton&family=Shippori+Mincho+B1:wght@400&display=swap',
    fontvars="--fd:'Anton',Impact,sans-serif;--fb:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;--fw:400",
    title='MENYA BUTTOKUIKIRO | Extra-thick noodles in Hommachi, Osaka',
    desc='A ramen and mazesoba shop 1 minute from Hommachi Station, Osaka. Extra-thick hand-rubbed noodles made from Japanese mochi wheat. Mazesoba from 980 yen. 16 seats, cash and cards accepted.',
    alt_hero='Lifting the extra-thick noodles',
    alt_video='Cooking at MENYA BUTTOKUIKIRO',
    video_cap='From our Instagram reel',
    h1='THICK. HOT. GOOD.',
    hero_sub='Hand-rubbed, extra-thick curly noodles made from Japanese mochi wheat. We rub every portion by hand after you order, so no two bowls feel exactly the same.',
    hero_meta='Opened 26 May 2025 &nbsp;/&nbsp; 1 min from Osaka Metro Hommachi Station, Exit 7 or 9 &nbsp;/&nbsp; Basement floor (B1)',
    promo='Every 22nd of the month: Mazesoba for 500 yen',
    about_lab='What we serve',
    about_h2='Mazesoba is our signature',
    about_body='Mazesoba is a bowl of noodles served without soup. You mix everything together yourself before eating. Our noodles are unusually thick, so the sauce and oil cling to them. If you have never had it, start with the plain Buttoi Mazesoba.',
    about_cards=[
        ('Extra-thick noodles', 'Japanese mochi wheat, hand-rubbed to order. Chewy and uneven on purpose.'),
        ('No soup', 'Mazesoba has no broth. Mix it well, then eat.'),
        ('Choose your size', '200g to 400g at no extra cost up to 300g. Mazesoba only.'),
    ],
    menu_lab='Menu',
    menu_h2='Prices',
    menu_groups=[
        ('MAZESOBA (no soup)', [
            ('Buttoi Mazesoba', '980 yen'),
            ('Buttoi Mazesoba with extra back fat', '1,280 yen'),
            ('Buttoi Mazesoba with kimchi and mayo', '1,280 yen'),
            ('Extra-strong niboshi (dried sardine) mazesoba', '1,180 yen'),
        ]),
        ('RAMEN (with soup)', [
            ('Buttoi Ramen', '1,080 yen'),
            ('Buttoi Chashu Ramen', '1,380 yen'),
        ]),
        ('TOPPINGS', [
            ('Chunk chashu (max 3 per bowl)', '1,000 yen'),
            ('Kimchi / mayonnaise / extra spring onion / rice / egg', '150 yen each'),
        ]),
        ('DRINKS', [
            ('Asahi small bottle / Kaku highball', '580 yen each'),
            ('Cola / ginger ale / oolong tea', '300 yen each'),
        ]),
    ],
    menu_note='All prices include tax. Noodle size for mazesoba: 200g and 300g are the same price, 400g is 150 yen more. Ramen comes in one size. There is also a monthly special - see the poster inside the shop.',
    how_lab='How to eat it',
    how_h2='Four steps for mazesoba',
    how_items=[
        ('1', 'Mix', 'Mix everything together thoroughly before your first bite. This is the most important step.'),
        ('2', 'Raw egg', 'Dip the noodles in the raw egg, the way you would eat sukiyaki.'),
        ('3', 'Change the flavour', 'On the table: flying-fish vinegar (one splash), house chilli oil (one spoon), garlic sauce (two spoons), fish powder.'),
        ('4', 'Finish', 'Add rice to what is left in the bowl. Or pour in dashi broth and finish it as a soup.'),
    ],
    info_lab='Visit',
    info_h2='Shop information',
    info_rows=[
        ('Hours', 'Mon-Fri 11:30-14:30 / 17:00-23:00<br>Sat, Sun 11:30-14:30'),
        ('Closed', 'Public holidays'),
        ('Address', 'Marumatsu Bldg. B1, 3-3-17 Minamihonmachi, Chuo-ku, Osaka 541-0054'),
        ('Access', 'Osaka Metro Hommachi Station, Exit 7 or 9 - 1 minute on foot'),
        ('Phone', '<a href="tel:0665637763" style="color:#f5f1e8;border-bottom:1px solid rgba(245,241,232,.35)">06-6563-7763</a>'),
        ('Seats', '16 (8 counter, 8 table). Non-smoking throughout.'),
        ('Budget', '1,000-2,000 yen'),
        ('Payment', 'Cash, credit cards, e-money, QR code payment'),
        ('Wi-Fi', 'Free. We are in the basement, so reception can be weak - please connect to the Wi-Fi once you are inside.'),
    ],
    notes_lab='Before you come',
    notes_h2='Good to know',
    notes_items=[
        'We do not take reservations. Please come directly.',
        'There is no parking.',
        'The shop is in the basement and can only be reached by stairs. It is not suitable for strollers.',
        'No takeaway. Please eat in the shop.',
        'We can tell you which ingredients we use - please ask a member of staff before ordering. We cannot accommodate every allergy or dietary requirement.',
        'Our staff speak limited English. Pointing at the menu works fine.',
    ],
    cta_map='Open in Google Maps',
    cta_call='Call the shop',
    bar_call='Call',
    bar_map='Map',
    ga_note='This site uses Google Analytics to understand how the site is used. Pages viewed and device information are sent to Google. No personally identifying information is sent. See <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener" style="color:rgba(245,241,232,.62);border-bottom:1px solid rgba(245,241,232,.3)">Google\'s policies</a>.',
)

LANGS['ko'] = dict(
    htmllang='ko',
    fonthref='https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&family=Shippori+Mincho+B1:wght@400&display=swap',
    fontvars="--fd:'Noto Sans KR',sans-serif;--fb:'Noto Sans KR',sans-serif;--fw:900",
    title='멘야 붓토쿠이키로 | 오사카 혼마치의 굵은 면 라멘·마제소바',
    desc='오사카 혼마치역에서 도보 1분. 일본산 찹쌀밀로 만든 손으로 주무른 굵은 면. 마제소바 980엔부터. 16석, 현금·카드 사용 가능.',
    alt_hero='굵은 면을 들어 올린 모습',
    alt_video='조리 모습',
    video_cap='인스타그램 릴스에서',
    h1='굵게, 뜨겁게, 맛있게.',
    hero_sub='일본산 찹쌀밀로 만든 굵은 곱슬면입니다. 주문을 받은 뒤 한 그릇씩 손으로 주물러 만들기 때문에, 같은 그릇이 하나도 없습니다.',
    hero_meta='2025년 5월 26일 오픈 &nbsp;/&nbsp; 오사카 메트로 혼마치역 7·9번 출구 도보 1분 &nbsp;/&nbsp; 지하 1층',
    promo='매월 22일은 마제소바 500엔',
    about_lab='어떤 가게인가',
    about_h2='간판 메뉴는 마제소바입니다',
    about_body='마제소바는 국물이 없는 면 요리입니다. 먹기 전에 직접 전부 비벼서 드십니다. 면이 매우 굵어서 소스와 기름이 잘 배어듭니다. 처음이시라면 기본 붓토이 마제소바를 추천합니다.',
    about_cards=[
        ('굵은 면', '일본산 찹쌀밀. 주문 후 손으로 주무릅니다. 쫄깃하고 굵기가 일정하지 않습니다.'),
        ('국물이 없습니다', '마제소바에는 국물이 없습니다. 잘 비벼서 드세요.'),
        ('양을 고를 수 있습니다', '200g~400g. 300g까지는 같은 가격. 마제소바만 해당됩니다.'),
    ],
    menu_lab='메뉴',
    menu_h2='가격',
    menu_groups=[
        ('마제소바 (국물 없음)', [
            ('붓토이 마제소바', '980엔'),
            ('붓토이 마제소바 · 등지방 추가', '1,280엔'),
            ('붓토이 마제소바 · 김치 마요', '1,280엔'),
            ('멸치 진한 니보시 마제소바', '1,180엔'),
        ]),
        ('라멘 (국물 있음)', [
            ('붓토이 라멘', '1,080엔'),
            ('붓토이 차슈멘', '1,380엔'),
        ]),
        ('토핑', [
            ('덩어리 차슈 (한 그릇에 3개까지)', '1,000엔'),
            ('김치 / 마요네즈 / 파 추가 / 밥 / 계란', '각 150엔'),
        ]),
        ('음료', [
            ('아사히 소병 / 가쿠 하이볼', '각 580엔'),
            ('콜라 / 진저에일 / 우롱차', '각 300엔'),
        ]),
    ],
    menu_note='모든 가격은 세금 포함입니다. 마제소바의 면 양은 200g과 300g이 같은 가격, 400g은 150엔 추가입니다. 라멘은 한 종류입니다. 매월 바뀌는 기간 한정 메뉴도 있습니다. 가게 안 포스터를 봐 주세요.',
    how_lab='먹는 방법',
    how_h2='마제소바를 먹는 네 단계',
    how_items=[
        ('1', '비빈다', '첫 입 전에 전부 잘 비벼 주세요. 가장 중요한 단계입니다.'),
        ('2', '날계란', '스키야키처럼 날계란에 찍어 드세요.'),
        ('3', '맛을 바꾼다', '테이블 위에 있습니다. 날치 식초 한 바퀴, 자가제 고추기름 한 스푼, 마늘 소스 두 스푼, 생선 가루.'),
        ('4', '마무리', '남은 그릇에 밥을 넣으세요. 또는 육수를 부어 오차즈케로 마무리합니다.'),
    ],
    info_lab='방문 안내',
    info_h2='매장 정보',
    info_rows=[
        ('영업시간', '월~금 11:30-14:30 / 17:00-23:00<br>토·일 11:30-14:30'),
        ('휴무', '공휴일'),
        ('주소', '오사카시 주오구 미나미혼마치 3초메 3-17 마루마쓰 빌딩 B1 (541-0054)'),
        ('오시는 길', '오사카 메트로 혼마치역 7·9번 출구에서 도보 1분'),
        ('전화', '<a href="tel:0665637763" style="color:#f5f1e8;border-bottom:1px solid rgba(245,241,232,.35)">06-6563-7763</a>'),
        ('좌석', '16석 (카운터 8, 테이블 8). 전 좌석 금연.'),
        ('예산', '1,000~2,000엔'),
        ('결제', '현금, 신용카드, 전자화폐, QR 코드 결제'),
        ('Wi-Fi', '무료. 지하 1층이라 전파가 약한 곳이 있습니다. 입장 후 Wi-Fi 연결을 권장합니다.'),
    ],
    notes_lab='오시기 전에',
    notes_h2='미리 알아 두실 점',
    notes_items=[
        '예약은 받지 않습니다. 직접 방문해 주세요.',
        '주차장이 없습니다.',
        '지하 1층이며 계단으로만 내려올 수 있습니다. 유모차로는 불편합니다.',
        '포장은 하지 않습니다. 매장에서 드셔 주세요.',
        '사용하는 원재료는 알려 드릴 수 있습니다. 주문 전에 직원에게 문의해 주세요. 다만 모든 알레르기와 식이 제한에 대응할 수는 없습니다.',
        '직원은 한국어를 하지 못합니다. 메뉴를 가리켜 주시면 됩니다.',
    ],
    cta_map='구글 지도에서 보기',
    cta_call='매장에 전화',
    bar_call='전화',
    bar_map='지도',
    ga_note='이 사이트는 이용 상황 파악을 위해 Google 애널리틱스를 사용하며, 열람한 페이지와 단말 정보가 Google로 전송됩니다. 개인을 특정할 수 있는 정보는 전송하지 않습니다. 자세한 내용은 <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener" style="color:rgba(245,241,232,.62);border-bottom:1px solid rgba(245,241,232,.3)">Google 정책</a>을 참조해 주세요.',
)

LANGS['zh-hans'] = dict(
    htmllang='zh-Hans',
    fonthref='https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700;900&family=Shippori+Mincho+B1:wght@400&display=swap',
    fontvars="--fd:'Noto Sans SC',sans-serif;--fb:'Noto Sans SC',sans-serif;--fw:900",
    title='面屋 BUTTOKUIKIRO | 大阪本町的超粗面拉面·拌面',
    desc='距大阪地铁本町站步行1分钟。使用日本产糯小麦、点单后手工揉制的超粗面。拌面980日元起。16个座位，可用现金和信用卡。',
    alt_hero='挑起超粗面条',
    alt_video='店内烹调',
    video_cap='来自Instagram短视频',
    h1='粗、烫、香。',
    hero_sub='使用日本产糯小麦制作的超粗卷面。每一份都在点单后手工揉制，所以没有两碗是完全一样的。',
    hero_meta='2025年5月26日开业 &nbsp;/&nbsp; 大阪地铁本町站7·9号出口步行1分钟 &nbsp;/&nbsp; 地下1层',
    promo='每月22日 拌面500日元',
    about_lab='本店特色',
    about_h2='招牌是拌面',
    about_body='拌面是没有汤的面。吃之前请自己充分拌匀。本店的面特别粗，酱汁和油能很好地附着在上面。第一次来的话，推荐先点基本款的超粗拌面。',
    about_cards=[
        ('超粗面', '日本产糯小麦。点单后手工揉制。有嚼劲，粗细刻意不均。'),
        ('没有汤', '拌面不带汤。请充分拌匀后食用。'),
        ('可选面量', '200克至400克。300克以内同价。仅限拌面。'),
    ],
    menu_lab='菜单',
    menu_h2='价格',
    menu_groups=[
        ('拌面（无汤）', [
            ('超粗拌面', '980日元'),
            ('超粗拌面 加背脂', '1,280日元'),
            ('超粗拌面 泡菜蛋黄酱', '1,280日元'),
            ('浓郁小鱼干拌面', '1,180日元'),
        ]),
        ('拉面（有汤）', [
            ('超粗拉面', '1,080日元'),
            ('超粗叉烧拉面', '1,380日元'),
        ]),
        ('加料', [
            ('厚切叉烧（每碗最多3块）', '1,000日元'),
            ('泡菜 / 蛋黄酱 / 加葱 / 米饭 / 鸡蛋', '各150日元'),
        ]),
        ('饮料', [
            ('朝日小瓶 / 角瓶高球', '各580日元'),
            ('可乐 / 姜汁汽水 / 乌龙茶', '各300日元'),
        ]),
    ],
    menu_note='所有价格均含税。拌面的面量：200克与300克同价，400克加收150日元。拉面只有一种分量。另有每月更换的限定菜单，请看店内海报。',
    how_lab='吃法',
    how_h2='拌面的四个步骤',
    how_items=[
        ('1', '拌匀', '第一口之前请充分拌匀。这是最重要的一步。'),
        ('2', '生鸡蛋', '像吃寿喜烧那样，蘸生鸡蛋食用。'),
        ('3', '换个味道', '桌上备有：飞鱼醋淋一圈、自制辣油一勺、蒜香酱两勺、鱼粉。'),
        ('4', '收尾', '往剩下的碗里加米饭。或者倒入高汤，做成茶泡饭收尾。'),
    ],
    info_lab='到店信息',
    info_h2='店铺信息',
    info_rows=[
        ('营业时间', '周一至周五 11:30-14:30 / 17:00-23:00<br>周六·周日 11:30-14:30'),
        ('休息日', '节假日'),
        ('地址', '大阪市中央区南本町3丁目3-17 丸松大厦B1（541-0054）'),
        ('交通', '大阪地铁本町站7·9号出口步行1分钟'),
        ('电话', '<a href="tel:0665637763" style="color:#f5f1e8;border-bottom:1px solid rgba(245,241,232,.35)">06-6563-7763</a>'),
        ('座位', '16席（吧台8席、桌位8席）。全席禁烟。'),
        ('人均消费', '1,000～2,000日元'),
        ('支付方式', '现金、信用卡、电子货币、二维码支付'),
        ('Wi-Fi', '免费。因位于地下1层，部分位置信号较弱，建议入店后连接Wi-Fi。'),
    ],
    notes_lab='来店之前',
    notes_h2='请先了解',
    notes_items=[
        '本店不接受预约，请直接到店。',
        '没有停车场。',
        '店铺位于地下1层，只能走楼梯，不便推婴儿车。',
        '不提供外带，请在店内享用。',
        '我们可以告知使用的原材料，点单前请询问店员。但无法应对所有过敏和饮食限制。',
        '店员不会中文。指着菜单点单即可。',
    ],
    cta_map='在谷歌地图打开',
    cta_call='致电本店',
    bar_call='电话',
    bar_map='地图',
    ga_note='本网站为掌握使用情况而使用Google Analytics，浏览的页面和设备信息会发送至Google。不会发送可识别个人身份的信息。详情请见<a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener" style="color:rgba(245,241,232,.62);border-bottom:1px solid rgba(245,241,232,.3)">Google的政策</a>。',
)

LANGS['zh-hant'] = dict(
    htmllang='zh-Hant',
    fonthref='https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700;900&family=Shippori+Mincho+B1:wght@400&display=swap',
    fontvars="--fd:'Noto Sans TC',sans-serif;--fb:'Noto Sans TC',sans-serif;--fw:900",
    title='麵屋 BUTTOKUIKIRO | 大阪本町的超粗麵拉麵·拌麵',
    desc='距大阪地鐵本町站步行1分鐘。使用日本產糯小麥、點餐後手工揉製的超粗麵。拌麵980日圓起。16個座位，可用現金與信用卡。',
    alt_hero='挑起超粗麵條',
    alt_video='店內烹調',
    video_cap='來自Instagram短影音',
    h1='粗、燙、香。',
    hero_sub='使用日本產糯小麥製作的超粗捲麵。每一份都在點餐後手工揉製，所以沒有兩碗是完全一樣的。',
    hero_meta='2025年5月26日開幕 &nbsp;/&nbsp; 大阪地鐵本町站7·9號出口步行1分鐘 &nbsp;/&nbsp; 地下1樓',
    promo='每月22日 拌麵500日圓',
    about_lab='本店特色',
    about_h2='招牌是拌麵',
    about_body='拌麵是沒有湯的麵。食用前請自己充分拌勻。本店的麵特別粗，醬汁與油能好好附著在上面。第一次來的話，建議先點基本款的超粗拌麵。',
    about_cards=[
        ('超粗麵', '日本產糯小麥。點餐後手工揉製。有嚼勁，粗細刻意不均。'),
        ('沒有湯', '拌麵不附湯。請充分拌勻後食用。'),
        ('可選麵量', '200公克至400公克。300公克以內同價。僅限拌麵。'),
    ],
    menu_lab='菜單',
    menu_h2='價格',
    menu_groups=[
        ('拌麵（無湯）', [
            ('超粗拌麵', '980日圓'),
            ('超粗拌麵 加背脂', '1,280日圓'),
            ('超粗拌麵 泡菜美乃滋', '1,280日圓'),
            ('濃郁小魚乾拌麵', '1,180日圓'),
        ]),
        ('拉麵（有湯）', [
            ('超粗拉麵', '1,080日圓'),
            ('超粗叉燒拉麵', '1,380日圓'),
        ]),
        ('加料', [
            ('厚切叉燒（每碗最多3塊）', '1,000日圓'),
            ('泡菜 / 美乃滋 / 加蔥 / 白飯 / 雞蛋', '各150日圓'),
        ]),
        ('飲料', [
            ('朝日小瓶 / 角瓶High Ball', '各580日圓'),
            ('可樂 / 薑汁汽水 / 烏龍茶', '各300日圓'),
        ]),
    ],
    menu_note='所有價格均含稅。拌麵的麵量：200公克與300公克同價，400公克加收150日圓。拉麵只有一種分量。另有每月更換的限定菜單，請看店內海報。',
    how_lab='吃法',
    how_h2='拌麵的四個步驟',
    how_items=[
        ('1', '拌勻', '第一口之前請充分拌勻。這是最重要的一步。'),
        ('2', '生雞蛋', '像吃壽喜燒那樣，沾生雞蛋食用。'),
        ('3', '換個味道', '桌上備有：飛魚醋淋一圈、自製辣油一匙、蒜香醬兩匙、魚粉。'),
        ('4', '收尾', '往剩下的碗裡加白飯。或者倒入高湯，做成茶泡飯收尾。'),
    ],
    info_lab='到店資訊',
    info_h2='店鋪資訊',
    info_rows=[
        ('營業時間', '週一至週五 11:30-14:30 / 17:00-23:00<br>週六·週日 11:30-14:30'),
        ('公休', '國定假日'),
        ('地址', '大阪市中央區南本町3丁目3-17 丸松大樓B1（541-0054）'),
        ('交通', '大阪地鐵本町站7·9號出口步行1分鐘'),
        ('電話', '<a href="tel:0665637763" style="color:#f5f1e8;border-bottom:1px solid rgba(245,241,232,.35)">06-6563-7763</a>'),
        ('座位', '16席（吧台8席、桌位8席）。全席禁菸。'),
        ('消費預算', '1,000～2,000日圓'),
        ('付款方式', '現金、信用卡、電子貨幣、QR Code支付'),
        ('Wi-Fi', '免費。因位於地下1樓，部分位置訊號較弱，建議入店後連接Wi-Fi。'),
    ],
    notes_lab='來店之前',
    notes_h2='請先了解',
    notes_items=[
        '本店不接受訂位，請直接到店。',
        '沒有停車場。',
        '店鋪位於地下1樓，只能走樓梯，不便推嬰兒車。',
        '不提供外帶，請在店內享用。',
        '我們可以告知使用的原材料，點餐前請詢問店員。但無法因應所有過敏與飲食限制。',
        '店員不會中文。指著菜單點餐即可。',
    ],
    cta_map='在Google地圖開啟',
    cta_call='致電本店',
    bar_call='電話',
    bar_map='地圖',
    ga_note='本網站為掌握使用狀況而使用Google Analytics，瀏覽的頁面與裝置資訊會傳送至Google。不會傳送可識別個人身分的資訊。詳情請見<a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener" style="color:rgba(245,241,232,.62);border-bottom:1px solid rgba(245,241,232,.3)">Google的政策</a>。',
)

if __name__ == '__main__':
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public')
    for code, L in LANGS.items():
        d = os.path.join(root, code)
        os.makedirs(d, exist_ok=True)
        f = os.path.join(d, 'index.html')
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(build(code, L))
        print('wrote', os.path.relpath(f, root), len(build(code, L)), 'chars')
