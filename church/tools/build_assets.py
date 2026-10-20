"""Build Church graphics using Pillow. Run with --game pointing to HOI4.

Binary layout reference: https://github.com/ross-g/io_pdx_mesh (ross-g).
This is a small independent static-mesh writer, not a Blender dependency.
"""
import argparse
import json
import math
from pathlib import Path
import struct
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--game', required=True, type=Path)
args = parser.parse_args()
game = args.game
model = ROOT / 'gfx/models/buildings/church'
icons = ROOT / 'gfx/interface/buildings'
for folder in [model, icons, ROOT/'map', ROOT/'art']:
    folder.mkdir(parents=True, exist_ok=True)

# Preserve every vanilla frame and append one new construction button.
strip = Image.open(game/'gfx/interface/buildings/building_icon_strip.dds').convert('RGBA')
assert strip.size == (31*46, 46), 'Recheck the icon strip after a game update.'
source = Image.open(ROOT/'art/church_source.png').convert('RGBA')
thumb = source.crop(source.getbbox())
thumb.thumbnail((40, 40), Image.Resampling.LANCZOS)
button = strip.crop((0, 0, 46, 46))
# Vanilla buttons include their own background; use a neutral matching panel.
button = Image.new('RGBA', (46, 46), (43, 46, 43, 255))
d = ImageDraw.Draw(button)
d.rectangle((0, 0, 45, 45), outline=(104, 108, 99), width=1)
button.alpha_composite(thumb, ((46-thumb.width)//2, (46-thumb.height)//2))
user_icon = ROOT/'art/church_user_icon.png'
borderless_icon = ROOT/'art/church_user_icon_borderless.png'
if borderless_icon.exists():
    user_icon = borderless_icon
large_cross_icon = ROOT/'art/church_user_icon_large_cross.png'
if large_cross_icon.exists():
    user_icon = large_cross_icon
extra_large_cross_icon = ROOT/'art/church_user_icon_extra_large_cross.png'
if extra_large_cross_icon.exists():
    user_icon = extra_large_cross_icon
if user_icon.exists():
    # User artwork is already a complete button; preserve its composition.
    button = Image.open(user_icon).convert('RGBA').resize((46,46), Image.Resampling.LANCZOS)
button.save(ROOT/'art/church_icon_preview.png')
atlas = Image.new('RGBA', (32*46, 46))
atlas.paste(strip, (0, 0))
atlas.paste(button, (31*46, 0))
atlas.save(icons/'church_building_icon_strip.dds')
small = source.crop(source.getbbox())
small.thumbnail((28, 28), Image.Resampling.LANCZOS)
small_icon = Image.new('RGBA', (32, 32))
small_icon.alpha_composite(small, ((32-small.width)//2, (32-small.height)//2))
if user_icon.exists():
    small_icon = Image.open(user_icon).convert('RGBA').resize((32,32), Image.Resampling.LANCZOS)
small_icon.save(icons/'church_small.dds')
assert Image.open(icons/'church_building_icon_strip.dds').size == (1472,46)
assert atlas.crop((0,0,1426,46)).tobytes() == strip.tobytes()

# Palette atlas: stone, slate, door timber, dark window, limestone trim, brass.
colors = [(173,160,135),(65,72,80),(81,56,37),(30,42,48),(208,195,162),(177,143,75)]
texture = Image.new('RGBA', (192,32))
draw = ImageDraw.Draw(texture)
for i,c in enumerate(colors):
    draw.rectangle((i*32,0,i*32+31,31), fill=(*c,255))
texture.save(model/'church_diffuse.dds')
# HOI4 uses tangent normals with X in alpha and Y in green.
Image.new('RGBA',(4,4),(128,128,255,128)).save(model/'church_normal.dds')
Image.new('RGBA',(4,4),(45,45,45,255)).save(model/'church_specular.dds')

positions, normals, tangents, uvs, triangles = [], [], [], [], []
faces = []
def face(points, color):
    # Each polygon gets independent vertices for sharp architectural edges.
    a,b,c = points[:3]
    u = [b[i]-a[i] for i in range(3)]
    v = [c[i]-a[i] for i in range(3)]
    n = [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
    length = math.sqrt(sum(x*x for x in n))
    n = [x/length for x in n]
    t = [x/math.sqrt(sum(y*y for y in u)) for x in u]
    start = len(positions)//3
    for p in points:
        positions.extend(map(float,p)); normals.extend(n); tangents.extend(t+[1.0])
        uvs.extend([(color+.5)/6,.5])
    for i in range(1,len(points)-1):
        triangles.extend([start,start+i,start+i+1])
    faces.append((points,color))

def box(x0,y0,z0,x1,y1,z1,col):
    p=[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),
       (x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
    for ids in [(0,3,2,1),(4,5,6,7),(0,4,7,3),(1,2,6,5),(3,7,6,2),(0,1,5,4)]:
        face([p[i] for i in ids],col)

def roof(x0,x1,z0,z1,eave,ridge,col=1):
    mid=(x0+x1)/2
    face([(x0,eave,z0),(mid,ridge,z0),(x1,eave,z0)],0)
    face([(x1,eave,z1),(mid,ridge,z1),(x0,eave,z1)],0)
    face([(x0,eave,z0),(x0,eave,z1),(mid,ridge,z1),(mid,ridge,z0)],col)
    face([(mid,ridge,z0),(mid,ridge,z1),(x1,eave,z1),(x1,eave,z0)],col)

# Nave, apse, bell tower, buttresses, entry steps, windows and cross.
box(-2.2,0,-3.8,2.2,.35,4.5,4)
box(-1.8,.35,-3.3,1.8,3.3,4,0)
roof(-2.05,2.05,-3.55,4.25,3.3,5)
box(-1.3,.35,4,1.3,2.8,5.2,0)
roof(-1.5,1.5,4,5.4,2.8,4)
box(-1.15,.35,-4.7,1.15,6.8,-2.6,0)
box(-1.3,4.9,-4.85,1.3,5.15,-2.45,4)
box(-1.3,6.6,-4.85,1.3,6.9,-2.45,4)
roof(-1.4,1.4,-4.95,-2.35,6.9,8.3)
box(-.09,8,-3.75,.09,9.3,-3.57,5)
box(-.5,8.85,-3.75,.5,9.03,-3.57,5)
box(-.55,.35,-4.74,.55,2.05,-4.7,2)
box(-.72,.35,-4.9,.72,.55,-4.72,4)
box(-.9,0,-5.15,.9,.27,-4.7,4)
box(-.48,5.35,-4.74,.48,6.35,-4.7,3)
box(1.15,5.35,-4.2,1.19,6.35,-3.2,3)
for z in [-1.4,.7,2.8]:
    for side in [-1,1]:
        x=side*1.8
        box(min(x,x+side*.04),1.6,z-.3,max(x,x+side*.04),2.9,z+.3,3)
        x=side*1.9
        box(x-.16,.35,z+.55,x+.16,2.8,z+.85,4)

def node(depth,name):
    return b'['*depth+name.encode('ascii')+b'\0'
def prop(name,values):
    label=name.encode('ascii')
    if isinstance(values,str):
        raw=values.encode('ascii')+b'\0'
        data=b's'+struct.pack('<ii',1,len(raw))+raw
    else:
        kind='i' if isinstance(values[0],int) else 'f'
        data=kind.encode()+struct.pack('<i',len(values))+struct.pack('<'+kind*len(values),*values)
    return b'!'+bytes([len(label)])+label+data

lo=[min(positions[i::3]) for i in range(3)]
hi=[max(positions[i::3]) for i in range(3)]
data=b'@@b@'+prop('pdxasset',[1,0])+node(1,'object')+node(2,'churchShape')+prop('lod',[0])+node(3,'mesh')
for name,values in [('p',positions),('n',normals),('ta',tangents),('u0',uvs),('tri',triangles),('boundingsphere',[0.,4.5,0.,7.])]:
    data+=prop(name,values)
data+=node(4,'aabb')+prop('min',lo)+prop('max',hi)+node(4,'material')
for name,value in [('shader','PdxMeshAdvancedSnow'),('diff','church_diffuse.dds'),('n','church_normal.dds'),('spec','church_specular.dds')]:
    data+=prop(name,value)
data+=node(1,'locator')
(model/'church.mesh').write_bytes(data)
# Editable source mesh for other 3D tools.
obj=[]
for i in range(0,len(positions),3):
    obj.append('v '+' '.join(str(x) for x in positions[i:i+3]))
for i in range(0,len(triangles),3):
    obj.append('f '+' '.join(str(x+1) for x in triangles[i:i+3]))
(ROOT/'art/church.obj').write_text('\n'.join(obj)+'\n')

# Use vanilla fort anchors: existing province-safe, terrain-height-adjusted positions.
# Keep every vanilla entry because map/buildings.txt is replaced as a whole.
base=(game/'map/buildings.txt').read_text(encoding='utf-8-sig')
anchors=[]
for line in base.splitlines():
    fields=line.split(';')
    if len(fields)>=7 and fields[1]=='bunker':
        fields[1]='church'
        anchors.append(';'.join(fields))
assert len(anchors)>1000
(ROOT/'map/buildings.txt').write_bytes((base.rstrip()+'\n'+'\n'.join(anchors)).encode('utf-8'))
(ROOT/'art/church_geometry.json').write_text(json.dumps({'faces':faces,'colors':colors}))
print(f'Built frame 32, {len(triangles)//3} triangles, {len(anchors)} church map anchors.')
