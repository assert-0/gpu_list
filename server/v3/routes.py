from typing import Optional, Union

from bson import ObjectId
from fastapi import APIRouter, Request, Response

from .model import MultipleGPUResponse, GenericResponse, SingleGPUResponse, MultipleGPUChipResponse, \
    SingleGPUChipResponse
from .view import GPUView, GPUChipView
from ...tools.model import GPUModel, GPUChip

api_v3_router = APIRouter(prefix="/api/v3")


@api_v3_router.api_route("/gpus", methods=["GET"], response_model=None)
async def gpus_all(response: Response) -> Optional[MultipleGPUResponse]:
    gpus = GPUModel.filter()

    if not gpus:
        response.status_code = 204
        return None
    else:
        response.status_code = 200
        return MultipleGPUResponse(
            status="OK",
            message="All GPUs retrieved",
            response=[GPUView.from_model(gpu) for gpu in gpus]
        )

@api_v3_router.api_route("/gpus", methods=["POST"], response_model=None)
async def gpus_create(request: Request, response: Response) -> Union[GenericResponse, SingleGPUResponse]:
    try:
        data = await request.json()
        gpu_view = GPUView(**data)
        gpu_model = gpu_view.to_model()
        gpu_model.save()
    except Exception as e:
        response.status_code = 400
        return GenericResponse(
            status="Bad Request",
            message="Invalid GPU model",
            response={"error": str(e)}
        )

    response.status_code = 201
    return SingleGPUResponse(
        status="Created",
        message="GPU created successfully",
        response=GPUView.from_model(gpu_model)
    )

@api_v3_router.api_route("/gpus", methods=["PUT", "PATCH", "DELETE"])
async def gpus_not_implemented(response: Response) -> GenericResponse:
    response.status_code = 501
    return GenericResponse(
        status="Not Implemented",
        message="This method is not implemented for the requested resource",
        response={}
    )

@api_v3_router.api_route("/gpus/{gpu_id}", methods=["GET"], response_model=None)
async def gpus_single_get(gpu_id: str, response: Response) -> Union[SingleGPUResponse, GenericResponse]:
    try:
        gpu = GPUModel.get(filter={"_id": ObjectId(gpu_id)})
    except Exception as e:
        response.status_code = 404
        return GenericResponse(
            status="Not Found",
            message="GPU not found",
            response={"error": str(e)}
        )

    response.status_code = 200
    return SingleGPUResponse(
        status="OK",
        message="GPU retrieved successfully",
        response=GPUView.from_model(gpu)
    )

@api_v3_router.api_route("/gpus/{gpu_id}", methods=["PUT"])
async def gpus_single_update(
        gpu_id: str, request: Request, response: Response
) -> Union[SingleGPUResponse, GenericResponse]:
    try:
        GPUModel.get(filter={"_id": ObjectId(gpu_id)})
    except Exception as e:
        response.status_code = 404
        return GenericResponse(
            status="Not Found",
            message="GPU not found",
            response={"error": str(e)}
        )

    try:
        data = await request.json()
        gpu_view = GPUView(**data)
        gpu_model = gpu_view.to_model()
        gpu_model.id = ObjectId(gpu_id)
        gpu_model.save()
    except Exception as e:
        response.status_code = 400
        return GenericResponse(
            status="Bad Request",
            message="GPU update failed",
            response={"error": str(e)}
        )

    response.status_code = 200
    return SingleGPUResponse(
        status="OK",
        message="GPU updated successfully",
        response=GPUView.from_model(gpu_model)
    )

@api_v3_router.api_route("/gpus/{gpu_id}", methods=["DELETE"])
async def gpus_single_delete(gpu_id: str, response: Response) -> GenericResponse:
    try:
        gpu = GPUModel.get(filter={"_id": ObjectId(gpu_id)})
        gpu.delete()
    except Exception as e:
        response.status_code = 404
        return GenericResponse(
            status="Not Found",
            message="GPU not found",
            response={"error": str(e)}
        )

    response.status_code = 200
    return GenericResponse(
        status="OK",
        message="GPU deleted successfully",
        response={}
    )

@api_v3_router.api_route("/gpus/{gpu_id}", methods=["POST", "PATCH"])
async def gpus_single_not_implemented(response: Response) -> GenericResponse:
    response.status_code = 501
    return GenericResponse(
        status="Not Implemented",
        message="This method is not implemented for the requested resource",
        response={}
    )

@api_v3_router.api_route("/gpuchips", methods=["GET"])
async def gpuchips_all(response: Response) -> Optional[MultipleGPUChipResponse]:
    chips = GPUChip.filter()

    if not chips:
        response.status_code = 204
        return None
    else:
        response.status_code = 200
        return MultipleGPUChipResponse(
            status="OK",
            message="All GPU chips retrieved",
            response=[GPUChipView.from_model(chip) for chip in chips]
        )

