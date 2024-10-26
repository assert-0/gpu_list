from bson import ObjectId
from pymongo.database import DBRef

from util import DBModel


# GPUDB utils

class GPUDB(DBModel):
    @staticmethod
    def get_database_name() -> str:
        return "gpu_db"


class GPUChipReference(DBRef):
    def __init__(self, _id: ObjectId):
        super().__init__(collection=GPUChip.get_collection_name(), id=_id, database=GPUChip.get_database_name())


# Models

class GPUChip(GPUDB):
    chipName: str
    architecture: str
    fab: str
    transistors: float
    dieSize: float


class GPUModel(GPUDB):
    modelName: str
    manufacturer: str
    chip: DBRef
    launchDate: str
    launchPrice: str
    memory: int
    computeUnits: int
    performance: float

    def to_dict(self) -> dict:
        chip = GPUChip.get({"_id": self.chip.id}).to_dict()

        return {
            "modelName": self.modelName,
            "manufacturer": self.manufacturer,
            "chip": chip,
            "launchDate": self.launchDate,
            "launchPrice": self.launchPrice,
            "memory": self.memory,
            "computeUnits": self.computeUnits,
            "performance": self.performance
        }
