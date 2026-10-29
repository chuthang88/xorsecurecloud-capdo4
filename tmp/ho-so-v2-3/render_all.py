import json, subprocess, sys, shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
root=Path(__file__).resolve().parent
paths=json.loads((root/'doc_manifest.json').read_text())
renderer='/Users/thangchu/.codex/plugins/cache/openai-primary-runtime/documents/26.1011.11113/skills/documents/render_docx.py'
def run(item):
    i,p=item
    out=root/'render'/f'{i:02d}_{Path(p).stem}'
    if out.exists():shutil.rmtree(out)
    proc=subprocess.run([sys.executable,renderer,p,'--output_dir',str(out),'--emit_pdf'],capture_output=True,text=True)
    (root/f'render-{i:02d}.log').write_text(proc.stdout+'\n'+proc.stderr)
    return {'index':i,'file':Path(p).name,'code':proc.returncode,'pages':len(list(out.glob('page-*.png'))),'dir':str(out),'error':proc.stderr[-500:] if proc.returncode else ''}
with ThreadPoolExecutor(max_workers=3) as pool:
    chosen=set(map(int,sys.argv[1:])) if len(sys.argv)>1 else set(range(len(paths)))
    old=json.loads((root/'render-results.json').read_text()) if (root/'render-results.json').exists() else []
    results=[r for r in old if r['index'] not in chosen]
    for f in as_completed([pool.submit(run,(i,p)) for i,p in enumerate(paths) if i in chosen]):
        r=f.result();results.append(r);print(json.dumps(r,ensure_ascii=False),flush=True)
(root/'render-results.json').write_text(json.dumps(sorted(results,key=lambda x:x['index']),ensure_ascii=False,indent=2))
if any(x['code'] for x in results):raise SystemExit(1)
