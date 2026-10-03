# -*- coding: utf-8 -*-
"""Build the approved news section, archive and detail pages from verified facts.

Run build_i18n.py first, then build_news.py. Dates below are website publication
dates, not Instagram post dates. Expiry removes time-limited news from the home
page; detail pages stay available in the archive. No automatic reposting.
"""
import json
import re
from html import escape
from pathlib import Path

BASE = 'https://buttokuikiro.com'
PUBLISHED = '2026-10-03'
ROOT = Path(__file__).resolve().parents[1] / 'public'
CODES = ['ja', 'en', 'ko', 'zh-hans', 'zh-hant']
NAMES = ['日本語', 'English', '한국어', '简体中文', '繁體中文']
HREFLANG = ['ja', 'en', 'ko', 'zh-Hans', 'zh-Hant']
SLUGS = ['2026-10-duck-mazesoba', '2026-10-opening-hours', '2026-10-buttoku-day']
SOURCES = ['https://www.instagram.com/buttoi_men/p/Dd6rGQXSfj1/', 'https://www.instagram.com/buttoi_men/p/Dd4N_flSf1y/', 'https://www.instagram.com/buttoi_men/p/Dd4N_flSf1y/']
EXPIRY = ['2026-10-31', '2026-10-31', '2026-10-22']
# Urgent closures, when approved, belong here rather than in the ordinary list.
IMPORTANT = {code: [] for code in CODES}
TEXT = {
 'ja': dict(heading='お知らせ', archive='お知らせ一覧', all='お知らせ一覧を見る', back='お知らせ一覧に戻る', home='公式サイトに戻る', source='公式Instagramの案内', caption='公式Instagramの告知画像（AI生成画像を含みます）', categories=['限定麺','営業案内','イベント'],
   titles=['鴨ネギまぜそば、10月も続投。','10月の営業スケジュール','10月22日は「ぶっとくの日」'],
   summaries=['好評につき、10月31日まで販売します。','土日はランチ営業のみ。祝日はお休みです。','ぶっといまぜそばが500円。11:30〜21:00の通し営業。'],
   bodies=[['9月の限定麺「鴨ネギまぜそば」は、ご好評につき10月も販売を継続します。','ご注文ごとに炙る鴨肉と焼きネギを、濃厚な卵黄と特製カエシに合わせた一杯。炙りたての香りと鴨の旨みを、ぶっとい麺と一緒にお楽しみください。','販売期間は10月31日まで。価格は1,580円（税込）〜です。毎月22日「ぶっとくの日」は限定麺を販売していません。'],
     ['10月の土曜・日曜はランチ営業のみ、祝日はお休みです。10月12日（月・祝）は定休日となります。','通常営業は、平日11:30〜14:30（ラストオーダー14:00）／17:00〜23:00（ラストオーダー22:30）。土曜・日曜は11:30〜14:30（ラストオーダー14:00）です。','10月22日（木）の「ぶっとくの日」は、11:30〜21:00（ラストオーダー20:30）の通し営業です。通常の営業時間と異なりますので、ご注意ください。'],
     ['10月22日（木）は「ぶっとくの日」。ぶっといまぜそばを500円（税込）でご提供します。','当日は11:30〜21:00（ラストオーダー20:30）の通し営業です。お昼から夜まで、中休みなしで営業します。','「ぶっとくの日」はまぜそばのみの販売です。ラーメン・昆布水つけ麺・限定麺は販売していません。']]),
 'en': dict(heading='News',archive='All news',all='View all news',back='Back to all news',home='Back to the official site',source='Official Instagram announcement',caption='Official Instagram artwork (includes AI-generated imagery)',categories=['Limited menu','Opening hours','Event'],
   titles=['Duck & Spring Onion Mazesoba continues in October','October opening schedule','October 22 is Buttoku Day'],
   summaries=['Available through October 31 following its popular September run.','Lunch only on Saturdays and Sundays. Closed on public holidays.','Buttoi Mazesoba for 500 yen. Open continuously from 11:30 to 21:00.'],
   bodies=[['Our September special, Duck & Spring Onion Mazesoba, will remain available throughout October.','Duck and spring onion are seared to order, then paired with a rich egg yolk and our house sauce. Enjoy their aroma and the duck’s savoury flavour with our extra-thick noodles.','Available through October 31, from 1,580 yen including tax. Limited specials are not served on the 22nd (Buttoku Day).'],
     ['In October, Saturdays and Sundays are lunch only. We are closed on public holidays, including Monday, October 12.','Regular weekday hours: 11:30–14:30 (last order 14:00) and 17:00–23:00 (last order 22:30). Saturdays and Sundays: 11:30–14:30 (last order 14:00).','On Thursday, October 22 (Buttoku Day), we are open continuously from 11:30 to 21:00, with last orders at 20:30. These differ from regular hours.'],
     ['Thursday, October 22 is Buttoku Day. Buttoi Mazesoba is 500 yen including tax.','We will be open continuously from 11:30 to 21:00, with last orders at 20:30 and no afternoon break.','Only mazesoba is served on Buttoku Day. Ramen, kombu water tsukemen and limited specials are not available.']]),
 'ko': dict(heading='소식',archive='전체 소식',all='전체 소식 보기',back='소식 목록으로 돌아가기',home='공식 사이트로 돌아가기',source='공식 Instagram 안내',caption='공식 Instagram 홍보 이미지 (AI 생성 이미지 포함)',categories=['한정 메뉴','영업 안내','이벤트'],
   titles=['오리·파 마제소바, 10월에도 판매합니다','10월 영업 일정','10월 22일은 「붓토쿠의 날」'],
   summaries=['호평에 힘입어 10월 31일까지 판매합니다.','토·일요일은 점심만 영업하며 공휴일은 쉽니다.','붓토이 마제소바 500엔. 11:30~21:00 브레이크 타임 없이 영업합니다.'],
   bodies=[['9월 한정 메뉴였던 오리·파 마제소바를 호평에 힘입어 10월에도 판매합니다.','주문마다 구운 오리고기와 파에 진한 노른자와 특제 소스를 곁들입니다. 갓 구운 향과 오리의 감칠맛을 굵은 면과 함께 즐겨보세요.','10월 31일까지, 세금 포함 1,580엔부터입니다. 매월 22일 「붓토쿠의 날」에는 한정 메뉴를 판매하지 않습니다.'],
     ['10월 토·일요일은 점심만 영업하며 공휴일은 쉽니다. 10월 12일(월·공휴일)은 휴무입니다.','평일 11:30~14:30(마지막 주문 14:00) / 17:00~23:00(마지막 주문 22:30). 토·일요일 11:30~14:30(마지막 주문 14:00)입니다.','10월 22일(목) 「붓토쿠의 날」에는 11:30~21:00(마지막 주문 20:30) 브레이크 타임 없이 영업합니다. 평소 영업시간과 다릅니다.'],
     ['10월 22일(목)은 「붓토쿠의 날」입니다. 붓토이 마제소바를 세금 포함 500엔에 제공합니다.','11:30~21:00(마지막 주문 20:30) 브레이크 타임 없이 영업합니다.','당일에는 마제소바만 판매합니다. 라멘·다시마물 츠케멘·한정 메뉴는 판매하지 않습니다.']]),
 'zh-hans': dict(heading='最新消息',archive='消息一览',all='查看全部消息',back='返回消息一览',home='返回官方网站',source='官方Instagram公告',caption='官方Instagram宣传图片（含AI生成图片）',categories=['限定菜单','营业通知','活动'],
   titles=['鸭肉葱拌面，10月继续供应','10月营业安排','10月22日是「ぶっとく之日」'],
   summaries=['广受好评，延长供应至10月31日。','周六、周日仅午餐营业，法定节假日休息。','招牌拌面500日元。11:30至21:00全天营业。'],
   bodies=[['9月限定的鸭肉葱拌面广受好评，将在10月继续供应。','鸭肉和葱接单后炙烤，再搭配浓郁蛋黄和特制酱汁。请与极粗面一起享受现烤香气与鸭肉鲜味。','供应至10月31日，含税1,580日元起。每月22日「ぶっとく之日」不供应限定菜单。'],
     ['10月周六、周日仅午餐营业，法定节假日休息。10月12日（周一、节假日）为休息日。','平日11:30–14:30（最后点单14:00）/17:00–23:00（最后点单22:30）。周六、周日11:30–14:30（最后点单14:00）。','10月22日（周四）「ぶっとく之日」11:30–21:00全天营业，最后点单20:30。与通常营业时间不同。'],
     ['10月22日（周四）是「ぶっとく之日」，招牌拌面含税500日元。','当天11:30–21:00全天营业，最后点单20:30，下午不休息。','当天仅供应拌面，不供应拉面、昆布水蘸面和限定菜单。']]),
 'zh-hant': dict(heading='最新消息',archive='消息一覽',all='查看全部消息',back='返回消息一覽',home='返回官方網站',source='官方Instagram公告',caption='官方Instagram宣傳圖片（含AI生成圖片）',categories=['限定菜單','營業通知','活動'],
   titles=['鴨肉蔥拌麵，10月繼續供應','10月營業安排','10月22日是「ぶっとく之日」'],
   summaries=['廣受好評，延長供應至10月31日。','週六、週日僅午餐營業，國定假日休息。','招牌拌麵500日圓。11:30至21:00全天營業。'],
   bodies=[['9月限定的鴨肉蔥拌麵廣受好評，將在10月繼續供應。','鴨肉和蔥接單後炙烤，再搭配濃郁蛋黃和特製醬汁。請與極粗麵一起享受現烤香氣與鴨肉鮮味。','供應至10月31日，含稅1,580日圓起。每月22日「ぶっとく之日」不供應限定菜單。'],
     ['10月週六、週日僅午餐營業，國定假日休息。10月12日（週一、國定假日）為休息日。','平日11:30–14:30（最後點餐14:00）/17:00–23:00（最後點餐22:30）。週六、週日11:30–14:30（最後點餐14:00）。','10月22日（週四）「ぶっとく之日」11:30–21:00全天營業，最後點餐20:30。與平常營業時間不同。'],
     ['10月22日（週四）是「ぶっとく之日」，招牌拌麵含稅500日圓。','當天11:30–21:00全天營業，最後點餐20:30，下午不休息。','當天僅供應拌麵，不供應拉麵、昆布水蘸麵和限定菜單。']]),
}

