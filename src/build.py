#!/usr/bin/env python3
"""Generate OIV's static bilingual website. Python 3.10+, standard library only."""
from pathlib import Path
import html, json, re
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs'
DATA=json.loads((ROOT/'src/content.json').read_text(encoding='utf-8'))
SITE=DATA['site']
ROUTES={
 'en':{'home':'index.html','work':'work.html','about':'about.html','resources':'resources.html','contact':'contact.html','privacy':'privacy.html','accessibility':'accessibility.html','solutions':'solutions.html'},
 'tr':{'home':'tr/index.html','work':'tr/calismalar.html','about':'tr/hakkimizda.html','resources':'tr/kaynaklar.html','contact':'tr/iletisim.html','privacy':'tr/gizlilik.html','accessibility':'tr/erisilebilirlik.html','solutions':'tr/cozumler.html'}
}
for lang in ('tr','en'):
 for s in DATA[lang]['services']:ROUTES[lang][s['id']]=('tr/cozumler/' if lang=='tr' else 'solutions/')+s['slug']+'.html'
# App privacy policies: public URLs for Google Play listings (https://oiv.onourimpram.com/legal/<slug>/).
APP_PRIVACY=json.loads((ROOT/'src/app-privacy.json').read_text(encoding='utf-8'))
for a in APP_PRIVACY['apps']:
 ROUTES['en']['app-'+a['slug']]='legal/'+a['slug']+'/index.html';ROUTES['tr']['app-'+a['slug']]='tr/yasal/'+a['slug']+'/index.html'
def page_url(path):return SITE['url']+'/'+re.sub(r'(^|/)index\.html$',r'\1',path)
esc=lambda s:html.escape(str(s),quote=True)
plain=lambda s:re.sub('<[^>]+>',' ',s)
ARROW='<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 12h15m-6-6 6 6-6 6" stroke="currentColor" stroke-width="1.5"/></svg>'
ICONS={
'brain':'<path d="M24 10c-5-7-12-1-10 5-7-1-10 9-4 12-4 6 1 13 7 11 0 6 7 8 10 3V12c0-5-5-7-8-4M27 12c1-7 10-7 12-1 7-1 10 7 5 12 6 5 3 14-4 14 0 7-9 10-13 5M17 18c6 0 7 5 3 8m-6 3c7-3 9 1 7 6m14-18c-5 2-5 7 0 8m4 5c-5-2-8 1-6 6"/>',
'workflow':'<circle cx="28" cy="9" r="5"/><circle cx="12" cy="40" r="5"/><circle cx="44" cy="40" r="5"/><circle cx="28" cy="40" r="5"/><path d="M28 14v11M12 35v-8c0-2 1-3 4-3h24c3 0 4 1 4 3v8m-16-9v9"/>',
'book':'<path d="M28 15c-7-6-16-5-22-3v32c8-3 15-2 22 3 7-5 14-6 22-3V12c-6-2-15-3-22 3Zm0 0v32M12 18c4-1 8 0 11 2m-11 5c4-1 8 0 11 2m10-7c3-2 7-3 11-2m-11 9c3-2 7-3 11-2"/>',
'research':'<path d="m28 8 10 5-11 21-10-5Zm1-4 12 6m-21 24-4 6m12-21c13 0 20 17 9 26M12 47h33M21 43v4M37 43v4M7 37h24"/><circle cx="36" cy="23" r="3"/>',
'chart':'<path d="M5 47h47M11 46V29h8v17M25 46V18h8v28M39 46V7h8v39"/>',
'search':'<circle cx="24" cy="24" r="14"/><path d="m34 34 13 13"/>',
'plus':'<path d="M28 10v36M10 28h36"/>',
'close':'<path d="m13 13 30 30M43 13 13 43"/>'}
def icon(name,cls='icon'):
 return f'<svg class="{cls}" viewBox="0 0 56 56" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'

