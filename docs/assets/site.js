/* Continuum. Procedural artwork, not a measurement or an AI performance demo. */
(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const header = document.querySelector('.site-header');
  const menu = document.getElementById('menu-toggle');
  const nav = document.getElementById('main-nav');
  if (menu && header && nav) {
    menu.hidden = false;
    const close = () => {header.classList.remove('menu-open'); menu.setAttribute('aria-expanded', 'false');};
    menu.addEventListener('click', () => {const open = menu.getAttribute('aria-expanded') !== 'true'; header.classList.toggle('menu-open', open); menu.setAttribute('aria-expanded', String(open));});
    nav.addEventListener('click', e => {if (e.target.closest('a')) close();});
    document.addEventListener('keydown', e => {if (e.key === 'Escape' && header.classList.contains('menu-open')) {close(); menu.focus();}});
  }
  function revealAnchor() {
    if (location.hash === '#register') {
      const register = document.getElementById('register');
      if (register) register.open = true;
    }
  }
  addEventListener('hashchange', revealAnchor); revealAnchor();
  const canvas = document.getElementById('continuum');
  const stage = document.getElementById('sculpture');
  const toggle = document.getElementById('motion-toggle');
  if (!canvas || !stage || !toggle) return;
  const ctx = canvas.getContext('2d', {alpha:true});
  if (!ctx) return;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  let paused = reduce.matches, visible = true, raf = 0, last = 0, time = 0;
  let px = 0, py = 0, tx = 0, ty = 0;
  const TAU = Math.PI * 2;
  const norm = a => {const d = Math.hypot(...a) || 1; return a.map(v => v / d);};
  const cross = (a,b) => [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
  const center = t => [(2+0.72*Math.cos(3*t))*Math.cos(2*t),(2+0.72*Math.cos(3*t))*Math.sin(2*t),0.9*Math.sin(3*t)];
  const rings = [];
  const N = 200, M = 48;
  // Tubes follow one continuous trefoil. Narrow gaps give the form a ribbed surface.
  for (let i=0;i<N;i++) {
    const row = [];
    for (const offset of [0,0.965]) {
      const t=(i+offset)/N*TAU, c=center(t), next=center(t+0.001);
      const tangent=norm(next.map((v,k)=>v-c[k]));
      const n=norm(cross(tangent,[0,0,1]));
      const b=norm(cross(tangent,n));
      const radius=0.41+0.035*Math.cos(3*t);
      const loop=[];
      for(let j=0;j<=M;j++) {
        const a=j/M*TAU;
        const normal=n.map((v,k)=>v*Math.cos(a)+b[k]*Math.sin(a));
        loop.push({p:c.map((v,k)=>v+radius*normal[k]),n:normal});
      }
      row.push(loop);
    }
    rings.push(row);
  }
  function rotate(v, ax, ay, az) {
    let [x,y,z]=v;
    [y,z]=[y*Math.cos(ax)-z*Math.sin(ax),y*Math.sin(ax)+z*Math.cos(ax)];
    [x,z]=[x*Math.cos(ay)+z*Math.sin(ay),-x*Math.sin(ay)+z*Math.cos(ay)];
    return [x*Math.cos(az)-y*Math.sin(az),x*Math.sin(az)+y*Math.cos(az),z];
  }
  function resize() {
    const rect=canvas.getBoundingClientRect();
    if(!rect.width || !rect.height) return;
    const ratio=Math.min(devicePixelRatio||1,1.5);
    const w=Math.round(rect.width*ratio),h=Math.round(rect.height*ratio);
    if(canvas.width!==w || canvas.height!==h){canvas.width=w;canvas.height=h;}
    draw();
  }
  function draw() {
    const w=canvas.width,h=canvas.height;
    if(!w||!h) return;
    ctx.clearRect(0,0,w,h);
    const scale=Math.min(w,h)*0.138;
    const ax=0.92+py,ay=-0.15+px+Math.sin(time*0.17)*0.10,az=-0.29+Math.sin(time*0.11)*0.04;
    const project=v=>{const perspective=10.5/(10.5-v[2]);return [w*.51+v[0]*scale*perspective,h*.46+v[1]*scale*perspective];};
    const light=norm([-0.6,-0.8,1.3]);
    const half=norm([-0.3,-0.4,1.3]);
    const faces=[];
    for(let i=0;i<N;i++) {
      const [a,b]=rings[i];
      for(let j=0;j<M;j++) {
        const source=[a[j],b[j],b[j+1],a[j+1]];
        const pts=source.map(v=>rotate(v.p,ax,ay,az));
        const n=rotate(norm(source.reduce((s,v)=>s.map((u,k)=>u+v.n[k]),[0,0,0])),ax,ay,az);
        const diffuse=Math.max(0,n.reduce((s,v,k)=>s+v*light[k],0));
        const spec=Math.pow(Math.max(0,n.reduce((s,v,k)=>s+v*half[k],0)),24);
        const facing=Math.abs(n[2]);
        let l=Math.round(36+160*diffuse+65*spec+17*(1-facing));
        l=Math.max(37,Math.min(238,l));
        // One quiet copper seam, not a second fake data layer.
        const copper=i===39 || i===40;
        const color=copper?`rgb(${Math.min(214,l+52)},${Math.max(50,l-22)},${Math.max(30,l-44)})`:`rgb(${Math.max(0,l-3)},${l+4},${l+1})`;
        faces.push({z:pts.reduce((s,v)=>s+v[2],0)/4,pts:pts.map(project),color});
      }
    }
    faces.sort((a,b)=>a.z-b.z);
    for(const face of faces){ctx.beginPath();face.pts.forEach((p,k)=>k?ctx.lineTo(...p):ctx.moveTo(...p));ctx.closePath();ctx.fillStyle=face.color;ctx.fill();ctx.strokeStyle=face.color;ctx.lineWidth=.45;ctx.stroke();}
    stage.classList.add('rendered');
  }
  function frame(now) {
    raf=0;
    if(paused||!visible||document.hidden)return;
    if(now-last>66){const dt=Math.min((now-last)/1000,.05);last=now;time+=dt;px+=(tx-px)*.06;py+=(ty-py)*.06;draw();}
    raf=requestAnimationFrame(frame);
  }
  function sync(){
    toggle.setAttribute('aria-pressed',String(paused));
    toggle.setAttribute('aria-label',paused?toggle.dataset.play:toggle.dataset.pause);
    toggle.querySelector('span').textContent=paused?'▷':'Ⅱ';
    if(raf){cancelAnimationFrame(raf);raf=0;}
    if(!paused && visible && !document.hidden){last=performance.now();raf=requestAnimationFrame(frame);}
  }
  toggle.hidden=false;
  toggle.addEventListener('click',()=>{paused=!paused;sync();});
  reduce.addEventListener('change',event=>{paused=event.matches;sync();if(paused)draw();});
  document.addEventListener('visibilitychange',sync);
  if('IntersectionObserver' in window){new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;sync();},{threshold:.05}).observe(stage);}
  if('ResizeObserver' in window)new ResizeObserver(resize).observe(stage);else addEventListener('resize',resize);
  if(matchMedia('(pointer:fine)').matches){stage.addEventListener('pointermove',e=>{const r=stage.getBoundingClientRect();tx=((e.clientX-r.left)/r.width-.5)*.28;ty=((e.clientY-r.top)/r.height-.5)*.2;});stage.addEventListener('pointerleave',()=>{tx=0;ty=0;});}
  resize();sync();
})();
