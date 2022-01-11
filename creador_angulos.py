import csv

f = open('tabla.csv','a')
for a in range(10):
    f.write("{},{}\n".format(a*0.1,a*0.1))
f.close()


f = open('tabla.csv','r')

mensaje = csv.reader(f)

for linea in mensaje:
    print("{} , {}".format(float(linea[0]),float(linea[1])))
