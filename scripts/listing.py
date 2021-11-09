h = 128
w = 256
def f(t):
	t = t-70
	x = t%(w*2)
	y = int(t/(w*2))
	return((int(x/2),h-y-1))

FILEX = open("G:/CHULIPTEST/XCOORDS3.txt", "w")
FILEX.write("x = [")
FILEY = open("G:/CHULIPTEST/YCOORDS3.txt", "w")
FILEY.write("y = [")



FILE = open("G:/CHULIPTEST/COORDS3.txt","w")

a = open("G:/CHULIPTEST/pics/0.bmp","rb")
for i in range(1,256*128+1):
    b = open("G:/CHULIPTEST/pics/"+str(i)+".bmp","rb")
    A = list(a)[0]
    B = list(b)[0]
    a.close()
    b.close()
    p = [i for i in range(len(A)) if A[i] != B[i]]
    try:
        FILEX.write(str(f(p[0])[0]))
        FILEX.write("\n")
        FILEY.write(str(f(p[0])[1]))
        FILEY.write("\n")
        FILE.write(str(f(p[0])))
        FILE.write("\n")
    except:
        print(i)
        FILE.write("(X,Y)\n")
        FILEX.write("X\n")
        FILEY.write("Y\n")
        #print(i)
    a = open("G:/CHULIPTEST/pics/"+str(i)+".bmp","rb")

a.close()
FILEX.write("]")
FILEX.close()
FILEY.write("]")
FILEY.close()
FILE.close()
