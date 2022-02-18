import pymongo
import certifi
from . import settings


class RocketdataPipeline:
    def __init__(self):
        # для работы с докером раскомментировать
        # self.conn = pymongo.MongoClient(
        #     settings.MONGO_URL,
        #     settings.MONGO_PORT
        # )

        # Если используете докер, то этот
        # MongoClient - закомментировать
        self.conn = pymongo.MongoClient(
            settings.MONGO_URL,
            tlsCAFile=certifi.where()
        )
        db = self.conn[settings.MONGO_DATABASE]
        self.collection = db[settings.MONGO_COLLECTION]

    def process_item(self, item, spider):
        self.collection.insert(item)
        # self.collection.insert(dict(item))
        return item
