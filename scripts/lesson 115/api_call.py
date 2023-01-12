'''
-Use the finnhub.io websockets API to retrieve in real-time data the bitcoin price from the Binance exchange. 

-You'll need to following symbol: BINANCE:BTCUSDT. The payload is json, 
    so use the json module in Python to transform the message to dict. 

-Your class should have the option to output in the console all relevant trades in the following format:
    2020-03-05 09:08:41  prlce:8921.06 volume:0.051236 

-Implement a data structure which calculates time averages. For each one minute period 
    (e.g. 10:00-10:01, 10:01-10:02, etc.) calculate the volume-weighted average price of trades 
    made during this minute. Keep in mind that there may be late-arriving data, 
    and the messages you receive are not guaranteed to be ordered. 
'''
import json
import websocket
from time import sleep
from threading import Thread
import datetime

class BTCReport:
    
    price = 0.0
    timestamp : datetime.datetime = ''
    volume = 0.0

    def __init__(self, price: float, timestamp: int, volume: float):
        self.timestamp = datetime.datetime.fromtimestamp(timestamp/1000.0)
        self.price = price
        self.volume = volume

    def to_string(self):
        return f'{self.timestamp} price:{"%.2f" % self.price} volume:{"%.7f" % self.volume}'  

def get_vwap_for_minute(timestamp, msg_list):
    a = 0.0
    b = 0.0
    
    for i in msg_list:
        a += (i.volume * i.price)
        b += i.volume    

    return timestamp, a/b

def get_data_for_a_minute(msg_list: list):

    result = []
    timestamp = ''

    old_list = msg_list

    old_list.sort(key = lambda x: x.timestamp)
    
    mins = old_list[0].timestamp.minute

    for i in old_list:
        if i.timestamp.minute == mins:
            result.append(i)
            if timestamp == '':
                timestamp = i.timestamp.strftime("%Y-%m-%d %H:%M")
            msg_list.remove(i)
    return timestamp, result 

reports = []

def print_vwap():

    while True:

        #waiting for a minute and 10 seconds
        sleep(70)
        data = get_data_for_a_minute(reports)

        result = get_vwap_for_minute(data[0], data[1])

        print("")
        
        #breakpoint here for testing purposes 
        print(f'---------------------------{result[0]} - VWAP = {result[1]}------------------------')
        continue


def on_message(ws, message):
    
    messages = json.loads(message)['data']
    for i in messages:
        if i == 'data':
            continue

        report = BTCReport(i['p'], i['t'], i['v'])

        reports.append(report)

        print(report.to_string())

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')

def ws_start():
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=cehgbjqad3idq68ps0m0cehgbjqad3idq68ps0mg",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.on_message = on_message
    ws.run_forever()

thread1 = Thread(target = ws_start)
thread2 = Thread(target = print_vwap)

thread1.start()
thread2.start()