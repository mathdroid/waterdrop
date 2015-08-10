#mdules
import random
import time as Time

#globals
J = 0
I = 0
job = [ ]
mesin = [ ]
T = { }
#4-4
# sampleT = {(1, 2): 7, (3, 2): 69, (1, 3): 4, (3, 3): 605, (4, 1): 317, (3, 1): 42, (4, 4): 7, (1, 4): 351, (2, 4): 358, (2, 3): 1, (2, 1): 3, (4, 3): 390, (2, 2): 638, (4, 2): 286, (3, 4): 284, (1, 1): 638}

#7-7
# sampleT = {(7, 3): 227, (4, 7): 166, (1, 3): 126, (6, 6): 165, (5, 6): 180, (5, 4): 45, (2, 1): 107, (6, 2): 74, (1, 6): 323, (5, 1): 64, (3, 7): 165, (2, 5): 220, (7, 2): 234, (1, 2): 176, (3, 1): 214, (6, 7): 61, (5, 5): 71, (7, 6): 8, (4, 4): 321, (6, 3): 98, (1, 5): 101, (3, 6): 130, (2, 2): 88, (3, 3): 118, (5, 3): 191, (4, 1): 5, (1, 1): 123, (6, 4): 302, (3, 2): 181, (2, 6): 11, (7, 1): 398, (4, 5): 204, (1, 4): 79, (7, 7): 3, (7, 5): 55, (2, 3): 154, (4, 2): 120, (6, 5): 211, (3, 5): 42, (2, 7): 244, (4, 6): 103, (3, 4): 56, (6, 1): 89, (5, 7): 238, (7, 4): 75, (4, 3): 33, (1, 7): 23, (5, 2): 123, (2, 4): 111}
#10-10
sampleT = {(7, 3): 88, (6, 9): 1, (1, 3): 86, (4, 8): 161, (2, 8): 55, (9, 8): 4, (6, 2): 2, (1, 6): 21, (7, 10): 1, (3, 7): 2, (2, 5): 1, (8, 5): 1, (5, 8): 1, (10, 8): 308, (6, 7): 1, (5, 5): 667, (10, 7): 6, (3, 10): 1, (6, 10): 75, (8, 10): 230, (3, 5): 2, (1, 1): 185, (4, 10): 676, (3, 2): 3, (2, 6): 2, (8, 2): 12, (4, 5): 1, (9, 3): 1, (1, 4): 6, (3, 9): 5, (2, 3): 3, (1, 9): 13, (8, 7): 419, (4, 2): 3, (9, 6): 183, (6, 5): 4, (5, 3): 1, (10, 5): 1, (6, 8): 1, (3, 1): 20, (9, 9): 147, (1, 7): 234, (7, 8): 195, (2, 4): 55, (8, 4): 1, (5, 9): 52, (4, 7): 1, (9, 1): 5, (6, 6): 41, (5, 6): 92, (10, 6): 1, (7, 7): 2, (2, 1): 282, (8, 9): 91, (9, 4): 1, (5, 1): 6, (10, 3): 185, (7, 2): 596, (1, 2): 2, (3, 8): 6, (7, 5): 1, (4, 9): 3, (3, 3): 13, (2, 9): 586, (8, 1): 3, (4, 4): 9, (6, 3): 573, (1, 5): 320, (3, 6): 458, (2, 2): 1, (1, 10): 1, (8, 6): 101, (4, 1): 1, (10, 9): 1, (9, 7): 332, (6, 4): 19, (5, 4): 178, (10, 4): 240, (7, 1): 14, (2, 10): 13, (9, 10): 1, (10, 1): 201, (7, 9): 101, (2, 7): 2, (8, 3): 5, (5, 10): 1, (4, 6): 100, (10, 10): 1, (9, 2): 324, (3, 4): 490, (6, 1): 283, (5, 7): 1, (7, 4): 1, (1, 8): 132, (8, 8): 137, (4, 3): 45, (9, 5): 2, (5, 2): 1, (7, 6): 1, (10, 2): 56}

av, bv, cv = 1, 0.01, 1 #algo params for velocity
aso, bso, cso = 1, 0.01, 1 #algo params for soil
initsoil = 10000 #soil initial
initvel = 200 #velocity initial
epsilon = 0.000001 #epsilon

N = 100 #waterdropMax
itermax = 500 #iterationMax
rhon = 0.3 #localUpdater
rhoiwd = 0.3 #globalUpdater

nodes = {}

allsoil= [ ]
soil= [ ]
fsoil= [ ]
gsoil= [ ]
pxy= [ ]

STA= { } #start time
FTA= { } #finish time
SGMA= { } #start gap machine
FGMA= { } #finish gap machine
PGMA= { } #panjang gap machine
SGJA= { } #start gap job
FGJA= { } #finish gap job
PGJA= { } #panjang gap job
dA= [ ]
eA= [ ]
OMA= [ ]
OJA= [ ]

