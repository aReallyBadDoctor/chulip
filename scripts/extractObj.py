from PIL import Image as im
import os
import sys

def intToFloat(n):
    mant = 1
    sign = (n & (2**31)) > 0
    if(sign):
        sign = -1
    else:
        sign = 1
    exp = ((n & (2**31 - 2**23))>>23) - 127
    if(exp == -128):
        exp = -126
        mant = 0
    mant += (n&8388607)/(2**23)
    product =  (2**exp) * mant * (sign)
    return product

def valid(i):
    if num[i*16] != 0:
        return False
    A = num[i*16+8]
    B = num[i*16+9]
    C = A + B * 256
    vVals = [int("181B",16),int("381B",16),int("280B",16)]
    if C in vVals:
        return True
    return False

#source = sys.argv[1]
#dest = sys.argv[2]

source = "../isoFiles/"
dest = "../models/"

if __name__ == "__main__":
    for D in os.walk(source):
        for file in D[2]:
            path = D[0]+"\\"+file
            save_dir = dest + path[path.index("isoFiles")+8:path.rfind(".")]+"\\"
            print(path)
            sz = os.stat(path).st_size
            FILE = open(path, "rb")
            num = list(FILE.read())
            FILE.close()

            for i in range(int(len(num)/16)):
                if(valid(i)):
                    offset = hex((i+1)*16)[2:]
                    while len(offset) < 8:
                        offset = "0"+offset
                    offset = "0x" + offset
                    try:
                        FILE = open(save_dir+offset+".obj", "w+")
                    except FileNotFoundError:
                        os.makedirs(save_dir)
                        FILE = open(save_dir+offset+".obj", "w+")
                    numV = num[i*16 + 13] * 256 + num[i*16 + 12]
                    #print(hex((i+1)*16), numV)
                    span = ((i+1),(i+numV+1))
                    for j in range(span[0],span[1]):
                        S = "v "
                        vals = []
                        for t in range(3):
                            I = 0
                            I += num[j*16 + t*4] * (16**0)
                            I += num[j*16 + 1 + t*4] * (16**2)
                            I += num[j*16 + 2 + t*4] * (16**4)
                            I += num[j*16 + 3 + t*4] * (16**6)
                            vals.append("{:f} ".format(intToFloat(I)))
                        S += vals[0]
                        S += vals[2]
                        S += vals[1]
                        FILE.write(S)
                        FILE.write("\n")
                    span = (span[1],(span[1]+numV))
                    for j in range(span[0],span[1]):
                        S = "vn "
                        vals = []
                        for t in range(3):
                            I = 0
                            I += num[j*16 + t*4] * (16**0)
                            I += num[j*16 + 1 + t*4] * (16**2)
                            I += num[j*16 + 2 + t*4] * (16**4)
                            I += num[j*16 + 3 + t*4] * (16**6)
                            vals.append("{:f} ".format(intToFloat(I)))
                        S += vals[0]
                        S += vals[2]
                        S += vals[1]
                        FILE.write(S)
                        FILE.write("\n")
                    span = (span[1], (span[1]+numV))
                    for j in range(span[0],span[1]):
                        S = "vt "
                        vals = []
                        I = 0
                        I += num[j*16] * (16**0)
                        I += num[j*16 + 1] * (16**2)
                        I += num[j*16 + 2] * (16**4)
                        I += num[j*16 + 3] * (16**6)
                        vals.append("{:f} ".format(intToFloat(I)))
                        I = 0
                        I += num[j*16 + 4] * (16**0)
                        I += num[j*16 + 5] * (16**2)
                        I += num[j*16 + 6] * (16**4)
                        I += num[j*16 + 7] * (16**6)
                        vals.append("{:f} ".format(1 - intToFloat(I)))
                        S += vals[0]
                        S += vals[1]
                        FILE.write(S)
                        FILE.write("\n")
                    V = 1
                    while(V<=numV):
                        S = "f "
                        S += "{}/{}/{} ".format(V,V,V)
                        V += 1
                        S += "{}/{}/{} ".format(V,V,V)
                        V += 1
                        S += "{}/{}/{}".format(V,V,V)
                        V += 1
                        FILE.write(S)
                        FILE.write("\n")
                    FILE.close()


