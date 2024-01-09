import matplotlib.pyplot as plt
import django
import random

print( django.get_version())

days=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]


priceOneValues=[]
for i in range(30):
    priceOneValues.append(random.uniform(4.01, 4.43))
priceSecondValues=[]
for i in range(30):
    priceSecondValues.append(random.uniform(3.91, 4.14))
plt.plot(days,priceOneValues)
#plt.plot(days,priceOneValues,'ro')
plt.plot(days,priceSecondValues)
#plt.plot(days,priceSecondValues,'go')
plt.xlabel('Dzień tygodnia')
plt.ylabel('Cena')

plt.ylim(min(priceSecondValues),max(priceOneValues));
plt.title("Kursy walut")

plt.show()

