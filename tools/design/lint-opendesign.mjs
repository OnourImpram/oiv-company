/* Execute the original OpenDesign lintArtifact module on HTML with linked CSS. */
import {readFileSync,existsSync,writeFileSync,mkdirSync} from 'node:fs';
import {resolve,dirname} from 'node:path';
import {pathToFileURL} from 'node:url';
const root=resolve(import.meta.dirname,'../..'),repo=root+'/.design-tools/repos/open-design';
const file=existsSync(repo+'/apps/daemon/dist/lint-artifact.js')?repo+'/apps/daemon/dist/lint-artifact.js':repo+'/apps/daemon/src/lint-artifact.ts';
const {lintArtifact}=await import(pathToFileURL(file));
const reports=[];
for(const relative of ['index.html','tr/index.html']){
 const path=resolve(root,'docs',relative);let html=readFileSync(path,'utf8');
 html=html.replace(/<link\b[^>]*rel="stylesheet"[^>]*>/g,link=>{const src=/href="([^"]+)"/.exec(link)?.[1];if(!src||/^https?:/.test(src))return link;return '<style>'+readFileSync(resolve(dirname(path),src.split('?')[0]),'utf8')+'</style>';});
 reports.push({file:relative,engine:'OpenDesign lintArtifact',revision:'055621c906ad78914d2cd72cdef859e7bd040de5',findings:lintArtifact(html)});
}
mkdirSync(root+'/tool-evidence',{recursive:true});writeFileSync(root+'/tool-evidence/opendesign-lint.json',JSON.stringify(reports,null,2));console.log(JSON.stringify(reports,null,2));
