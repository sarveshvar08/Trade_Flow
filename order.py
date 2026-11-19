class Order:
    def __init__(self, order_id, symbol, side, price, quantity):
        self.order_id = order_id
        self.symbol = symbol
        self.side = side
        self.price = price
        self.quantity = quantity
        self.remaining_quantity = quantity
        self.status = "OPEN"

    def __str__(self):
        return f"{self.order_id} | {self.symbol} | {self.side} | {self.price} | {self.remaining_quantity} | {self.status}"