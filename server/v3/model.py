from typing import List

from pydantic import BaseModel

from .view import GPUView, GPUChipView


class GenericResponse(BaseModel):
    status: str
    message: str
    response: dict

class SingleGPUResponse(GenericResponse):
    response: GPUView

class MultipleGPUResponse(GenericResponse):
    response: List[GPUView]

class SingleGPUChipResponse(GenericResponse):
    response: GPUChipView

class MultipleGPUChipResponse(GenericResponse):
    response: List[GPUChipView]
