"""Simple orthographic preview of the source geometry (not an in-game render)."""
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
root=Path(__file__).resolve().parents[1]
geo=json.loads((root/'art/church_geometry.json').read_text())
image=Image.new('RGBA',(640,640),(32,36,39,255))
draw=ImageDraw.Draw(image)
pixels=np.array(image)
depth=np.full((640,640),-np.inf)
def project(p):
    x,y,z=p
    return (320+32*(.82*x+.57*z),420+32*(-.28*z+.4*x-.9*y))
faces=sorted(geo['faces'],key=lambda f: sum(p[0]*.513-p[2]*.738+p[1]*.458 for p in f[0])/len(f[0]))
for points,index in faces:
    a,b,c=points[:3]
    u=[b[i]-a[i] for i in range(3)];v=[c[i]-a[i] for i in range(3)]
    n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
    length=math.sqrt(sum(t*t for t in n));n=[t/length for t in n]
    # Only front-facing surfaces for this camera.
    if n[0]*.57+n[1]*.55-n[2]*.82<=0: continue
    shade=.7+.3*max(0,sum(n[i]*[.3,.8,-.5][i] for i in range(3)))
    color=tuple(min(255,int(t*shade)) for t in geo['colors'][index])+(255,)
    for k in range(1,len(points)-1):
        tri=[points[0],points[k],points[k+1]]
        xy=np.array([project(p) for p in tri])
        z=np.array([p[0]*.513-p[2]*.738+p[1]*.458 for p in tri])
        x0,y0=np.maximum(0,np.floor(xy.min(axis=0)).astype(int))
        x1,y1=np.minimum(639,np.ceil(xy.max(axis=0)).astype(int))
        if x0>x1 or y0>y1: continue
        xx,yy=np.meshgrid(np.arange(x0,x1+1)+.5,np.arange(y0,y1+1)+.5)
        a,b,c=xy
        denom=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
        if abs(denom)<1e-8: continue
        w0=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/denom
        w1=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/denom
        w2=1-w0-w1
        zz=w0*z[0]+w1*z[1]+w2*z[2]
        target=depth[y0:y1+1,x0:x1+1]
        mask=(w0>=0)&(w1>=0)&(w2>=0)&(zz>target)
        target[mask]=zz[mask]
        pixels[y0:y1+1,x0:x1+1][mask]=color
image=Image.fromarray(pixels)
image.save(root/'art/church_model_preview.png')
