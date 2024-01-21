import random
import smtplib
from datetime import datetime,timedelta
from exchange.models import EXCHANGE_NAME, getData, getDataByName
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pytz
import mpld3

class Email():
    
    def sendMessenger(self):
        
        address = 'smtp.yandex.com'
        port = 465
        login = 'HurtowniaDanych@yandex.com'
        appPassword = 'ohkkdbnwmynrpxqp'
        smtpObj = smtplib.SMTP_SSL(address, port)
        plot = Plot()
        fig = plot.GetPlot()
        
        print(smtpObj.login(login, appPassword))
        message = ""
        for i in plot.tab:
            print(i, plot.tab[i])
            message += i+"->Max:"+str(plot.tab[i][0]) + "Min: "+ str(plot.tab[i][1]) +"\n"
            
        
        msg = MIMEMultipart()
        msg['Subject'] = 'Wiadomosc od swiata'
        msg['From'] = 'HurtowniaDanych@yandex.com'
        msg['To'] = 'HurtowniaDanych@yandex.com'
        msg.attach(MIMEText(message))
        msg.attach(MIMEText(fig, 'html'))

        smtpObj.sendmail('HurtowniaDanych@yandex.com',
                    'HurtowniaDanych@yandex.com', msg.as_string()
                    )
        
        smtpObj.quit

class Plot():
    def FinMinAndMax(self, Array):
        max = None
        min = None
        for liczba in Array:
            if max is None or liczba > max:
                max = liczba
            if min is None or liczba < min:
                min = liczba
        return max, min
    
    def __init__(self) -> None:
        self.tab ={}
    
    def GetPlot(self)->str:
        date = datetime.today().date() - timedelta(days=30)
        ax:Axes
        fig, ax = plt.subplots()
        days = []
        for single_date in (date + timedelta(n) for n in range(30)):
            if(single_date.weekday()!=6 and single_date.weekday()!=5):
                days.append(single_date.strftime(r'%m-%d'))
        print(days)
        for i in EXCHANGE_NAME:
            exchange = getDataByName(date, i[0])
            exchange = exchange.order_by("date")
            values=[0.0]*len(days)
            for j in exchange:
                ind = days.index(j.date.strftime(r'%m-%d'))
                values[ind] = j.value
            self.tab[i[1]] = self.FinMinAndMax(values)
            ax.plot(days, values, label=i[1])
            
        ax.set_xticklabels(days)
        ax.set(xlabel='Dzień tygodnia', ylabel='Cena',
            title='Kursy walut')
        ax.legend()
        ax.grid()
        return mpld3.fig_to_html(fig)
