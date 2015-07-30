#BUAT INPUT
print("START INISIALISASI PARAMETER MASALAH")
J = 2
I = 2
job = [ ]
mesin = [ ]
for a in range(1,J+1):
    for b in range(1,I+1):
        job.append(a)
        mesin.append(b)
T = {(1, 2): 2, (1, 1): 1, (2, 1): 3, (2, 2): 1}
print (T)
print("END INISIALISASI PARAMETER MASALAH")
print(" ")

#INISIALISASI PARAMETER ALGORITMA
print("START INISIALISASI PARAMETER ALGORITMA")
av,bv,cv = 1, 0.01, 1
aso,bso,cso = 1, 0.01, 1
N = 2
itermax = 2
rhon = 0.5
rhoiwd = 0.1
initsoil=10000
initvel=200
epsilon= 0.000001
print("initsoil = 10.000")
print("initvel = 200")
print("END INISIALISASI PARAMETER ALGORITMA")
print(" ")

#ALGO BUAT BSA
print("START ALGORITMA PENYUSUN LIST NODE AWAL")
BSA= list(zip(job, mesin))
print("BSA: ", BSA)
print ("Node yang mungkin dilalui: ", BSA)
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
def nol(x):
    return 0
def ribu(x):
    return 10000
print("allsoil: ", allsoil)
soil= list(map(ribu, allsoil))
fsoil= list(map(ribu, allsoil))
gsoil= list(map(ribu, allsoil))
pxy= list(map(nol, allsoil))
print("soil map: ", soil)
print("fsoil map: ", fsoil)
print("gsoil map: ", gsoil)
print("pxy map: ", pxy)
    
print("END ALGORITMA SET SOIL(X,Y) = INITSOIL")
print(" ")