MSTB= 999999
TB= [ ]

soils = {}

dicetime = []
iwdtimes = []
makespantimes = []
#classes
class Soil:
    def __init__(self, node1, node2, defsoil, defchance):
        self.soil = defsoil
        self.fsoil = defsoil
        self.gsoil = defsoil
        self.pxy = defchance
        self.nodes = [node1, node2]

class Node:
    def __init__(self, job, machine, duration):
        self.job = job
        self.machine = machine
        self.duration = duration
        self.value = (job, machine)

class Waterdrop:
    def __init__(self):
        self.velocity = initvel

#funcs
def updategapj(j,i,w, ST, SGJ, FT, FGJ, PGJ, e):
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

def updategapi(j,i,u,ST,SGM,FT,FGM,d,PGM):
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

def updategapujung(j,i,ST,SGM,d,FGM,PGM,FT,e,SGJ,FGJ,PGJ):
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

def jadwalujung(j,i,SGJ,e,SGM,d,ST,FT,T,OM,OJ): #a=j, b=i
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


#initialization
print("START INISIALISASI PARAMETER MASALAH")
J = int(input("Jumlah job: "))
I = int(input("Jumlah mesin: "))
startTime = Time.time()
for a in range(1,J+1):
    for b in range(1,I+1):
        job.append(a)
        mesin.append(b)
        node = Node(a, b, int(random.randint(1,250)))
        if (a,b) in sampleT:
            node.duration = sampleT[(a,b)]
        print("node ({},{}) duration: {}".format(node.job, node.machine, node.duration))
        nodes[(a,b)] = node

        T[a,b] = nodes[(a,b)].duration
        # T[a,b] = int(input((a,b)))

print("Nodes: {}".format(len(nodes)))
print("job: {}".format(job))
print("mesin: {}".format(mesin))
print("END INISIALISASI PARAMETER MASALAH")
print(" ")

#INISIALISASI PARAMETER ALGORITMA
print("START INISIALISASI PARAMETER ALGORITMA")


# N = int(input("Jumlah water drop: "))
# itermax = int(input("Jumlah iterasi: "))
# rhon = float(input("Parameter update local: "))
# rhoiwd = float(input("Parameter update global: "))



print("initsoil = {}".format(initsoil))
print("initvel = {}".format(initvel))
print("END INISIALISASI PARAMETER ALGORITMA")
print(" ")


#ALGO BUAT BSA
print("START ALGORITMA PENYUSUN LIST NODE AWAL")

BSA = list(zip(job, mesin))
#nodes

print ("Node yang mungkin dilalui: {}".format(BSA))
print("END ALGORITMA PENYUSUN LIST NODE AWAL")
print(" ")

#ALGO SET SOIL X,Y = INITSOIL DAN SOIL2 LAINNYA
print("START ALGORITMA SET SOIL(X,Y) = INITSOIL DAN SOIL-SOIL LAINNYA")

for a in range(len(BSA)-1):
    for b in range(a+1,len(BSA)):
        x= BSA[a]
        y= BSA[b]
        allsoil.append((x,y))
        allsoil.append((y,x))

for key, value in nodes.items():
    for key2, value2 in nodes.items():
        if not key==key2:
            soils[(key,key2)] = Soil(value, value2, 10000, 0)
        if (key2,key) in soils:
            del soils[(key2,key)]

print("soils length: {}".format(len(soils)))
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

for q in range(0, len(BSA)): #buat ngeset ST sama FT= 0
    helper = BSA[q]
    STA[helper]= 0
    FTA[helper]= 0
# print("STA,FTA: ",STA,FTA)
for q in range(0, I+1): #buat ngeset OM=0
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

