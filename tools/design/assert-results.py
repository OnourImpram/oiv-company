"""Make detector findings distinct from failed installations and functional tests."""
import csv,sys
from pathlib import Path
rows=list(csv.DictReader(open('tool-evidence/commands.tsv'),delimiter='\t'))
allowed={'impeccable-detect':{'0','2'},'impeccable-rendered':{'0','2'}}
bad=[r for r in rows if r['exit_code'] not in allowed.get(r['step'],{'0'})]
assert rows,'No commands executed'
if bad: print('FAILED',bad);sys.exit(1)
assert Path('review-generated/manifest.json').is_file(),'Verified review source missing'
print('Installation and functional checks succeeded. Detector findings remain visible for review.')