def build(lang,key,body,title,summary=None):
 d=DATA[lang];path=ROUTES[lang][key];depth=len(Path(path).parts)-1;root='../'*depth;other='en' if lang=='tr' else 'tr'
 link=lambda k:root+ROUTES[lang][k]
 canonical=page_url(path)
 navkeys=[('home','#solutions'),('work',''),('home','#approach'),('about',''),('resources',''),('contact','')]
 nav=''.join(f'<a href="{link(k)+a}"'+(' aria-current="page"' if key==k and k!='home' else '')+f'>{label}</a>' for (k,a),label in zip(navkeys,d['nav']))
 schema={'@context':'https://schema.org','@type':'Organization','name':SITE['legalName'],'alternateName':SITE['name'],'url':SITE['url'],'email':SITE['email'],'logo':SITE['url']+'/assets/img/oiv-logo.png','identifier':SITE['companyNumber'],'founder':{'@type':'Person','name':'Onour Impram'},'sameAs':['https://find-and-update.company-information.service.gov.uk/company/'+SITE['companyNumber']]}
 langs=''.join(f'<a href="{root+ROUTES[l][key]}" lang="{l}" hreflang="{l}"'+(' aria-current="page"' if l==lang else '')+f'>{l.upper()}</a>' for l in ['en','tr'])
 # Identity facts stay visible without interaction (tests/test_contract.py, tests/browser.mjs).
 company=f'''<section class="company-details" aria-labelledby="company-heading"><h2 class="company-heading" id="company-heading">{d['company']}</h2><div class="company-grid"><div><span>{'Tescilli unvan' if lang=='tr' else 'Legal name'}</span><p>{SITE['legalName']}</p></div><div><span>{'Şirket numarası' if lang=='tr' else 'Company number'}</span><p><a href="https://find-and-update.company-information.service.gov.uk/company/{SITE['companyNumber']}">{SITE['companyNumber']} {ARROW}</a></p></div><div><span>D-U-N-S</span><p>{SITE['duns']}</p></div><div><span>{'Kayıtlı adres' if lang=='tr' else 'Registered office'}</span><p>{SITE['registeredOffice']}</p></div><div><span>{'Faaliyet kodları' if lang=='tr' else 'SIC codes'}</span><p>{SITE['sic']}</p></div><div><span>{'E-posta' if lang=='tr' else 'Email'}</span><p><a href="mailto:{SITE['email']}">{SITE['email']}</a></p></div></div><p class="company-boundary">{d['footerBoundary']}</p></section>'''
 body=body.replace('{{root}}',root)
 output=f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'self' data:; style-src 'self'; script-src 'self'; font-src 'self'; connect-src 'none'; base-uri 'none'; form-action 'none'; object-src 'none'">
