import re
from os import path
from os import walk
import shutil


for root, dirs, files in walk(r'C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\gfx\flags'):

    for file in files:
        if 'democratic' not in file:
            continue
        new_file = file.replace('democratic', 'chritianity')
        shutil.copy2(path.join(root, file), path.join(r'C:\Users\SMZYE\OneDrive\Documents\Paradox Interactive\Hearts of Iron IV\mod\church\gfx\flags', new_file))

        # print(path.join(root, file), path.join(r'C:\Users\SMZYE\OneDrive\Documents\Paradox Interactive\Hearts of Iron IV\mod\church\gfx\flags', new_file))

for root, dirs, files in walk(r'C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\gfx\flags\medium'):

    for file in files:
        if 'democratic' not in file:
            continue
        new_file = file.replace('democratic', 'chritianity')
        shutil.copy2(path.join(root, file), path.join(r'C:\Users\SMZYE\OneDrive\Documents\Paradox Interactive\Hearts of Iron IV\mod\church\gfx\flags\medium', new_file))

        print(path.join(root, file), path.join(r'C:\Users\SMZYE\OneDrive\Documents\Paradox Interactive\Hearts of Iron IV\mod\church\gfx\flags\medium', new_file))

