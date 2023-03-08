'''
Part 2 (Lucas)
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

logging.getLogger('client').setLevel('ERROR')
logger = logging.getLogger(__name__)



BASKET_INSTRUMENT_ID = 'C2_GREEN_ENERGY_ETF'
STOCK_INSTRUMENT_IDS = ['C2_SOLAR_CO', 'C2_WIND_LTD']
TRADING_VOLUME = 50


Diff = 0.05 #can make it larger to have the largest or smallest value

'''
def spread(basket_book):
    basket_largest_bid = basket_book.bids[0].price
    basket_smallest_ask = basket_book.asks[0].price

    diff =  basket_largest_bid - basket_smallest_ask
    if diff > 0 :
        return "Postive"
    elif diff < 0:
        return "Negative"
    else :
        return "Equal"
'''    


def action(e,basket_book):
    basket_largest_bid = basket_book.bids[0].price
    basket_smallest_ask = basket_book.asks[0].price
    
    asks_Volume = basket_book.asks[0].volume
    
    diff =  basket_smallest_ask - basket_largest_bid 
    
    if asks_Volume >= 0 and diff > 0: 

        bid_response: InsertOrderResponse = e.insert_order(BASKET_INSTRUMENT_ID, price=basket_largest_bid + Diff, volume=TradingVolume, side=SIDE_BID, order_type=ORDER_TYPE_LIMIT)
        print(f"Buy: '{BASKET_INSTRUMENT_ID}' for '{basket_largest_bid + Diff}'")
        
        ask_response: InsertOrderResponse = e.insert_order(BASKET_INSTRUMENT_ID, price=basket_smallest_ask - Diff, volume=TradingVolume, side=SIDE_ASK, order_type=ORDER_TYPE_LIMIT)
        print(f"Sold: '{BASKET_INSTRUMENT_ID}' for '{basket_smallest_ask - Diff}'")
    
    elif diff <0:
        pass
    
    else:
        diff == 0
        pass
  
        

def trade_cycle(e: Exchange):
    basket_book = e.get_last_price_book(BASKET_INSTRUMENT_ID)
    action(e,basket_book)

    
 
 
 '''
 Idea behind this is find the current largest bid and smallest asks
 Then calculate the diff of the two values
 If postive meaning it is doable:
 1.Buy in the bid with the largest price 
 2.Sell the asks with smallest price
 3 Repeat and repeat
 
 If negative do nothing
 
"""
    
       

'''
def create_basket_ask(basket_book, volume):
    ask_price = basket_book.bids[0].price - SMALL
    ask_response: InsertOrderResponse = e.insert_order(BASKET_INSTRUMENT_ID, price=ask_price, volume=TRADING_VOLUME, side=SIDE_ASK, order_type=ORDER_TYPE_LIMIT)
    
def create_basket_bid(basket_book, volume):
    bid_price = basket_book.bids[0].price + SMALL
    bid_response: InsertOrderResponse = e.insert_order(BASKET_INSTRUMENT_ID, price=bid_price, volume=TRADING_VOLUME, side=SIDE_BID, order_type=ORDER_TYPE_LIMIT)
'''