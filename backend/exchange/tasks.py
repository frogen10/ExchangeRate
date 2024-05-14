
from exchange.models import EXCHANGE_NAME, EXCHANGE_TYPE, getDataByDate, getDataByTypeName,Exchange
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
    for i in EXCHANGE_NAME[1:]:
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
    for i in EXCHANGE_NAME[1:]:
        try:
            end_date: datetime
            end_date = datetime.today().date()
            start_date = end_date- timedelta(days=30)
            
            delta = timedelta(days=1)
            print(start_date,end_date)
            while start_date <= end_date:
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
    exchange = getDataByTypeName(EXCHANGE_NAME[0][0], 1)
    if(exchange.count()<1):
        try:
            exchange = Exchange(name=EXCHANGE_NAME[0][0], midValue=1, bidValue=1, askValue=1, date=datetime.today().date())
            exchange.save()
        except Exception as ex:
            print("Exception: ", ex)
    
            
