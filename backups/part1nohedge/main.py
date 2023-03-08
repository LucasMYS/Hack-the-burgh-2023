import time
from optibook.synchronous_client import Exchange
import part1green as part1green
import part1fossil as part1fossil
import part2 as part2

def main():
    exchange = Exchange()
    exchange.connect()

    sleep_duration_sec = 2
    while True:
        initial_pnl = exchange.get_pnl()
        part1green.trade_cycle(exchange)
        part1fossil.trade_cycle(exchange)
        #part2.trade_cycle(exchange)
        print("Delta PnL: ",  exchange.get_pnl() - initial_pnl)
        time.sleep(sleep_duration_sec)

if __name__ == '__main__':
    main()
