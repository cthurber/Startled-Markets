from flask import Flask
from splinter import Browser
from selenium import webdriver
from bs4 import BeautifulSoup
import time
# from splinter.driver.zopetestbrowser import ZopeTestBrowser

# _DRIVERS['zope.testbrowser'] = ZopeTestBrowser
driver = webdriver.PhantomJS(executable_path="/Applications/phantomjs.app/Contents/MacOS/phantomjs")
gameRoot = "http://www.marketwatch.com/game/2016-drew-wall-street-semester-game"
Name = "Chris Thurber"
class MarketWatch(object):
    def __init__(self):
        self.browser = Browser(driver)

    def read_loginfo(self):
        with open('.loginfo') as loginfo:
            email = loginfo.readline()
            password = loginfo.readline()
            credentials = [email,password]
        loginfo.close()
        return credentials

    def login(self):
        # Login to MarketWatch
        login_url = "https://id.marketwatch.com/access/50eb2d087826a77e5d000001/latest/login_standalone.html"
        self.browser.visit(login_url)
        print(self.browser.html)
        self.browser.fill('username', self.read_loginfo()[0])
        self.browser.fill('password', self.read_loginfo()[1])
        login_button = self.browser.find_by_id('submitButton')
        login_button.click()
        time.sleep(2)
        return True

    def get_balance(self):
        try:
            self.login()
            self.browser.visit(gameRoot+"/portfolio")
            portfolio_page = BeautifulSoup(self.browser.html, "html.parser")
            balance = float(str(portfolio_page.find("span", {"class" : "data"}).text).lstrip("$").replace(',',''))
            return balance
        except:
            self.login()
            self.get_balance()

    def get_ticker(self,symbol):
        symbol = symbol.upper()
        return 1

    def get_price(self,symbol):
        symbol = symbol.upper()
        try:
            # Get potential short positions
            self.browser.visit(gameRoot+"/trade")
            symbol_lookup = self.browser.find_by_value("Enter company name or symbol")
            symbol_lookup.fill(symbol)
            self.browser.find_by_tag("button")[2].click()
            time.sleep(1)
            results = BeautifulSoup(self.browser.html, "html.parser")
            symbol = results.find("div", {'class' : 'chips'})
            if len(symbol) >= 2:
                price = str(results.find("p", {'class' : 'last'}).text).rstrip('\n').lstrip("\n$").replace(',','')
                return price
        except:
            self.login()
            self.get_price(symbol)

    def trade(self,symbol,position,shares,order_type=["market"]):
        symbol = symbol.upper()
        shares = int(shares)

        # try:
        # Get stock
        price = self.get_price(symbol)
        trade_button = self.browser.find_by_css("button.trade")
        trade_button.click()
        time.sleep(1)

        # Determine position
        if (position == "long"):
            long_button = self.browser.find_by_text("Buy")
            long_button.click()
        elif (position == "short"):
            short_button = self.browser.find_by_text("Sell Short")
            short_button.click()
        else:
            print("Error, position not specified. Must be 'long' or 'short'")
            return False

        # TODO order types should be dicts
        # Determine order_type
        if (order_type[0] == "market"):
            market_order = self.browser.find_by_text("Market")
            market_order.click()
        elif (order_type[0] == "limit"):
            limit_order = self.browser.find_by_css("span.option")
            limit_order.click()
            time.sleep(1)
            limit_amount = self.browser.find_by_css("input.monetary")
            limit_amount.fill(str(order_type[1]))
        elif (order_type[0] == "stop"):
            stop_order = self.browser.find_by_css("span.option")[1]
            stop_order.click()
            time.sleep(1)
            stop_amount = self.browser.find_by_css("input.monetary")[1]
            stop_amount.fill(str(order_type[1]))
        else:
            print("Error, order not specified. Must be 'market', 'limit', or 'stop'")
            return False

        # Count shares
        share_slider = self.browser.find_by_value("0")
        share_slider.fill(shares)
        time.sleep(1)

        # Execute Order
        submit_order = self.browser.find_by_text("Submit Order")
        submit_order.click()
        verfiy_trade = self.browser.find_by_text("Your order was submitted successfully")
        while len(verfiy_trade) <= 0:
            submit_order = self.browser.find_by_text("Submit Order")
            submit_order.click()
            time.sleep(1)
        time.sleep(2)
        print("Ordered",shares,"shares of",symbol,position,"@",price,end=" ")
        if len(order_type) > 1:
            print(order_type[0],":",order_type[1])
        else:
            print("\n")
        return True
        # except:
            # self.login()
            # self.trade(symbol,position,shares,order_type)
#
# MW_Driver = MarketWatch()
# print(MW_Driver.get_balance())
# MW_Driver.trade("spxs","long",1,["stop","18.80"])
