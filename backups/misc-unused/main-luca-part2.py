import time
from optibook.synchronous_client import Exchange
import part1green as part1green
import part1fossil as part1fossil
import part2_luca
import reset_positions

def main(verbose=True):
    exchange = Exchange()
    exchange.connect()

    sleep_duration_sec = 2
    initial_pnl = exchange.get_pnl()
    prices_used = {"price_sold": "", "price_bought": ""}
    while True:
        #part1fossil.trade_cycle(exchange)
        #part1green.trade_cycle(exchange)
        prices_used = part2_luca.trade_cycle(exchange, prices_used)
        if verbose:
            print("Positions: ", end="")
            print(exchange.get_positions())
            print("Delta PnL: ",  exchange.get_pnl() - initial_pnl)
            print()
            print("----------------------------")
            print()
        time.sleep(sleep_duration_sec)
        


if __name__ == '__main__':
    main()