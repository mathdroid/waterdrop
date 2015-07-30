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
print(T)
y = np.arange(35).reshape(5,7)
print(y)
