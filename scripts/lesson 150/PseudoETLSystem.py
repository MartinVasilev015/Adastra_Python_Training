from abc import ABC, abstractmethod
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

#region DataSource
class DataSource(ABC):  
    @abstractmethod
    def sourcemsg():
        pass


class RandomDataSource(DataSource):
    def sourcemsg():

        results = []

        msg_num = random.randint(1, 5)

        for i in range(msg_num):
            characters = string.ascii_letters + string.digits

            upper_limit = random.randint(15, 20)

            key = ''.join(random.choice(characters) for j in range(upper_limit))

            value = round(random.uniform(0, 100), 2)

            ts = datetime.datetime.now()

            results.append(Message(key, value, ts))
        
        return results


class FileDataSource(DataSource):
    def sourcemsg():

        results = []

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


class SourceFactory:

    def get_source(self, type):

        dataSource = DataSource

        match type:
            case 'Simulation':
                dataSource = RandomDataSource
            case 'File':
                dataSource = FileDataSource
            case _:
                pass
        
        return dataSource
#endregion


#region DataSink
class DataSink(ABC): 
    @abstractmethod
    def sinkmsg(self, lst):
        pass


class ConsoleDataSink(DataSink):
    def sinkmsg(lst: list):
        for msg in lst:
            print(msg.to_json().center(25))
        return True
       

class PosgressDataSink(DataSink):
    def sinkmsg(lst: list):
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
                        for msg in lst:
                            record_to_insert = (msg.key, msg.value, msg.ts)
                            cursor.execute(postgres_insert_query, record_to_insert)
                        conn.commit()
                        return True
                        
            except Exception as e:
                print("something went wrong")
                return False
            '''
        return True


class SinkFactory:

    def get_sink(self, type):

        dataSink = DataSink

        match type:
            case 'Console':
                dataSink = ConsoleDataSink
            case 'Posgress':
                dataSink = PosgressDataSink
            case _:
                pass
        
        return dataSink
#endregion


srcf = SourceFactory() 
srcinstance = srcf.get_source('Simulation')
#srcinstance = srcf.get_source('File')

sinkf = SinkFactory()
sinkinstance = sinkf.get_sink('Console')

sinkinstance.sinkmsg(srcinstance.sourcemsg())
