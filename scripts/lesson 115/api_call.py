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
import time
import threading
import datetime

class BTCReport:
    
    price = 0.0
    timespamp = 0
    volume = 0.0

    def __init__(self, price: float, timespamp: int, volume: float):
        self.timespamp = timespamp
        self.price = price
        self.volume = volume

    def to_string(self):
        return (str(datetime.datetime.fromtimestamp(self.timespamp/1000.0)) + " price:" + 
            str("%.2f" % self.price) + " volume:" + str("%.7f" % self.volume))  

class MessageManager:

    messages_result = []

    def on_message(self, ws, message):
        messages = json.loads(message)['data']
            
        for i in messages:
            if i == 'data':
                continue

            var = BTCReport(i['p'], i['t'], i['v'])
            self.messages_result.append(var)

    def on_error(ws: any, error):
        print(error)

    def on_close(self, a, b):
        print("")

    def on_open(self, ws):
        ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')

    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=cehgbjqad3idq68ps0m0cehgbjqad3idq68ps0mg",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)

    def get_messages(self):
        self.ws.on_open = self.on_open
        self.ws.on_message = self.on_message
        self.ws.run_forever()

    def start(self):
        self.timer = threading.Timer(1.0, self.get_messages)
        self.timer.start()
    
    def stop(self):
        self.ws.keep_running = False
        self.timer.cancel()

    def print_results(self):
        for i in self.messages_result:
            print(i.to_string())

    def get_vwac(self):
        
        a = 0.0
        b = 0.0

        for i in self.messages_result:

            a += (i.volume * i.price)
            b += i.volume    

        return a/b


mm = MessageManager()

mm.start()
time.sleep(5)
#time.sleep(60)
mm.stop()

print("--------------")
mm.print_results()

print("-----VWAP-----")
print(mm.get_vwac())
