import random
import smtplib
from datetime import datetime,timedelta
from exchange.models import EXCHANGE_NAME, getData, getDataByName
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from matplotlib.figure import Figure
import matplotlib.dates as mdates

class Email():
    
    def sendMessenger(self):
        
        address = 'smtp.yandex.com'
        port = 465
        login = 'HurtowniaDanych@yandex.com'
        appPassword = 'ohkkdbnwmynrpxqp'
        smtpObj = smtplib.SMTP_SSL(address, port)
        plot = Plot()
        fig = plot.GetPlot()
        plot_filename = 'sin_wave_plot.png'
        fig.savefig(plot_filename)
        print(smtpObj.login(login, appPassword))
        message = ""
        for i in plot.tab:
            print(i, plot.tab[i])
            message += i+"->Max:"+str(plot.tab[i][0])+" Min:"+str(plot.tab[i][1])+"\n"
            
        
        msg = MIMEMultipart()
        msg['Subject'] = 'Wiadomosc od swiata'
        msg['From'] = 'HurtowniaDanych@yandex.com'
        msg['To'] = 'HurtowniaDanych@yandex.com'
        msg.attach(MIMEText(message))

        with open(plot_filename, 'rb') as attachment:
            image = MIMEImage(attachment.read())
            image.add_header('Content-Disposition', f'attachment; filename={plot_filename}')
            msg.attach(image)
            
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
    
    def GetPlot(self)->Figure:
        date = datetime.today().date() - timedelta(days=30)
        ax:Axes
        fig, ax = plt.subplots()
        days2 = []
        days = []
        for single_date in (date + timedelta(n) for n in range(31)):
            days.append(single_date.strftime(r'%Y-%m-%d'))
            days2.append(single_date)
        print(days)
        for i in EXCHANGE_NAME:
            exchange = getDataByName(date, i[0])
            exchange = exchange.order_by("date")
            values=[0.0]*len(days)
            print(len(exchange))
            for j in exchange:
                ind = days.index(j.date.strftime(r'%Y-%m-%d'))
                values[ind] = j.midValue
            print(days, values)
            result=[]
            daysResult=[]
            for j in range(len(values)):
                daysResult.append(days[j])
                if values[j]!=0.0:
                    result.append(values[j])
                elif j>0:
                    result.append(result[j-1])
                else:
                    k= j+1
                    while values[k]==0:
                        k+=1
                    result.append(values[k+1])
            print(daysResult, result)
            
            self.tab[i[1]] = self.FinMinAndMax(result)
            ax.plot(days2, result, label=i[1])
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.set(xlabel='Dzień tygodnia', ylabel='Cena',
            title='Kursy walut')
        ax.legend()
        ax.grid()
        return fig
