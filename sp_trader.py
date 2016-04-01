from stratbox_api import MarketWatch
from CBOE_API import getLatest

def trade():
    # Grab CBOE Data
    cboe_data = getLatest() # <- TODO fix that function in lib

    # Initialize MarketWatch Trading component & login
    MarketWatchDriver = MarketWatch()
    MarketWatchDriver.login()
    available_balance = float(MarketWatchDriver.get_balance())

    # ETF data
    spxs_price = MarketWatchDriver.get_price("SPXS")
    spxl_price = MarketWatchDriver.get_price("SPXL")

    # Step 1
    # - Determine position: Long/Short based on percentage
    spx_allocation_centage = cboe_data["ratio"]*.10
    spx_cash_alloc = available_balance*spx_allocation_centage
    spx_share_alloc = int(spx_cash_alloc / spxs_price)


    if(float(cboe_data["ratio"]) > 1):
        decision = {"position":"long", "allocation":spx_share_alloc, "price":spxs_price}
    elif(float(cboe_data["ratio"]) < 1):
        decision = {"position":"short", "allocation":spx_share_alloc, "price":spxs_price}

    # - Determine magnitude: (need metric...)
    # - Determine SPXS/L weighting/allocation
    # - Allocate remaining capital*weight to SP500 companies

    # Step 2
    # Package {CBOE_data : dat, Portfolio : portfolio, Trades : [trades]} to be returned for webpage

    if(cboe_data["status"][0] == "open"):
        MarketWatchDriver.trade("SPXS",decision["position"],decision["allocation"])

    return {
        "CBOE_data" : cboe_data,
        "decision" : decision
    }