def prefix(code):
    return '' if code == 'ja' else '/' + code

def news_path(code, slug=''):
    return prefix(code) + '/news/' + (slug + '/' if slug else '')

def rows(code):
    L = TEXT[code]
    result = []
    for i, slug in enumerate(SLUGS):
        thumb = '<img class="news-thumb" src="/news-duck-202610.jpg" alt="" width="72" height="72" loading="lazy">' if i == 0 else '<span></span>'
        result.append('<a class="news-entry" data-valid-until="%s" href="%s"><time class="news-date" datetime="%s">%s</time><span class="news-category">%s</span><span class="news-copy"><span class="news-title">%s</span><span class="news-summary">%s</span></span>%s<span class="news-arrow" aria-hidden="true">→</span></a>' % (EXPIRY[i], news_path(code, slug), PUBLISHED, PUBLISHED.replace('-', '.'), escape(L['categories'][i]), escape(L['titles'][i]), escape(L['summaries'][i]), thumb))
    return '\n'.join(result)

def home_section(code):
    L = TEXT[code]
    important = ''.join('<div class="news-important">%s</div>' % escape(x) for x in IMPORTANT[code])
    return '<!-- NEWS START -->\n<section class="news-section" id="news" aria-labelledby="news-heading"><div class="news-wrap"><div class="news-heading"><h2 id="news-heading">%s</h2><span class="news-kicker">NEWS</span></div>%s<div class="news-list">%s</div><div class="news-actions"><a href="%s">%s　→</a></div></div></section>\n<script>(function(){var today=new Intl.DateTimeFormat("sv-SE",{timeZone:"Asia/Tokyo"}).format(new Date());document.querySelectorAll("#news [data-valid-until]").forEach(function(a){if(a.dataset.validUntil<today)a.hidden=true;});})();</script>\n<!-- NEWS END -->' % (escape(L['heading']), important, rows(code), news_path(code), escape(L['all']))

