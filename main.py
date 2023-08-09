# modules
import os
import mmap

fname = input("SELECT MISSION ID: ")
fname = "./lurfiles/"+fname+".lur"
print(fname)
f = open(fname, "r")    
mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
mmread = mm.read()

class LurDecompiler():
    def __init__(self):
        self.chunks = []
        self.chunk = {}
        self.index = 0

    def read_file(id, l1, l2, dec):
        f = open(id, "r")    
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        mm = mm.read()
        if l2 == True:
            l2 = len(mm)
        if dec:
            res = []
            for m in mm:
                res.append(m)
            return res[l1:l2]
        else:
            return mm[l1:l2]

    def read_header(id, dec):
        f = LurDecompiler.read_file(id, 0, 38, dec)
        return f

    def get_first_byte(id, islist, dec):
        if islist:
            res = []
            for lur in os.listdir("./lurfiles"):
                f = os.path.join("./lurfiles", lur)
                if os.path.isfile(f):
                    if dec:
                        res.append([LurDecompiler.read_file(f, 37, 38, dec)[0], lur])
                    else:
                        res.append([LurDecompiler.read_file(f, 37, 38, dec), lur])
            return res
        else:
            res = []
            if dec:
                res.append(LurDecompiler.read_file(id, 37, 38, dec)[0])
            else:
                res.append(LurDecompiler.read_file(id, 37, 38, dec))
        return res

    def byte_to_hex(id, l1, l2):
        f = open(id, "r")    
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        mm = mm.read()
        res = []
        hex = mm.hex()
        for i in range(0, len(hex), 2):
            res.append(hex[i] + hex[i+1])
        return res

    def map_hex_to_byte(id, byte):
        hex = LurDecompiler.byte_to_hex(id, 0, True)
        return bytes.fromhex(hex[byte])

    def identify_functions(id):
        f = str(LurDecompiler.read_file(fname, 0, True, False))
        f = f.split("\\")
        res = []
        for byte in f:
            if byte[0] == "x":
                byte = byte[3:len(byte)]  
                if len(byte) > 1 :
                    print(byte)
                    res.append(byte)
        return res

    def edit_byte(id, pos, val):
        f = open(id, "r+b")    
        mm = mmap.mmap(f.fileno(), 0)
        mm[pos] = val
        return mm[pos]

Lur = LurDecompiler
print(Lur.identify_functions(fname))
