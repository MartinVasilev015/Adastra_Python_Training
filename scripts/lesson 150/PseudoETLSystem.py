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
from abc import ABC, abstractmethod
import datetime
import json
import random
import string
import json
from types import SimpleNamespace
from pathlib import Path

class Message:

    key = ""
    value = 0.0
    ts = ""

    def __init__(self, key: str, value: float, ts: datetime.datetime):
        self.key = key
        self.value = value
        self.ts = str(ts)


def to_json(message):
    x = {
        "key": message.key,
        "value": message.value,
        "ts": str(message.ts)
    }
    return json.dumps(x)

class IDataSinkFactory (ABC):
    @abstractmethod
    def post_data(self, data):
        pass


class PosgreDataSinkFactory (IDataSinkFactory):
    def post_data(self, data):
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

                    for i in self.messages:
                        record_to_insert = (i.key, i.value, i.ts)
                        cursor.execute(postgres_insert_query, record_to_insert)
                    conn.commit()
                    
        except Exception as e:
            print("something went wrong")
        '''
        pass


class ConsoleDataSinkFactory (IDataSinkFactory):
    def post_data(self, data):
        for item in data:
            item_json = to_json(item)
            print(item_json)


class MessageManager:

    def __init__(self):
        self.messages = []

    def get_random_message(self, count):

        for i in range(count):
            characters = string.ascii_letters + string.digits

            upper_limit = random.randint(15, 20)

            key = ''.join(random.choice(characters) for i in range(upper_limit))

            value = round(random.uniform(0, 100), 2)

            ts = datetime.datetime.now()
            self.messages.append(Message(key, value, ts))
            i += 1


    def get_message_from_file(self, path):
        try:
            with open(path) as file:
                file_text = file.read().replace('\n', '').replace(' ', '').replace('}{', '},{').replace('},', '}},')

                if file_text[0] == '[' and file_text[len(file_text)- 1] == ']':
                    file_text = file_text.replace('[', '').replace(']', '')

                file_lines = file_text.split('},')

                for i in file_lines:

                    data = json.loads(i, object_hook=lambda d: SimpleNamespace(**d))
                    message = Message(data.key, data.value, data.ts)
                    self.messages.append(message)
        except Exception as e:
            print("No such file found")


    def send_message_to_console(self):
        ConsoleDataSinkFactory.post_data(ConsoleDataSinkFactory(), self.messages)

    def send_message_to_postgresql(self):
        PosgreDataSinkFactory.post_data(PosgreDataSinkFactory(), self.messages)        


test = MessageManager()

test.get_random_message(1)
test.get_message_from_file(Path("C:/Users/martin.vasilev/Downloads/Python Course/git repo/scripts/lesson 150/test_json.json"))
test.get_random_message(2)
test.send_message_to_console()