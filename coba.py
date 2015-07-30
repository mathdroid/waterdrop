J = int(input("Jumlah job: "))
I = int(input("Jumlah mesin: "))
T = { }
for a in range(J):
    for b in range(I):
        T[a,b] = int(input((a+1,b+1)))


BSA = [ ]
for a in range (J):
    for b in range (I):
        BSA.append((a+1,b+1))
print ("Node yang mungkin dilalui: ", BSA)


allsoil= [ ]
soilxy= [ ]
for a in range(len(BSA)-1):
    for b in range(a+1,len(BSA)):
        x= BSA[a]
        y= BSA[b]
        allsoil.append((x,y))
        allsoil.append((y,x))
print (allsoil)
for a in range(len(allsoil)):
    b = 10000
    soilxy.append(b)
print (soilxy)
