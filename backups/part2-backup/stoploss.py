import logging
import time
from typing import List
from optibook import common_types as t
from optibook import ORDER_TYPE_IOC, ORDER_TYPE_LIMIT, SIDE_ASK, SIDE_BID
from optibook.exchange_responses import InsertOrderResponse
from optibook.synchronous_client import Exchange
import random
import json

#INSTRUMENTS_ID = ["C1_FOSSIL_FUEL_ETF", "C1_GAS_INC", "C1_OIL_CORP"]
INSTRUMENTS_ID = "C2_GREEN_ENERGY_ETF"

#C1_FOSSIL_FUEL_ETF, C1_GAS_INC, C1_OIL_CORP

e = Exchange()
e.connect()

basket_book = e.get_last_price_book(INSTRUMENTS_ID)
basket_ask_price = basket_book.asks[0].price
basket_bid_price = basket_book.bids[0].price
average_val = (basket_ask_price + basket_bid_price) / 2

def stoploss(price, stoploss_val):
    if average_val < price*(1-stoploss_val):
        reset_position()

def takeprofit(price, takeprofit_val):
    if average_val > price*(1+takeprofit_val):
        reset_position()
    
def reset_position():
    part2.setRunning(False)
    for INSTRUMENT_ID in INSTRUMENTS_ID:
        positions = e.get_positions()
        while positions[INSTRUMENT_ID] != 0:

            positions = e.get_positions()
            print(positions)

            if positions[INSTRUMENT_ID] < 0:
                BUY = True
            elif positions[INSTRUMENT_ID] > 0:
                BUY = False
            else:
                continue

            if BUY:
                SIDE = SIDE_BID
                price = e.get_last_price_book(INSTRUMENT_ID).asks[0].price
            else:
                SIDE = SIDE_ASK
                price = e.get_last_price_book(INSTRUMENT_ID).bids[0].price

            volume = abs(positions[INSTRUMENT_ID])
            print("Volume: ", volume)
            bid_response: InsertOrderResponse = e.insert_order(INSTRUMENT_ID, price=price, volume=volume, side=SIDE, order_type=ORDER_TYPE_IOC)
            print(bid_response)
            time.sleep(1)
            print("Position: ", positions[INSTRUMENT_ID])
            
        else:
            print(f"Position of '{INSTRUMENT_ID}' is 0")