<title>{esc(title)}</title><meta name="description" content="{esc(summary or d['description'])}"><meta name="theme-color" content="#102431"><meta name="color-scheme" content="dark">
<link rel="canonical" href="{canonical}"><link rel="alternate" hreflang="en" href="{page_url(ROUTES['en'][key])}"><link rel="alternate" hreflang="tr" href="{page_url(ROUTES['tr'][key])}">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(summary or d['description'])}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{SITE['url']}/assets/img/social-card.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{root}assets/img/favicon.png"><link rel="stylesheet" href="{root}assets/css/site.css"><script defer src="{root}assets/js/core.js"></script><script defer src="{root}assets/js/search-data.js"></script><script defer src="{root}assets/js/site.js"></script>
<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script>
</head>
<body data-page="{key}" data-root="{root}" data-language="{lang}" id="top">
<a class="skip-link" href="#main">{d['skip']}</a>
<header class="site-header"><div class="container header-inner"><a class="brand" href="{link('home')}" aria-label="Onour Impram Ventures"><img src="{root}assets/img/oiv-logo.png" width="480" height="271" alt="OIV"><span>ONOUR IMPRAM<br>VENTURES</span></a><nav class="main-nav" id="main-nav" aria-label="{'Ana menü' if lang=='tr' else 'Main navigation'}">{nav}</nav><div class="header-tools"><button type="button" class="search-toggle icon-button" aria-label="{d['searchLabel']}" aria-controls="site-search" hidden>{icon('search')}</button><div class="languages" aria-label="{'Dil' if lang=='tr' else 'Language'}">{langs}</div><button class="menu-toggle" id="menu-toggle" type="button" aria-label="{d['menu']}" aria-expanded="false" aria-controls="main-nav" hidden><span>{d['menu']}</span><span class="menu-lines" aria-hidden="true"></span></button></div></div></header>
<main id="main" tabindex="-1">{body}</main>
<footer class="site-footer"><div class="container"><div class="footer-top"><a class="brand" href="{link('home')}" aria-label="Onour Impram Ventures"><img src="{root}assets/img/oiv-logo.png" width="480" height="271" alt="OIV"><span>ONOUR IMPRAM<br>VENTURES</span></a><nav aria-label="{'Alt menü' if lang=='tr' else 'Footer navigation'}"><a href="{link('work')}">{d['nav'][1]}</a><a href="{link('about')}">{d['nav'][3]}</a><a href="{link('resources')}">{d['nav'][4]}</a><a href="{link('contact')}">{d['nav'][5]}</a></nav><p>{d['footerLine']}</p></div>{company}<div class="footer-bottom"><p>© {SITE['year']} {SITE['legalName']}. {d['copyright']}</p><p class="supported-by">{d['supportedBy']} <a href="https://e2b.dev" rel="noopener">E2B</a> <span>({d['supportNote']})</span></p><div><a href="{link('privacy')}">{d['privacy']}</a><a href="{link('accessibility')}">{d['accessibility']}</a><a class="to-top" href="#top" aria-label="{'Başa dön' if lang=='tr' else 'Back to top'}">↑</a></div></div></div></footer>
<dialog id="site-search" aria-labelledby="search-title" class="search-dialog"><div class="search-dialog-inner"><div class="dialog-heading"><h2 id="search-title">{d['searchLabel']}</h2><button class="close-search icon-button" type="button" aria-label="{d['close']}">{icon('close')}</button></div><label class="sr-only" for="search-input">{d['searchLabel']}</label><input type="search" id="search-input" placeholder="{d['searchPlaceholder']}" maxlength="80" autocomplete="off"><p class="search-help">{d['searchHint']}</p><div id="search-results" aria-live="polite" data-empty="{d['searchEmpty']}"></div></div></dialog>
<div class="toast" role="status" aria-live="polite" hidden></div>
</body></html>'''
 target=OUT/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(output,encoding='utf-8')

def link(lang,key,anchor=''):return '{{root}}'+ROUTES[lang][key]+anchor

def btn(label,url,kind='gold'):
 return f'<a class="button button-{kind}" href="{url}"><span>{label}</span>{ARROW}</a>'
def textlink(label,url):return f'<a class="text-link" href="{url}"><span>{label}</span>{ARROW}</a>'
def cta(lang):
 d=DATA[lang]
 return f'<section class="cta-band section" data-od-id="contact-cta"><div class="container cta-grid"><div><h2>{d["contactTitle"]}</h2></div><p>{d["contactIntro"]}</p><div class="cta-actions">{btn(d["contactButton"],link(lang,"contact"))}{btn(d["aboutButton"],link(lang,"about"),"outline")}</div></div></section>'
def solution_cards(lang):
 d=DATA[lang]
 return '<div class="solution-grid">'+''.join(f'<article class="solution-card">{icon(s["icon"])}<h3><a href="{link(lang,s["id"])}">{s["title"]}</a></h3><p>{s["intro"]}</p>{textlink(d["detail"],link(lang,s["id"]))}</article>' for s in d['services'])+'</div>'
def process(lang):
 d=DATA[lang]
 return '<ol class="process-list">'+''.join(f'<li><div class="step-line"><span>{i+1:02}</span><i aria-hidden="true"></i></div><h3>{s[0]}</h3><p>{s[1]}</p></li>' for i,s in enumerate(d['steps']))+'</ol>'

def ethos_values(values):
 # The four values share their first word ("More" / "Daha"): set it once as a gold lead-in and
 # keep each full phrase for screen readers.
 lead = values[0].split(' ', 1)[0]
 if not all(v.split(' ', 1)[0] == lead for v in values):
  return '<ul class="ethos-values">' + ''.join('<li>' + v + '</li>' for v in values) + '</ul>'
 items = ''.join(f'<li><span class="sr-only">{lead} </span>{v.split(" ", 1)[1]}</li>' for v in values)
 return f'<div class="ethos-values"><p class="ethos-lead" aria-hidden="true">{lead}</p><ul>{items}</ul></div>'

def home(lang):
 d=DATA[lang]
 nodes=''.join(f'<a class="compass-node node-{s["id"]}" href="{link(lang,s["id"])}" aria-label="{s["title"]}">{icon(s["icon"])}<span>{s["short"]}</span></a>' for s in d['services'])
 compass=f'''<div class="compass" role="group" aria-label="{d['compassLabel']}"><svg class="compass-lines" viewBox="0 0 500 440" fill="none" aria-hidden="true" focusable="false"><path d="M250 18v405M49 220h400M93 66l314 308M90 378 408 60" class="faint"/></svg><svg class="ring ring-outer" viewBox="0 0 500 440" fill="none" aria-hidden="true" focusable="false"><circle cx="250" cy="220" r="181"/><circle class="point" cx="250" cy="39" r="3"/><circle class="point" cx="250" cy="401" r="2"/></svg><svg class="ring ring-pulse" viewBox="0 0 500 440" fill="none" aria-hidden="true" focusable="false"><circle class="pulse-glow" cx="250" cy="220" r="181" pathLength="360"/><circle class="pulse" cx="250" cy="220" r="181" pathLength="360"/></svg><svg class="ring ring-mid" viewBox="0 0 500 440" fill="none" aria-hidden="true" focusable="false"><circle cx="250" cy="220" r="116"/><circle class="point" cx="250" cy="104" r="3"/><circle class="point" cx="250" cy="336" r="3"/></svg><svg class="ring ring-inner" viewBox="0 0 500 440" fill="none" aria-hidden="true" focusable="false"><circle cx="250" cy="220" r="90"/><circle class="point" cx="160" cy="220" r="3"/><circle class="point" cx="340" cy="220" r="3"/></svg><div class="compass-center"><img src="{{{{root}}}}assets/img/oiv-logo.png" alt="" width="480" height="271"></div>{nodes}<p class="compass-aside">{'<br>'.join(d['compassAside'])}</p><p class="compass-quote">“{d['compassQuote']}”</p></div>'''
 purpose=f'''<div class="purpose-text"><p>{d['purposeText']}</p><ul class="purpose-principles">{''.join('<li>'+x+'</li>' for x in d['purposePrinciples'])}</ul></div>'''
 body=f'''<section class="hero dark" data-od-id="hero"><div class="hero-landscape" aria-hidden="true"></div><div class="container hero-grid"><div class="hero-copy"><h1><span>{d['heroTitle'][0]}</span><span>{d['heroTitle'][1]}</span><span>{d['heroTitle'][2]}</span></h1><p class="hero-lead">{d['heroText']}</p><div class="hero-actions">{btn(d['cta'],link(lang,'contact'))}{btn(d['explore'],'#solutions','light')}</div></div>{compass}</div></section>
