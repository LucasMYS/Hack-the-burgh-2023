'''
Part 2 (SubZero)
'''
import logging
import time
from typing import List
from optibook import common_types as t
from optibook import ORDER_TYPE_IOC, ORDER_TYPE_LIMIT, SIDE_ASK, SIDE_BID
from optibook.exchange_responses import InsertOrderResponse
from optibook.synchronous_client import Exchange
import random
import json
import stoploss

logging.getLogger('client').setLevel('ERROR')
logger = logging.getLogger(__name__)

BASKET_INSTRUMENT_ID = 'C2_GREEN_ENERGY_ETF'

def isNotRunning():
    if isNotRunning:
        return True
    else:
        return False
        
def setNotRunning(boolean):
    isNotRunning = boolean
    
def setPrice(num):
    price = num
    
def trade_cycle(e: Exchange):
    basket_book = e.get_last_price_book(BASKET_INSTRUMENT_ID)
    
    if basket_book and basket_book.bids and basket_book.asks:
        
        highestbid = basket_book.bids[0].price
        lowestask = basket_book.asks[0].price
        bidaskspread = (lowestask - highestbid)/highestbid
        
        #Maximum bid ask spread as % of price, so 0.005 is 0.5%
        bspread = 0.005
        #Spread for the bid and ask orders as %, so 0.1 is 10%
        spreadnum = 0.1
        #stop loss as %, so 0.1 is 10%
        stoplossnum = 0.1
        #take profit as %, so 0.1 is 10%
        takeprofitnum = 0.1
        
        if (highestbid < bspread) and (isNotRunning):
            
            spread = spreadnum*(lowestask+highestbid)/2
            basket_bid_price = highestbid*(1+spread)
            basket_ask_price = lowestask*(1-spread)
            setPrice((basket_ask_price+basket_ask_price)/2)
            
            bid_response: InsertOrderResponse = e.insert_order(BASKET_INSTRUMENT_ID, price=basket_bid_price, volume=100, side=SIDE_ASK, order_type=ORDER_TYPE_LIMIT)
            if not bid_response:
                print("Trade failed")
            print(f"Sold: '{BASKET_INSTRUMENT_ID}' for '{basket_bid_price}'")
                
            ask_response: InsertOrderResponse = e.insert_order(BASKET_INSTRUMENT_ID, price=basket_ask_price, volume=100, side=SIDE_BID, order_type=ORDER_TYPE_LIMIT)
            if not ask_response:
                print("Trade failed")
            print(f"Bought: '{BASKET_INSTRUMENT_ID}' for '{basket_ask_price}'")
                
            isNotRunning = False
            
        try:
            stoploss.stoploss(price, stoplossnum)
            stoploss.takeprofit(price, takeprofitnum)
        except NameError:
            pass