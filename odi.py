import random
import time as Time

#globals
J = 0
I = 0
job = [ ]
mesin = [ ]
# T = { }
T = {(7, 3): 227, (4, 7): 166, (1, 3): 126, (6, 6): 165, (5, 6): 180, (5, 4): 45, (2, 1): 107, (6, 2): 74, (1, 6): 323, (5, 1): 64, (3, 7): 165, (2, 5): 220, (7, 2): 234, (1, 2): 176, (3, 1): 214, (6, 7): 61, (5, 5): 71, (7, 6): 8, (4, 4): 321, (6, 3): 98, (1, 5): 101, (3, 6): 130, (2, 2): 88, (3, 3): 118, (5, 3): 191, (4, 1): 5, (1, 1): 123, (6, 4): 302, (3, 2): 181, (2, 6): 11, (7, 1): 398, (4, 5): 204, (1, 4): 79, (7, 7): 3, (7, 5): 55, (2, 3): 154, (4, 2): 120, (6, 5): 211, (3, 5): 42, (2, 7): 244, (4, 6): 103, (3, 4): 56, (6, 1): 89, (5, 7): 238, (7, 4): 75, (4, 3): 33, (1, 7): 23, (5, 2): 123, (2, 4): 111}

av, bv, cv = 1, 0.01, 1
aso, bso, cso = 1, 0.01, 1
initsoil = 10000
initvel = 200
epsilon = 0.000001

#classes
class Soil:
    def __init__(self, defsoil, defchance):
        self.soil = defsoil
        self.fsoil = defsoil
        self.gsoil = defsoil
        self.pxy = defchance

class Node:
    def __init__(self, jobNum, machineNum):
        self.job = jobNum
        self.machine = machineNum
        self.value = (jobNum,machineNum)

#initialization
print("START INISIALISASI PARAMETER MASALAH")
J = int(input("Jumlah job: "))
I = int(input("Jumlah mesin: "))
startTime = Time.time()
for a in range(1,J+1):
    for b in range(1,I+1):
        job.append(a)
        mesin.append(b)
        # T[a,b] = int(random.randint(1,10))
        # T[a,b] = int(input((a,b)))

print("job: {}").format(job)
print("mesin: {}").format(mesin)
print("END INISIALISASI PARAMETER MASALAH")
print(" ")

#INISIALISASI PARAMETER ALGORITMA
print("START INISIALISASI PARAMETER ALGORITMA")


# N = int(input("Jumlah water drop: "))
# itermax = int(input("Jumlah iterasi: "))
# rhon = float(input("Parameter update local: "))
# rhoiwd = float(input("Parameter update global: "))

N = 10
itermax = 20
rhon = 0.5
rhoiwd = 0.1

print("initsoil = {}").format(initsoil)
print("initvel = {}").format(initvel)
print("END INISIALISASI PARAMETER ALGORITMA")
print(" ")


#ALGO BUAT BSA
print("START ALGORITMA PENYUSUN LIST NODE AWAL")

BSA = list(zip(job, mesin))

print ("Node yang mungkin dilalui: {}").format(BSA)
print("END ALGORITMA PENYUSUN LIST NODE AWAL")
print(" ")

#ALGO SET SOIL X,Y = INITSOIL DAN SOIL2 LAINNYA
print("START ALGORITMA SET SOIL(X,Y) = INITSOIL DAN SOIL-SOIL LAINNYA")
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

# print("allsoil: {}").format(allsoil)
allsoilLength = len(allsoil)

# def nol(x):
#     return 0
# def ribu(x):
#     return 10000

soil= list(map(lambda x:10000, allsoil))
fsoil= list(map(lambda x:10000, allsoil))
gsoil= list(map(lambda x:10000, allsoil))
pxy= list(map(lambda x:0, allsoil))

# soil= [10000] * allsoilLength
# fsoil= [10000] * allsoilLength
# gsoil= [10000] * allsoilLength
# pxy= [0] * allsoilLength

# print("soil map: {}").format(soil)
# print("fsoil map: {}").format(fsoil)
# print("gsoil map: {}").format(gsoil)
# print("pxy map: {}").format(pxy)

print("END ALGORITMA SET SOIL(X,Y) = INITSOIL")
print(" ")

