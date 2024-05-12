from django.db import models
import requests
from exchange.models import Exchange
from datetime import datetime

class NBP():
    def get(self, value= "USD", date = datetime.today()) -> Exchange:
        ''' Pobieranie danych z API
        # http://api.nbp.pl/
        
        #Tabela A
        
        http://api.nbp.pl/api/exchangerates/rates/{table}/{code}/
        # dla EUR
        response_eur = requests.get("http://api.nbp.pl/api/exchangerates/rates/A/EUR/?format=json")
        '''
        site = f"http://api.nbp.pl/api/exchangerates/rates/A/{value}/{date.strftime(r'%Y-%m-%d')}?format=json"
        site2 = f"http://api.nbp.pl/api/exchangerates/rates/C/{value}/{date.strftime(r'%Y-%m-%d')}?format=json"
        print(site)
        response = requests.get(site)
        if response.status_code == 200:
            # Dane zostały pomyślnie pobrane
            data = response.json()
        else:
            # Błąd podczas pobierania danych
            raise Exception(response.status_code)
        
        dat = datetime.strptime(data["rates"][0]["effectiveDate"], r"%Y-%m-%d")
        midVal = data["rates"][0]["mid"]
        
        response = requests.get(site2)
        if response.status_code == 200:
            # Dane zostały pomyślnie pobrane
            data = response.json()
        else:
            # Błąd podczas pobierania danych
            raise Exception(response.status_code)
        bidValue = data["rates"][0]["bid"]
        askValue = data["rates"][0]["ask"]
        exchange = Exchange(name=value, midValue=midVal, bidValue=bidValue, askValue=askValue, date=dat)
        return exchange