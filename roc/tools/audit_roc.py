"""Check ROC identifiers against an installed HOI4. Does not launch the game."""
import argparse
from pathlib import Path
import re

def parse(path):
    text=Path(path).read_text(encoding='utf-8-sig',errors='replace')
    tokens=re.findall(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]|[=<>!]+|[^\s{}=<>!]+',text)
    tokens=[x for x in tokens if not x.startswith('#')]
    i=0
    def block(nested=False):
        nonlocal i
        result=[]
        while i<len(tokens):
            k=tokens[i];i+=1
            if k=='}':
                assert nested, f'Unexpected closing brace: {path}'
                return result
            if i<len(tokens) and tokens[i] in ['=','>','<','>=','<=','!=','==','?=']:
                op=tokens[i];i+=1
                assert i<len(tokens),path
                v=tokens[i];i+=1
                if v=='{':v=block(True)
                result.append((k,op,v))
            else:result.append(k)
        assert not nested,f'Unclosed block: {path}'
        return result
    return block()

def children(tree,key):
    return [x[2] for x in tree if isinstance(x,tuple) and x[0]==key]
def walk(tree):
    for x in tree:
        if isinstance(x,tuple):
            yield x
            if isinstance(x[2],list):yield from walk(x[2])
def definitions(folder,container=None):
    result=set()
    for p in Path(folder).glob('*.txt'):
        tree=parse(p)
        groups=children(tree,container) if container else [tree]
        for group in groups:
            if isinstance(group,list):
                result.update(x[0] for x in group if isinstance(x,tuple) and isinstance(x[2],list))
    return result

def dump(tree,depth=0):
    lines=[]
    for item in tree:
        if isinstance(item,str):lines.append('    '*depth+item)
        else:
            k,op,v=item
            if isinstance(v,list):
                lines.append('    '*depth+f'{k} {op} {{')
                lines.extend(dump(v,depth+1))
                lines.append('    '*depth+'}')
            else:lines.append('    '*depth+f'{k} {op} {v}')
    return lines

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--game',required=True,type=Path)
    args=parser.parse_args()
    game=args.game;root=Path(__file__).resolve().parents[1]
    tech=definitions(game/'common/technologies','technologies')
    projects=definitions(game/'common/special_projects/projects')
    units=definitions(game/'common/unit_leader','leader_traits')
    leaders=definitions(game/'common/country_leader','leader_traits')
    leaders |= definitions(root/'common/country_leader','leader_traits')
    equipment=definitions(game/'common/units/equipment','equipments')
    scientists=definitions(game/'common/scientist_traits','scientist_traits')
    errors=[]
    for p in list((root/'common').rglob('*.txt'))+list((root/'history').rglob('*.txt')):
        tree=parse(p)
        for k,op,v in walk(tree):
            if k=='set_technology' and isinstance(v,list):
                for x in v:
                    if isinstance(x,tuple) and x[0] not in tech and x[0] not in ['popup','show_effect']:
                        errors.append(f'{p.relative_to(root)}: unknown technology {x[0]}')
            if k=='complete_special_project':
                names=[v] if isinstance(v,str) else children(v,'project')
                for name in names:
                    if name.removeprefix('sp:') not in projects:errors.append(f'Unknown project {name}')
            if k=='add_equipment_to_stockpile':
                for name in children(v,'type'):
                    if name not in equipment:errors.append(f'Unknown equipment {name}')
        if p.parent.name=='characters':
            for group in children(tree,'characters'):
                for character in group:
                    if not isinstance(character,tuple):continue
                    for role,_,roledata in [x for x in character[2] if isinstance(x,tuple) and isinstance(x[2],list)]:
                        valid=leaders if role=='advisor' else units
                        if role not in ['advisor','field_marshal','corps_commander','navy_leader']:continue
                        for traitset in children(roledata,'traits'):
                            for trait in traitset:
                                if isinstance(trait,str) and trait not in valid:errors.append(f'{role}: unknown trait {trait}')
    for error in sorted(set(errors)):print(error)
    print(f'{len(set(errors))} identifier issues; {len(tech)} vanilla technologies indexed.')
    return bool(errors)

if __name__=='__main__':raise SystemExit(main())