print("START ALGORITMA SET ST, FT, d, e, SGM, FGM, SGJ, FGJ")
STA= { }
FTA= { }
SGMA= { }
FGMA= { }
PGMA= { }
SGJA= { }
FGJA= { }
PGJA= { }
dA= [ ]
eA= [ ]
OMA= [ ]
OJA= [ ]
for q in range(0,len(BSA)): #buat ngeset ST sama FT= 0
    STA[BSA[q]]= 0
    FTA[BSA[q]]= 0
# print("STA,FTA: ",STA,FTA)
for q in range(0,I+1): #buat ngeset OM=0
    OMA.append(0)
    dA.append(1)
for q in range(1,I+1): #buat ngeset OM=0
    SGMA[q,1]= 0
    FGMA[q,1]= 999999
    PGMA[q,1]= 999999
# print("OMA: ",OMA)
# print("dA,SGMA,FGMA,PGMA: ",dA,SGMA,FGMA,PGMA)
for q in range(0,J+1): #buat ngeset OM=0
    OJA.append(0)
    eA.append(1)
for q in range(1,J+1): #buat ngeset OJ=0
    SGJA[q,1]= 0
    FGJA[q,1]= 999999
    PGJA[q,1]= 999999
# print("OJA: ",OJA)
# print("eA,SGJA,FGJA,PGJA: ",eA,SGJA,FGJA,PGJA)
print("END ALGORITMA SET ST, FT, d, e, SGM, FGM, SGJ, FGJ")

