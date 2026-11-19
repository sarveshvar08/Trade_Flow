class Trade:
    def __init__(self, trade_id, symbol, price, quantity, buy_order_id, sell_order_id):
        self.trade_id = trade_id
        self.symbol = symbol
        self.price = price
        self.quantity = quantity
        self.buy_order_id = buy_order_id
        self.sell_order_id = sell_order_id

    def __str__(self):
        return f"{self.trade_id} | {self.symbol} | {self.price} | {self.quantity} | {self.buy_order_id} | {self.sell_order_id}" 