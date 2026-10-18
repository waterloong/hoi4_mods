"""Restore the old mod's democratic-flag fallback for Christian governments."""
import argparse
from pathlib import Path
import shutil
parser=argparse.ArgumentParser()
parser.add_argument('--game',required=True,type=Path)
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]
count=0
for size in ['', 'medium', 'small']:
    source=args.game/'gfx/flags'/size
    dest=root/'gfx/flags'/size
    dest.mkdir(parents=True,exist_ok=True)
    for flag in source.glob('*_democratic.tga'):
        name=flag.name.removesuffix('_democratic.tga')+'_christianity.tga'
        shutil.copyfile(flag,dest/name)
        count+=1
print(f'Created {count} Christian flag fallbacks across three sizes.')