#ALGORITMA BESAR
print("START ALGORITMA UMUM")
MSTB= 999999
TB= [ ]
for iterasi in range(1,itermax + 1): #Mulai loop buat sekian iterasi
    MSIB= 999999
    IB= [ ]
    SIB= 0
    for n in range(1,N+1): #Mulai loop buat sekian n
        BS= list(BSA)
        MS= 0
        VC= [ ]
        CVC= 0
        CBS= len(BS)
        Vn= initvel
        Sn= 0
        j= random.randint(1,J)
        i= random.randint(1,I)
        x= (j,i)
        # print("Node pertama: ",j,i)
        VC.append((j,i))
        BS.remove((j,i))
        CVC= len(VC)
        CBS= len(BS)
        # print("CVC,CBS:",CVC,CBS)
        # print("allsoil:",allsoil)
        # print("soil:",soil)

        #START ALGORITMA IWD
        # print("BS:",BS)
        for a in range(0,CBS): #Mulai loop buat ngisi VC
            sigmaf= 0
            p= 0
            minsoil= min(soil)
            # print("minsoil:",minsoil)
            for q in range(0,CBS): #loop buat fsoil
                y= BS[q]
                straightIndex = allsoil.index((x,y))
                revIndex = allsoil.index((y,x))
                if minsoil>= 0:
                    gsoil[straightIndex] = soil[straightIndex]
                    gsoil[revIndex] = gsoil[straightIndex]
                else:
                    gsoil[straightIndex] = soil[straightIndex] - minsoil
                    gsoil[revIndex] = gsoil[straightIndex]
                fsoil[straightIndex]= 1/ (epsilon + gsoil[straightIndex])
                fsoil[revIndex]=  fsoil[straightIndex]
                # print("gsoil x y: ",gsoil[straightIndex])
                # print("fsoil x y", fsoil[straightIndex])
                sigmaf= sigmaf + fsoil[straightIndex]
            # print("sigmaf:",sigmaf)
            for q in range(0,CBS): #loop buat ngitung pxy
                y= BS[q]
                pxy[straightIndex]= (fsoil[straightIndex]/ sigmaf)
                pxy[revIndex]= pxy[straightIndex]
            # print("pxy:",pxy)
            u= random.uniform(0,1)
            # print("u:",u)
            q= 0
            while u > p: #loop buat milih y
                y= BS[q]
                p= p + pxy[straightIndex]
                q= q + 1
                # print("y:",y)
                # print("p:",p)
            else:
                VC.append(y)
                BS.remove(y)
                CVC= len(VC)
                CBS= len(BS)
            # print("tji: ",T[y])
            #Rumus-rumus buat update
            Vn= Vn + av/ (bv+ cv* soil[straightIndex]* soil[straightIndex])
            # print("Vn: ",Vn)
            HUD= 1/ (epsilon+ T[y])
            # print("HUD: ",HUD)
            time= HUD/ Vn
            # print("time: ",time)
            dsoil= aso/ (bso+ cso* time* time)
            # print("delta soil:",dsoil)
            soil[straightIndex]= (1- rhon)*soil[straightIndex]- rhon* dsoil
            soil[revIndex]= soil[straightIndex]
            # print("soil x,y updated: ",soil[straightIndex])
            # print("soil baru: ", soil)
            Sn = Sn+ dsoil
            # print("Sn updated: ",Sn)
            x=y
            # print("x:",x)
            # print("VC akhir:",VC)
            # print("BS akhir:",BS)
            # print("CVC akhir:",CVC)
            # print("CBS akhir:",CBS)

        #END OF IWD


        #START ALGORITMA PENJADWALAN DAN MAKESPAN
        ST= dict(STA)
        FT= dict(FTA)
        SGM= dict(SGMA)
        FGM= dict(FGMA)
        PGM= dict(PGMA)
        SGJ= dict(SGJA)
        FGJ= dict(FGJA)
        PGJ= dict(PGJA)
        d= list(dA)
        e= list(eA)
        OM= list(OMA)
        OJ= list(OJA)
        def jadwalujung(j,i): #a=j, b=i
            if SGJ[j,e[j]]<= SGM[i,d[i]]: #buat penjadwalan di ujung, cek mau dijadwalin di ujung gap job atau gap mesin
                ST[j,i]= SGM[i,d[i]]
                FT[j,i]= ST[j,i]+ T[j,i]
                OM[i]= OM[i]+ 1
                OJ[j]= OJ[j]+ 1
            else:
                ST[j,i]= SGJ[j,e[j]]
                FT[j,i]= ST[j,i]+ T[j,i]
                OM[i]= OM[i]+ 1
                OJ[j]= OJ[j]+ 1
        def updategapujung(j,i):
            if ST[j,i]== SGM[i,d[i]]:
                pass
            else:
                FGM[i,d[i]]= ST[j,i]
                PGM[i,d[i]]= FGM[i,d[i]]- SGM[i,d[i]]
                d[i]= d[i]+ 1
            SGM[i,d[i]]= FT[j,i]
            FGM[i,d[i]]= 999999
            PGM[i,d[i]]= 999999
            if ST[j,i]== SGJ[j,e[j]]:
                pass
            else:
                FGJ[j,e[j]]= ST[j,i]
                PGJ[j,e[j]]= FGJ[j,e[j]]- SGJ[j,e[j]]
                e[j]= e[j]+ 1
            SGJ[j,e[j]]= FT[j,i]
            FGJ[j,e[j]]= 999999
            PGJ[j,e[j]]= 999999
        def updategapi(j,i,u):
            if ST[j,i]== SGM[i,u]:
                if FT[j,i]== FGM[i,u]:
                    for u in range(u,d[i]):
                        SGM[i,u]= SGM[i,u+1]
                        FGM[i,u]= FGM[i,u+1]
                        PGM[i,u]= PGM[i,u+1]
                    del SGM[i,d[i]]
                    del FGM[i,d[i]]
                    del PGM[i,d[i]]
                    d[i]= d[i]- 1
                else:
                    SGM[i,u]= FT[j,i]
                    PGM[i,u]= FGM[i,u]- SGM[i,u]
            else:
                if FT[j,i]== FGM[i,u]:
                    FGM[i,u]= ST[j,i]
                    PGM[i,u]= FGM[i,u]- SGM[i,u]
                else:
                    d[i]= d[i]+ 1
                    SGM[i,d[i]]= SGM[i,d[i]-1]
                    FGM[i,d[i]]= FGM[i,d[i]-1]
                    PGM[i,d[i]]= PGM[i,d[i]-1]
                    if d[i]-u >= 2:
                        for r in range(d[i],u+2):
                            SGM[i,r+1]= SGM[i,r]
                            FGM[i,r+1]= FGM[i,r]
                            PGM[i,r+1]= PGM[i,r]
                    SGM[i,u+1]= FT[j,i]
                    FGM[i,u+1]= FGM[i,u]
                    PGM[i,u+1]= FGM[i,u+1]- SGM[i,u+1]
                    FGM[i,u]= ST[j,i]
                    PGM[i,u]= FGM[i,u]- SGM[i,u]
        def updategapj(j,i,w):
            if ST[j,i]== SGJ[j,w]:
                if FT[j,i]== FGJ[j,w]:
                    for w in range(w,e[j]):
                        SGJ[j,w]= SGJ[j,w+1]
                        FGJ[j,w]= FGJ[j,w+1]
                        PGJ[j,w]= PGJ[j,w+1]
                    del SGJ[j,e[j]]
                    del FGJ[j,e[j]]
                    del PGJ[j,e[j]]
                    e[j]= e[j]- 1
                else:
                    SGJ[j,w]= FT[j,i]
                    PGJ[j,w]= FGJ[j,w]- SGJ[j,w]
            else:
                if FT[j,i]== FGJ[j,w]:
                    FGJ[j,w]= ST[j,i]
                    PGJ[j,w]= FGJ[j,w]- SGJ[j,w]
                else:
                    e[j]= e[j]+ 1
                    SGJ[j,e[j]]= SGJ[j,e[j]-1]
                    FGJ[j,e[j]]= FGJ[j,e[j]-1]
                    PGJ[j,e[j]]= PGJ[j,e[j]-1]
                    if e[j]-w >=2:
                        for r in range(e[j],w+2):
                            SGJ[j,r+1]= SGJ[j,r]
                            FGJ[j,r+1]= FGJ[j,r]
                            PGJ[j,r+1]= PGJ[j,r]
                    SGJ[j,w+1]= FT[j,i]
                    FGJ[j,w+1]= FGJ[j,w]
                    PGJ[j,w+1]= FGJ[j,w+1]- SGJ[j,w+1]
                    FGJ[j,w]= ST[j,i]
                    PGJ[j,w]= FGJ[j,w]- SGJ[j,w]

        for q in range(CVC): #mulai pengisian gantt chart
            (j,i)=VC[q]
            # print("j,i: ",j,i)
            if OM[i]== 0: #cek OMi = 0
                if OJ[j]==0: #cek OJj=0
                    jadwalujung(j,i)
                    updategapujung(j,i)
                else:
                    if e[j]== 1: #buat yang OJj ga 0 dan gap job 1
                        jadwalujung(j,i)
                        updategapujung(j,i)
                    else: #buat yang OMi 0, OJj ga 0 dan gap job ga 1
                        for w in range(1,e[j]):
                            if T[j,i]<= PGJ[j,w]:
                                ST[j,i]= SGJ[j,w]
                                FT[j,i]= ST[j,i]+ T[j,i]
                                OM[i]= OM[i]+ 1
                                OJ[j]= OJ[j]+ 1
                                updategapi(j,i,1)
                                updategapj(j,i,w)
                                break
                        else: #buat yang OMi 0, OJj ga 0, gap job ga 1, tapi gap job ga ada yang muat
                            jadwalujung(j,i)
                            updategapujung(j,i)
            else: #buat yang OMi ga 0
                if d[i]== 1: #cek gap mesin
                    if e[j]== 1: #cek gap job
                        jadwalujung(j,i)
                        updategapujung(j,i)
                    else: #buat OMi ga 0, gap mesin 1, dan gap job ga 1
                        u= 1
                        w= 1
                        PGI= 0
                        SGI= 0
                        FGI= 0
                        for w in range(1,e[j]):
                            if SGM[i,u]>= SGJ[j,w]:
                                if FGM[i,u] >= FGJ[j,w]:
                                    if FGJ[j,w] >= SGM[i,u]:
                                        SGI= SGM[i,u]
                                        FGI= FGJ[j,w]
                                        PGI= FGI- SGI
                                    else:
                                        PGI= 0
                                else:
                                    SGI= SGM[i,u]
                                    FGI= FGM[i,u]
                                    PGI= FGI- SGI
                            else:
                                if FGM[i,u]< FGJ[j,w]:
                                    if FGM[i,u] > SGJ[j,w]:
                                        SGI= SGJ[j,w]
                                        FGI= FGM[i,u]
                                        PGI= FGI- SGI
                                    else:
                                        PGI= 0
                                else:
                                    SGI= SGJ[j,w]
                                    FGI= FGJ[j,w]
                                    PGI= FGI- SGI
                            if T[j,i] <= PGI:
                                ST[j,i]= SGI
                                FT[j,i]= ST[j,i] + T[j,i]
                                OM[i]= OM[i]+ 1
                                OJ[j]= OJ[j]+ 1
                                updategapi(j,i,u)
                                updategapj(j,i,w)
                                break
                        else:
                            jadwalujung(j,i)
                            updategapujung(j,i)
                else: #buat OMi ga 0 dan gap mesin ga 1
                    for u in range(1,d[i]):
                        PGI= 0
                        SGI= 0
                        FGI= 0
                        if T[j,i] <= PGM[i,u]:
                            for w in range(1,e[j]+1):
                                if SGM[i,u]>= SGJ[j,w]:
                                    if FGM[i,u] >= FGJ[j,w]:
                                        if FGJ[j,w] >= SGM[i,u]:
                                            SGI= SGM[i,u]
                                            FGI= FGJ[j,w]
                                            PGI= FGI- SGI
                                        else:
                                            PGI= 0
                                    else:
                                        SGI= SGM[i,u]
                                        FGI= FGM[i,u]
                                        PGI= FGI- SGI
                                else:
                                    if FGM[i,u]< FGJ[j,w]:
                                        if FGM[i,u] > SGJ[j,w]:
                                            SGI= SGJ[j,w]
                                            FGI= FGM[i,u]
                                            PGI= FGI- SGI
                                        else:
                                            PGI= 0
                                    else:
                                        SGI= SGJ[j,w]
                                        FGI= FGJ[j,w]
                                        PGI= FGI- SGI
                                if T[j,i] <= PGI:
                                    ST[j,i]= SGI
                                    FT[j,i]= ST[j,i] + T[j,i]
                                    OM[i]= OM[i]+ 1
                                    OJ[j]= OJ[j]+ 1
                                    updategapi(j,i,u)
                                    updategapj(j,i,w)
                                    break
                            if T[j,i]<= PGI:
                                break
                    else:
                        jadwalujung(j,i)
                        updategapujung(j,i)
        #     print("STji: ",ST[j,i])
        #     print("FTji: ",FT[j,i])
        #     print("SGM: ",SGM)
        #     print("FGM: ",FGM)
        #     print("SGJ: ",SGJ)
        #     print("FGJ: ",FGJ)
        #     print("OMi: ",OM[i])
        #     print("OJj: ",OJ[j])
        #     print("d",i,": ", d[i])
        #     print("e",j,": ", e[j])
        # print("ST: ",ST)
        # print("FT: ",FT)
        # print("SGM: ",SGM)
        # print("FGM: ",FGM)
        # print("SGJ: ",SGJ)
        # print("FGJ: ",FGJ)
        # print("OM: ",OM)
        # print("OJ: ",OJ)
        MS= max(FT.values())
        # print("MSn: ",MS)
        if MS < MSIB: #update MSIB
            MSIB= MS
            IB= VC
            SIB= Sn
            STB= ST
            FTB= FT
        print "waterdrop {} of iteration {} done.".format(n,iterasi)
    # print("MSIB: ",MSIB)
    # print("IB: ",IB)
    # print("SIB: ",SIB)
    for q in range(CVC-1): #update soil
        x= IB[q]
        y= IB[q+1]
        
        straightIndex = allsoil.index((x,y))
        revIndex = allsoil.index((y,x))
        soil[straightxIndex]= (1+ rhoiwd)* soil[straightxIndex]-rhoiwd*(1/(J*I-1))*SIB
        soil[revxIndex]= soil[straightxIndex]
    if MSIB< MSTB: #update MSTB
        MSTB= MSIB
        TB= IB
        STT= STB
        FTT= FTB
        best= iterasi
    print "iteration number {} done. MSIB: {}".format(iterasi, MSIB)
print("MSTB: {}").format(MSTB)
print("TB: ",TB)
print("Start time best: ",STT)
print("Finish time best: ",FTT)
print("best iteration: ",best)

endTime = Time.time()
print("time elapsed: {}").format(endTime - startTime)
