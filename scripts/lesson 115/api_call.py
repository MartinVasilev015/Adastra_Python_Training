import json
import websocket
import datetime

class BTCReport:
    
    price = 0.0
    timestamp : datetime.datetime = ''
    volume = 0.0

    def __init__(self, price: float, timestamp: int, volume: float):
        self.timestamp = datetime.datetime.fromtimestamp(timestamp/1000.0).__format__("%d-%m-%Y, %H:%M")
        self.price = price
        self.volume = volume

    def to_string(self):
        return f'{self.timestamp} price:{"%.2f" % self.price} volume:{"%.7f" % self.volume}'  


class CustomList:

    array_list = []

    def add(self, item:BTCReport):

        self.array_list.append(item)

        if len(self.array_list) > 0:

            self.array_list.sort(key = lambda x: x.timestamp)

            min_timestamp = self.array_list[0].timestamp
            minutes = int(min_timestamp.split(':')[1])

            if int(item.timestamp.split(':')[1]) == minutes + 2:

                a = 0.0
                b = 0.0
                result = 0.0

                #temp_list = self.array_list

                for i in self.array_list[:]:
                    if i.timestamp == min_timestamp:
                        a += (i.volume * i.price)
                        b += i.volume    
                        self.array_list.remove(i)


                result = a/b
                print("-----------------VWAC:" + min_timestamp + ": " + str(result) + " -------------")


lst = CustomList()

def on_message(ws, message):
    
    messages = json.loads(message)['data']
    for i in messages:
        if i == 'data':
            continue

        report = BTCReport(i['p'], i['t'], i['v'])
        print(report.to_string())

        lst.add(report)
        
def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')


websocket.enableTrace(False)
ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=cehgbjqad3idq68ps0m0cehgbjqad3idq68ps0mg",
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close)
ws.on_open = on_open
ws.on_message = on_message
ws.run_forever()