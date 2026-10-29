import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {resolve,extname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
import {Script} from 'node:vm';
import ts from '../xor-docs-services/node_modules/typescript/lib/typescript.js';
import {getSiteContent} from '../xor-docs-services/content/site.mjs';
import {route} from '../xor-docs-services/content/i18n.mjs';
import {examQuestions} from '../xor-docs-services/content/academy.mjs';

const folder=fileURLToPath(new URL('.',import.meta.url)),repo=resolve(folder,'../xor-docs-services');
const file=resolve(process.argv[2]||resolve(folder,'XOR-CLOUD-HDSD-3-SAN-PHAM.html'));
const bytes=readFileSync(file),html=bytes.toString('utf8');
const language=html.match(/<html\b[^>]*\blang="([^"]+)"/)?.[1];
assert.ok(['vi','en'].includes(language),`Unsupported export language: ${language}`);
const {docs,collections}=getSiteContent(language);
const hash=value=>createHash('sha256').update(value).digest('hex');
const decode=value=>String(value).replace(/&(#x[0-9a-f]+|#\d+|amp|lt|gt|quot|apos|nbsp);/gi,(_,entity)=>entity[0]==='#'?String.fromCodePoint(entity[1].toLowerCase()==='x'?parseInt(entity.slice(2),16):Number(entity.slice(1))):({amp:'&',lt:'<',gt:'>',quot:'"',apos:"'",nbsp:' '}[entity.toLowerCase()]));
const plain=value=>decode(value.replace(/<[^>]*>/g,' ')).replace(/\s+/g,' ').trim();
const attrs=tag=>Object.fromEntries([...tag.matchAll(/\s([^\s=<>]+)="([^"]*)"/g)].map(match=>[match[1],decode(match[2])]));
const tags=(source,name)=>[...source.matchAll(new RegExp(`<${name}\\b[^>]*>`,'g'))].map(match=>({tag:match[0],attrs:attrs(match[0])}));
const anchors=source=>[...source.matchAll(/<a\b[^>]*>[\s\S]*?<\/a>/g)].map(match=>({html:match[0],attrs:attrs(match[0].slice(0,match[0].indexOf('>')+1))}));
const textOnly=html.replace(/<(script|style)\b[^>]*>[\s\S]*?<\/\1>/g,'');
const shell=html.replace(/<(script|style)(\b[^>]*)>[\s\S]*?<\/\1>/g,'<$1$2></$1>');
const allIds=[...shell.matchAll(/\sid="([^"]+)"/g)].map(match=>decode(match[1])),ids=new Set(allIds);
assert.equal(allIds.length,ids.size,'Duplicate export IDs');
assert.match(html,/^<!doctype html>/i);assert.equal(tags(shell,'h1').length,1,`One ${language} document title is required`);
assert.equal(docs.length,253);assert.equal(docs.filter(doc=>doc.status==='guide').length,242);assert.equal(docs.filter(doc=>doc.status==='outline').length,11);
for(const product of ['XOR STACK CLOUD','XOR SECURE CLOUD','XOR SECURE DATA'])assert.ok(plain(textOnly).includes(product),`Missing product: ${product}`);

let localLinks=0,externalLinks=0;
for(const {tag,attrs:a} of [...shell.matchAll(/<[a-z][^>]*>/g)].map(match=>({tag:match[0],attrs:attrs(match[0])}))){
  for(const key of ['aria-labelledby','aria-describedby','aria-controls','headers','for'])if(a[key])for(const id of a[key].split(/\s+/))assert.ok(ids.has(id),`Missing ${key} target: ${id}`);
  assert.ok(!Object.keys(a).some(key=>/^on/i.test(key)),`Inline event handler in export: ${tag.slice(0,100)}`);
  if(a.href){
    if(a.href.startsWith('#')){assert.ok(a.href.length>1,'Empty fragment link');assert.ok(ids.has(decodeURIComponent(a.href.slice(1))),`Missing fragment: ${a.href}`);localLinks++;}
    else{assert.match(a.href,/^(https?:|mailto:|tel:)/,`Nonportable link: ${a.href}`);assert.ok(/^<a\b/.test(tag),`External rendering dependency: ${tag.slice(0,100)}`);externalLinks++;}
  }
  for(const key of ['src','poster','srcset','data','background'])if(a[key])assert.ok(key==='src'&&/^<img\b/.test(tag)&&a[key].startsWith('data:image/'),`Resource outside the HTML: ${key}=${a[key].slice(0,100)}`);
}
assert.ok(!/<(?:iframe|object|embed|base|link)\b/i.test(shell),'External or embedded document dependencies are not allowed');
const styles=[...html.matchAll(/<style\b[^>]*>([\s\S]*?)<\/style>/g)].map(match=>match[1]);
assert.ok(styles.length,'Missing inline styles');
for(const css of styles){assert.ok(!/@import\b/i.test(css),'CSS imports need a network');for(const match of css.matchAll(/url\(\s*['"]?([^)'"\s]+)/g))assert.ok(/^(data:|#)/.test(match[1]),`External CSS resource: ${match[1]}`);}

const scriptBlocks=[...html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/g)].map(match=>({attrs:attrs('<script '+match[1]+'>'),body:match[2]}));
assert.equal(scriptBlocks.filter(script=>script.attrs.id==='export-manifest').length,1);
const manifest=JSON.parse(scriptBlocks.find(script=>script.attrs.id==='export-manifest').body);
assert.ok(typeof manifest.title==='string'&&manifest.title.trim(),'Export manifest title missing');
if(language==='en')assert.ok(!/[À-ỹ]/u.test(manifest.title),'Vietnamese manifest title in English export');
assert.equal(manifest.language,language,'Manifest and HTML languages differ');assert.equal(manifest.guideCount,242);assert.equal(manifest.outlineCount,11);assert.equal(manifest.sectionCount,787);assert.equal(manifest.imageCount,288);assert.equal(manifest.tableCount,137);
assert.equal(manifest.sourceCommit,execFileSync('git',['rev-parse','HEAD'],{cwd:repo,encoding:'utf8'}).trim(),'Export source commit does not match the current registry');
assert.deepEqual(manifest.documents,docs.map(doc=>({id:doc.id,status:doc.status,collection:doc.collection,sectionIds:doc.sections.map(section=>section.id)})),'Export manifest lost document coverage or order');
let executableScripts=0;
for(const script of scriptBlocks){
  assert.ok(!script.attrs.src,'Scripts must be inline');if(script.attrs.type==='application/json')continue;
  assert.ok(!script.attrs.type||script.attrs.type==='text/javascript','Unexpected script type');new Script(script.body,{filename:'offline-export.js'});executableScripts++;
  const ast=ts.createSourceFile('offline-export.js',script.body,ts.ScriptTarget.Latest,true,ts.ScriptKind.JS);
  assert.equal(ast.parseDiagnostics.length,0,'Invalid offline JavaScript');
  function visit(node){
    if(ts.isImportDeclaration(node)||ts.isExportDeclaration(node))assert.fail('Offline script imports another file');
    if(language==='en'&&ts.isStringLiteralLike(node)&&!['đ','Đ'].includes(node.text))assert.ok(!/[À-ỹ]/u.test(node.text),`Vietnamese UI text in English offline script: ${node.text}`);
    if(ts.isCallExpression(node)||ts.isNewExpression(node)){
      const callee=node.expression.getText(ast);
      assert.ok(!/^(?:fetch|import|require|XMLHttpRequest|WebSocket|EventSource|Worker|SharedWorker)$|(?:^|\.)(?:fetch|sendBeacon|importScripts)$/.test(callee),`Offline script network/module call: ${callee}`);
      assert.ok(!/serviceWorker\.register$/.test(callee),'Offline script registers a service worker');
    }
    ts.forEachChild(node,visit);
  }
  visit(ast);
}
assert.ok(executableScripts,'Missing standalone search/zoom script');
for(const question of examQuestions){assert.ok(!html.includes(question.id),`Private exam ID leaked: ${question.id}`);for(const lang of ['vi','en'])assert.ok(!html.includes(question.question[lang]),`Private exam text leaked: ${question.id}`);}

const records=[...html.matchAll(/<article\b[^>]*data-doc-id="[^"]+"[^>]*>[\s\S]*?<\/article>/g)].map(match=>({html:match[0],attrs:attrs(match[0].slice(0,match[0].indexOf('>')+1))}));
assert.equal(records.length,docs.length);assert.equal(new Set(records.map(record=>record.attrs['data-doc-id'])).size,docs.length);
const byId=new Map(records.map(record=>[record.attrs['data-doc-id'],record]));
const routes=new Map(docs.map(doc=>[route(language,doc.id),doc.id]));
const expectedSourceLinks=docs.reduce((total,doc)=>total+doc.sections.reduce((count,section)=>count+anchors(section.html).length,0),0);
const assetBytes=new Map(),seenSourceAssets=new Set();let sectionCount=0,imageCount=0,tableCount=0,sourceLinks=0;
const structure=['p','ol','ul','li','table','thead','tbody','tr','th','td','figure','figcaption','img','code','pre','aside','dl','dt','dd','strong','em','kbd'];
for(const doc of docs){
  const record=byId.get(doc.id);assert.ok(record,`Missing article: ${doc.id}`);assert.equal(record.attrs.id,'doc-'+doc.id);assert.equal(record.attrs['data-status'],doc.status);
  assert.equal(record.attrs['data-product'],doc.collection==='stack'?'stack-cloud':doc.collection==='data'?'secure-data':'secure-cloud');
  assert.equal(plain(record.html.match(/<h4\b[^>]*>([\s\S]*?)<\/h4>/)[1]),doc.title,`Wrong article title: ${doc.id}`);
  assert.equal(plain(record.html.match(/<p class="lead">([\s\S]*?)<\/p>/)[1]),doc.summary,`Wrong article summary: ${doc.id}`);
  if(doc.status==='outline'){
    const notice=record.html.match(/<p class="outline-notice">([\s\S]*?)<\/p>/)?.[1];assert.ok(notice,`Outline notice missing: ${doc.id}`);
    if(language==='vi')assert.match(plain(notice),/Khung quản trị tham khảo.*chưa phải quy trình vận hành hoàn chỉnh/u,`Outline status hidden: ${doc.id}`);
    else{assert.match(plain(notice),/outline|reference/i,`Outline status hidden: ${doc.id}`);assert.match(plain(notice),/\bnot\b.*\b(?:complete|full)\b|\bincomplete\b/i,`English outline implies complete instructions: ${doc.id}`);}
  }
  if(doc.sourceVersion){const version=record.html.match(/<p class="version">([\s\S]*?)<\/p>/)?.[1];assert.ok(version,`Source version missing: ${doc.id}`);assert.deepEqual(plain(version).match(/\d+(?:\.\d+)+/g),[doc.sourceVersion],`Source version changed: ${doc.id}`);}
  const sections=[...record.html.matchAll(/<section\b[^>]*data-source-section="[^"]+"[^>]*>([\s\S]*?)<\/section>/g)].map(match=>({html:match[1],attrs:attrs(match[0].slice(0,match[0].indexOf('>')+1))}));
  assert.deepEqual(sections.map(section=>section.attrs['data-source-section']),doc.sections.map(section=>section.id),`Section coverage/order differs: ${doc.id}`);
  for(const [index,section] of doc.sections.entries()){
    const actual=sections[index],heading=actual.html.match(/^<h5\b[^>]*>([\s\S]*?)<\/h5>/),context=doc.id+'/'+section.id;
    assert.ok(heading,`Section heading missing: ${context}`);assert.equal(actual.attrs.id,doc.id+'--'+section.id);
    assert.equal(plain(heading[1].replace(/<a\b[^>]*>[\s\S]*?<\/a>/g,'')),section.title,`Section title changed: ${context}`);
    const body=actual.html.slice(heading[0].length);sectionCount++;
    assert.equal(plain(body),plain(section.html),`Source text changed, lost or reordered: ${context}`);
    for(const name of structure)assert.equal(tags(body,name).length,tags(section.html,name).length,`Source ${name} structure changed: ${context}`);
    assert.deepEqual(tags(body,'li').map(item=>item.attrs.value||null),tags(section.html,'li').map(item=>item.attrs.value||null),`Numbered instructions or markers changed: ${context}`);
    assert.deepEqual(tags(body,'ol').map(item=>item.attrs.start||null),tags(section.html,'ol').map(item=>item.attrs.start||null),`Ordered-list starts changed: ${context}`);
    const attributes=['data-state','data-crop','data-manual-asset','data-source-document','data-image-index'];
    for(const attribute of attributes){const values=source=>[...source.matchAll(new RegExp(`\\s${attribute}="([^"]*)"`,'g'))].map(match=>decode(match[1]));assert.deepEqual(values(body),values(section.html),`Availability/evidence metadata changed: ${context}/${attribute}`);}
    for(const match of section.html.matchAll(/\sid="([^"]+)"/g))assert.ok(tags(body,'span').some(item=>item.attrs.id===doc.id+'--'+match[1])||body.includes(`id="${doc.id}--${match[1]}"`),`Legacy source anchor lost: ${context}/${match[1]}`);
    const images=tags(body,'img'),sourceImages=tags(section.html,'img');assert.equal(images.length,sourceImages.length);tableCount+=tags(body,'table').length;
    for(const [i,source] of sourceImages.entries()){
      const a=images[i].attrs,src=source.attrs.src;assert.equal(a['data-source-src'],src,`Image placement/source changed: ${context}/${i}`);assert.ok(src.startsWith('/assets/'));
      if(!assetBytes.has(src))assetBytes.set(src,readFileSync(resolve(repo,'.'+src)));
      const expected=assetBytes.get(src),expectedHash=hash(expected);seenSourceAssets.add(src);imageCount++;
      assert.equal(a['data-source-sha256'],expectedHash,`Image source hash changed: ${context}/${src}`);
      const data=a.src.match(/^data:(image\/[\w.+-]+);base64,([A-Za-z0-9+/]+={0,2})$/);assert.ok(data,`Image not fully embedded: ${context}/${src}`);
      assert.equal(data[1],({'.png':'image/png','.webp':'image/webp','.jpg':'image/jpeg','.jpeg':'image/jpeg','.svg':'image/svg+xml'})[extname(src)],`Image media type changed: ${src}`);
      const embedded=Buffer.from(data[2],'base64');assert.equal(embedded.length,expected.length);assert.equal(hash(embedded),expectedHash,`Embedded image bytes changed: ${context}/${src}`);
      for(const key of ['alt','width','height'])assert.equal(a[key],source.attrs[key],`Image ${key} changed: ${context}/${src}`);
      const declarations=value=>Object.fromEntries((value||'').split(';').filter(Boolean).map(pair=>{const colon=pair.indexOf(':');return [pair.slice(0,colon).trim(),pair.slice(colon+1).trim()];}));
      const expectedStyle=declarations(source.attrs.style),actualStyle=declarations(a.style);
      for(const [property,value] of Object.entries(expectedStyle))assert.equal(actualStyle[property],value,`Source image crop style changed: ${context}/${property}`);
      for(const [property,value] of Object.entries(actualStyle)){
        if(property in expectedStyle)continue;
        assert.ok(['--source-width','--source-ratio'].includes(property),`Unexpected image style: ${context}/${property}`);
        if(property==='--source-width')assert.equal(value,source.attrs.width+'px',`Wrong reserved image width: ${context}`);
        if(property==='--source-ratio'){const values=value.split('/').map(Number);assert.equal(values[0]/values[1],Number(source.attrs.width)/Number(source.attrs.height),`Wrong reserved image ratio: ${context}`);}
      }
    }
    const sourceCrops=anchors(section.html).filter(anchor=>anchor.attrs.class?.split(/\s+/).includes('manual-crop'));
    const crops=anchors(body).filter(anchor=>anchor.attrs.class?.split(/\s+/).includes('manual-crop'));
    assert.deepEqual(crops.map(anchor=>anchor.attrs.style),sourceCrops.map(anchor=>anchor.attrs.style),`Stack crop aspect ratios changed: ${context}`);
    const links=anchors(body),sourceAnchors=anchors(section.html);assert.equal(links.length,sourceAnchors.length,`Source links lost: ${context}`);
    for(const [i,source] of sourceAnchors.entries()){
      const href=source.attrs.href,target=links[i].attrs.href;sourceLinks++;
      if(href.startsWith('/assets/')){const image=tags(links[i].html,'img')[0];assert.ok(image,`Zoom link lost its image: ${context}`);assert.equal(target,'#'+image.attrs.id);assert.notEqual(links[i].attrs.target,'_blank','Image zoom opens another heavy HTML tab');}
      else if(href.startsWith('#'))assert.equal(target,'#'+doc.id+'--'+decodeURIComponent(href.slice(1)),`Local source anchor changed: ${context}`);
      else{const url=new URL(href,'https://docs.chudaihiep.cloud');if(url.origin==='https://docs.chudaihiep.cloud'){const targetDoc=routes.get(url.pathname);assert.ok(targetDoc,`Unknown source documentation link: ${href}`);assert.equal(target,url.hash?'#'+targetDoc+'--'+decodeURIComponent(url.hash.slice(1)):'#doc-'+targetDoc,`Cross-document source link changed: ${context}`);}else assert.equal(target,href,`External reference changed: ${context}`);}
    }
  }
}
assert.equal(sectionCount,787);assert.equal(imageCount,288);assert.equal(seenSourceAssets.size,285);assert.equal(tableCount,137);assert.equal(sourceLinks,expectedSourceLinks);
const allImages=tags(shell,'img');assert.equal(allImages.length,imageCount+1,'Only the source images and one brand logo are expected');
const logo=allImages.find(image=>!image.attrs['data-source-src']);assert.ok(logo?.attrs.src.startsWith('data:image/png;base64,'));
const logoBytes=readFileSync(resolve(repo,'assets/x-or-logo.png'));assert.equal(hash(Buffer.from(logo.attrs.src.split(',')[1],'base64')),hash(logoBytes));assetBytes.set('/assets/x-or-logo.png',logoBytes);
assert.deepEqual(manifest.assets.map(asset=>[asset.src,asset.sha256,asset.bytes]).sort((a,b)=>a[0].localeCompare(b[0])),[...assetBytes].map(([src,value])=>[src,hash(value),value.length]).sort((a,b)=>a[0].localeCompare(b[0])),'Embedded asset manifest does not match current source bytes');
assert.ok(ids.has('secure-installation-status'));
const installation=textOnly.match(/<aside\b[^>]*id="secure-installation-status"[^>]*>([\s\S]*?)<\/aside>/)?.[1];assert.ok(installation,'Installation status missing');
if(language==='vi'){assert.match(plain(installation),/hướng dẫn cài đặt XOR SECURE CLOUD hiện chưa có nội dung/u);assert.match(plain(textOnly),/khung quản trị tham khảo theo OpenStack 2026\.2/u);}
else{
  assert.match(plain(installation),/installation guide/i);assert.match(plain(installation),/\b(?:not|no|pending|unavailable)\b/i,'Installation status implies complete instructions');
  assert.match(plain(textOnly),/OpenStack 2026\.2/,'Administrator reference version missing');
  let chrome=plain(textOnly.replace(/<article\b[^>]*data-doc-id="[^"]+"[^>]*>[\s\S]*?<\/article>/g,''));
  // The English native source deliberately quotes Vietnamese UI labels. Only
  // exact source article/group titles may appear outside the checked bodies.
  const titles=[...docs.map(doc=>doc.title),...collections.flatMap(collection=>collection.groups.map(group=>group.title))].sort((a,b)=>b.length-a.length);
  for(const title of titles)chrome=chrome.replaceAll(title,'');
  assert.ok(!/[À-ỹ]/u.test(chrome),'Vietnamese text in English export navigation or cover');
}
console.log(JSON.stringify({result:'PASS',file,language,bytes:bytes.length,articles:records.length,guides:242,outlines:11,sections:sectionCount,tables:tableCount,imagePlacements:imageCount,uniqueEvidenceImages:seenSourceAssets.size,embeddedLogo:1,sourceLinks,localLinks,externalLinks,uniqueIds:ids.size,executableScripts,sourceCommit:manifest.sourceCommit,checked:'exact localized section text, structure, source links, image bytes and dimensions/crops; no external rendering dependencies, network APIs or private assessment content'},null,2));
