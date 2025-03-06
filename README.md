# Real-Time Stock Trading Engine

This project implements a simple real-time stock trading engine in Python. It simulates matching stock buy and sell orders based on price criteria while supporting up to 1,024 tickers.

## Features

- **Order Book Structure:**  
  Each ticker has its own order book represented as a pair of lists (buy orders and sell orders). No dictionary or map-like data structures are used.

- **Order Matching:**  
  The `matchOrder` function iterates over each ticker's orders in O(n) time, matching a buy order with a sell order if the buy price is greater than or equal to the lowest sell price available.

- **Concurrency Simulation:**  
  Multiple threads simulate active stock transactions by continuously adding orders with random parameters. The main thread continuously processes order matches.

- **Lock-Free Approach:**  
  The code leverages Python's GIL and atomic list operations to simulate lock-free concurrency, ideal for this simulation.

## Components

- **Order Class:**  
  Represents an order with attributes for order type (Buy/Sell), ticker symbol, quantity, and price.

- **addOrder Function:**  
  Accepts parameters (order type, ticker symbol, quantity, price) and appends the order to the respective order book.

- **matchOrder Function:**  
  Scans through the order book, finds matching orders, executes trades, and updates or removes orders accordingly.

- **Simulation Functions:**  
  - `simulate_orders`: Randomly generates orders to mimic a live trading environment.
  - `simulate_trading`: Spawns multiple threads for order generation and periodically calls `matchOrder` to process trades.

## Running the Simulation

1. **Requirements:**  
   Ensure you have Python 3.6 or later installed.

2. **Setup:**  
   Save the provided code to a file (e.g., `trading_engine.py`).

3. **Execution:**  
   Run the simulation with:
   ```bash
   python trading_engine.py
   ```
   The simulation will start generating orders and matching them in real time. Press `Ctrl+C` to stop the simulation.

## Notes

- This engine is a simulation and is not intended for production use.
- For a production system, consider using robust lock-free data structures and proper concurrency controls.
- The design avoids dictionaries or similar data structures by relying solely on Python lists.

Enjoy experimenting with the real-time stock trading simulation!
