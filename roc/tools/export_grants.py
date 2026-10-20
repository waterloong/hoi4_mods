"""Print grants from real installed definitions, avoiding retired/nested IDs."""
import argparse
from pathlib import Path
from audit_roc import definitions

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--game',required=True,type=Path)
    parser.add_argument('--kind',choices=['technologies','projects'],default='technologies')
    args=parser.parse_args()
    if args.kind=='technologies':
        names=definitions(args.game/'common/technologies','technologies')
        print('set_technology = {')
        for name in sorted(names):print(f'    {name} = 1')
        print('}')
    else:
        for name in sorted(definitions(args.game/'common/special_projects/projects')):
            print(f'complete_special_project = sp:{name}')

if __name__=='__main__':main()
