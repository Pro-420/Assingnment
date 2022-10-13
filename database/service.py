import pymongo

class Database:

    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://localhost:27017')
        self.database = self.client.Ennea
        self.collection = self.database.Products
            
    def data_insert(self,data):
        try:
            data=data.to_dict('records')
            self.collection.insert_many(data)
            return True
        except Exception:
            return False

    def data_finder(self,data: dict):
        try:
            record_list: list = []
            records = self.collection.find(data)
            for record in records:
                record_list.append({'product':record['code'], 'stock':record['stock']})
            return record_list
        except Exception:
            return None