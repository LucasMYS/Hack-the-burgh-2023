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
    
    max_trade_volume = 10
    max_hedged_position = 50
    min_hedged_position = -50
    
    basket_book = e.get_last_price_book(BASKET_INSTRUMENT_ID)
    stock_books = [e.get_last_price_book(ID) for ID in STOCK_INSTRUMENT_IDS]
    
    if basket_book and basket_book.bids and basket_book.asks:
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
        hedged_positions = [(positions[ID] + basket_position * 0.5) for ID in STOCK_INSTRUMENT_IDS]
        
        print("Basket ask: ", basket_ask_price)
        print("Stock bid: ", 0.5 * sum(stock_bid_prices))
        print("Stock ask: ", 0.5 * sum(stock_ask_prices))
        print("Basket bid: ", basket_bid_price)
        print(hedged_positions)
        
        
        if (basket_ask_price < 0.5 * sum(stock_bid_prices)) and -50 <= hedged_positions[0] <= 50 and -50 <= hedged_positions[1] <= 50:
            volume_to_trade = (min(min(stock_bid_volume), basket_ask_volume, max_trade_volume)//2)*2

            bid_response: InsertOrderResponse = e.insert_order(BASKET_INSTRUMENT_ID, price=basket_ask_price, volume=volume_to_trade, side=SIDE_BID, order_type=ORDER_TYPE_IOC)
            if not bid_response:
                print("Trade failed")
            print(f"Bought: '{BASKET_INSTRUMENT_ID}' for '{basket_ask_price}'")
            ask_response1: InsertOrderResponse = e.insert_order(STOCK_INSTRUMENT_IDS[0], price=stock_bid_prices[0], volume=volume_to_trade/2, side=SIDE_ASK, order_type=ORDER_TYPE_IOC)
            if not ask_response1:
                print("Trade failed")
            print(f"Sold: '{STOCK_INSTRUMENT_IDS[0]}' for '{stock_bid_prices[0]}'")
            ask_response2: InsertOrderResponse = e.insert_order(STOCK_INSTRUMENT_IDS[1], price=stock_bid_prices[1], volume=volume_to_trade/2, side=SIDE_ASK, order_type=ORDER_TYPE_IOC)
            if not ask_response2:
                print("Trade failed")
            print(f"Sold: '{STOCK_INSTRUMENT_IDS[1]}' for '{stock_bid_prices[1]}'")

                    
        elif (basket_bid_price > 0.5 * sum(stock_ask_prices)) and -50 <= hedged_positions[0] <= 50 and -50 <= hedged_positions[1] <= 50:
            volume_to_trade = (min(min(stock_ask_volume), basket_bid_volume, max_trade_volume)//2)*2
            
            bid_response: InsertOrderResponse = e.insert_order(BASKET_INSTRUMENT_ID, price=basket_bid_price, volume=volume_to_trade, side=SIDE_ASK, order_type=ORDER_TYPE_IOC)
            if not bid_response:
                print("Trade failed")
            print(f"Sold: '{BASKET_INSTRUMENT_ID}' for '{basket_bid_price}'")
            ask_response1: InsertOrderResponse = e.insert_order(STOCK_INSTRUMENT_IDS[0], price=stock_ask_prices[0], volume=volume_to_trade/2, side=SIDE_BID, order_type=ORDER_TYPE_IOC)
            if not ask_response1:
                print("Trade failed")
            print(f"Bought: '{STOCK_INSTRUMENT_IDS[0]}' for '{stock_ask_prices[0]}'")
            ask_response2: InsertOrderResponse = e.insert_order(STOCK_INSTRUMENT_IDS[1], price=stock_ask_prices[1], volume=volume_to_trade/2, side=SIDE_BID, order_type=ORDER_TYPE_IOC)
            if not ask_response2:
                print("Trade failed")
            print(f"Bought: '{STOCK_INSTRUMENT_IDS[1]}' for '{stock_ask_prices[1]}'")
            
        else:
            logger.info("No trades were made for part1")
            
        print(positions)
        #print(basket_book)
        #print(stock_books)
        print()
        
    else:
        logger.info('No top bid/ask or no book at all for the basket instrument')