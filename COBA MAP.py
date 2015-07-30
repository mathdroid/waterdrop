I= 3
J= 3
SGMA= { }
for q in range(1,I+1): #buat ngeset OM=0
    SGMA[q,1]= 0

print("SGMA",SGMA)

SGM= dict(SGMA)


del SGM[1,1]
print("SGM",SGM)
print("SGMA",SGMA)
