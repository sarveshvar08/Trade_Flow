from trade import Trade


class MatchingEngine:
    def __init__(self, order_book):
        self.order_book = order_book
        self.trades = []
        self.trade_counter = 1

    def match_orders(self):
        buy_orders = self.order_book.buy_orders
        sell_orders = self.order_book.sell_orders

        while buy_orders and sell_orders:
            buy_order = buy_orders[0]
            sell_order = sell_orders[0]

            if buy_order.symbol != sell_order.symbol:
                break

            if buy_order.price < sell_order.price:
                break

            matched_quantity = min(
                buy_order.remaining_quantity,
                sell_order.remaining_quantity
            )

            execution_price = sell_order.price

            buy_order.remaining_quantity -= matched_quantity
            sell_order.remaining_quantity -= matched_quantity

            trade = Trade(
                self.trade_counter,
                buy_order.symbol,
                execution_price,
                matched_quantity,
                buy_order.order_id,
                sell_order.order_id
            )

            self.trades.append(trade)
            self.trade_counter += 1

            if buy_order.remaining_quantity == 0:
                buy_order.status = "FILLED"
                self.order_book.remove_order(buy_order)
            else:
                buy_order.status = "PARTIALLY_FILLED"

            if sell_order.remaining_quantity == 0:
                sell_order.status = "FILLED"
                self.order_book.remove_order(sell_order)
            else:
                sell_order.status = "PARTIALLY_FILLED"

    def display_trades(self):
        print("\nEXECUTED TRADES")

        for trade in self.trades:
            print(trade)