/* OIV Precision. First-party progressive enhancement. No network or persistence. */
(function () {
  'use strict';
  const TAU = Math.PI * 2;
  const unit = v => { const d = Math.hypot(...v) || 1; return v.map(x => x / d); };
  const cross = (a,b) => [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
  function makeGeometry(segments=320, sides=40) {
    if (!Number.isInteger(segments) || !Number.isInteger(sides) || segments<24 || sides<8 || (segments+1)*(sides+1)>65535) throw new RangeError('Invalid mesh resolution');
    const curve = t => [(2+.72*Math.cos(3*t))*Math.cos(2*t),(2+.72*Math.cos(3*t))*Math.sin(2*t),.90*Math.sin(3*t)];
    const vertices = new Float32Array((segments+1)*(sides+1)*8);
    const indices = new Uint16Array(segments*sides*6);
    let v=0, k=0;
    for(let i=0;i<=segments;i++) {
      const t=i/segments*TAU,c=curve(t),d=curve(t+.0001);
      const tangent=unit(d.map((x,j)=>x-c[j])),n=unit(cross(tangent,[0,0,1])),b=unit(cross(tangent,n));
      for(let j=0;j<=sides;j++) {
        const a=j/sides*TAU,co=Math.cos(a),si=Math.sin(a);
        const normal=unit(n.map((x,h)=>x*co/.55+b[h]*si/.31));
        for(let h=0;h<3;h++) vertices[v++]=c[h]+.55*co*n[h]+.31*si*b[h];
        for(let h=0;h<3;h++) vertices[v++]=normal[h];
        vertices[v++]=i/segments;vertices[v++]=j/sides;
        if(i<segments && j<sides) {
          const p=i*(sides+1)+j,q=p+sides+1;
          for(const index of [p,q,p+1,p+1,q,q+1]) indices[k++]=index;
        }
      }
    }
    return {vertices,indices};
  }
  function buildBrief(language,topic,description) {
    const tr=language==='tr';
    const topics=tr?{evaluation:'Yapay zekâ değerlendirmesi',research:'Araştırma işbirliği',product:'Bir ürün fikri',training:'Atölye ve eğitim'}:{evaluation:'AI evaluation',research:'Research collaboration',product:'A product idea',training:'Workshop or training'};
    const label=topics[topic]||topics.evaluation;
    const clean=String(description||'').replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/g,'').slice(0,1200).trim();
    const subject='OIV. '+label;
    const body=(tr?'Görüşme konusu. ':'Conversation topic. ')+label+'\n\n'+(clean||(tr?'Projemin kapsamını birlikte değerlendirmek istiyorum.':'I would like to discuss the scope of a project.'));
    return {text:subject+'\n\n'+body,href:'mailto:onour@onourimpram.com?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(body)};
  }
  if(typeof module!=='undefined' && module.exports) module.exports={makeGeometry,buildBrief};
  if(typeof document==='undefined') return;
  document.documentElement.classList.add('js');
  const $=s=>document.querySelector(s);
  const header=$('.site-header'),menu=$('#menu-toggle'),nav=$('#main-nav');
  if(header && menu && nav) {
    menu.hidden=false;
    const close=()=>{header.classList.remove('menu-open');menu.setAttribute('aria-expanded','false');};
    menu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';header.classList.toggle('menu-open',open);menu.setAttribute('aria-expanded',String(open));});
    nav.addEventListener('click',e=>{if(e.target.closest('a')) close();});
    document.addEventListener('keydown',e=>{if(e.key==='Escape' && header.classList.contains('menu-open')){close();menu.focus();}});
    matchMedia('(min-width:781px)').addEventListener('change',close);
    if('IntersectionObserver' in window) {
      const targets=[...nav.querySelectorAll('a[href^="#"]')];
      const inView=new Map();
      const observer=new IntersectionObserver(entries=>{
        entries.forEach(entry=>inView.set(entry.target.id,entry.isIntersecting));
        const current=targets.find(a=>inView.get(a.hash.slice(1)));
        targets.forEach(a=>a===current?a.setAttribute('aria-current','location'):a.removeAttribute('aria-current'));
      },{rootMargin:'-10% 0px -65% 0px',threshold:0});
      targets.forEach(a=>{const target=document.getElementById(a.hash.slice(1));if(target)observer.observe(target);});
    }
  }
  const revealAnchor=()=>{if(location.hash==='#register'){const el=$('#register');if(el)el.open=true;}};
  addEventListener('hashchange',revealAnchor);revealAnchor();
  const brief=$('#brief-builder'),topic=$('#brief-topic'),description=$('#brief-description');
  if(brief && topic && description) {
    const email=$('#email-brief'),copy=$('#copy-brief'),status=$('#brief-status'),fallback=$('#copy-fallback'),count=$('#brief-count'),tr=document.documentElement.lang==='tr';
    brief.hidden=false;
    const value=()=>buildBrief(tr?'tr':'en',topic.value,description.value);
    const refresh=()=>{if(description.value.length>1200)description.value=description.value.slice(0,1200);email.href=value().href;count.textContent=description.value.length+' / 1200';status.textContent='';fallback.hidden=true;};
    topic.addEventListener('change',refresh);description.addEventListener('input',refresh);refresh();
    copy.addEventListener('click',async()=>{
      try {
        if(!navigator.clipboard?.writeText)throw new Error('Clipboard unavailable');
        await navigator.clipboard.writeText(value().text);
        status.textContent=tr?'Özet kopyalandı. Henüz mesaj gönderilmedi.':'Brief copied. No message has been sent.';
      } catch {
        fallback.value=value().text;fallback.hidden=false;fallback.focus();fallback.select();
        status.textContent=tr?'Otomatik kopyalama kullanılamıyor. Seçili metni cihazınızın kopyalama komutuyla kopyalayın.':'Automatic copying is unavailable. Copy the selected text using your device’s copy command.';
      }
    });
  }
  // Scene failures must never prevent navigation or the contact flow.
  try { setupSculpture(); } catch { const stage=$('#sculpture');if(stage)stage.dataset.renderer='fallback'; }
  function setupStaticSculpture(canvas,stage) {
    const ctx=canvas.getContext('2d');
    if(!ctx){stage.dataset.renderer='fallback';return;}
    const {vertices,indices}=makeGeometry(220,36);
    const rotate=p=>{let [x,y,z]=p;const ax=-.89,ay=.15,az=.36;[y,z]=[y*Math.cos(ax)-z*Math.sin(ax),y*Math.sin(ax)+z*Math.cos(ax)];[x,z]=[x*Math.cos(ay)+z*Math.sin(ay),-x*Math.sin(ay)+z*Math.cos(ay)];return [x*Math.cos(az)-y*Math.sin(az),x*Math.sin(az)+y*Math.cos(az),z];};
    const faces=[];
    for(let i=0;i<indices.length;i+=6){
      const ids=[indices[i],indices[i+1],indices[i+5],indices[i+2]];
      const points=ids.map(id=>rotate(Array.from(vertices.slice(id*8,id*8+3))));
      const n=unit(ids.reduce((sum,id)=>sum.map((v,j)=>v+vertices[id*8+3+j]),[0,0,0]));
      const normal=rotate(n);const facing=Math.max(0,normal[2]);
      const diffuse=Math.max(0,normal[0]*-.3+normal[1]*.6+normal[2]*.74);
      const l=Math.min(243,Math.max(26,42+diffuse*154+Math.pow(facing,19)*42));
      const copper=Math.abs(vertices[ids[0]*8+6]-.212)<.016;
      const color=copper?`rgb(${Math.min(246,l+28)},${l*.66},${l*.41})`:`rgb(${l*.94},${l},${l*.91})`;
      faces.push({points,z:points.reduce((n,p)=>n+p[2],0)/4,color});
    }
    faces.sort((a,b)=>a.z-b.z);
    let width=0,height=0;
    const draw=()=>{
      const box=canvas.getBoundingClientRect(),ratio=Math.min(devicePixelRatio||1,1.5),w=Math.round(box.width*ratio),h=Math.round(box.height*ratio);
      if(!w||!h||(w===width&&h===height))return;width=w;height=h;canvas.width=w;canvas.height=h;
      ctx.clearRect(0,0,w,h);
      for(const f of faces){ctx.beginPath();f.points.forEach((p,j)=>{const denom=1-p[2]*.075;const x=w/2+p[0]*h*.146/denom,y=h/2-(p[1]*.146+.0125)*h/denom;j?ctx.lineTo(x,y):ctx.moveTo(x,y);});ctx.closePath();ctx.fillStyle=f.color;ctx.fill();ctx.strokeStyle=f.color;ctx.lineWidth=.6;ctx.stroke();}
      stage.classList.add('rendered');stage.dataset.renderer='static-canvas';
    };
    if('ResizeObserver' in window)new ResizeObserver(draw).observe(stage);else addEventListener('resize',draw);draw();
  }
  function setupSculpture() {
    const canvas=$('#continuum'),stage=$('#sculpture'),toggle=$('#motion-toggle'),views=$('.view-switch');
    if(!canvas || !stage || !toggle || !views)return;
    const gl=canvas.getContext('webgl',{alpha:true,antialias:true,powerPreference:'low-power',preserveDrawingBuffer:false});
    if(!gl){setupStaticSculpture(canvas,stage);return;}
    const vs=`attribute vec3 aPosition;attribute vec3 aNormal;attribute vec2 aUV;
      uniform mat3 uRotation;uniform float uAspect;
      varying vec3 vNormal;varying vec3 vPosition;varying vec2 vUV;
      void main(){vec3 p=uRotation*aPosition;vPosition=p;vNormal=uRotation*aNormal;vUV=aUV;
      float w=1.0-p.z*.075;gl_Position=vec4(p.x*.292/uAspect,p.y*.292+.025,-p.z*.085,w);}`;
    const fs=`precision mediump float;varying vec3 vNormal;varying vec3 vPosition;varying vec2 vUV;uniform float uWire;
      void main(){vec3 n=normalize(vNormal),v=normalize(vec3(0.,0.,12.)-vPosition),r=reflect(-v,n);
      float sky=smoothstep(-.65,.85,r.y);
      vec3 env=mix(vec3(.075,.14,.105),vec3(.84,.89,.78),sky);
      float key=pow(max(dot(r,normalize(vec3(-.55,.75,1.))),0.),22.);
      float rim=pow(max(dot(r,normalize(vec3(.85,.2,.5))),0.),38.);
      float band=1.-smoothstep(.06,.20,abs(r.x+.30));band*=smoothstep(-.7,-.4,r.y)*(1.-smoothstep(.65,.95,r.y));
      env+=vec3(.75,.78,.69)*key+vec3(.68,.72,.62)*rim+vec3(.29,.32,.26)*band;
      float diff=.72+.28*max(dot(n,normalize(vec3(-.4,.8,1.))),0.);
      float seams=1.-smoothstep(.012,.018,abs(vUV.x-.212));
      float brush=.985+.015*cos(vUV.x*6.2831853*210.);
      vec3 color=env*diff*brush;
      color=mix(color,color*vec3(1.18,.59,.32)+vec3(.12,.035,.005),seams);
      vec2 grid=abs(fract(vUV*vec2(96.,24.)+.5)-.5);
      float line=1.-smoothstep(.024,.065,min(grid.x,grid.y));
      vec3 technical=mix(vec3(.79,.86,.75),vec3(.11,.24,.16),line)*(.72+.28*max(n.z,0.));
      color=mix(color,technical,uWire);
      gl_FragColor=vec4(pow(clamp(color,0.,1.),vec3(.83)),1.);}`;
    const compile=(type,source)=>{const s=gl.createShader(type);gl.shaderSource(s,source);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS)){gl.deleteShader(s);throw new Error('Sculpture shader unavailable');}return s;};
    const vertex=compile(gl.VERTEX_SHADER,vs),fragment=compile(gl.FRAGMENT_SHADER,fs),program=gl.createProgram();
    gl.attachShader(program,vertex);gl.attachShader(program,fragment);gl.linkProgram(program);gl.deleteShader(vertex);gl.deleteShader(fragment);
    if(!gl.getProgramParameter(program,gl.LINK_STATUS)){gl.deleteProgram(program);throw new Error('Sculpture program unavailable');}
    gl.useProgram(program);
    const mesh=makeGeometry(),vb=gl.createBuffer(),ib=gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER,vb);gl.bufferData(gl.ARRAY_BUFFER,mesh.vertices,gl.STATIC_DRAW);
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,ib);gl.bufferData(gl.ELEMENT_ARRAY_BUFFER,mesh.indices,gl.STATIC_DRAW);
    for(const [name,size,offset] of [['aPosition',3,0],['aNormal',3,12],['aUV',2,24]]){const a=gl.getAttribLocation(program,name);gl.enableVertexAttribArray(a);gl.vertexAttribPointer(a,size,gl.FLOAT,false,32,offset);}
    const rotation=gl.getUniformLocation(program,'uRotation'),aspect=gl.getUniformLocation(program,'uAspect'),wire=gl.getUniformLocation(program,'uWire');
    gl.enable(gl.DEPTH_TEST);gl.clearColor(0,0,0,0);
    let paused=true,visible=true,lost=false,raf=0,last=0,time=0,wireMode=0;
    const reduce=matchMedia('(prefers-reduced-motion: reduce)');
    function matrix(ax,ay,az){
      const transform=(x,y,z)=>{let yy=y*Math.cos(ax)-z*Math.sin(ax),zz=y*Math.sin(ax)+z*Math.cos(ax);let xx=x*Math.cos(ay)+zz*Math.sin(ay);zz=-x*Math.sin(ay)+zz*Math.cos(ay);return [xx*Math.cos(az)-yy*Math.sin(az),xx*Math.sin(az)+yy*Math.cos(az),zz];};
      return new Float32Array([...transform(1,0,0),...transform(0,1,0),...transform(0,0,1)]);
    }
    function draw(){
      if(lost)return;
      gl.viewport(0,0,canvas.width,canvas.height);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);
      gl.uniformMatrix3fv(rotation,false,matrix(-.89,.15+Math.sin(time*.25)*.18,.36+Math.sin(time*.16)*.055));
      gl.uniform1f(aspect,canvas.width/canvas.height);gl.uniform1f(wire,wireMode);
      gl.drawElements(gl.TRIANGLES,mesh.indices.length,gl.UNSIGNED_SHORT,0);
      stage.classList.add('rendered');stage.dataset.renderer='webgl';
    }
    function resize(){const box=canvas.getBoundingClientRect();if(!box.width||!box.height||lost)return;const dpr=Math.min(devicePixelRatio||1,1.75);canvas.width=Math.round(box.width*dpr);canvas.height=Math.round(box.height*dpr);draw();}
    function frame(now){raf=0;if(paused||!visible||document.hidden||lost)return;if(now-last>=42){time+=Math.min((now-last)/1000,.1);last=now;draw();}raf=requestAnimationFrame(frame);}
    function sync(){
      toggle.setAttribute('aria-pressed',String(paused));toggle.setAttribute('aria-label',paused?toggle.dataset.play:toggle.dataset.pause);toggle.querySelector('span').textContent=paused?'▷':'Ⅱ';
      if(raf){cancelAnimationFrame(raf);raf=0;}if(!paused&&visible&&!document.hidden&&!lost){last=performance.now();raf=requestAnimationFrame(frame);}
    }
    toggle.hidden=false;views.hidden=false;
    toggle.addEventListener('click',()=>{paused=!paused;sync();});
    views.addEventListener('click',e=>{const button=e.target.closest('button[data-view]');if(!button)return;wireMode=button.dataset.view==='wire'?1:0;views.querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));draw();});
    reduce.addEventListener('change',e=>{if(e.matches){paused=true;sync();}});
    document.addEventListener('visibilitychange',sync);
    if('IntersectionObserver' in window)new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;sync();},{threshold:.05}).observe(stage);
    if('ResizeObserver' in window)new ResizeObserver(resize).observe(stage);else addEventListener('resize',resize);
    canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();lost=true;paused=true;sync();stage.classList.remove('rendered');stage.dataset.renderer='fallback';toggle.hidden=true;views.hidden=true;});
    resize();sync();
  }
})();