<section class="section solutions" id="solutions" data-od-id="solutions"><div class="container"><div class="section-heading"><div><h2>{d['solutionsTitle']}</h2></div><p>{d['solutionsText']}</p>{textlink(d['allSolutions'],link(lang,'solutions'))}</div>{solution_cards(lang)}</div></section>
<section class="purpose dark section" id="purpose" data-od-id="purpose"><div class="container purpose-grid"><h2>{d['purposeTitle']}</h2>{purpose}</div></section>
<section class="section process" id="approach" data-od-id="process"><div class="container"><div class="section-heading"><div><h2>{d['processTitle']}</h2></div><p>{d['processText']}</p>{textlink(d['processLink'],link(lang,'about','#method'))}</div>{process(lang)}</div></section>
<section class="section philosophy dark" data-od-id="philosophy"><div class="container ethos"><div class="ethos-copy"><h2>{d['aboutTitle']}</h2><p>{d['aboutText']}</p></div>{ethos_values(d['aboutValues'])}</div></section>{cta(lang)}'''
 build(lang,'home',body,d['homeTitle'])

def intro(lang,label,title,lead):
 d=DATA[lang]
 return f'<section class="inner-hero dark section" data-od-id="intro"><div class="container"><div class="breadcrumb"><a href="{link(lang,"home")}">{d["home"]}</a><span aria-hidden="true">/</span><span>{label}</span></div><h1>{title}</h1><p class="inner-lead">{lead}</p></div></section>'

def service(lang,s):
 d=DATA[lang];p=d['servicePage'];related=next(x for x in d['services'] if x['id']==s['related'])
 body=intro(lang,s['title'],s['headline'],s['lead'])
 body+=f'''<section class="section service-body" data-od-id="service"><div class="container service-layout"><aside class="service-nav"><p class="eyebrow">{p['label']}</p>{''.join(f'<a href="{link(lang,a["id"])}"'+(' aria-current="page"' if a['id']==s['id'] else '')+f'>{icon(a["icon"])}<span>{a["title"]}</span>{ARROW}</a>' for a in d['services'])}</aside><div class="service-content"><h2>{p['what']}</h2><ul class="deliverables">{''.join('<li>'+v+'</li>' for v in s['deliverables'])}</ul><h2>{p['examples']}</h2><div class="example-list">{''.join('<p>'+v+'</p>' for v in s['examples'])}</div><aside class="scope-note"><h3>{p['bounds']}</h3><p>{s['boundary']}</p></aside>{btn(p['cta'],link(lang,'contact')+'?topic='+s['id'])}<div class="related"><p>{p['connect']}</p>{textlink(related['title'],link(lang,related['id']))}</div></div></div></section>{cta(lang)}'''
 build(lang,s['id'],body,s['title']+' | OIV',s['intro'])

def work(lang):
 d=DATA[lang];p=d['projectsPage']
 body=intro(lang,d['nav'][1],p['title'],p['lead'])
 body+=f'<section class="section work-page" data-od-id="portfolio"><div class="container"><div class="filter-bar" hidden><div role="group" aria-label="{p["products"]}"><button type="button" data-filter="all" aria-pressed="true">{p["all"]}</button><button type="button" data-filter="source" aria-pressed="false">{p["openSource"]}</button><button type="button" data-filter="product" aria-pressed="false">{p["products"]}</button></div><p class="filter-count" role="status"></p></div><div class="portfolio-list">'
 for pid,name in [('mergen','Mergen Verdict'),('mneme','mneme Record')]:
  body+=f'''<article class="project-detail" id="{pid}" data-category="source"><div class="project-emblem dark"><img src="{{{{root}}}}assets/img/{pid}.webp" alt="{name}" width="240" height="240" loading="lazy"></div><div><h2>{name}</h2><p class="eyebrow meta">{p['openSource']} / {d[pid+'Role']}</p><p>{d[pid+'Copy']}</p><div class="project-links">{textlink(d['repo'],'https://github.com/OnourImpram/'+pid)}{textlink('Python / PyPI','https://pypi.org/project/'+('mergen-verdict' if pid=='mergen' else 'mneme-core')+'/')}</div><details class="scope-detail"><summary>{'Kapsam ve sınırlar' if lang=='tr' else 'Scope and limitations'}<span aria-hidden="true">+</span></summary><p>{p[pid+'Limit']}</p></details></div></article>'''
 body+='</div><div class="apps-grid">'
 for a in DATA['apps']:
  body+=f'''<article class="app-card" data-category="product"><img src="{{{{root}}}}assets/img/{a['image']}" alt="" width="176" height="176" loading="lazy"><p class="app-status">{p[a['status']]}</p><h2>{a['name']}</h2><p>{a[lang]}</p>{textlink(p['store'] if a['status']=='published' else p['legal'],a['url'])}</article>'''
 body+=f'</div><p class="footnote">{p["statusNote"]}</p>'
 # Apps still being built: text only, no store link, no product mark (2026-09-24, not published).
 body+=f'<div class="dev-apps" id="in-development"><div class="dev-apps-heading"><h2>{p["devTitle"]}</h2><p>{p["devNote"]}</p></div><ul class="dev-app-list">'
 body+=''.join(f'<li data-category="product"><h3>{a["name"]}</h3><p>{a[lang]}</p><span class="app-status">{p["development"]}</span></li>' for a in DATA['devApps'])
 body+=f'</ul></div></div></section>{cta(lang)}'
 build(lang,'work',body,d['nav'][1]+' | OIV')

def about(lang):
 d=DATA[lang];p=d['aboutPage']
 body=intro(lang,d['nav'][3],p['title'],p['lead'])
 body+=f'''<section class="section" data-od-id="about"><div class="container about-layout"><div><h2>{p['activities']}</h2><p>{p['activitiesText']}</p><div class="about-services">{''.join(textlink(s['title'],link(lang,s['id'])) for s in d['services'])}</div></div><aside class="founder-panel"><h2>Onour Impram</h2><p class="eyebrow meta">{p['founder']}</p><p>{p['founderText']}</p>{textlink(p['profile'],'https://onourimpram.com/en/about')}<p class="footnote">{p['bounds']}</p></aside></div></section><section class="section method-section" id="method" data-od-id="method"><div class="container"><div class="section-heading"><div><h2>{d['processTitle']}</h2></div><p>{d['processText']}</p></div>{process(lang)}</div></section>{cta(lang)}'''
 build(lang,'about',body,d['nav'][3]+' | OIV')

def resources(lang):
 d=DATA[lang];p=d['resourcesPage']
 body=intro(lang,d['nav'][4],p['title'],p['lead'])
 body+=f'''<section class="section" data-od-id="resources"><div class="container"><div class="resources-top"><div><h2>{p['brief']}</h2><p>{p['briefText']}</p><a class="button button-ink" href="{{{{root}}}}downloads/oiv-discussion-{lang}.txt" download>{p['briefDownload']}{ARROW}</a></div><div class="resource-links"><p class="eyebrow">{p['code']}</p>{textlink('Mergen Verdict','https://github.com/OnourImpram/mergen')}{textlink('mneme Record','https://github.com/OnourImpram/mneme')}{textlink(d['nav'][1],link(lang,'work'))}</div></div><div class="publication-heading"><h2>{p['books']}</h2><p>{p['bookNote']}</p></div><div class="publications"><article><div class="book-cover"><img src="{{{{root}}}}assets/img/book-ai.jpg" alt="Üretken Yapay Zekâ ve Ruh Sağlığı" width="264" height="389" loading="lazy"></div><div><h3>Üretken Yapay Zekâ ve Ruh Sağlığı</h3><p class="eyebrow meta">{'Yapay zekâ ve insan' if lang=='tr' else 'AI and people'}</p>{textlink(p['books'],'https://onourimpram.com/en/about')}</div></article><article><div class="book-cover"><img src="{{{{root}}}}assets/img/book-positive.jpg" alt="Pozitif Psikoloji" width="264" height="431" loading="lazy"></div><div><h3>Pozitif Psikoloji</h3><p class="eyebrow meta">{'Psikoloji ve araştırma' if lang=='tr' else 'Psychology and research'}</p>{textlink(p['books'],'https://onourimpram.com/en/about')}</div></article></div></div></section>{cta(lang)}'''
 build(lang,'resources',body,d['nav'][4]+' | OIV')


def contact(lang):
 d=DATA[lang];p=d['contactPage']
 options='<option value="general">'+p['general']+'</option>'+''.join(f'<option value="{s["id"]}">{s["title"]}</option>' for s in d['services'])+f'<option value="support">{p["support"]}</option>'
 fields=''.join(f'<div class="field"><label for="{field}">{p[key]} <span>{p["optional"]}</span></label><input id="{field}" name="{field}" type="{typ}" autocomplete="{auto}" maxlength="{length}"><p class="field-error" id="{field}-error" hidden></p></div>' for field,key,typ,auto,length in [('name','name','text','name',80),('organization','org','text','organization',120),('email','email','email','email',100)])
 body=intro(lang,p['label'],p['title'],p['lead'])
 body+=f'''<section class="section contact-section" data-od-id="contact"><div class="container contact-layout"><aside class="contact-aside"><p class="eyebrow">{p['direct']}</p><a class="direct-email" href="mailto:{SITE['email']}">{SITE['email']}</a><ol class="contact-steps">{''.join('<li>'+s+'</li>' for s in p['steps'])}</ol><p class="privacy-note">{p['note']}</p>{textlink(d['privacy'],link(lang,'privacy'))}</aside><div class="brief-app" hidden>
