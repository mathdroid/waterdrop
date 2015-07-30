#START ALGORITMA PENJADWALAN DAN MAKESPAN
J = 7
I = 7
VC=  [(6, 3), (2, 6), (2, 2), (1, 3), (7, 2), (7, 6), (5, 7), (1, 6), (7, 7), (1, 5), (1, 4), (4, 4), (4, 6), (5, 2), (3, 3), (3, 1), (6, 2), (4, 2), (1, 7), (6, 4), (5, 4), (3, 7), (5, 5), (4, 7), (6, 5), (6, 7), (4, 1), (5, 6), (3, 5), (3, 6), (5, 1), (6, 6), (2, 3), (7, 3), (7, 5), (2, 1), (3, 2), (2, 4), (6, 1), (1, 2), (7, 4), (2, 7), (3, 4), (1, 1), (4, 5), (4, 3), (7, 1), (2, 5), (5, 3)]
CVC= J * I
MS= 0
MSIB= 999999
MSTB= 999999
T = {(7, 3): 227, (4, 7): 166, (1, 3): 126, (6, 6): 165, (5, 6): 180, (5, 4): 45, (2, 1): 107, (6, 2): 74, (1, 6): 323, (5, 1): 64, (3, 7): 165, (2, 5): 220, (7, 2): 234, (1, 2): 176, (3, 1): 214, (6, 7): 61, (5, 5): 71, (7, 6): 8, (4, 4): 321, (6, 3): 98, (1, 5): 101, (3, 6): 130, (2, 2): 88, (3, 3): 118, (5, 3): 191, (4, 1): 5, (1, 1): 123, (6, 4): 302, (3, 2): 181, (2, 6): 11, (7, 1): 398, (4, 5): 204, (1, 4): 79, (7, 7): 3, (7, 5): 55, (2, 3): 154, (4, 2): 120, (6, 5): 211, (3, 5): 42, (2, 7): 244, (4, 6): 103, (3, 4): 56, (6, 1): 89, (5, 7): 238, (7, 4): 75, (4, 3): 33, (1, 7): 23, (5, 2): 123, (2, 4): 111}
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
for q in range(1,J+1): #buat ngeset ST sama FT= 0
    for z in range(1,I+1):
        ST[q,z]= 0
        FT[q,z]= 0
print("ST,FT: ",ST,FT)
for q in range(0,I+1): #buat ngeset OM=0
    OM.append(0)    
print("OM: ",OM)
for q in range(0,J+1): #buat ngeset OJ=0
    OJ.append(0)
print("OJ: ",OJ)
for q in range(0,I+1): #buat ngeset jumlah gap mesin
    d.append(1)
for q in range(1,I+1): #buat ngeset waktu gap mesin
    SGM[q,1]= 0
    FGM[q,1]= 999999
    PGM[q,1]= 999999
print("d,SGM,FGM,PGM: ",d,SGM,FGM,PGM)
for q in range(0,J+1): #buat ngeset jumlah gap job
    e.append(1)
for q in range(1,J+1): #buat ngeset waktu gap job
    SGJ[q,1]= 0
    FGJ[q,1]= 999999
    PGJ[q,1]= 999999
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
                        updategapj(j,i,w)
                        updategapi(j,i,1)
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
                    if T[j,i] <= PGI:
                        break
            else:
                jadwalujung(j,i)
                updategapujung(j,i)
            print("PGI: ", PGI)
            print("SGI: ", SGI)
            print("FGI: ", FGI)
    print("STji: ",ST[j,i])
    print("FTji: ",FT[j,i])
    print("SGM: ",SGM)
    print("FGM: ",FGM)
    print("PGM: ",PGM)
    print("SGJ: ",SGJ)
    print("FGJ: ",FGJ)
    print("PGJ: ",PGJ)
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
for w in range(1,J+1):
    for u in range(1,I+1):
        if FT[w,u]> MS:
            MS= FT[w,u]
print("MSn: ",MS)
if MS < MSIB: #update MSIB
    MSIB= MS
    IB= VC
    STB= ST
    FTB= FT
print("MSIB: ",MSIB)
print("IB: ",IB)
if MSIB< MSTB: #update MSTB
    MSTB= MSIB
    TB= IB
print("MSTB: ",MSTB)
print("TB: ",TB)
print("Start time best: ",STB)
print("Finish time best: ",FTB)

