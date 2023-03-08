import time
from optibook.synchronous_client import Exchange
import part1_refactored2 as part1_refactored2
import part1_refactored1 as part1_refactored1
import reset_positions

def main():
    exchange = Exchange()
    exchange.connect()

    sleep_duration_sec = 0.5
    reset_positions.reset_positions(exchange, verbose=True)
    initial_pnl = exchange.get_pnl()
    
    while True:
        #part1fossil.trade_cycle(exchange)
        #part1green.trade_cycle(exchange)
        #part2.trade_cycle(exchange)
        part1_refactored2.trade_cycle(exchange,False)
        part1_refactored1.trade_cycle(exchange,False)
        print("Positions: ", end="")
        print(exchange.get_positions())
        print("Delta PnL: ",  exchange.get_pnl() - initial_pnl)
        print()
        print("----------------------------")
        print()
        time.sleep(sleep_duration_sec)

if __name__ == '__main__':
    main()