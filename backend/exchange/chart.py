from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from .models import Exchange, EXCHANGE_NAME, getDataByName, getDataByDate
COLORS = ["Red", "Blue", "Green", "Yellow", "Orange", "Purple", "GOLD", "Pink", "Brown"]


now = datetime.now().date()

LABELS = {
    "1D": [(now - timedelta(hours=i)).strftime('%I:%M%p') for i in range(24)],
    "1W": [(now - timedelta(days=i)).strftime('%m-%d-%Y') for i in range(7)],
    "1M": [(now - timedelta(days=i)).strftime('%m-%d-%Y') for i in range(30)],
    "1Y": [(now - relativedelta(months=i)).strftime('%m-%Y') for i in range(12)],
    "5Y": [(now - relativedelta(months=i)).strftime('%Y-%m') for i in range(0, 60, 3)],
}
DAYS = {
    "1D": [(now - timedelta(hours=i))for i in range(24)],
    "1W": [(now - timedelta(days=i)) for i in range(7)],
    "1M": [(now - timedelta(days=i)) for i in range(30)],
    "1Y": [(now - relativedelta(months=i)) for i in range(12)],
    "5Y": [(now - relativedelta(months=i)) for i in range(0, 60, 3)],
}

class Chart():
    labels = []
    values = []
    label=""
    color=""
    def __init__(self, fromCurrencyName:str, toCurrencyName: str, day:str) -> None:
        for i in range(len(EXCHANGE_NAME)):
            if(EXCHANGE_NAME[i][0] == fromCurrencyName):
                self.color = COLORS[i]
                self.label = EXCHANGE_NAME[i][1]
                break
        self.label = LABELS[day]
        days = DAYS[day]
        for i in days:
            try:
                fromCurrency = getDataByName(i, fromCurrencyName)[0]
                toCurrency = getDataByName(i, toCurrencyName)[0]
                self.values.append((1 * fromCurrency.askValue / toCurrency.bidValue))
            except:
                self.values.append(0)