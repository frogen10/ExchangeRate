from django.db import models
import requests


class MyView():
    def get(self, value = "USD") ->float:
        ''' Pobieranie danych z API
        # http://api.nbp.pl/
        response = requests.get("https://example.com/api/v1/data")
        
        #Tabele mogą być typu A, B, C
        
        http://api.nbp.pl/api/exchangerates/rates/{table}/{code}/
        # dla PLN
        response_pln = requests.get("http://api.nbp.pl/api/exchangerates/rates/A/PLN/")     
        # dla EUR
        response_eur = requests.get("http://api.nbp.pl/api/exchangerates/rates/A/EUR/")
        # dla GBP
        response_gbp = requests.get("http://api.nbp.pl/api/exchangerates/rates/A/GBP/")
        # dla CHF
        response_chf = requests.get("http://api.nbp.pl/api/exchangerates/rates/A/CHF?format=json")
        '''
        # dla USD
        response = requests.get(f"http://api.nbp.pl/api/exchangerates/rates/B/{value}?format=json")
        if response.status_code == 200:
            # Dane zostały pomyślnie pobrane
            data = response.json()
        else:
            # Błąd podczas pobierania danych
            raise Exception(response.status_code)

        # Przetwarzenie danych z API (tutaj napisać)
        # ...

        # Zwróc dane klientowi
        return data["rates"][0]["mid"]
    
    
    #W powyższym przykładzie, dane z API są przetwarzane w metodzie get() widoku. 
    #Metoda get() przyjmuje jako argumenty obiekt request oraz dowolne dodatkowe argumenty,
    # które zostały przekazane podczas wywoływania widoku.
    
    
    #KOMUNIKATY BLEDOW:
    # 404 Not Found - poprawny zakres czasowy, lecz brak danych
    # 400 Bad Request - Nieprawidlowe zapytanie
    # 400 Bad Request -  Przekroczony Limit - przekracza limit zwracanych danych