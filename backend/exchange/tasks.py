
from exchange.models import EXCHANGE_NAME, getDataByDate
from exchange.email import Email, Plot
from exchange.api import NBP
from kernel.celery import app
from datetime import datetime, timedelta
import pytz

@app.task
def sendEmail():
    try:
        emailer = Email() 
        emailer.sendMessenger()
    except Exception as ex:
        print("Exception: ", ex)

@app.task
def getData():
    api = NBP()
    for i in EXCHANGE_NAME:
        try:
            if datetime.now().weekday()==5 or datetime.now().weekday()==6:
                break
            ex = api.get(i[0])
            ex.save()
        except Exception as ex:
            print("Exception: ", ex)

@app.task
def checkData():
    api = NBP()
    for i in EXCHANGE_NAME:
        try:
            end_date: datetime
            end_date = datetime.today().date()
            start_date = end_date- timedelta(days=30)
            
            delta = timedelta(days=1)
            print(start_date,end_date)
            while start_date <= end_date:
                if start_date.weekday()!=5 and start_date.weekday()!=6:
                    data = getDataByDate(start_date,i[0])
                    if data.count()<1:
                        try:
                            exchange = api.get(i[0], start_date)
                            exchange.save()
                        except Exception as ex:
                            print("Exception: ", ex)
                start_date += delta
        except Exception as ex:
            print("Exception: ", ex)