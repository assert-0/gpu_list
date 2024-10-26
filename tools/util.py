from abc import ABC, abstractmethod
from typing import Optional, List

from bson import ObjectId
from pydantic import BaseModel, Field
from pymongo import MongoClient
from pymongo.collection import Collection


class DBClient:
    _instance: MongoClient = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = MongoClient('mongodb://localhost:27017/')
        return cls._instance


class DBModel(BaseModel, ABC):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")

    model_config = {
        "arbitrary_types_allowed": True,
        "populate_by_name": True,
    }

    @classmethod
    def get_collection_name(cls) -> str:
        return cls.__name__.lower()

    @staticmethod
    @abstractmethod
    def get_database_name() -> str:
        pass

    def to_dict(self) -> dict:
        return self.model_dump()

    def to_db(self) -> dict:
        return self.model_dump()

    @classmethod
    def get_collection(cls) -> Collection:
        client = DBClient.get_instance()
        db = client[cls.get_database_name()]
        return db[cls.get_collection_name()]

    @classmethod
    def filter(cls, filter: Optional[dict] = None) -> List['DBModel']:
        collection = cls.get_collection()
        results = list(collection.find(filter=filter))
        return [cls.model_validate(result) for result in results]

    @classmethod
    def get(cls, filter: Optional[dict] = None) -> 'DBModel':
        results = cls.filter(filter)

        if not results:
            raise ValueError(f"No document found with filter {filter}")
        if len(results) > 1:
            raise ValueError(f"Multiple documents found with filter {filter}")

        return results[0]

    def save(self) -> None:
        collection = self.__class__.get_collection()
        document = self.to_db()
        document.pop("id")
        collection.replace_one({"_id": self.id}, document, upsert=True)
