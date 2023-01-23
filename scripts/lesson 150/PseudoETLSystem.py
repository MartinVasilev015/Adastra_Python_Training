'''
-You are creating a pseudo-ETL system, which needs to be able to retrieve data from various sources and transmit the data 
    to various sinks. By data, in this case, we mean short json messages with predefined structure. 
    Here is an example: {"key": "A123", "value":"15.6", "ts":'2020-10-07 13:28:43.399620+02:00'} 
-You need to implement at least the following functionality: 
    -Data source is Simulation: this source will generate random data. 
    -Data source is File: the messages are read from an input file which contains a json array of messages. 
    -Data sink is Console: the consumed messages are printed to stdout. 
    -Data sink is PostgreSQL: the consumed messages are inserted in a database table in PostgreSQL 
-Messages should be read and transmitted one by one until the source has no more messages. 
-The Simulation source is infinite - it should always have a new message, if asked. 
-The File source is finite, it ends when the whole file is read. 
'''
import datetime
import json
import random
import string
from types import SimpleNamespace

class Message:

    key = ""
    value = 0.0
    ts = ""

    def __init__(self, key: str, value: float, ts: datetime.datetime):
        self.key = key
        self.value = value
        self.ts = str(ts)


    def to_json(self):
        x = {
            "key": self.key,
            "value": self.value,
            "ts": str(self.ts)
        }
        return json.dumps(x)


class SourceFactory:

    def get_source(self, source_type):
        results = []

        if source_type == 'Simulation':

            msg_num = random.randint(1, 5)

            for i in range(msg_num):
                characters = string.ascii_letters + string.digits

                upper_limit = random.randint(15, 20)

                key = ''.join(random.choice(characters) for j in range(upper_limit))

                value = round(random.uniform(0, 100), 2)

                ts = datetime.datetime.now()

                results.append(Message(key, value, ts))

        elif source_type == 'File':
            try:
                print("Enter Path:")

                path = input().replace('\\', '/')

                with open(path) as file:
                    file_text = file.read().replace('\n', '').replace(' ', '').replace('}{', '},{').replace('},', '}},')

                    if file_text[0] == '[' and file_text[len(file_text)- 1] == ']':
                        file_text = file_text.replace('[', '').replace(']', '')

                    file_lines = file_text.split('},')

                    for i in file_lines:

                        data = json.loads(i, object_hook=lambda d: SimpleNamespace(**d))
                        results.append(Message(data.key, data.value, data.ts))
            
            except Exception as e:
                print("Something went wrong")
        
        return results


class SinkFactory:

    messages = []

    def load_messages(self, msgs):
        for i in msgs:
            self.messages.append(i)

    def sink(self, sink_type):
        if sink_type == 'Console':
            for msg in self.messages:
                print(msg.to_json().center(25))
            return True

        elif sink_type == 'Posgress':
            '''
            try:
                with psycopg2.connect(
                    database = db_name, 
                    user = user, 
                    password = password,
                    host=host,
                    port= port) as conn:

                    with conn.cursor() as cursor:
                        postgres_insert_query = """ INSERT INTO Messsages (KEY, VALUE, TS) VALUES (%s,%s,%s)"""
                        for msg in self.messages:
                            record_to_insert = (msg.key, msg.value, msg.ts)
                            cursor.execute(postgres_insert_query, record_to_insert)
                        conn.commit()
                        return True
                        
            except Exception as e:
                print("something went wrong")
                return False
            '''
            return True

        else:
            return False


srcf = SourceFactory()
sinkf = SinkFactory()

sinkf.load_messages(srcf.get_source('Simulation'))
sinkf.load_messages(srcf.get_source('File'))

if sinkf.sink('Console'):
    print("Success")