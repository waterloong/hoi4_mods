"""Generate country-specific Christian party names from vanilla country keys."""
import argparse
from pathlib import Path
import re
parser=argparse.ArgumentParser()
parser.add_argument('--game',required=True,type=Path)
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]
text=(args.game/'localisation/english/countries_l_english.yml').read_text(encoding='utf-8-sig')
country_names=set(re.findall(r'^\s*([A-Z][A-Z0-9]{2}):',text,re.M))
tags=set()
for path in (args.game/'common/country_tags').glob('*.txt'):
    tags.update(re.findall(r'^\s*([A-Z][A-Z0-9]{2})\s*=',path.read_text(encoding='utf-8-sig'),re.M))
lines=['l_english:',
       ' christianity_party:0 "Church of [ROOT.GetNonIdeologyName]"',
       ' christianity_party_long:0 "Church of [ROOT.GetNonIdeologyName]"']
for tag in sorted(tags & country_names):
    country='England' if tag=='ENG' else f'${tag}$'
    for suffix in ['party','party_long']:
        lines.append(f' {tag}_christianity_{suffix}:0 "Church of {country}"')
(root/'localisation/english/church_parties_l_english.yml').write_text('\n'.join(lines)+'\n',encoding='utf-8-sig')
assert ' CHI_christianity_party:0 "Church of $CHI$"' in lines
assert ' ENG_christianity_party:0 "Church of England"' in lines
print(f'Generated party names for {len(tags & country_names)} country tags, plus dynamic fallbacks.')
