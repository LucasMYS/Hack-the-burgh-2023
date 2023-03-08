'''
Part 2 (Not SubZero)
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
TRADING_VOLUME = 5
SMALL = 0.01


def create_basket_ask(e, ask_price, volume):
    ask_response: InsertOrderResponse = e.insert_order(BASKET_INSTRUMENT_ID, price=ask_price, volume=TRADING_VOLUME, side=SIDE_ASK, order_type=ORDER_TYPE_LIMIT)
    
def create_basket_bid(e, bid_price, volume):
    bid_response: InsertOrderResponse = e.insert_order(BASKET_INSTRUMENT_ID, price=bid_price, volume=TRADING_VOLUME, side=SIDE_BID, order_type=ORDER_TYPE_LIMIT)


def is_basket_bought(e, basket_book, last_price, trades):
    outstanding_orders = e.get_outstanding_orders(BASKET_INSTRUMENT_ID)
    outstanding_orders_values = list(outstanding_orders.values())
    print("Order: ", outstanding_orders_values)
    if len(outstanding_orders) != 0:
        for outstanding_order in outstanding_orders_values:
            if outstanding_order.side == "bid":
                print("Order volume: ", outstanding_orders_values[0].volume)
    
    
    print("Sellers: ", end="")
    print([trade.seller for trade in trades])
    if last_price == "":
        return {"happened": False}
    amount_traded = TRADING_VOLUME - outstanding_orders_values[0].volume
    if amount_traded != 0:
        return {"happened": True, "volume": trade.volume}
    return {"happened": False}

def is_basket_sold(e, basket_book, last_price, trades):
    outstanding_orders = e.get_outstanding_orders(BASKET_INSTRUMENT_ID)
    outstanding_orders_values = list(outstanding_orders.values())
    print("Order: ", outstanding_orders_values)
    if len(outstanding_orders) != 0:
        for outstanding_order in outstanding_orders_values:
            if outstanding_order.side == "ask":
                print("Order volume: ", outstanding_orders_values[0].volume)
    
    
    print("Sellers: ", end="")
    print([trade.seller for trade in trades])
    amount_traded = TRADING_VOLUME - outstanding_orders_values[0].volume
    if amount_traded != 0:
        return {"happened": True, "volume": trade.volume}
    return {"happened": False}


def buy_stock(volume):
    while volume > 0:
        stock_books = [e.get_last_price_book(ID) for ID in STOCK_INSTRUMENT_IDS]
        stock_ask_prices = [(stock_book).asks[0].price for stock_book in stock_books]
        
        ask_response1: InsertOrderResponse = e.insert_order(STOCK_INSTRUMENT_IDS[0], price=stock_ask_prices[0], volume=volume, side=SIDE_BID, order_type=ORDER_TYPE_IOC)
        if not ask_response1:
            print("Trade failed")
        if verbose:
            print(f"Bought: '{STOCK_INSTRUMENT_IDS[0]}' for '{stock_ask_prices[0]}'")

        ask_response2: InsertOrderResponse = e.insert_order(STOCK_INSTRUMENT_IDS[1], price=stock_ask_prices[1], volume=basket_volume/2, side=SIDE_BID, order_type=ORDER_TYPE_IOC)
        if not ask_response2:
            print("Trade failed")
        if verbose:
            print(f"Bought: '{STOCK_INSTRUMENT_IDS[1]}' for '{stock_ask_prices[1]}'")
        if verbose:
            print(f"Bought: Stocks for '{0.5 * sum(stock_ask_prices)}'")


def trade_cycle(e: Exchange, prices_used):
    basket_book = e.get_last_price_book(BASKET_INSTRUMENT_ID)
    trades = e.poll_new_trade_ticks(BASKET_INSTRUMENT_ID)
    
    ask_price = basket_book.asks[0].price - SMALL
    bid_price = basket_book.bids[0].price + SMALL
    
    print(basket_book)
    
    basket_bought = is_basket_bought(e, basket_book, prices_used["price_bought"], trades)
    print(basket_bought)
    if basket_bought["happened"]:
        sell_stock(basket_bought["volume"])
        
    basket_sold = is_basket_sold(e, basket_book, prices_used["price_sold"], trades)
    print(basket_sold)
    if basket_sold["happened"]:
        buy_stock(basket_sold["volume"])
    
    e.delete_orders(BASKET_INSTRUMENT_ID)
    create_basket_ask(e, ask_price, TRADING_VOLUME)
    create_basket_bid(e, bid_price, TRADING_VOLUME)