"""Write or extend English localisation with HOI4's required UTF-8 BOM."""
from pathlib import Path
import sys
path=Path(sys.argv[1])
text=sys.stdin.read()
if path.exists():
    text=path.read_text(encoding='utf-8-sig').rstrip()+'\n'+text
else:
    text='l_english:\n'+text
path.parent.mkdir(parents=True,exist_ok=True)
path.write_text(text.rstrip()+'\n',encoding='utf-8-sig')
