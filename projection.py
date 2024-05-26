from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


# 点の座標を取得
vertex = {}
f = open('vertex.txt', 'r', encoding='UTF-8')
line = f.readline()
label = []
while line:
    if (line.rstrip("\n").split(" ")[0] in label):
        print("名前 "+line.rstrip("\n").split(" ")[0]+" の重複")
    vertex[line.rstrip("\n").split(" ")[0]]  = np.array([float(s) for s in line.rstrip("\n").split(" ")[1].split(",")])
    label.append(line.rstrip("\n").split(" ")[0])
    line = f.readline()
f.close()
print(vertex)




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

id = 0
text = ""
number = 0
f = open('projection.csv', 'r', encoding='UTF-8')
line = f.readline()
while line:
    if (line[0]=="#"):
        line = f.readline()
        continue
    if (line.rstrip("\n")==""):
        file = open('image'+str(id)+'.ply', 'w')
        file.writelines(["""ply
format ascii 1.0
element vertex """+str(number)+"""
property double x
property double z
property double y
property uchar red
property uchar green
property uchar blue
end_header
""",text])
        file.close()
        id += 1
        text = ""
        number = 0
        line = f.readline()
        continue

    data = line.rstrip("\n").split(",")
    print(data)
    X = int(data[10])
    Y = int(data[11])

    im = np.array(Image.open('image/'+data[9]).resize((X,Y)))

    size = X*Y
    number += size

    A = np.array([int(data[4]),int(data[3])])
    B = np.array([int(data[6]),int(data[5])])
    C = np.array([int(data[8]),int(data[7])])

    a = vertex[data[0]]
    b = vertex[data[1]]
    c = vertex[data[2]]

    AB = B-A
    AC = C-A
    ab = b-a
    ac = c-a
    M = np.vstack([AB, AC]).T

    for x in range(im.shape[0]):
        for y in range(im.shape[1]):
            if (include(np.array([x,y]), A,B,C)):
                P = np.array([x,y])
                res = np.linalg.solve(M, (P-A).reshape(2, 1))
                pos = ab*res[0]+ac*res[1]+a
                text += str(pos[0])+" " + str(pos[1])+" " + str(pos[2])+" " + str(im[x,y,0])+" " + str(im[x,y,1])+" " + str(im[x,y,2]) + "\n"
    line = f.readline()
f.close()



file = open('image'+str(id)+'.ply', 'w')
file.writelines(["""ply
format ascii 1.0
element vertex """+str(number)+"""
property double x
property double z
property double y
property uchar red
property uchar green
property uchar blue
end_header
""",text])
file.close()

# plt.imshow(im)
# plt.show()