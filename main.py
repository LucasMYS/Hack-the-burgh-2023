"""
Main - call to use bots
"""
import time
from optibook.synchronous_client import Exchange
import part1_refactored as part1_green
import part1_refactored1 as part1_fossil
import reset_positions

def main(verbose=True):
    exchange = Exchange()
    exchange.connect()

    sleep_duration_sec = 0.2
    # Resets the positions to zero (for testing)
    # reset_positions.reset_positions(exchange, instruments="green", verbose=verbose)
    # reset_positions.reset_positions(exchange, instruments="fossil", verbose=verbose)
    initial_pnl = exchange.get_pnl()
    while True:
        # Calls the "trade_cycle" function for all bots
        part1_green.trade_cycle(exchange, verbose=verbose)
        part1_fossil.trade_cycle(exchange, verbose=verbose)
        if verbose:
            print("Positions: ", end="")
            print(exchange.get_positions())
            print("Delta PnL: ",  exchange.get_pnl() - initial_pnl)
            print()
            print("----------------------------")
            print()
        time.sleep(sleep_duration_sec)

if __name__ == '__main__':
    main(verbose=True)