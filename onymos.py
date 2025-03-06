import threading
import random
import time

# Maximum number of tickers supported.
NUM_TICKERS = 1024

# Each ticker's order book is represented as a pair of lists:
# [ list_of_buy_orders, list_of_sell_orders ]
# We initialize an array with 1024 entries.
order_books = [[[], []] for _ in range(NUM_TICKERS)]

class Order:
    def __init__(self, order_type, ticker, quantity, price):
        self.order_type = order_type  # "Buy" or "Sell"
        self.ticker = ticker          # e.g. "TICKER42"
        self.quantity = quantity
        self.price = price

    def __str__(self):
        return f"{self.order_type} {self.ticker} Qty:{self.quantity} Price:{self.price}"

def ticker_to_index(ticker):
    """
    Convert ticker symbol (e.g., "TICKER42") to an integer index.
    Assumes ticker symbol format is "TICKER" followed by a number in [0, NUM_TICKERS-1].
    """
    try:
        # Extract the numeric part
        index = int(ticker.replace("TICKER", ""))
        if 0 <= index < NUM_TICKERS:
            return index
    except Exception:
        pass
    # Fallback: modulo mapping
    return hash(ticker) % NUM_TICKERS

def addOrder(order_type, ticker, quantity, price):
    """
    Add an order to the order book.
    order_type: "Buy" or "Sell"
    ticker: e.g., "TICKER42"
    quantity: int
    price: float
    """
    index = ticker_to_index(ticker)
    new_order = Order(order_type, ticker, quantity, price)
    # Append order to the appropriate list in the order book.
    if order_type == "Buy":
        # Append to buy orders (index 0)
        order_books[index][0].append(new_order)
    elif order_type == "Sell":
        # Append to sell orders (index 1)
        order_books[index][1].append(new_order)
    else:
        print("Invalid order type:", order_type)

def matchOrder():
    """
    For each ticker, match orders using the rule:
      If there exists a buy order with a price >= lowest sell order price,
      execute a trade.
    This function scans each ticker’s order book in O(n) time (n = number of orders).
    It repeatedly processes matches until no further match exists.
    """
    # Iterate over every ticker's order book
    for ticker_index in range(NUM_TICKERS):
        buy_orders = order_books[ticker_index][0]
        sell_orders = order_books[ticker_index][1]
        # Continue matching as long as both lists are non-empty.
        while sell_orders and buy_orders:
            # Find the sell order with the lowest price (linear scan, O(n))
            lowest_sell_index = 0
            for i in range(1, len(sell_orders)):
                if sell_orders[i].price < sell_orders[lowest_sell_index].price:
                    lowest_sell_index = i
            lowest_sell_order = sell_orders[lowest_sell_index]
            
            # Find a buy order that can meet the price condition.
            match_found = False
            for j in range(len(buy_orders)):
                if buy_orders[j].price >= lowest_sell_order.price:
                    match_found = True
                    match_index = j
                    break
            # If no matching buy order is found, exit the loop for this ticker.
            if not match_found:
                break

            # Found a match – execute a trade.
            buy_order = buy_orders[match_index]
            traded_qty = min(buy_order.quantity, lowest_sell_order.quantity)
            # In a real system, you would record the trade details here.
            print(f"Trade executed for {buy_order.ticker}: "
                  f"Quantity {traded_qty} at price {lowest_sell_order.price}")
            # Update quantities.
            buy_order.quantity -= traded_qty
            lowest_sell_order.quantity -= traded_qty
            # Remove orders that have been fully executed.
            if buy_order.quantity == 0:
                # Remove buy order from list.
                # (List pop is atomic in CPython due to the GIL.)
                buy_orders.pop(match_index)
            if lowest_sell_order.quantity == 0:
                sell_orders.pop(lowest_sell_index)

def simulate_orders():
    """
    Randomly generate orders to simulate active stock transactions.
    This function continuously calls addOrder with random parameters.
    """
    order_types = ["Buy", "Sell"]
    while True:
        # Randomly choose order parameters.
        o_type = random.choice(order_types)
        ticker_index = random.randint(0, NUM_TICKERS - 1)
        ticker = f"TICKER{ticker_index}"
        quantity = random.randint(1, 100)
        price = round(random.uniform(10, 1000), 2)
        addOrder(o_type, ticker, quantity, price)
        # Sleep a little to simulate a realistic stream of orders.
        time.sleep(random.uniform(0.01, 0.05))

def simulate_trading():
    """
    Spawn several threads that simulate order entry while the main thread
    periodically matches orders. Note that we do not use locks here – we
    rely on CPython’s GIL and atomic list operations. In a production system,
    lock-free data structures or atomic primitives would be used.
    """
    # Create a few threads to simulate active stockbrokers placing orders.
    order_threads = []
    for _ in range(5):  # for example, 5 concurrent order generators
        t = threading.Thread(target=simulate_orders)
        t.daemon = True
        order_threads.append(t)
        t.start()

    # Continuously match orders in the main thread.
    try:
        while True:
            matchOrder()
            # Sleep briefly before checking again.
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Simulation stopped.")

# Start the simulation if run as a script.
if __name__ == '__main__':
    simulate_trading()
