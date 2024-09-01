import time
import requests
from binance.client import Client
from binance.enums import *
from datetime import datetime

# הגדרות API
api_key = '6eXv9HvdwA4uIPdMfqlCmGZz5diFZHQ2EjE3pYNnbjObSuzhXnVSGodx4KRmyeNn'
api_secret = 'Gf0oBvn8PjI7TV7v3kQeMbhC4o3WWb3FntfXkuEzVvzN5PyvUBsNZp0Fl7DUILaC'
telegram_token = '7010633003:AAGPz4yUwapEz656FPq1HO7iWUX1KYeCqHU'
chat_id = '-4591812648'

client = Client(api_key, api_secret)

# הגדרות מסחר
symbol = 'SOLUSDC'
buy_threshold = 0.002
sell_threshold = 0.004
quantity = 0.7
max_trades_per_minute = 2

# עקוב אחרי פוזיציות
total_positions = 0
closed_positions = 0
open_positions = 0

# פונקציה לשליחת הודעה ב-Telegram
def send_telegram_message(message):
    telegram_api_url = f'https://api.telegram.org/bot{telegram_token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': message}
    response = requests.post(telegram_api_url, json=payload)
    if response.status_code != 200:
        print(f"Failed to send message: {response.text}")

# פונקציה לבדוק אם TP התבצע
def check_take_profit():
    try:
        orders = client.futures_get_open_orders(symbol=symbol)
        for order in orders:
            if order['status'] == ORDER_STATUS_FILLED:
                # TP הצליח
                send_telegram_message(f"Take Profit executed for order: {order}")
                # ניתן כאן למחוק את ההזמנה אם יש צורך
                # client.futures_cancel_order(symbol=symbol, orderId=order['orderId'])
    except Exception as e:
        send_telegram_message(f"Error checking take profit: {e}")

# פונקציות נוספות
def get_symbol_info(symbol):
    info = client.futures_exchange_info()
    for item in info['symbols']:
        if item['symbol'] == symbol:
            return item
    return None

def get_current_price(symbol):
    ticker = client.futures_symbol_ticker(symbol=symbol)
    return float(ticker['price'])

def buy(symbol, quantity):
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=SIDE_BUY,
            type=FUTURE_ORDER_TYPE_MARKET,
            quantity=quantity
        )
        send_telegram_message(f"Buy order executed: {order}")
        return order
    except Exception as e:
        send_telegram_message(f"Error executing buy order: {e}")
        return None

def sell(symbol, quantity, price):
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=SIDE_SELL,
            type=FUTURE_ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=quantity,
            price=f"{price:.4f}"
        )
        send_telegram_message(f"Sell limit order placed: {order}")
        return order
    except Exception as e:
        send_telegram_message(f"Error placing sell limit order: {e}")
        return None

def get_latest_candle(symbol):
    candles = client.futures_klines(symbol=symbol, interval=KLINE_INTERVAL_1MINUTE, limit=2)
    return candles[-1]

symbol_info = get_symbol_info(symbol)
price_precision = symbol_info['pricePrecision']
quantity_precision = symbol_info['quantityPrecision']
tick_size = float(symbol_info['filters'][0]['tickSize'])

def round_to_tick_size(price, tick_size):
    return round(price / tick_size) * tick_size

previous_price = get_current_price(symbol)
print(f"Initial price: {previous_price}")

trade_count = 0
start_time = datetime.now()

while True:
    try:
        current_time = datetime.now()
        elapsed_time = (current_time - start_time).total_seconds()

        if elapsed_time >= 60:
            trade_count = 0
            start_time = current_time

        if trade_count < max_trades_per_minute:
            current_price = get_current_price(symbol)
            print(f"Current price: {current_price}")

            action_taken = False

            if (previous_price - current_price) / previous_price >= buy_threshold:
                print(f"Drop of {((previous_price - current_price) / previous_price) * 100:.2f}%. Buying...")
                order = buy(symbol, round(quantity, quantity_precision))
                if order:
                    total_positions += 1
                    open_positions += 1
                    sell_price = round_to_tick_size(current_price * (1 + sell_threshold), tick_size)
                    sell_quantity = round(quantity * 0.9, quantity_precision)
                    print(f"Attempting to place sell limit order for {sell_quantity} at {sell_price}")
                    sell_order = sell(symbol, sell_quantity, sell_price)
                    if sell_order:
                        closed_positions += 1
                        open_positions -= 1
                        print(f"Sell limit order placed: {sell_order}")
                    else:
                        print("Failed to place sell limit order")
                    trade_count += 1
                    action_taken = True

            latest_candle = get_latest_candle(symbol)
            open_price = float(latest_candle[1])
            close_price = float(latest_candle[4])
            if (open_price - close_price) / open_price >= buy_threshold:
                print(f"1-minute candle drop of {((open_price - close_price) / open_price) * 100:.2f}%. Buying...")
                order = buy(symbol, round(quantity, quantity_precision))
                if order:
                    total_positions += 1
                    open_positions += 1
                    sell_price = round_to_tick_size(close_price * (1 + sell_threshold), tick_size)
                    sell_quantity = round(quantity * 0.9, quantity_precision)
                    print(f"Attempting to place sell limit order for {sell_quantity} at {sell_price}")
                    sell_order = sell(symbol, sell_quantity, sell_price)
                    if sell_order:
                        closed_positions += 1
                        open_positions -= 1
                        print(f"Sell limit order placed: {sell_order}")
                    else:
                        print("Failed to place sell limit order")
                    trade_count += 1
                    action_taken = True

            previous_price = current_price

            if not action_taken:
                print("***")

        # בדוק את TP (Take Profit) כל 10 שניות
        check_take_profit()

        print("------------------------------------------------------")

        time.sleep(5)

    except Exception as e:
        send_telegram_message(f"Error: {e}")
        print(f"Error: {e}")
        time.sleep(5)
