from PIL import Image as im
from PIL import ImagePalette as pal
import os
import sys
        
def F(n):
    return n * 17


def RowVal(L, i):
    val = 0
    for j in range(16):
        val += L[i+j] * (256 ** j)
    return val

def hexToRGB(t):
    if t == 0:
        return [0,0,0,0]
    r =  t & 0b11111
    g = (t >> 5) & 0b11111
    b = (t >> 10) & 0b11111
    R = G = B = 0
    R = int(r/31 * 255 + .5)
    G = int(g/31 * 255 + .5)
    B = int(b/31 * 255 + .5)
    return [R,G,B,255]

def RGBToHex(r,g,b):
    r = int(r/255 * 31 + .5)
    g = int(g/255 * 31 + .5)
    b = int(b/255 * 31 + .5)
    R = r
    G = g << 5
    B = b << 10
    t = R | G | B
    return t

def makePalette(L):
    colors = []
    for i in range(16):
        colors.append(hexToRGB(L[2*i] + 256 * L[2*i+1]))
    return colors

#i is index of line
#h is height of texture
#w is width of image

#each pixel is represented by a 4 bit color index
#size of texture will then be h*w/2 bytes

#after the image data is a table of colors that the color indices reference
#table holds 16 colors, each 

def extract(i,h,w):
            h = int(h * 2)
            w = int(w / 2)
            offset = hex((i+1)*16)[2:]
            while len(offset) < 8:
                offset = "0"+offset
            offset = "0x" + offset
            cOffset = (i+1)*16 + int(h*w/2)
            Cbytes = num[cOffset:cOffset+32]
            colors = makePalette(Cbytes)
            FILE = open("buffer","w+b")
            for y in range(h):
                for x in range(int(w)):
                    try:
                        FILE.write(bytes(colors[num[(i+1)*16 + (w*y)+(x)]&15]))
                    except:
                        #print(len(num),(i+1)*16 + (w*y)+(x),x,y)
                        pass
                    try:
                        FILE.write(bytes(colors[(num[(i+1)*16 + (w*y)+(x)]>>4)&15]))
                    except:
                        #print(len(num),(i+1)*16 + (w*y)+(x),x,y,w,h)
                        pass
            FILE.seek(0)
            frame = im.frombytes("RGBA", (w*2,int(h/2)), FILE.read(w*h*4))
            try:
                frame.save(save_dir+offset+name_base+".png")
            except OSError:
                os.makedirs(save_dir)
                frame.save(save_dir+offset+name_base+".png")
            FILE.close()    


xy256_256 = open("COORDS256_256.txt","r")
XY256_256 = [xy256_256.readline().replace(" ","").replace("\n","").replace("(","").replace(")","").split(",") for i in range(256*256)]
XY256_256 = [(int(i[0]),int(i[1])) for i in XY256_256]
xy256_256.close()

def extract_interlace(i,h,w):
    XY = []
    for c in XY256_256:
        if (c[0] < w) and (c[1] < h):
            XY.append(c)
    BUFFERARRAY = [[bytes([255,0,0,255]) for x in range(w)] for y in range(h)]
    offset = hex((i+1)*16)[2:]
    while len(offset) < 8:
        offset = "0"+offset
    offset = "0x" + offset
    cOffset = (i+1)*16 + int(h*w/2)
    Cbytes = num[cOffset:cOffset+32]
    colors = makePalette(Cbytes)
    for t in range(int(h*w/2)):
        t1 = t*2
        t2 = t*2+1
        x1 = XY[t1][0]
        y1 = XY[t1][1]
        x2 = XY[t2][0]
        y2 = XY[t2][1]
        try:
            BUFFERARRAY[y2][x2] = bytes(colors[num[(i+1)*16 + t]&15])
            BUFFERARRAY[y1][x1] = bytes(colors[num[(i+1)*16 + t]>>4])
        except:
            pass

    FILE = open("buffer","w+b")
    
    for t in range(h*w):
            FILE.write(BUFFERARRAY[int(t/w)][t%w])
    FILE.seek(0)
    frame = im.frombytes("RGBA", (w,h), FILE.read(h*w*4))
    try:
        frame.save(save_dir+offset+name_base+".png")
    except OSError:
        os.makedirs(save_dir)
        frame.save(save_dir+offset+name_base+".png")
    FILE.close()


#source = sys.argv[1]
#dest = sys.argv[2]

source = "..\\isoFiles\\"
dest = "..\\images\\"


if __name__ == "__main__":
    for D in os.walk(source):
        for file in D[2]:
            path = D[0]+"\\"+file
            save_dir = dest + "\\" + path[path.index("isoFiles")+8:path.rfind(".")]+"\\"
            name_base = ""
            print(path)
            FILE = open(path, "rb")
            sz = os.stat(path).st_size
            num = list(FILE.read())
            stretch = 1
            FILE.close()
            for i in range(int(len(num)/16)):
                rv = RowVal(num,i*16)
                try:
                    if  (rv == int("00020008004000400000000800000200",16)):
                        extract(i, 64,64)#64x64
                        pass
                    elif(rv == int("00020008001000100000000800000020",16)):
                        extract(i,  16, 16)#16x16
                        pass
                    elif(rv == int("00020008002000200000000800000080",16)):
                        extract(i,  32,32)#32x32
                        pass
                    elif(rv == int("00020008008001000000000800001000",16)):
                        extract_interlace(i,128,256)
                        pass
                    elif(rv == int("00020008004000200000000800000100",16)):
                        extract(i,64 ,32)#64x32
                        pass
                    elif(rv == int("00020008008000400000000800000400",16)):
                        extract_interlace(i,128,64)
                        pass
                    elif(rv == int("00020008008000800000000800000800",16)):
                        extract_interlace(i,128,128)
                        pass
                    elif(rv == int("00020008008000200000000800000200",16)):
                        extract(i, 128,32)#128x32
                        pass
                    elif(rv == int('00020008002000100000000800000040',16)):
                        extract(i, 32, 16)#16x32
                        pass
                    elif(rv == int('00020008001000200000000800000040',16)):
                        extract(i, 16, 32)#32x16
                        pass
                    elif(rv == int('00020008002000400000000800000100',16)):
                        extract(i, 32, 64)#64x32
                        pass
                    elif(rv == int('00020008002000800000000800000200',16)):
                        extract(i, 32, 128)#128x32
                        pass
                    elif(rv == int('00020008004000800000000800000400',16)):
                        extract_interlace(i, 64, 128)
                        pass
                    elif(rv == int('00020008000800080000000800000008',16)):
                        extract(i, 8, 8)#8x8
                        pass
                    elif(rv == int('00020008004000100000000800000080',16)):
                        extract(i,64,16)#16x64
                        pass
                    elif(rv == int('00020008004001000000000800000800',16)):
                        extract(i,64,256)#256x64
                        pass
                    elif(rv == int('00020008010000800000000800001000',16)):
                        extract_interlace(i,256,128)
                        pass
                    elif(rv == int('00020008010001000000000800002000',16)):
                        extract_interlace(i,256,256)
                        pass
                    elif(rv == int('00020008010000400000000800000800',16)):
                        extract(i,256,64)#64x256
                        pass
                    
                except OSError:
                    print("Issue with ", path," at ", hex(i*16),", moving on.")


