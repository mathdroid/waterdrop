#BUAT INPUT
print("START INISIALISASI PARAMETER MASALAH")
J = int(input("Jumlah job: "))
I = int(input("Jumlah mesin: "))
T = { }
for a in range(1,J+1):
    for b in range(1,I+1):
        T[a,b] = int(input((a,b)))
print ("T =",T)
print("END INISIALISASI PARAMETER MASALAH")
print(" ")