def document(code, slug=None):
    L = TEXT[code]
    current = news_path(code, slug or '')
    title = L['archive'] if slug is None else L['titles'][SLUGS.index(slug)]
    nav, alternates = [], []
    for c, name, h in zip(CODES, NAMES, HREFLANG):
        path = news_path(c, slug or '')
        nav.append('<a href="%s" hreflang="%s"%s>%s</a>' % (path, h, ' aria-current="page"' if c == code else '', name))
        alternates.append('<link rel="alternate" hreflang="%s" href="%s%s">' % (h, BASE, path))
    alternates.append('<link rel="alternate" hreflang="x-default" href="%s%s">' % (BASE, news_path('ja', slug or '')))
    if code == 'ja':
        fonts = 'https://fonts.googleapis.com/css2?family=Yuji+Syuku&display=swap'
        variables = "--fd:'Yuji Syuku',serif;--fb:'Yuji Syuku',serif"
    else:
        from build_i18n import LANGS
        fonts, variables = LANGS[code]['fonthref'], LANGS[code]['fontvars']
        fonts = fonts.replace('&display=swap', '&family=Yuji+Syuku&display=swap')
    if slug is None:
        content = '<section class="news-section"><div class="news-wrap"><div class="news-heading"><h2>%s</h2><span class="news-kicker">ARCHIVE</span></div><div class="news-list">%s</div><a class="news-back" href="%s/">%s</a></div></section>' % (escape(title), rows(code), prefix(code), escape(L['home']))
        schema = ''
        description = L['heading'] + ' · ' + ' / '.join(L['titles'])
    else:
        i = SLUGS.index(slug)
        description = L['summaries'][i]
        picture = '<figure style="margin:0"><img class="news-image" src="/news-duck-202610.jpg" alt="%s" width="1402" height="1752"><figcaption>%s</figcaption></figure>' % (escape(L['titles'][i]), escape(L['caption'])) if i == 0 else ''
        content = '<article class="news-article"><div class="news-meta"><time class="news-date" datetime="%s">%s</time><span class="news-category">%s</span></div><h1>%s</h1>%s%s<p><a href="%s" target="_blank" rel="noopener">%s</a></p><a class="news-back" href="%s">← %s</a></article>' % (PUBLISHED, PUBLISHED.replace('-', '.'), escape(L['categories'][i]), escape(title), ''.join('<p>%s</p>' % escape(x) for x in L['bodies'][i]), picture, SOURCES[i], escape(L['source']), news_path(code), escape(L['back']))
        schema = '<script type="application/ld+json">%s</script>' % json.dumps({'@context':'https://schema.org','@type':'NewsArticle','headline':title,'description':description,'datePublished':PUBLISHED+'T12:00:00+09:00','dateModified':PUBLISHED+'T12:00:00+09:00','inLanguage':code,'mainEntityOfPage':BASE+current,'author':{'@type':'Organization','name':'麺屋 ぶっとく生きろ。','url':BASE+'/'},'image':[BASE+'/news-duck-202610.jpg'] if i == 0 else []}, ensure_ascii=False)
    return '<!DOCTYPE html>\n<html lang="%s"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>%s｜麺屋 ぶっとく生きろ。</title><meta name="description" content="%s"><link rel="canonical" href="%s%s">%s<link rel="icon" href="/favicon.ico"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="%s"><link rel="stylesheet" href="/news.css"><style>*{box-sizing:border-box}:root{%s}</style><script async src="https://www.googletagmanager.com/gtag/js?id=G-BLYH7L3V1X"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-BLYH7L3V1X");</script>%s</head><body class="news-page"><header class="news-header"><a href="%s/"><img src="/logo-brush-trim.png" alt="麺屋 ぶっとく生きろ。" width="1200" height="323"></a><nav class="news-languages" aria-label="Language">%s</nav></header><main>%s</main><footer class="news-footer">MENYA BUTTOKUIKIRO · © 2026</footer></body></html>\n' % (code, escape(title), escape(description, quote=True), BASE, current, '\n'.join(alternates), escape(fonts, quote=True), variables, schema, prefix(code), ''.join(nav), content)

