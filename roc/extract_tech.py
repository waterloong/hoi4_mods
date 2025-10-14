


import re
from os import path
from os import walk


for root, dirs, files in walk(r'C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\common\technologies'):

    for file in files:
        with open(path.join(root, file)) as f:
            lines = f.readlines()
            for l in lines:
                match = re.match('	([a-z_0-9]+) = \{', l)
                if not match:
                    continue
                tech = match.group(1)
                print(f'''			set_technology = {{
				{tech} = 1
            }}''')


specs = ['air',  'land', 'nuclear', 'naval', 'radar', 'rocket']

for s in specs:
    p = 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Hearts of Iron IV\\common\\special_projects\\projects\\' + s + '_projects.txt'
    with open(p, mode='r') as f:
        lines = f.readlines()
        for l in lines:
            match = re.match('([a-z_]+) = \{', l)
            if not match:
                continue
            tech = match.group(1)
            #print(f'''            complete_special_project = sp:{tech}''')


