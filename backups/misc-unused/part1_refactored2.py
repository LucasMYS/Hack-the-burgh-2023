'''
Part 1 implementation
'''

import logging
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

MAX_TRANSACT_SIZE = 500
MAX_PER_INSTRUMENT = 500


def print_order_response(order_response: InsertOrderResponse):
    if order_response.success:
        logger.info(f"Inserted order successfully, order_instrument='{order_response.instrument_id}', order_price='{order_response.price}'")
    else:
        logger.info(f"Unable to insert order with reason: '{order_response.success}'")


def get_hedge_positions(e):
    positions = e.get_positions()
    return [0.5 * positions[BASKET_INSTRUMENT_ID] + positions[ID] for ID in STOCK_INSTRUMENT_IDS]


def sell_basket_buy_stock(e, basket_volume, basket_bid_price, stock_ask_prices, verbose=True):
    basket_volume = (basket_volume//2)*2
    
    bid_response: InsertOrderResponse = e.insert_order(BASKET_INSTRUMENT_ID, price=basket_bid_price, volume=basket_volume, side=SIDE_ASK, order_type=ORDER_TYPE_IOC)
    if not bid_response:
        print("Trade failed")
    if verbose:
        print(f"Sold: '{BASKET_INSTRUMENT_ID}' for '{basket_bid_price}'")

    ask_response1: InsertOrderResponse = e.insert_order(STOCK_INSTRUMENT_IDS[0], price=stock_ask_prices[0], volume=basket_volume/2, side=SIDE_BID, order_type=ORDER_TYPE_IOC)
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
    
    
def buy_basket_sell_stock(e, basket_volume, basket_ask_price, stock_bid_prices, verbose=True):
    basket_volume = (basket_volume//2)*2
    
    bid_response: InsertOrderResponse = e.insert_order(BASKET_INSTRUMENT_ID, price=basket_ask_price, volume=basket_volume, side=SIDE_BID, order_type=ORDER_TYPE_IOC)
    if not bid_response:
        print("Trade failed")
    if verbose:
        print(f"Bought: '{BASKET_INSTRUMENT_ID}' for '{basket_ask_price}'")
        
    ask_response1: InsertOrderResponse = e.insert_order(STOCK_INSTRUMENT_IDS[0], price=stock_bid_prices[0], volume=basket_volume/2, side=SIDE_ASK, order_type=ORDER_TYPE_IOC)
    if not ask_response1:
        print("Trade failed")
    if verbose:
        print(f"Sold: '{STOCK_INSTRUMENT_IDS[0]}' for '{stock_bid_prices[0]}'")
        
    ask_response2: InsertOrderResponse = e.insert_order(STOCK_INSTRUMENT_IDS[1], price=stock_bid_prices[1], volume=basket_volume/2, side=SIDE_ASK, order_type=ORDER_TYPE_IOC)
    if not ask_response2:
        print("Trade failed")
    if verbose:
        print(f"Sold: '{STOCK_INSTRUMENT_IDS[1]}' for '{stock_bid_prices[1]}'")
    if verbose:
        print(f"Sold: Stocks for '{0.5 * sum(stock_bid_prices)}'")
        

def trade_cycle(e: Exchange, verbose=True):
    basket_book = e.get_last_price_book(BASKET_INSTRUMENT_ID)
    stock_books = [e.get_last_price_book(ID) for ID in STOCK_INSTRUMENT_IDS]
    
    if basket_book and basket_book.bids and basket_book.asks and stock_books[0] and stock_books[1] and stock_books[0].bids and stock_books[0].asks and stock_books[1].bids and stock_books[1].asks:
        
        basket_book = e.get_last_price_book(BASKET_INSTRUMENT_ID)
        stock_books = [e.get_last_price_book(ID) for ID in STOCK_INSTRUMENT_IDS]
        
        basket_ask_price = basket_book.asks[0].price
        basket_bid_price = basket_book.bids[0].price
        stock_bid_prices = [(stock_book).bids[0].price for stock_book in stock_books]
        stock_ask_prices = [(stock_book).asks[0].price for stock_book in stock_books]
        
        basket_ask_volume = basket_book.asks[0].volume
        basket_bid_volume = basket_book.bids[0].volume
        stock_bid_volumes = [stock_book.bids[0].volume for stock_book in stock_books]
        stock_ask_volumes = [stock_book.asks[0].volume for stock_book in stock_books]
        
        if verbose:
            print("Basket ask price: ", basket_ask_price)
            print("Stock bid price: ", 0.5 * sum(stock_bid_prices))
            print("Stock ask price: ", 0.5 * sum(stock_ask_prices))
            print("Basket bid price: ", basket_bid_price)
            print()
        
        positions = e.get_positions()
        basket_position = positions[BASKET_INSTRUMENT_ID]
        
        if (basket_ask_price < 0.5 * sum(stock_bid_prices)) and abs(max(get_hedge_positions(e))) <= 50:
            basket_buy_volume = min(basket_bid_volume, min(stock_ask_volumes) * 2, MAX_TRANSACT_SIZE)
            if basket_position + basket_buy_volume > MAX_PER_INSTRUMENT or positions[STOCK_INSTRUMENT_IDS[0]] - basket_buy_volume/2 < -MAX_PER_INSTRUMENT or positions[STOCK_INSTRUMENT_IDS[1]] - basket_buy_volume/2 < -MAX_PER_INSTRUMENT:
                pass
            else:
                buy_basket_sell_stock(e, basket_buy_volume, basket_ask_price, stock_bid_prices, verbose)
                if verbose:
                    print("basket ask < stock_bid")
        
        elif (basket_bid_price > 0.5 * sum(stock_ask_prices)) and abs(max(get_hedge_positions(e))) <= 50:
            basket_sell_volume = min(basket_ask_volume, min(stock_bid_volumes) * 2, MAX_TRANSACT_SIZE)
            if basket_position - basket_sell_volume < -MAX_PER_INSTRUMENT or positions[STOCK_INSTRUMENT_IDS[0]] + basket_sell_volume/2 > MAX_PER_INSTRUMENT or positions[STOCK_INSTRUMENT_IDS[1]] + basket_sell_volume/2 > MAX_PER_INSTRUMENT:
                pass
            else:
                sell_basket_buy_stock(e, basket_sell_volume, basket_bid_price, stock_ask_prices, verbose)
                if verbose:
                    print("basket bid > stock_ask")
            
        else:
            if verbose:
                logger.info("No trades were made for part1")
        if verbose:
            print("Hedge positions:", end="")
            print(get_hedge_positions(e))
            
    else:
        logger.info('No top bid/ask or no book at all')