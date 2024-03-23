from django.db import models
import requests
from exchange.models import Exchange
from datetime import datetime

class NBP():
    def get(self, value= "USD", date = datetime.today()) ->Exchange:
        ''' Pobieranie danych z API
        # http://api.nbp.pl/
        response = requests.get("https://example.com/api/v1/data")
        
        #Tabele mogą być typu A, B, C
        
        http://api.nbp.pl/api/exchangerates/rates/{table}/{code}/
        # dla EUR
        response_eur = requests.get("http://api.nbp.pl/api/exchangerates/rates/A/EUR/?format=json")
        # dla GBP
        response_gbp = requests.get("http://api.nbp.pl/api/exchangerates/rates/A/GBP/?format=json")
        # dla CHF
        response_chf = requests.get("http://api.nbp.pl/api/exchangerates/rates/A/CHF?format=json")
        '''
        site =f"http://api.nbp.pl/api/exchangerates/rates/A/{value}/{date.strftime(r'%Y-%m-%d')}?format=json"
        print(site)
        response = requests.get(site)
        if response.status_code == 200:
            # Dane zostały pomyślnie pobrane
            data = response.json()
        else:
            # Błąd podczas pobierania danych
            raise Exception(response.status_code)

        # Przetwarzenie danych z API (tutaj napisać)
        # ...

        # Zwróc dane klientowi
        
        dat = datetime.strptime(data["rates"][0]["effectiveDate"], r"%Y-%m-%d")
        val = data["rates"][0]["mid"]
        exchange = Exchange(name=value, value = val, date = dat.date())
        return exchange

        
    
    #W powyższym przykładzie, dane z API są przetwarzane w metodzie get() widoku. 
    #Metoda get() przyjmuje jako argumenty obiekt request oraz dowolne dodatkowe argumenty,
    # które zostały przekazane podczas wywoływania widoku.
    
    
    #KOMUNIKATY BLEDOW:
    # 404 Not Found - poprawny zakres czasowy, lecz brak danych
    # 400 Bad Request - Nieprawidlowe zapytanie
    # 400 Bad Request -  Przekroczony Limit - przekracza limit zwracanych danych