from stratbox_api import MarketWatch

# Initialize MarketWatch Trading component & login
MarketWatchDriver = MarketWatch()
MarketWatchDriver.login()
available_balance = MarketWatchDriver.get_balance()
