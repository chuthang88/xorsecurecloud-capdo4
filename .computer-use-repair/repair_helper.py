from pathlib import Path
import os
import plistlib
import signal
import subprocess
from datetime import datetime

source = Path('/Applications/ChatGPT.app/Contents/Resources/cua_node/lib/node_modules/@oai/sky/Codex Computer Use.app')
base = Path('/Users/thangchu/.codex/computer-use')
target = base / 'Codex Computer Use.app'
tag = datetime.now().strftime('%Y%m%d-%H%M%S')
stage = base / ('repair-stage-' + tag) / target.name
backup = base / 'repair-backups' / tag / target.name

def run(*args):
    return subprocess.run(args, check=True, capture_output=True, text=True)

def version(path):
    with (path / 'Contents/Info.plist').open('rb') as f:
        return plistlib.load(f)['CFBundleVersion']

old_version = version(target)
new_version = version(source)
assert old_version != new_version, 'Helper already matches bundled version'
run('/usr/bin/codesign', '--verify', '--strict', str(source))
stage.parent.mkdir(parents=True, exist_ok=False)
backup.parent.mkdir(parents=True, exist_ok=False)
run('/usr/bin/ditto', str(source), str(stage))
run('/usr/bin/codesign', '--verify', '--strict', str(stage))
target.rename(backup)
try:
    stage.rename(target)
    run('/usr/bin/codesign', '--verify', '--strict', str(target))
except BaseException:
    if target.exists():
        target.rename(stage)
    backup.rename(target)
    raise

expected = str(target / 'Contents/MacOS/SkyComputerUseService')
processes = run('/bin/ps', '-axo', 'pid=,comm=').stdout.splitlines()
stopped = []
for line in processes:
    parts = line.strip().split(None, 1)
    if len(parts) == 2 and parts[1] == expected:
        pid = int(parts[0])
        current = run('/bin/ps', '-p', str(pid), '-o', 'comm=').stdout.strip()
        if current == expected:
            os.kill(pid, signal.SIGTERM)
            stopped.append(pid)
print('Previous version:', old_version)
print('Installed bundled version:', new_version)
print('Backup:', backup)
print('Computer Use service processes signalled for restart:', stopped)
