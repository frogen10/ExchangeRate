import random
import smtplib

class Email():

    def sendMessenger(self, firstMinValue,firstMaxValue,secondMinValue,secondMaxValue):
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