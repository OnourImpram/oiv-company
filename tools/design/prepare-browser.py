"""Reuse this repository's CDP harness for the institutional candidate."""
from pathlib import Path
R=Path(__file__).resolve().parents[2]
s=(R/'tests/browser.mjs').read_text()
start=s.index(' for(const lang of');end=s.index(' assert.equal(errors.length',start)
s=s[:start]+''' for(const lang of ['tr','en'])for(const w of [320,390,768,1024,1440,1920]){
 await load(lang,w);
 await check(`${lang}/${w}/no-overflow`,'document.documentElement.scrollWidth<=innerWidth');
 await check(`${lang}/${w}/images`,'[...document.images].filter(i=>i.getClientRects().length).every(i=>i.complete&&i.naturalWidth>0)');
 await check(`${lang}/${w}/real-fonts`,`document.fonts.check('16px "IBM Plex Sans"')`);
 await check(`${lang}/${w}/one-heading`,'document.querySelectorAll("h1").length===1');
 await check(`${lang}/${w}/no-3d`,'document.querySelectorAll("canvas,#motion-toggle").length===0');
 await check(`${lang}/${w}/published-default`,'document.querySelectorAll("#product-list article:not([hidden])").length===2');
 if(w===1440){await screenshot('Desktop_'+lang.toUpperCase());await screenshot('Full_'+lang.toUpperCase(),true);}
 if(w===390){
  await screenshot('Mobile_'+lang.toUpperCase());
  await evaluate('document.querySelector("#menu-toggle").click()');
  await check(`${lang}/menu-open`,'document.querySelector("#menu-toggle").getAttribute("aria-expanded")==="true"');
  await send('Input.dispatchKeyEvent',{type:'keyDown',key:'Escape',code:'Escape'});await send('Input.dispatchKeyEvent',{type:'keyUp',key:'Escape',code:'Escape'});
  await check(`${lang}/escape-focus`,'document.activeElement.id==="menu-toggle"&&document.querySelector("#menu-toggle").getAttribute("aria-expanded")==="false"');
  await evaluate('document.querySelector("[data-filter=submitted]").click()');
  await check(`${lang}/submitted-four`,'document.querySelectorAll("#product-list article:not([hidden])").length===4');
  await check(`${lang}/announcement`,'document.querySelector("#product-count").textContent.includes("4")');
  await evaluate('document.querySelector("[data-filter=all]").focus()');
  await send('Input.dispatchKeyEvent',{type:'keyDown',key:'Enter',code:'Enter'});await send('Input.dispatchKeyEvent',{type:'keyUp',key:'Enter',code:'Enter'});
  await check(`${lang}/keyboard-six`,'document.querySelectorAll("#product-list article:not([hidden])").length===6');
  await evaluate('document.querySelector("#brief").open=true;document.querySelector("#topic").value="research";document.querySelector("#topic").dispatchEvent(new Event("change"));document.querySelector("#project-note").value="İnsan ve yapay zekâ. &subject=body";document.querySelector("#project-note").dispatchEvent(new Event("input"));');
  await check(`${lang}/email-encoding`,'new URL(document.querySelector("#draft-email").href).searchParams.get("body").includes("&subject=body")');
  await check(`${lang}/input-label`,'document.querySelector("label[for=project-note]").textContent.length>0');
 }
}
await load('tr',1440);
await evaluate('document.querySelector("#register").open=true');await check('company-details','document.querySelector("#register").textContent.includes("17429906")');
await send('Emulation.setScriptExecutionDisabled',{value:true});await send('Page.navigate',{url:base+'tr/'});await delay(700);
await check('no-js-six-products','document.querySelectorAll("#product-list article:not([hidden])").length===6');
await check('no-js-navigation','getComputedStyle(document.querySelector("#primary-nav")).display!=="none"');
await send('Emulation.setScriptExecutionDisabled',{value:false});
''' +s[end:]
s=s.replace("out=resolve('test-evidence')","out=resolve('tool-evidence/browser')")
s=s.replace('document.body?.dataset.edition==="precision" && document.fonts.status==="loaded" && !!document.querySelector("#sculpture")?.dataset.renderer','document.querySelector("#product-filters")?.hidden===false && document.fonts.status==="loaded"')
s=s.replace('document.body?.dataset.edition==="precision"','document.querySelector("#product-filters")?.hidden===false')
(R/'.design-tools/browser-review.mjs').write_text(s)
print('Prepared current CDP tests. No old sculpture checks remain.')