for iterasi in range(1, itermax + 1): #Mulai loop buat sekian iterasi

    MSIB= 999999
    IB= [ ]
    SIB= 0

    for n in range(1, N+1): #Mulai loop buat sekian n

        BS= list(BSA) #unfinished city
        MS= 0 #makespan of current waterdrop
        VC= [ ] #visited city
        CVC= 0 #visited counter
        CBS= len(BS) #unfinished counter
        Vn= initvel #waterdrop speed
        Sn= 0 #waterdrop soil
        j= random.randint(1, J)
        i= random.randint(1, I)
        x= (j,i) #first node

        VC.append((j,i))
        BS.remove((j,i))
        CVC= len(VC)
        CBS= len(BS)

        current_node = x

        unfinished_cities = dict(nodes)
        finished_cities = {}
        finished_cities_list = []
        finished_cities_list.append(x)
        finished_cities[x] = unfinished_cities[x]
        del unfinished_cities[x]

        count_unfinished = len(unfinished_cities)
        count_finished = len(finished_cities)

        # print("first node: ",x)
        #START ALGORITMA IWD
        iwdStart = Time.time()
        while len(unfinished_cities)>0: #Mulai loop buat ngisi VC
            sigmaf = 0
            p = 0
            minsoil = 10001

            for city in unfinished_cities:
                address = (current_node,city)
                if address not in soils:
                    address = (city,current_node)
                if soils[address].soil < minsoil:
                    minsoil = soils[address].soil

            for city in unfinished_cities:
                address = (current_node,city)
                if address not in soils:
                    address = (city,current_node)
                path = soils[address]

                if minsoil >= 0:
                    path.gsoil = path.soil
                else:
                    path.gsoil = path.soil - minsoil
                path.fsoil = 1 / (epsilon + path.gsoil)
                sigmaf += path.fsoil
                soils[address] = path

            for city in unfinished_cities:
                address = (current_node,city)
                if address not in soils:
                    address = (city,current_node)
                soils[address].pxy = (soils[address].fsoil / sigmaf)


            # # for city in BS:
            # for y in BS:
            #     if soil[allsoil.index((x,y))] < minsoil:
            #         minsoil= soil[allsoil.index((x,y))]



            #offsetting all soils with the minsoil, if minsoil if negative.
            # for y in BS:
            #     straightIndex = allsoil.index((x,y))
            #     revIndex = allsoil.index((y,x))
            #     if minsoil>= 0:
            #         gsoil[straightIndex] = soil[straightIndex]
            #         gsoil[revIndex] = gsoil[straightIndex]
            #     else:
            #         gsoil[straightIndex] = soil[straightIndex] - minsoil
            #         gsoil[revIndex] = gsoil[straightIndex]
            #     fsoil[straightIndex] = 1/ (epsilon + gsoil[straightIndex])
            #     fsoil[revIndex] =  fsoil[straightIndex]
            #     sigmaf += fsoil[straightIndex]
            # for y in BS:
            #     straightIndex = allsoil.index((x,y))
            #     revIndex = allsoil.index((y,x))
            #     pxy[straightIndex]= (fsoil[straightIndex]/ sigmaf)
            #     pxy[revIndex]= pxy[straightIndex]

            u= random.uniform(0,1)
            q= 0
            chancetime = Time.time()
            the_city = current_node
            the_address = ()

            unfinished_cities_list = list(unfinished_cities.items())

            while u > p:
                city = unfinished_cities_list[q]
                address = (current_node,city[0])
                if address not in soils:
                    address = (city[0],current_node)
                the_address=address
                the_city=city[0]
                p += soils[the_address].pxy
                q += 1
            dicetime.append(Time.time()-chancetime)
            finished_cities_list.append(city[0])
            finished_cities[city[0]] = unfinished_cities[city[0]]
            del unfinished_cities[city[0]]
            count_finished += 1
            count_unfinished -= 1

            Vn += av/ (bv+ cv* soils[the_address].soil**2)
            HUD= 1/ (epsilon+ T[the_city])
            time= HUD/ Vn
            dsoil= aso/ (bso+ cso* time**2)
            soils[the_address].soil *= (1- rhon)
            soils[the_address].soil -= rhon* dsoil
            Sn = Sn+ dsoil
            current_node = the_city
            # print("current_node: ", current_node)
            # while u > p: #loop buat milih y
            #     y= BS[q]
            #
            #     straightIndex = allsoil.index((x,y))
            #     p= p + pxy[straightIndex]
            #     q= q + 1
            # dicetime.append(Time.time()-chancetime)
            # VC.append(y)
            # BS.remove(y)
            # CVC += 1
            # CBS -= 1

            #Rumus-rumus buat update

            # straightIndex = allsoil.index((x,y))
            # revIndex = allsoil.index((y,x))
            # Vn= Vn + av/ (bv+ cv* soil[straightIndex]**2)
            # HUD= 1/ (epsilon+ T[y])
            # time= HUD/ Vn
            # dsoil= aso/ (bso+ cso* time* time)
            # soil[straightIndex]= (1- rhon)*soil[straightIndex]- rhon* dsoil
            # soil[revIndex]= soil[straightIndex]
            # Sn = Sn+ dsoil
            # x=y
        # print(finished_cities_list)
        #END OF IWD
        iwdEnd = Time.time()

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

        # print("finished_cities_list:", finished_cities_list)
        for q in range(count_finished): #mulai pengisian gantt chart
            (j,i) = finished_cities_list[q]
            # print("j,i: ",j,i)
            if OM[i]== 0: #cek OMi = 0
                if OJ[j]==0: #cek OJj=0
                    jadwalujung(j,i,SGJ,e,SGM,d,ST,FT,T,OM,OJ)
                    updategapujung(j,i,ST,SGM,d,FGM,PGM,FT,e,SGJ,FGJ,PGJ)
                else:
                    if e[j]== 1: #buat yang OJj ga 0 dan gap job 1
                        jadwalujung(j,i,SGJ,e,SGM,d,ST,FT,T,OM,OJ)
                        updategapujung(j,i,ST,SGM,d,FGM,PGM,FT,e,SGJ,FGJ,PGJ)
                    else: #buat yang OMi 0, OJj ga 0 dan gap job ga 1
                        for w in range(1,e[j]):
                            if T[j,i]<= PGJ[j,w]:
                                ST[j,i]= SGJ[j,w]
                                FT[j,i]= ST[j,i]+ T[j,i]
                                OM[i]= OM[i]+ 1
                                OJ[j]= OJ[j]+ 1
                                updategapi(j,i,1,ST,SGM,FT,FGM,d,PGM)
                                updategapj(j,i,w, ST, SGJ, FT, FGJ, PGJ, e)
                                break
                        else: #buat yang OMi 0, OJj ga 0, gap job ga 1, tapi gap job ga ada yang muat
                            jadwalujung(j,i,SGJ,e,SGM,d,ST,FT,T,OM,OJ)
                            updategapujung(j,i,ST,SGM,d,FGM,PGM,FT,e,SGJ,FGJ,PGJ)
            else: #buat yang OMi ga 0
                if d[i]== 1: #cek gap mesin
                    if e[j]== 1: #cek gap job
                        jadwalujung(j,i,SGJ,e,SGM,d,ST,FT,T,OM,OJ)
                        updategapujung(j,i,ST,SGM,d,FGM,PGM,FT,e,SGJ,FGJ,PGJ)
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
                                updategapi(j,i,u,ST,SGM,FT,FGM,d,PGM)
                                updategapj(j,i,w, ST, SGJ, FT, FGJ, PGJ, e)
                                break
                        else:
                            jadwalujung(j,i,SGJ,e,SGM,d,ST,FT,T,OM,OJ)
                            updategapujung(j,i,ST,SGM,d,FGM,PGM,FT,e,SGJ,FGJ,PGJ)
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
                                    updategapi(j,i,u,ST,SGM,FT,FGM,d,PGM)
                                    updategapj(j,i,w, ST, SGJ, FT, FGJ, PGJ, e)
                                    break
                            if T[j,i]<= PGI:
                                break
                    else:
                        jadwalujung(j,i,SGJ,e,SGM,d,ST,FT,T,OM,OJ)
                        updategapujung(j,i,ST,SGM,d,FGM,PGM,FT,e,SGJ,FGJ,PGJ)

        MS= max(FT.values())

        if MS < MSIB: #update MSIB
            MSIB= MS
            IB= finished_cities_list
            SIB= Sn
            STB= ST
            FTB= FT

        makespanEnd = Time.time()
        iwdtimes.append(iwdEnd-iwdStart)
        makespantimes.append(chancetime-iwdStart)
        # print "IWD took {} seconds and makespan took {} seconds for this waterdrop.".format(iwdEnd-iwdStart, makespanEnd-iwdEnd)
        # print "waterdrop {} of iteration {} done.".format(n,iterasi)

    for q in range(count_finished-1): #update soil
        x= IB[q]
        y= IB[q+1]
        address = (x,y)
        # print(address)
        if address not in soils:
            address = (y,x)
        soils[address].soil = (1+ rhoiwd)* soils[address].soil - rhoiwd*(1/(J*I-1))*SIB

        # straightxIndex = allsoil.index((x,y))
        # revxIndex = allsoil.index((y,x))
        # soil[straightxIndex]= (1+ rhoiwd)* soil[straightxIndex]-rhoiwd*(1/(J*I-1))*SIB
        # soil[revxIndex]= soil[straightxIndex]

    # for soil_n in soils:
    #     print("soil for {}: {}".format(soil_n,soils[soil_n].soil))
    if MSIB< MSTB: #update MSTB
        MSTB= MSIB
        TB= IB
        STT= STB
        FTT= FTB
        best= iterasi
    print("iteration number {} done. MSIB: {}. Best: {}".format(iterasi, MSIB, MSTB))
# print("MSTB: {}".format(MSTB))
# print("TB: {}".format(TB))
print("Start time best: {}".format(STT))
print("Finish time best: {}".format(FTT))
print("best iteration: {}".format(best))

print("MSTB: {}".format(MSTB))
print("TB: {}".format(TB))
endTime = Time.time()
print("time elapsed: {}".format(endTime - startTime))
print("dice time max: {}".format(max(dicetime)))
print("iwd time max: {}".format(max(iwdtimes)))
print("makespan time max: {}".format(max(makespantimes)))
# print nodes