<form id="brief-form" novalidate><div class="form-fields">{fields}<div class="field"><label for="topic">{p['topic']}</label><select name="topic" id="topic">{options}</select></div></div><div class="field"><label for="message">{p['message']}</label><textarea id="message" name="message" rows="7" maxlength="3000" minlength="20" required placeholder="{p['placeholder']}" aria-describedby="message-help message-error"></textarea><div class="field-bottom"><p id="message-help">{p['helper']}</p><span class="char-count">0 / 3000</span></div><p class="field-error" id="message-error" hidden></p></div><button class="button button-ink" type="submit">{p['review']}{ARROW}</button></form>
<section id="brief-preview" aria-labelledby="preview-title" hidden><h2 id="preview-title" tabindex="-1">{p['previewTitle']}</h2><p class="eyebrow meta">{p['ready']}</p><label class="sr-only" for="brief-text">{p['previewTitle']}</label><textarea id="brief-text" rows="13" readonly></textarea><p class="long-brief-note" hidden>{p['long']}</p><div class="brief-actions"><a class="button button-ink" id="email-draft" href="mailto:{SITE['email']}">{p['openEmail']}{ARROW}</a><button class="button button-outline" type="button" id="copy-brief">{p['copy']}</button><button class="text-button" type="button" id="save-brief">{p['download']}</button></div><p id="copy-result" role="status" aria-live="polite" data-ok="{p['copied']}" data-failed="{p['copyFailed']}"></p><button class="text-button edit-brief" type="button">← {p['edit']}</button></section></div><noscript><div class="nojs-contact"><h2>{p['direct']}</h2><p>{p['note']}</p>{btn(p['openEmail'],'mailto:'+SITE['email'],'ink')}</div></noscript></div></section>'''
 build(lang,'contact',body,d['nav'][5]+' | OIV')

def policies(lang):
 d=DATA[lang];tr=lang=='tr'
 privacy=[
  (('Bu web sitesi' if tr else 'This website'),('Bu site, ONOUR IMPRAM VENTURES LTD’nin hizmet ve çalışmalarını tanıtır. İletişim adresi onour@onourimpram.com adresidir.' if tr else 'This site describes the services and work of ONOUR IMPRAM VENTURES LTD. Contact onour@onourimpram.com.')),
  (('Görüşme notunuz' if tr else 'Your enquiry note'),('Görüşme aracı yalnızca bu sayfada çalışır. Yazdığınız bilgiler sunucuya gönderilmez, tarayıcı depolamasına kaydedilmez. Kopyalama, cihaz panonuzu kullanır. İndirme seçeneği cihazınızda bir metin dosyası oluşturur. E-posta bağlantısı kendi e-posta uygulamanızı açar. Gönderme kararı sizdedir.' if tr else 'The enquiry tool runs only in this page. It does not transmit your input to a server or write it to browser storage. Copying uses your device clipboard. Downloading creates a text file on your device. The email link opens your own email application. You decide whether to send.')),
  (('Çerezler ve barındırma' if tr else 'Cookies and hosting'),('Bu paket analiz aracı, reklam takibi, üçüncü taraf yazı tipi veya uygulama çerezi içermez. Barındırma sağlayıcısı güvenlik ve hizmet sunumu amacıyla IP adresi ve erişim zamanı gibi teknik kayıtları işleyebilir. Böyle bir işlem bu sayfanın yerel görüşme aracından ayrıdır.' if tr else 'This package contains no analytics, advertising tracking, third party fonts or application cookies. A hosting provider may process technical information such as IP addresses and access times for security and service delivery. This is separate from the local enquiry tool.')),
  (('Dış bağlantılar' if tr else 'External links'),('GitHub, PyPI, uygulama mağazaları ve kurucunun sitesi kendi koşullarıyla çalışır. Site dışına çıktığınızda ilgili sağlayıcının gizlilik bilgilerini inceleyin.' if tr else 'GitHub, PyPI, app stores and the founder’s website operate under their own terms. Review their privacy information when following an external link.')),
  (('Bize ulaşın' if tr else 'Contact us'),('Web sitesi veya kişisel verilerle ilgili sorularınızı onour@onourimpram.com adresine iletebilirsiniz. Hassas veri, danışan kaydı veya erişim anahtarı göndermeyin.' if tr else 'For questions about the site or personal information, contact onour@onourimpram.com. Do not send sensitive data, clinical records or access credentials.'))]
 accessibility=[
  (('Kullanım yaklaşımı' if tr else 'Our approach'),('Site gerçek metin başlıkları, klavyeyle kullanılabilen kontroller, görünür odak göstergeleri ve farklı ekranlarda yeniden düzenlenen yerleşim kullanır. Dönüp duran bir nesne, otomatik video veya kaydırma kontrolünü devralan efekt yoktur.' if tr else 'The site uses real text headings, keyboard operable controls, visible focus indicators and responsive layouts. There is no rotating object, autoplay video or scroll hijacking.')),
  (('Klavye ve hareket' if tr else 'Keyboard and motion'),('Sekme tuşuyla bağlantılar ve kontroller arasında ilerleyebilirsiniz. Escape tuşu arama penceresini ve mobil menüyü kapatır. Cihazın azaltılmış hareket tercihi dikkate alınır.' if tr else 'Use Tab to move through links and controls. Escape closes the search dialog and mobile menu. The device’s reduced motion preference is respected.')),
  (('JavaScript olmadan' if tr else 'Without JavaScript'),('Sayfa içerikleri, hizmet bağlantıları, ürünler ve doğrudan e-posta bağlantısı kullanılabilir. Yerel arama, filtreler ve görüşme notu hazırlayıcısı JavaScript gerektirir.' if tr else 'Page content, solution links, products and the direct email link remain available. Local search, filters and the enquiry composer require JavaScript.')),
  (('Geri bildirim' if tr else 'Feedback'),('Bir erişim sorunu yaşarsanız sayfa adresi, kullandığınız tarayıcı ve sorunun kısa açıklamasıyla onour@onourimpram.com adresine yazabilirsiniz. Bu metin bağımsız erişilebilirlik sertifikası veya tüm cihazlarda uygunluk garantisi değildir.' if tr else 'Report an accessibility issue to onour@onourimpram.com with the page, your browser and a short description. This statement is not independent accessibility certification or a guarantee for every device.'))]
 for key,sections in [('privacy',privacy),('accessibility',accessibility)]:
  body=intro(lang,d[key],d[key],('Web sitesinin nasıl çalıştığına dair açık bilgiler.' if tr else 'Clear information about how this website works.'))
  apps=''
  if key=='privacy':apps='<h2>'+('Uygulama gizlilik politikaları' if tr else 'App privacy policies')+'</h2><ul>'+''.join(f'<li><a href="{link(lang,"app-"+a["slug"])}">{esc(a["name"])}</a></li>' for a in APP_PRIVACY['apps'])+'</ul>'
  body+='<section class="section" data-od-id="policy"><div class="container prose">'+''.join('<h2>'+h+'</h2><p>'+v+'</p>' for h,v in sections)+apps+f'<p class="updated">{SITE["year"]} · {SITE["legalName"]}</p></div></section>'
  build(lang,key,body,d[key]+' | OIV')

def app_policies(lang):
 d=DATA[lang];tr=lang=='tr';L=APP_PRIVACY['links'];eff=APP_PRIVACY['effective'][lang]
 ul=lambda items:'<ul>'+''.join('<li>'+esc(i)+'</li>' for i in items)+'</ul>'
 for a in APP_PRIVACY['apps']:
  c=a[lang];name=esc(a['name'])
  title=(f'{name} gizlilik politikası' if tr else f'{name} privacy policy')
  lead=(f'Yürürlük tarihi: {eff}. Google Play paket kimliği: {a["package"]}.' if tr else f'Effective {eff}. Google Play package: {a["package"]}.')
  body=intro(lang,d['privacy'],title,lead)
  who=(f'{name} uygulamasını, Birleşik Krallık’ta 17429906 şirket numarasıyla kayıtlı {SITE["legalName"]} yayımlar ve bu politikadaki kişisel verilerin sorumlusudur. İletişim: <a href="mailto:{SITE["email"]}">{SITE["email"]}</a>.' if tr else f'{name} is published by {SITE["legalName"]}, a company registered in the United Kingdom under company number 17429906, which is responsible for the personal data described here. Contact: <a href="mailto:{SITE["email"]}">{SITE["email"]}</a>.')
  sec=[(('Kısaca' if tr else 'In short'),'<p>'+esc(c['summary'])+'</p>'),
   (('Kimiz' if tr else 'Who we are'),'<p>'+who+'</p>'),
   (('Cihazınızda kalan veriler' if tr else 'Data that stays on your device'),'<p>'+('Aşağıdaki bilgiler yalnızca cihazınızdaki uygulama depolamasında tutulur ve bize gönderilmez:' if tr else 'The following is stored only in the app’s storage on your device and is not sent to us:')+'</p>'+ul(c['device'])),
   (('Hizmet sağlayıcılar' if tr else 'Service providers'),ul(c['processors'])+'<p>'+(f'RevenueCat gizlilik politikası: <a href="{L["revenuecat"]}">{L["revenuecat"]}</a>. Google gizlilik politikası: <a href="{L["google"]}">{L["google"]}</a>.' if tr else f'RevenueCat privacy policy: <a href="{L["revenuecat"]}">{L["revenuecat"]}</a>. Google privacy policy: <a href="{L["google"]}">{L["google"]}</a>.')+'</p>'),
   (('Yapmadıklarımız' if tr else 'What we do not do'),ul(c['never'])),
   (('İzinler' if tr else 'Permissions'),ul(c['permissions'])),
   (('Seçimleriniz ve silme' if tr else 'Your choices and deletion'),'<p>'+esc(c['controls'])+'</p>'),
   (('Haklarınız' if tr else 'Your rights'),'<p>'+('Bulunduğunuz yerdeki veri koruma kurallarına göre kişisel verilerinize erişme, düzeltme, silme ve itiraz etme haklarınız olabilir. Taleplerinizi e-postayla iletin; yanıt vermek için gerekenden fazla bilgi istemeyiz. Birleşik Krallık’ta Information Commissioner’s Office’e şikâyette bulunma hakkınız da vardır.' if tr else 'Depending on where you live, you may have rights to access, correct, delete or object to the processing of your personal data. Send requests by email; we will not ask for more information than we need to respond. In the United Kingdom you can also complain to the Information Commissioner’s Office.')+'</p>'),
   (('Çocuklar' if tr else 'Children'),'<p>'+(f'{name} 13 yaşın altındaki çocuklara yönelik değildir ve onlardan bilerek kişisel veri toplamaz.' if tr else f'{name} is not directed to children under 13 and does not knowingly collect personal data from them.')+'</p>'),
   (('Değişiklikler' if tr else 'Changes'),'<p>'+('Bu politikayı uygulamanın veri uygulamaları değiştiğinde, değişiklik yayımlanmadan önce güncelleriz. Yürürlük tarihi sayfanın başında yer alır.' if tr else 'We update this policy before any change to the app’s data practices is released. The effective date is shown at the top of this page.')+'</p>')]
  body+='<section class="section" data-od-id="policy"><div class="container prose">'+''.join('<h2>'+h+'</h2>'+v for h,v in sec)+f'<p class="updated">{eff} · {SITE["legalName"]}</p></div></section>'
  build(lang,'app-'+a['slug'],body,title+' | OIV',c['summary'])


def main():
 for lang in ('en','tr'):
  home(lang);work(lang);about(lang);resources(lang);contact(lang);policies(lang);app_policies(lang)
  d=DATA[lang]
  build(lang,'solutions',intro(lang,d['nav'][0],d['solutionsTitle'],d['solutionsText'])+'<section class="section" data-od-id="all-solutions"><div class="container"><h2 class="sr-only">'+d['solutionsLabel']+'</h2>'+solution_cards(lang)+'</div></section>'+cta(lang),d['nav'][0]+' | OIV')
  for s in DATA[lang]['services']:service(lang,s)
 # Search is a local static index. It requires no fetch, remote API or backend.
 records={}
 for lang in ('en','tr'):
  d=DATA[lang];records[lang]=[{'title':s['title'],'text':s['intro']+' '+s['lead'],'href':ROUTES[lang][s['id']]} for s in d['services']]
  records[lang]+=[{'title':name,'text':d[pid+'Copy'],'href':ROUTES[lang]['work']+'#'+pid} for pid,name in [('mergen','Mergen Verdict'),('mneme','mneme Record')]]
  records[lang]+=[{'title':d['nav'][i],'text':d['description'],'href':ROUTES[lang][k]} for i,k in [(3,'about'),(4,'resources'),(5,'contact')]]
 (OUT/'assets/js/search-data.js').write_text('window.OIV_SEARCH = '+json.dumps(records,ensure_ascii=False)+';\n',encoding='utf-8')
 (OUT/'downloads').mkdir(exist_ok=True)
 for lang in ('en','tr'):
  d=DATA[lang];lines=[d['resourcesPage']['brief'],'ONOUR IMPRAM VENTURES LTD','',d['contactIntro'],'']
  questions=['Hangi problemi çözmek istiyorsunuz','Mevcut süreç nasıl işliyor','Kimler kullanacak veya eğitime katılacak','Hangi veri ve araçlar kullanılacak','Başarıyı neye göre değerlendireceksiniz','Hangi adımlarda insan onayı gerekiyor'] if lang=='tr' else ['What problem are you trying to solve','How does the current process work','Who will use the system or attend the training','What data and tools will be involved','How will you evaluate success','Which actions need human approval']
  for i,q in enumerate(questions):lines.extend([str(i+1)+'. '+q,'',''])
  lines+=['onour@onourimpram.com',SITE['url'],d['contactPage']['helper']]
  (OUT/f'downloads/oiv-discussion-{lang}.txt').write_text('\n'.join(lines),encoding='utf-8')
 paths=[v for m in ROUTES.values() for v in m.values()]
 sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('<url><loc>'+page_url(p)+'</loc></url>\n' for p in paths)+'</urlset>\n'
 (OUT/'sitemap.xml').write_text(sitemap,encoding='utf-8')
 (OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+SITE['url']+'/sitemap.xml\n',encoding='utf-8')
 (OUT/'.nojekyll').touch()
 if not (OUT/'CNAME').exists():(OUT/'CNAME').write_text(SITE['url'].split('//')[1],encoding='utf-8')
 (OUT/'404.html').write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Page not found | OIV</title><link rel="stylesheet" href="/assets/css/site.css"></head><body><main class="not-found dark"><h1>A different way forward.</h1><p>This page could not be found.</p><a class="button button-gold" href="/">Return to OIV</a><p lang="tr">Bu sayfa bulunamadı. <a href="/tr/">Türkçe ana sayfaya dönün.</a></p></main></body></html>''',encoding='utf-8')
 print('Generated',len(paths)+1,'HTML pages, local search index, downloads and metadata.')
if __name__=='__main__':main()
