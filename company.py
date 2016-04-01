import finsymbols
from stratbox_api import MarketWatch
from datetime import datetime

class Company(object):
    def __init__(self, name, ticker, price, beta="N/A", marketcap="N/A", sentiment="N/A"):
        self.name = name
        self.ticker = ticker
        self.price = price
        self.beta = beta
        self.marketcap = marketcap
        self.sentiment = sentiment

# TODO move to data scraping lib...
# Returns dictionary of tickers and company objects
def compileSPY():
    totaltime = datetime.now()-datetime.now()
    count = 0

    driver = MarketWatch()

    SPY = finsymbols.get_sp500_symbols()
    for ticker in SPY:
        # Time testing
        start=datetime.now()

        company_name = str(ticker['company'].decode("utf8"))
        symbol = str(ticker['symbol'].decode("utf8"))
        current_price = driver.get_price(symbol)
        current_marketcap = driver.get_marketcap(symbol)
        firm = Company(company_name,symbol,current_price,current_marketcap)

        # Time testing
        endtime = datetime.now()-start
        totaltime += endtime
        count+=1

        print(firm.name,",",firm.ticker,",",firm.price,",",firm.marketcap,",",endtime)

    print("=== runtime ===")
    print("Total:",totaltime)
    print("Avg:",totaltime/count)


compileSPY()
