/* OIV. Pure, offline enquiry and search helpers. No network or persistence. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.OIV = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const topics = {
    tr: {ai:'Yapay zekâ sistemleri',workflows:'İş akışları ve otomasyon',training:'Eğitim ve atölyeler',research:'Uygulamalı araştırma',evaluation:'Değerlendirme',general:'Genel görüşme',support:'Ürün desteği'},
    en: {ai:'AI systems',workflows:'Workflows and automation',training:'Training and workshops',research:'Applied research',evaluation:'Evaluation',general:'General enquiry',support:'Product support'}
  };
  const normalize = value => String(value || '').toLocaleLowerCase('tr-TR').normalize('NFKD').replace(/[\u0300-\u036f]/g,'').replace(/ı/g,'i');
  function search(records, query) {
    const words=normalize(query).slice(0,80).trim().split(/\s+/).filter(Boolean).slice(0,6);
    if (!words.length) return records.slice(0,6);
    return records.map(record => {
      const title=normalize(record.title), text=normalize(record.text);
      return {record,score:words.every(w=>(title+' '+text).includes(w)) ? words.reduce((s,w)=>s+(title.includes(w)?4:1),0):0};
    }).filter(r=>r.score>0).sort((a,b)=>b.score-a.score).slice(0,8).map(r=>r.record);
  }
  function validate(data, locale) {
    const tr=locale==='tr', errors={},message=String(data.message||'').trim(),email=String(data.email||'').trim();
    if(message.length<20) errors.message=tr?'Lütfen ihtiyacınızı en az 20 karakterle açıklayın.':'Please describe your enquiry in at least 20 characters.';
    else if(message.length>3000) errors.message=tr?'Proje notu en fazla 3000 karakter olabilir.':'The project note can contain up to 3000 characters.';
    if(email && !/^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$/.test(email)) errors.email=tr?'Geçerli bir e-posta adresi yazın veya alanı boş bırakın.':'Enter a valid email address or leave this optional field empty.';
    return errors;
  }
  function buildBrief(data, locale) {
    const lang=locale==='tr'?'tr':'en',tr=lang==='tr';
    const clean=(v,n=3000)=>String(v||'').replace(/[\u0000-\u0008\u000b-\u001f\u007f]/g,' ').trim().slice(0,n);
    const topic=Object.hasOwn(topics[lang],data.topic)?data.topic:'general';
    const subject='OIV | '+topics[lang][topic];
    const rows=[tr?'OIV görüşme notu':'OIV enquiry brief','',`${tr?'Konu':'Topic'}: ${topics[lang][topic]}`];
    for (const [field,label] of [['name',tr?'Ad':'Name'],['organization',tr?'Kurum':'Organization'],['email',tr?'E-posta':'Email']]) {
      const value=clean(data[field],field==='organization'?120:100);if(value) rows.push(label+': '+value);
    }
    rows.push('',tr?'İhtiyaç ve hedef':'Context and objective',clean(data.message)|| (tr?'Kapsamı birlikte konuşmak istiyorum.':'I would like to discuss the scope together.'));
    const body=rows.join('\n');
    const prefix='mailto:onour@onourimpram.com?subject='+encodeURIComponent(subject);
    const full=prefix+'&body='+encodeURIComponent(body),tooLong=full.length>1800;
    return {subject,body,tooLong,url:tooLong?prefix:full,topic};
  }
  return {normalize,search,validate,buildBrief,topics};
});