#ALGORITMA BESAR
print("START ALGORITMA UMUM")
MSTB= 999999
TB= [ ]
minsoil = 10001
for iterasi in range(1,itermax + 1): #Mulai loop buat sekian iterasi
    MSIB= 999999
    IB= [ ]
    SIB= 0
    for n in range(1,N+1): #Mulai loop buat sekian n
        BS= list(BSA[:len(BSA)])
        MS= 0
        VC= [ ]
        CVC= 0
        CBS= len(BS)
        Vn= initvel
        Sn= 0
        import random
        if iterasi==1:
            if n == 1:
                j = 1
                i = 2
        else:
            j= random.randint(1,J)
            i= random.randint(1,I)
        x= (j,i)
        print("Node pertama: ",j,i)
        VC.append((j,i))
        BS.remove((j,i))
        CVC= len(VC)
        CBS= len(BS)
        print("CVC,CBS:",CVC,CBS)
        print("allsoil:",allsoil)
        print("soil:",soil)
        #START ALGORITMA IWD
        print("BS:",BS)
        for a in range(0,CBS): #Mulai loop buat ngisi VC
            sigmaf= 0
            p= 0
            for q in range(0,CBS):
                y = BS[q]
                if soil[allsoil.index((x,y))] < minsoil:
                    minsoil= soil[allsoil.index((x,y))]
            print("minsoil:",minsoil)
            for q in range(0,CBS): #loop buat fsoil
                y= BS[q]
                if minsoil>= 0:
                    gsoil[allsoil.index((x,y))] = soil[allsoil.index((x,y))]
                    gsoil[allsoil.index((y,x))] = gsoil[allsoil.index((x,y))]
                else:
                    gsoil[allsoil.index((x,y))] = soil[allsoil.index((x,y))] - minsoil
                    gsoil[allsoil.index((y,x))] = gsoil[allsoil.index((x,y))]
                fsoil[allsoil.index((x,y))]= 1/ (epsilon + gsoil[allsoil.index((x,y))])
                fsoil[allsoil.index((y,x))]=  fsoil[allsoil.index((x,y))]
                print("gsoil x y: ",gsoil[allsoil.index((x,y))])
                print("fsoil x y", fsoil[allsoil.index((x,y))])
                sigmaf= sigmaf + fsoil[allsoil.index((x,y))]
            print("sigmaf:",sigmaf)
            for q in range(0,CBS): #loop buat ngitung pxy
                y= BS[q]
                pxy[allsoil.index((x,y))]= (fsoil[allsoil.index((x,y))]/ sigmaf)
                pxy[allsoil.index((y,x))]= pxy[allsoil.index((x,y))]
            print("pxy:",pxy)
            u= random.uniform(0,1)
            print("u:",u)
            q= 0
            while u > p: #loop buat milih y
                y= BS[q]
                p= p + pxy[allsoil.index((x,y))]
                q= q + 1
                print("y:",y)
                print("p:",p)
            else:
                VC.append(y)
                BS.remove(y)
                CVC= len(VC)
                CBS= len(BS)
            print("tji: ",T[y])
            #Rumus-rumus buat update
            Vn= Vn + av/ (bv+ cv* soil[allsoil.index((x,y))]* soil[allsoil.index((x,y))])
            print("Vn: ",Vn)
            HUD= 1/ (epsilon+ T[y])
            print("HUD: ",HUD)
            time= HUD/ Vn
            print("time: ",time)
            dsoil= aso/ (bso+ cso* time* time)
            print("delta soil:",dsoil)
            soil[allsoil.index((x,y))]= (1- rhon)*soil[allsoil.index((x,y))]- rhon* dsoil
            soil[allsoil.index((y,x))]= soil[allsoil.index((x,y))]
            print("soil x,y updated: ",soil[allsoil.index((x,y))])
            print("soil baru: ", soil)
            Sn = Sn+ dsoil
            print("Sn updated: ",Sn)
            x=y
            print("x:",x)
            print("VC akhir:",VC)
            print("BS akhir:",BS)
            print("CVC akhir:",CVC)
            print("CBS akhir:",CBS)
        #START ALGORITMA PENJADWALAN DAN MAKESPAN
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
        for q in range(0,len(BSA)): #buat ngeset ST sama FT= 0
            ST[BSA[q]]= 0
            FT[BSA[q]]= 0
        print("ST,FT: ",ST,FT)
        for q in range(0,I+1): #buat ngeset OM=0
            OM.append(0)
            d.append(1)
        for q in range(1,I+1): #buat ngeset OM=0
            SGM[q,1]= 0
            FGM[q,1]= 999999
            PGM[q,1]= 999999
        print("OM: ",OM)
        print("d,SGM,FGM,PGM: ",d,SGM,FGM,PGM)
        for q in range(0,J+1): #buat ngeset OM=0
            OJ.append(0)
            e.append(1)
        for q in range(1,J+1): #buat ngeset OJ=0
            SGJ[q,1]= 0
            FGJ[q,1]= 999999
            PGJ[q,1]= 999999
        print("OJ: ",OJ)
        print("e,SGJ,FGJ,PGJ: ",e,SGJ,FGJ,PGJ)
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
            print("j,i: ",j,i)
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
            print("STji: ",ST[j,i])
            print("FTji: ",FT[j,i])
            print("SGM: ",SGM)
            print("FGM: ",FGM)
            print("SGJ: ",SGJ)
            print("FGJ: ",FGJ)
            print("OMi: ",OM[i])
            print("OJj: ",OJ[j])
            print("d",i,": ", d[i])
            print("e",j,": ", e[j])
        print("ST: ",ST)
        print("FT: ",FT)
        print("SGM: ",SGM)
        print("FGM: ",FGM)
        print("SGJ: ",SGJ)
        print("FGJ: ",FGJ)
        print("OM: ",OM)
        print("OJ: ",OJ)
        MS= max(FT.values())
        print("MSn: ",MS)
        if MS < MSIB: #update MSIB
            MSIB= MS
            IB= VC
            SIB= Sn
            STB= ST
            FTB= FT
    print("MSIB: ",MSIB)
    print("IB: ",IB)
    print("SIB: ",SIB)
    for q in range(CVC-1): #update soil
        x= IB[q]
        y= IB[q+1]
        soil[allsoil.index((x,y))]= (1+ rhoiwd)* soil[allsoil.index((x,y))]-rhoiwd*(1/(J*I-1))*SIB
        soil[allsoil.index((y,x))]= soil[allsoil.index((x,y))]
    if MSIB< MSTB: #update MSTB
        MSTB= MSIB
        TB= IB
        STT= STB
        FTT= FTB
        best= iterasi
print("MSTB: ",MSTB)
print("TB: ",TB)
print("Start time best: ",STT)
print("Finish time best: ",FTT)
print("best iteration: ",best)
        
                                                         
