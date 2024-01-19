import matplotlib.pyplot as plt
import random
import smtplib

def FinMinAndMax(Array):
    max = None
    min = None
    for liczba in Array:
        if max is None or liczba > max:
            max = liczba
        if min is None or liczba < min:
            min = liczba
    return max, min

def sendMessenger(firstMinValue,firstMaxValue,secondMinValue,secondMaxValue):
    address = 'smtp.yandex.com'
    port = 465
    login = 'HurtowniaDanych@yandex.com'
    appPassword = 'ohkkdbnwmynrpxqp'
    smtpObj = smtplib.SMTP_SSL(address, port)

    print(smtpObj.login(login, appPassword))

    smtpObj.sendmail('HurtowniaDanych@yandex.com',
                 'HurtowniaDanych@yandex.com',
                 """Subject: Wiadomosc od swiata\n
                 Cenne informacje najniszy i najwyzszy kurs zanotowany dla pierwszej waluty to \n"""+ str(firstMinValue) +""" oraz """+ str(firstMaxValue) + """ A dla drugiej """ +str(secondMinValue) +""" oraz """+str(secondMaxValue))
    
    smtpObj.quit



days=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]


priceOneValues=[]
for i in range(30):
    priceOneValues.append(random.uniform(4.01, 4.43))
priceSecondValues=[]
for i in range(30):
    priceSecondValues.append(random.uniform(3.91, 4.14))
plt.plot(days,priceOneValues)
plt.plot(days,priceSecondValues)
plt.xlabel('Dzień tygodnia')
plt.ylabel('Cena')
plt.ylim(min(priceSecondValues),max(priceOneValues));
plt.title("Kursy walut")
firstMin,firstMax=FinMinAndMax(priceOneValues)
SecondMin,SecondMax=FinMinAndMax(priceSecondValues)
sendMessenger(round(firstMin, 2),round(firstMax,2),round(SecondMin,2),round(SecondMax,2))
plt.show()



