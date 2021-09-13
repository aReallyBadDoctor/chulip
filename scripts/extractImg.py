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
                    FILE.write(bytes(colors[num[(i+1)*16 + (w*y)+(x)]&15]))
                    FILE.write(bytes(colors[(num[(i+1)*16 + (w*y)+(x)]>>4)&15]))
            FILE.seek(0)
            frame = im.frombytes("RGBA", (w*2,int(h/2)), FILE.read(w*h*4))
            try:
                frame.save(save_dir+offset+name_base+".png")
            except OSError:
                os.makedirs(save_dir)
                frame.save(save_dir+offset+name_base+".png")
            FILE.close()

#source = sys.argv[1]
#dest = sys.argv[2]

source = "G:/emu/ps2/iso/Chulip/EXTRACTED/Chulip (USA)/"
dest = "G:\Github\chulip\images"


if __name__ == "__main__":
    for D in os.walk(source):
        for file in D[2]:
            path = D[0]+"\\"+file
            save_dir = dest + "\\" + path[path.index("Chulip (USA)")+13:path.rfind(".")]+"\\"
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
                        extract(i, 128,32)
                    elif(rv == int("00020008001000100000000800000020",16)):
                        extract(i,  32, 8)
                    elif(rv == int("00020008002000200000000800000080",16)):
                        extract(i,  64,16)
                    elif(rv == int("00020008008001000000000800001000",16)):
                        extract(i,1024,32)
                    elif(rv == int("00020008004000200000000800000100",16)):
                        extract(i,128 ,16)
                    elif(rv == int("00020008008000400000000800000400",16)):
                        extract(i,64, 128)#???? unknown dimensions
                    elif(rv == int("00020008008000800000000800000800",16)):
                        extract(i,64, 256)#???? unknown dimensions
                    elif(rv == int("00020008008000200000000800000200",16)):
                        extract(i, 256,16)
                except:
                    print("Issue with ", path," at ", hex(i*16),", moving on.")


