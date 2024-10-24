from bson import ObjectId
from pydantic import Field
from pymongo.database import DBRef

from util import DBModel


class GPUChip(DBModel):
    @staticmethod
    def get_database_name() -> str:
        return "gpu_db"

    _id: ObjectId
    chipName: str
    architecture: str
    fab: str
    transistors: float
    dieSize: float


class GPUChipReference(DBRef):
    def __init__(self, id: ObjectId):
        super().__init__(collection=GPUChip.get_collection_name(), id=id, database=GPUChip.get_database_name())


class GPUModel(DBModel):
    @staticmethod
    def get_database_name() -> str:
        return "gpu_db"

    modelName: str
    manufacturer: str
    chip: GPUChipReference
    launchDate: str
    launchPrice: str
    memory: int
    computeUnits: int
    performance: float

    model_config = {
        "arbitrary_types_allowed": True,
    }
