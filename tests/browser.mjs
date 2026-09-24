/* Real Chromium/CDP checks, design-independent. Node 22+, Chrome, no npm dependencies.
   Contract for any design: no horizontal overflow, images decoded, no declared web font failed
   to load (the 2026-09-24 design uses system faces), one h1, identity facts visible without interaction, content
   visible under reduced motion, a visible focus ring, the mobile menu (#menu-toggle) opens and
   closes with Escape returning focus, no runtime exceptions. */
import {spawn} from 'node:child_process';
import {createServer} from 'node:http';
import {readFile,writeFile,mkdir,mkdtemp,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {resolve,extname,sep} from 'node:path';
import assert from 'node:assert/strict';
const root=resolve('docs'),out=resolve('test-evidence');await mkdir(out,{recursive:true});
const delay=ms=>new Promise(r=>setTimeout(r,ms));
const results=[],logs=[];let server,browser,socket;
const profile=await mkdtemp(resolve(tmpdir(),'oiv-chrome-'));
const types={'.html':'text/html; charset=utf-8','.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml','.png':'image/png','.webp':'image/webp','.jpg':'image/jpeg','.woff2':'font/woff2','.txt':'text/plain','.xml':'application/xml'};
const IDENTITY=['ONOUR IMPRAM VENTURES LTD','17429906','235117532','WC2H 9JQ','onour@onourimpram.com'];
try{
 let base=process.env.OIV_BASE_URL;
 if(!base){
  server=createServer(async(req,res)=>{try{const path=decodeURIComponent(new URL(req.url,'http://local').pathname);if(!path.startsWith('/'))throw Error('Not found');let relative=path.slice(1);if(!relative||relative.endsWith('/'))relative+='index.html';const file=resolve(root,relative);if(!file.startsWith(root+sep))throw Error('Not found');const bytes=await readFile(file);res.writeHead(200,{'Content-Type':types[extname(file)]||'application/octet-stream'});res.end(bytes);}catch{res.writeHead(404);res.end('Not found');}});
  await new Promise(r=>server.listen(0,'127.0.0.1',r));base=`http://127.0.0.1:${server.address().port}/`;
 }
 const args=['--headless=new','--no-sandbox','--disable-dev-shm-usage','--remote-debugging-port=0','--use-angle=swiftshader','--enable-unsafe-swiftshader','--user-data-dir='+profile,'about:blank'];
 browser=spawn(process.env.CHROME||'google-chrome',args,{stdio:['ignore','ignore','pipe']});browser.stderr.on('data',d=>logs.push(String(d)));
 let port;for(let i=0;i<300;i++){try{port=(await readFile(profile+'/DevToolsActivePort','utf8')).split('\n')[0];break;}catch{await delay(100);}}assert.ok(port,'Chrome debug endpoint started');
 const target=await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`,{method:'PUT'})).json();
 socket=new WebSocket(target.webSocketDebuggerUrl);await new Promise((r,j)=>{socket.onopen=r;socket.onerror=j;});
 let seq=0;const pending=new Map(),errors=[];
 socket.onmessage=e=>{const message=JSON.parse(e.data);if(message.id){const request=pending.get(message.id);if(request){pending.delete(message.id);message.error?request.reject(Error(JSON.stringify(message.error))):request.resolve(message.result);}}else if(message.method==='Runtime.exceptionThrown')errors.push(message.params.exceptionDetails);};
 const send=(method,params={})=>new Promise((resolve,reject)=>{const id=++seq;pending.set(id,{resolve,reject});socket.send(JSON.stringify({id,method,params}));setTimeout(()=>{if(pending.has(id)){pending.delete(id);reject(Error('CDP timeout '+method));}},15000).unref();});
 const evaluate=async code=>{const r=await send('Runtime.evaluate',{expression:code,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
 const check=async(name,code)=>{const value=await evaluate(code);assert.ok(value,name);results.push({name,passed:true});console.log('PASS',name);};
 const key=async k=>{await send('Input.dispatchKeyEvent',{type:'keyDown',key:k,code:k});await send('Input.dispatchKeyEvent',{type:'keyUp',key:k,code:k});};
 await send('Page.enable');await send('Runtime.enable');
 async function load(lang,width,height=900){
  await send('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:width<600});
  await send('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'reduce'}]});
  await send('Page.navigate',{url:base+(lang==='tr'?'tr/':'')});
  await send('Page.bringToFront');
  for(let i=0;i<150;i++){try{if(await evaluate(`document.readyState==="complete"&&document.documentElement.lang===${JSON.stringify(lang)}&&document.fonts.status==="loaded"`))break;}catch{}await delay(100);}
  await evaluate('(async()=>{const images=[...document.images];images.forEach(i=>i.loading="eager");for(let y=0,h=document.documentElement.scrollHeight;y<h;y+=650){scrollTo(0,y);await new Promise(r=>setTimeout(r,25));}await Promise.race([Promise.all(images.map(i=>i.decode().catch(()=>{}))),new Promise((_,reject)=>setTimeout(()=>reject(new Error("Image decode timeout: "+images.filter(i=>!i.complete).map(i=>i.src).join(","))),6000))]);scrollTo(0,0);await document.fonts.ready;await new Promise(r=>setTimeout(r,120));})()');
 }
 async function screenshot(name,full=false){const m=await send('Page.getLayoutMetrics');const clip=full?{x:0,y:0,width:m.cssContentSize.width,height:m.cssContentSize.height,scale:1}:undefined;const r=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:full,...(clip?{clip}:{})});await writeFile(out+'/'+name+'.png',Buffer.from(r.data,'base64'));}
 const loadedFace=f=>`[...document.fonts].some(x=>x.family.replace(/["']/g,"")===${JSON.stringify(f)}&&x.status==="loaded")`;
 for(const lang of ['tr','en'])for(const w of [320,390,768,1024,1440,1920]){
  await load(lang,w);
  await check(`${lang}/${w}/no-overflow`,'document.documentElement.scrollWidth<=innerWidth');
  await check(`${lang}/${w}/images`,'[...document.images].every(i=>i.complete&&i.naturalWidth>0)');
  await check(`${lang}/${w}/declared-fonts-loaded`,'[...document.fonts].every(x=>x.status!=="error")');
  await check(`${lang}/${w}/one-h1`,'document.querySelectorAll("h1").length===1');
  if(w===1440){
   await check(`${lang}/identity-visible`,`${JSON.stringify(IDENTITY)}.every(s=>document.body.innerText.includes(s))`);
   await check(`${lang}/reduced-motion-no-animation`,'document.getAnimations().length===0&&!document.documentElement.classList.contains("motion")');
   await check(`${lang}/reduced-motion-content-visible`,'[...document.querySelectorAll("main h1, main h2, main h3, main p")].every(e=>{const s=getComputedStyle(e);return s.opacity!=="0"&&s.visibility!=="hidden";})');
   await evaluate('document.activeElement?.blur();scrollTo(0,0)');await key('Tab');
   await check(`${lang}/focus-ring-visible`,'(()=>{const a=document.activeElement,s=getComputedStyle(a);return a!==document.body&&((s.outlineStyle!=="none"&&parseFloat(s.outlineWidth)>=2)||s.boxShadow!=="none");})()');
   await screenshot('Desktop_'+lang.toUpperCase());await screenshot('Full_'+lang.toUpperCase(),true);
  }
  if(w===390){
   await screenshot('Mobile_'+lang.toUpperCase());await screenshot('MobileFull_'+lang.toUpperCase(),true);
   await evaluate('document.querySelector("#menu-toggle").click()');
   const isOpen='(t=>t.getAttribute("aria-expanded")==="true"||!!t.closest("details")?.open)(document.querySelector("#menu-toggle"))';
   await check(`${lang}/mobile-menu-open`,isOpen);
   await key('Escape');
   await check(`${lang}/mobile-menu-escape`,`document.activeElement.id==="menu-toggle"&&!${isOpen}`);
  }
 }
 // Motion allowed: only transform/opacity animate, frames stay light, the hero pauses offscreen.
 await send('Emulation.setDeviceMetricsOverride',{width:1440,height:900,deviceScaleFactor:1,mobile:false});
 await send('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'no-preference'}]});
 await send('Page.navigate',{url:base});
 for(let i=0;i<100;i++){try{if(await evaluate('document.readyState==="complete"&&document.documentElement.classList.contains("motion")'))break;}catch{}await delay(100);}
 await delay(1500);
 await check('motion/hero-animations-running','document.getAnimations().filter(a=>a.playState==="running"&&a.effect.target.closest(".compass")).length>=9');
 await check('motion/transform-opacity-only','document.getAnimations().every(a=>a instanceof CSSTransition?["transform","opacity"].includes(a.transitionProperty):a.effect.getKeyframes().every(k=>Object.keys(k).every(p=>["offset","easing","composite","computedOffset","transform","opacity"].includes(p))))');
 const frames=await evaluate('(async()=>{const t=[];let last=performance.now();await new Promise(r=>{const f=n=>{t.push(n-last);last=n;t.length<150?requestAnimationFrame(f):r();};requestAnimationFrame(f);});t.shift();t.sort((a,b)=>a-b);return {n:t.length,median:t[t.length>>1],p95:t[Math.floor(t.length*.95)]};})()');
 results.push({name:'motion/frame-timing',passed:true,frames});console.log('FRAMES',JSON.stringify(frames));
 await check('motion/frame-p95-under-50ms',String(frames.p95<50));
 await screenshot('Motion_A');await delay(4000);await screenshot('Motion_B');
 await evaluate('scrollTo(0,document.documentElement.scrollHeight)');await delay(400);
 await check('motion/paused-offscreen','document.getAnimations().filter(a=>a.effect.target.closest(".compass")&&a.effect.getTiming().iterations===Infinity).every(a=>a.playState==="paused")');
 assert.equal(errors.length,0,'No runtime exceptions: '+JSON.stringify(errors).slice(0,500));results.push({name:'no-runtime-exceptions',passed:true});
 await writeFile(out+'/browser-report.json',JSON.stringify({base,mode:process.env.OIV_BASE_URL?'live':'production files on local HTTP',browser:await send('Browser.getVersion'),checks:results},null,2));
 console.log('BROWSER VERIFIED',results.length,'checks');
}catch(error){await writeFile(out+'/failure.json',JSON.stringify({error:String(error),checks:results,chromeLog:logs.join('').slice(-8000)},null,2));console.error(error);process.exitCode=1;}
finally{socket?.close();browser?.kill('SIGTERM');server?.close();await delay(200);await rm(profile,{recursive:true,force:true}).catch(()=>{});}
