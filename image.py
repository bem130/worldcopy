from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def include(p,a,b,c):
    ab = b-a
    bp = p-b
    bc = c-b
    cp = p-c
    ca = a-c
    ap = p-a
    c1 = ab[0]*bp[1] - ab[1]*bp[0]
    c2 = bc[0]*cp[1] - bc[1]*cp[0]
    c3 = ca[0]*ap[1] - ca[1]*ap[0]
    return (c1 >= 0 and c2 >= 0 and c3 >= 0)or(c1 <= 0 and c2 <= 0 and c3 <= 0)


X = 400
Y = 800

im = np.array(Image.open('image/1.jpg').resize((X,Y)))


plt.imshow(im)
plt.show()