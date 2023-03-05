'''
Contains reset_position function
Will call reset_position on "green" if run directly
'''
from typing import List
from optibook import common_types as t
from optibook import ORDER_TYPE_IOC, ORDER_TYPE_LIMIT, SIDE_ASK, SIDE_BID
from optibook.exchange_responses import InsertOrderResponse
from optibook.synchronous_client import Exchange
from time import sleep

# Resets all instruments to zero by buying/selling them
def reset_positions(e, instruments="green", verbose=False):
    if instruments == "green":
        INSTRUMENTS_ID = ["C2_GREEN_ENERGY_ETF", "C2_SOLAR_CO", "C2_WIND_LTD"]
    elif instruments == "fossil":
        INSTRUMENTS_ID = ["C1_FOSSIL_FUEL_ETF", "C1_GAS_INC", "C1_OIL_CORP"]
    else:
        print(f"Please enter a valid instrument. You entered '{instruments}'")
        return
    for INSTRUMENT_ID in INSTRUMENTS_ID:
        positions = e.get_positions()
        while positions[INSTRUMENT_ID] != 0:

            positions = e.get_positions()
            if verbose:
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
            if verbose:
                print("Volume: ", volume)
            bid_response: InsertOrderResponse = e.insert_order(INSTRUMENT_ID, price=price, volume=volume, side=SIDE, order_type=ORDER_TYPE_IOC)
            if verbose:
                print(bid_response)
            sleep(1)
            if verbose:
                print("Position: ", positions[INSTRUMENT_ID])
            
        else:
            if verbose:
                print(f"Position of '{INSTRUMENT_ID}' is 0")
    

if __name__ == '__main__':
    e = Exchange()
    e.connect()
    reset_positions(e, "green")
