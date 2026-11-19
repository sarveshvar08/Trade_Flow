class OrderBook:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []

    def add_order(self, order):
        if order.side == "BUY":
            self.buy_orders.append(order)
            self.buy_orders.sort(key=lambda x: x.price, reverse=True)
        else:
            self.sell_orders.append(order)
            self.sell_orders.sort(key=lambda x: x.price)

    def remove_order(self, order):
        if order.side == "BUY":
            self.buy_orders.remove(order)
        else:
            self.sell_orders.remove(order)

    def display_orders(self):
        print("\nBUY ORDERS")
        for order in self.buy_orders:
            print(order)

        print("\nSELL ORDERS")
        for order in self.sell_orders:
            print(order)