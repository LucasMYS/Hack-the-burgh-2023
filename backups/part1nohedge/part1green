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

def print_order_response(order_response: InsertOrderResponse):
    if order_response.success:
        logger.info(f"Inserted order successfully, order_instrument='{order_response.instrument_id}', order_price='{order_response.price}'")
    else:
        logger.info(f"Unable to insert order with reason: '{order_response.success}'")


def trade_cycle(e: Exchange):
    
    basket_book = e.get_last_price_book(BASKET_INSTRUMENT_ID)
    stock_books = [e.get_last_price_book(ID) for ID in STOCK_INSTRUMENT_IDS]
    
    if basket_book and basket_book.bids and basket_book.asks and stock_books[0] and stock_books[0].bids and stock_books[0].asks and stock_books[1] and stock_books[1].bids and stock_books[1].asks:
        logger.info(f'Order book for {BASKET_INSTRUMENT_ID}: best bid={basket_book.bids[0].price:.2f}, best ask={basket_book.asks[0].price:.2f}')
        
        basket_ask_price = basket_book.asks[0].price
        basket_bid_price = basket_book.bids[0].price
        stock_bid_prices = [(stock_book).bids[0].price for stock_book in stock_books]
        stock_ask_prices = [(stock_book).asks[0].price for stock_book in stock_books]
        
        basket_ask_volume = basket_book.asks[0].volume
        basket_bid_volume = basket_book.bids[0].volume
        stock_bid_volume = [stock_book.bids[0].volume for stock_book in stock_books]
        stock_ask_volume = [stock_book.asks[0].volume for stock_book in stock_books]
        
        
        positions = e.get_positions()
        basket_position = positions[BASKET_INSTRUMENT_ID]
        
        
        buyvolume = min(basket_bid_volume, stock_ask_volume[0], stock_ask_volume[1], 100)
        sellvolume = min(basket_ask_volume, stock_bid_volume[0], stock_bid_volume[1], 100)
        
        if buyvolume % 2 == 1:
            buyvolume = buyvolume - 1
            
        if sellvolume % 2 == 1:
            sellvolume = sellvolume - 1
        
        
        if (basket_ask_price < 0.5 * sum(stock_bid_prices)):
            if (basket_bid_price > 0.5 * sum(stock_ask_prices)) and (basket_bid_price - 0.5 * sum(stock_ask_prices) > (0.5 * sum(stock_bid_prices) - basket_ask_price)):
                
                bid_response: InsertOrderResponse = e.insert_order(BASKET_INSTRUMENT_ID, price=basket_bid_price, volume=buyvolume, side=SIDE_ASK, order_type=ORDER_TYPE_IOC)
                if not bid_response:
                    print("Trade failed")
                print(f"Sold: '{BASKET_INSTRUMENT_ID}' for '{basket_bid_price}'")
                ask_response1: InsertOrderResponse = e.insert_order(STOCK_INSTRUMENT_IDS[0], price=stock_ask_prices[0], volume=buyvolume/2, side=SIDE_BID, order_type=ORDER_TYPE_IOC)
                if not ask_response1:
                    print("Trade failed")
                print(f"Bought: '{STOCK_INSTRUMENT_IDS[0]}' for '{stock_ask_prices[0]}'")
                ask_response2: InsertOrderResponse = e.insert_order(STOCK_INSTRUMENT_IDS[1], price=stock_ask_prices[1], volume=buyvolume/2, side=SIDE_BID, order_type=ORDER_TYPE_IOC)
                if not ask_response2:
                    print("Trade failed")
                print(f"Bought: '{STOCK_INSTRUMENT_IDS[1]}' for '{stock_ask_prices[1]}'")

            else:
                bid_response: InsertOrderResponse = e.insert_order(BASKET_INSTRUMENT_ID, price=basket_ask_price, volume=sellvolume, side=SIDE_BID, order_type=ORDER_TYPE_IOC)
                if not bid_response:
                    print("Trade failed")
                print(f"Bought: '{BASKET_INSTRUMENT_ID}' for '{basket_ask_price}'")
                ask_response1: InsertOrderResponse = e.insert_order(STOCK_INSTRUMENT_IDS[0], price=stock_bid_prices[0], volume=sellvolume/2, side=SIDE_ASK, order_type=ORDER_TYPE_IOC)
                if not ask_response1:
                    print("Trade failed")
                print(f"Sold: '{STOCK_INSTRUMENT_IDS[0]}' for '{stock_bid_prices[0]}'")
                ask_response2: InsertOrderResponse = e.insert_order(STOCK_INSTRUMENT_IDS[1], price=stock_bid_prices[1], volume=sellvolume/2, side=SIDE_ASK, order_type=ORDER_TYPE_IOC)
                if not ask_response2:
                    print("Trade failed")
                print(f"Sold: '{STOCK_INSTRUMENT_IDS[1]}' for '{stock_bid_prices[1]}'")

                    
        elif (basket_bid_price > 0.5 * sum(stock_ask_prices)):
            if (basket_ask_price < 0.5 * sum(stock_bid_prices)) and (basket_bid_price - 0.5 * sum(stock_ask_prices) < (0.5 * sum(stock_bid_prices) - basket_ask_price)):
                
                bid_response: InsertOrderResponse = e.insert_order(BASKET_INSTRUMENT_ID, price=basket_ask_price, volume=sellvolume, side=SIDE_BID, order_type=ORDER_TYPE_IOC)
                if not bid_response:
                    print("Trade failed")
                print(f"Bought: '{BASKET_INSTRUMENT_ID}' for '{basket_ask_price}'")
                ask_response1: InsertOrderResponse = e.insert_order(STOCK_INSTRUMENT_IDS[0], price=stock_bid_prices[0], volume=sellvolume/2, side=SIDE_ASK, order_type=ORDER_TYPE_IOC)
                if not ask_response1:
                    print("Trade failed")
                print(f"Sold: '{STOCK_INSTRUMENT_IDS[0]}' for '{stock_bid_prices[0]}'")
                ask_response2: InsertOrderResponse = e.insert_order(STOCK_INSTRUMENT_IDS[1], price=stock_bid_prices[1], volume=sellvolume/2, side=SIDE_ASK, order_type=ORDER_TYPE_IOC)
                if not ask_response2:
                    print("Trade failed")
                print(f"Sold: '{STOCK_INSTRUMENT_IDS[1]}' for '{stock_bid_prices[1]}'")
            
            else:
                
                bid_response: InsertOrderResponse = e.insert_order(BASKET_INSTRUMENT_ID, price=basket_bid_price, volume=buyvolume, side=SIDE_ASK, order_type=ORDER_TYPE_IOC)
                if not bid_response:
                    print("Trade failed")
                print(f"Sold: '{BASKET_INSTRUMENT_ID}' for '{basket_bid_price}'")
                ask_response1: InsertOrderResponse = e.insert_order(STOCK_INSTRUMENT_IDS[0], price=stock_ask_prices[0], volume=buyvolume/2, side=SIDE_BID, order_type=ORDER_TYPE_IOC)
                if not ask_response1:
                    print("Trade failed")
                print(f"Bought: '{STOCK_INSTRUMENT_IDS[0]}' for '{stock_ask_prices[0]}'")
                ask_response2: InsertOrderResponse = e.insert_order(STOCK_INSTRUMENT_IDS[1], price=stock_ask_prices[1], volume=buyvolume/2, side=SIDE_BID, order_type=ORDER_TYPE_IOC)
                if not ask_response2:
                    print("Trade failed")
                print(f"Bought: '{STOCK_INSTRUMENT_IDS[1]}' for '{stock_ask_prices[1]}'")
            
        else:
            logger.info("No trades were made for part1")
            
        print(positions)
        #print(basket_book)
        #print(stock_books)
        
    else:
        logger.info('No top bid/ask or no book at all for the basket instrument')
