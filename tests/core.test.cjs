const { test } = require('node:test');
const assert = require('node:assert/strict');
let core;
try { core = require('../docs/assets/js/core.js'); } catch { core = {}; }
test('Turkish search normalizes dotted and dotless I and diacritics', () => {
 assert.equal(typeof core.normalize, 'function');
 assert.equal(core.normalize('İŞ AKIŞLARI, EĞİTİM'), 'is akislari, egitim');
});
test('search ranks relevant services without requiring exact accents', () => {
 assert.equal(typeof core.search, 'function');
 const records=[{title:'İş akışları',text:'Süreç tasarımı ve otomasyon',href:'workflows.html'},{title:'Eğitim',text:'Ekip atölyeleri',href:'training.html'}];
 assert.equal(core.search(records,'is akis')[0].href,'workflows.html');
 assert.equal(core.search(records,'zzzz').length,0);
});
test('blank search returns finite starter results', () => {
 assert.equal(typeof core.search, 'function');
 assert.equal(core.search(Array.from({length:20},(_,i)=>({title:String(i),text:'',href:'a.html'})),'').length,6);
});
test('enquiry validation requires a real note but email is optional', () => {
 assert.equal(typeof core.validate, 'function');
 assert.ok(core.validate({message:'a'},'tr').message);
 assert.deepEqual(core.validate({message:'A sufficiently detailed project request.'},'en'),{});
});
test('bad email and excessive note are rejected', () => {
 assert.equal(typeof core.validate, 'function');
 assert.ok(core.validate({email:'x@',message:'A sufficiently detailed project request.'},'en').email);
 assert.ok(core.validate({message:'x'.repeat(3001)},'en').message);
});
test('brief includes all five service choices', () => {
 assert.equal(typeof core.buildBrief, 'function');
 for(const topic of ['ai','workflows','training','research','evaluation']) {
  const b=core.buildBrief({topic,message:'A sufficiently detailed project request.'},'tr');
  assert.ok(b.body.includes('A sufficiently detailed'));
  assert.ok(b.url.startsWith('mailto:onour@onourimpram.com?'));
 }
});
test('untrusted topic and CRLF cannot inject mail headers', () => {
 assert.equal(typeof core.buildBrief, 'function');
 const b=core.buildBrief({topic:'x\r\nBcc:attacker@x.com',name:'Test\r\nBcc:xx',message:'A sufficiently detailed project request.'},'en');
 assert.ok(!b.subject.includes('Bcc:'));
 assert.ok(!b.body.includes('\r'));
 assert.ok(!b.url.includes('&bcc='));
});
test('long brief falls back to short mail URL without losing its text', () => {
 assert.equal(typeof core.buildBrief, 'function');
 const b=core.buildBrief({message:'İ'.repeat(2400),topic:'training'},'tr');
 assert.equal(b.tooLong,true);assert.ok(b.url.length<1800);assert.ok(b.body.includes('İ'.repeat(2400)));
});
test('short brief URL preserves Turkish content and fixed recipient', () => {
 assert.equal(typeof core.buildBrief, 'function');
 const b=core.buildBrief({topic:'workflows',message:'Kurumumuz için iş akışlarını birlikte tasarlayalım.'},'tr');
 assert.equal(b.tooLong,false);assert.ok(decodeURIComponent(b.url).includes('iş akışlarını'));
});
