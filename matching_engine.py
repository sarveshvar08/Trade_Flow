class MatchingEngine:
    def __init__(self, order_book):
        self.order_book = order_book

    def match_orders(self):
        buy_orders = self.order_book.buy_orders
        sell_orders = self.order_book.sell_orders

        while buy_orders and sell_orders:
            buy_order = buy_orders[0]
            sell_order = sell_orders[0]

            if buy_order.price < sell_order.price:
                break

            matched_quantity = min(
                buy_order.remaining_quantity,
                sell_order.remaining_quantity
            )

            buy_order.remaining_quantity -= matched_quantity
            sell_order.remaining_quantity -= matched_quantity

            if buy_order.remaining_quantity == 0:
                self.order_book.remove_order(buy_order)

            if sell_order.remaining_quantity == 0:
                self.order_book.remove_order(sell_order)