@api_v3_router.api_route("/gpuchips", methods=["POST"])
async def gpuchips_create(request: Request, response: Response) -> Union[GenericResponse, SingleGPUChipResponse]:
    try:
        data = await request.json()
        chip_view = GPUChipView(**data)
        chip_model = chip_view.to_model()
        chip_model.save()
    except Exception as e:
        response.status_code = 400
        return GenericResponse(
            status="Bad Request",
            message="Invalid GPU chip model",
            response={"error": str(e)}
        )

    response.status_code = 201
    return SingleGPUChipResponse(
        status="Created",
        message="GPU chip created successfully",
        response=GPUChipView.from_model(chip_model)
    )

@api_v3_router.api_route("/gpuchips", methods=["PUT", "PATCH", "DELETE"])
async def gpuchips_not_implemented(response: Response) -> GenericResponse:
    response.status_code = 501
    return GenericResponse(
        status="Not Implemented",
        message="This method is not implemented for the requested resource",
        response={}
    )

@api_v3_router.api_route("/gpuchips/{chip_id}", methods=["GET"])
async def gpuchips_single_get(chip_id: str, response: Response) -> Union[SingleGPUChipResponse, GenericResponse]:
    try:
        chip = GPUChip.get(filter={"_id": ObjectId(chip_id)})
    except Exception as e:
        response.status_code = 404
        return GenericResponse(
            status="Not Found",
            message="GPU chip not found",
            response={"error": str(e)}
        )

    response.status_code = 200
    return SingleGPUChipResponse(
        status="OK",
        message="GPU chip retrieved successfully",
        response=GPUChipView.from_model(chip)
    )

@api_v3_router.api_route("/gpuchips/{chip_id}", methods=["PUT"])
async def gpuchips_single_update(
        chip_id: str, request: Request, response: Response
) -> Union[SingleGPUChipResponse, GenericResponse]:
    try:
        GPUChip.get(filter={"_id": ObjectId(chip_id)})
    except Exception as e:
        response.status_code = 404
        return GenericResponse(
            status="Not Found",
            message="GPU chip not found",
            response={"error": str(e)}
        )

    try:
        data = await request.json()
        chip_view = GPUChipView(**data)
        chip_model = chip_view.to_model()
        chip_model.id = ObjectId(chip_id)
        chip_model.save()
    except Exception as e:
        response.status_code = 400
        return GenericResponse(
            status="Bad Request",
            message="GPU chip update failed",
            response={"error": str(e)}
        )

    response.status_code = 200
    return SingleGPUChipResponse(
        status="OK",
        message="GPU chip updated successfully",
        response=GPUChipView.from_model(chip_model)
    )

@api_v3_router.api_route("/gpuchips/{chip_id}", methods=["DELETE"])
async def gpuchips_single_delete(chip_id: str, response: Response) -> GenericResponse:
    try:
        chip = GPUChip.get(filter={"_id": ObjectId(chip_id)})
        chip.delete()
    except Exception as e:
        response.status_code = 404
        return GenericResponse(
            status="Not Found",
            message="GPU chip not found",
            response={"error": str(e)}
        )

    try:
        for gpu in GPUModel.filter(filter={"chip.$id": chip.id}):
            gpu.delete()
    except Exception as e:
        response.status_code = 500
        return GenericResponse(
            status="Internal Server Error",
            message="GPU chip deletion failed (cascade delete)",
            response={"error": str(e)}
        )

    response.status_code = 200
    return GenericResponse(
        status="OK",
        message="GPU chip and its parent GPUs deleted successfully",
        response={}
    )

@api_v3_router.api_route("/gpuchips/{chip_id}", methods=["POST", "PATCH"])
async def gpuchips_single_not_implemented(response: Response) -> GenericResponse:
    response.status_code = 501
    return GenericResponse(
        status="Not Implemented",
        message="This method is not implemented for the requested resource",
        response={}
    )

@api_v3_router.api_route("/gpuchips/{chip_id}/gpus", methods=["GET"])
async def gpuchips_gpus_get(chip_id: str, response: Response) -> Union[MultipleGPUResponse, GenericResponse, None]:
    try:
        chip = GPUChip.get(filter={"_id": ObjectId(chip_id)})
    except Exception as e:
        response.status_code = 404
        return GenericResponse(
            status="Not Found",
            message="GPU chip not found",
            response={"error": str(e)}
        )

    gpus = GPUModel.filter(filter={"chip.$id": chip.id})

    if not gpus:
        response.status_code = 204
        return None
    else:
        response.status_code = 200
        return MultipleGPUResponse(
            status="OK",
            message="All GPUs for GPU chip retrieved",
            response=[GPUView.from_model(gpu) for gpu in gpus]
        )
