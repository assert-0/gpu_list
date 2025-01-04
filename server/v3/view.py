from typing import Optional

from bson import ObjectId
from pydantic import BaseModel

from ...tools.model import GPUModel, GPUChip, GPUChipReference


class GPUChipView(BaseModel):
    id: Optional[str] = None
    chipName: str
    architecture: str
    fab: str
    transistors: float
    dieSize: float

    @staticmethod
    def from_model(model: GPUChip):
        return GPUChipView(
            id=str(model.id),
            chipName=model.chipName,
            architecture=model.architecture,
            fab=model.fab,
            transistors=model.transistors,
            dieSize=model.dieSize,
        )

    def to_model(self) -> GPUChip:
        return GPUChip(
            chipName=self.chipName,
            architecture=self.architecture,
            fab=self.fab,
            transistors=self.transistors,
            dieSize=self.dieSize,
        )

class GPUView(BaseModel):
    id: Optional[str] = None
    modelName: str
    manufacturer: str
    chip: GPUChipView
    launchDate: str
    launchPrice: str
    memory: int
    computeUnits: int
    performance: float

    @staticmethod
    def from_model(model: GPUModel):
        return GPUView(
            id=str(model.id),
            modelName=model.modelName,
            manufacturer=model.manufacturer,
            chip=GPUChipView.from_model(model.get_chip()),
            launchDate=model.launchDate,
            launchPrice=model.launchPrice,
            memory=model.memory,
            computeUnits=model.computeUnits,
            performance=model.performance,
        )

    def to_model(self) -> GPUModel:
        chip_id = ObjectId(self.chip.id)
        try:
            GPUChip.get({"_id": chip_id})
        except ValueError:
            raise ValueError(f"No GPU chip found with ID {chip_id}")

        return GPUModel(
            modelName=self.modelName,
            manufacturer=self.manufacturer,
            chip=GPUChipReference(chip_id),
            launchDate=self.launchDate,
            launchPrice=self.launchPrice,
            memory=self.memory,
            computeUnits=self.computeUnits,
            performance=self.performance,
        )
