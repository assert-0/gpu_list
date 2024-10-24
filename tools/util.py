from abc import ABC, abstractmethod

from pydantic import BaseModel
from pymongo import MongoClient


class DBClient:
    _instance: MongoClient = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = MongoClient('mongodb://localhost:27017/')
        return cls._instance


class DBModel(BaseModel, ABC):
    @classmethod
    def get_collection_name(cls) -> str:
        return cls.__name__.lower()

    @staticmethod
    @abstractmethod
    def get_database_name() -> str:
        pass

    def save(self):
        client = DBClient.get_instance()
        db = client[self.get_database_name()]
        collection = db[self.get_collection_name()]
        collection.insert_one(self.model_dump(by_alias=True))