def main():
    for code in CODES:
        for slug in [None] + SLUGS:
            dest = ROOT / news_path(code, slug or '').lstrip('/') / 'index.html'
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(document(code, slug), encoding='utf-8')
    # Japanese top has hand-authored markup; replace only this managed section.
    index = ROOT / 'index.html'
    source = index.read_text(encoding='utf-8')
    section = home_section('ja')
    if '<!-- NEWS START -->' in source:
        source = re.sub(r'<!-- NEWS START -->.*?<!-- NEWS END -->', lambda _: section, source, flags=re.S)
    else:
        anchor = '<div style="background:#efe9dc;color:#141210;padding:clamp(44px,7vw,96px)'
        pos = source.index(anchor)
        source = source[:pos] + section + '\n\n' + source[pos:]
    if '<link rel="stylesheet" href="/news.css">' not in source:
        source = source.replace('</head>', '<link rel="stylesheet" href="/news.css">\n</head>', 1)
    index.write_text(source, encoding='utf-8')
    sitemap = ROOT / 'sitemap.xml'
    text = sitemap.read_text(encoding='utf-8')
    text = re.sub(r'\s*<url><loc>https://buttokuikiro.com/(?:en/|ko/|zh-hans/|zh-hant/)?news/.*?</url>', '', text)
    additions = ['  <url><loc>%s%s</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>' % (BASE, news_path(c, slug or ''), PUBLISHED) for c in CODES for slug in [None] + SLUGS]
    text = text.replace('</urlset>', '\n'.join(additions) + '\n</urlset>')
    sitemap.write_text(text, encoding='utf-8')
    print('Built news in 5 languages: latest 3 entries, archives, 15 detail pages.')

if __name__ == '__main__':
    main()
