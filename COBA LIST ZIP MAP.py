import numpy as np
J = int(input("Jumlah job: "))
I = int(input("Jumlah mesin: "))
job = [ ]
mesin = [ ]
T = { }
for a in range(1,J+1):
    for b in range(1,I+1):
        job.append(a)
        mesin.append(b)
        T[a,b] = int(input((a,b)))
time= max(T.values())
print("T: ", T)

BSA= list(zip(job, mesin))
print("BSA: ", BSA)

allsoil= [ ]
soil= [ ]
fsoil= [ ]
gsoil= [ ]
pxy= [ ]
for a in range(len(BSA)-1):
    for b in range(a+1,len(BSA)):
        x= BSA[a]
        y= BSA[b]
        allsoil.append((x,y))
        allsoil.append((y,x))
        soil.append(10000)
        fsoil.append(10000)
        gsoil.append(10000)
        pxy.append(0)
soil= soil + soil
gsoil= gsoil + gsoil
fsoil= fsoil + fsoil
pxy= pxy + pxy
print("allsoil: ", allsoil)
print("soil: ", soil)
print("fsoil: ", fsoil)
print("gsoil: ", gsoil)
print("pxy: ", pxy)

minsoil= min(soil)
print("minsoil: ", minsoil)

ST= { }
FT= { }
SGM= { }
FGM= { }
PGM= { }
SGJ= { }
FGJ= { }
PGJ= { }
d= [ ]
e= [ ]
OM= [ ]
OJ= [ ]
BS= list(BSA[:len(BSA)])
print("BS: ", BS)
print("BSA: ", BSA)

for q in range(0,len(BSA)): #buat ngeset ST sama FT= 0
    ST[BSA[q]]= 0
    FT[BSA[q]]= 0
print("ST: ", ST)
print("FT: ", FT)          


for q in range(1,I+1): #buat ngeset OM=0
    OM.append(0)
    d.append(1)
    SGM[q,1]= 0
    FGM[q,1]= 999999
    PGM[q,1]= 999999
print("OM: ",OM)
print("d,SGM,FGM,PGM: ",d,SGM,FGM,PGM)
for q in range(1,J+1): #buat ngeset OJ=0
    OJ.append(0)
    e.append(1)
    SGJ[q,1]= 0
    FGJ[q,1]= 999999
    PGJ[q,1]= 999999
print("OJ: ",OJ)
print("e,SGJ,FGJ,PGJ: ",e,SGJ,FGJ,PGJ)
