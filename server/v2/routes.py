import typing
from typing import List, Union

from fastapi import APIRouter, Response
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from ...tools.model import GPUChip, GPUModel
from .consts import FILTER_TO_FIELD_MAPPING
from .util import filter_gpu_model, filter_gpu_chip, filter_all_fields, export_csv, export_json

api_v2_router = APIRouter(prefix="/api/v2")


@api_v2_router.get("/filter", response_model=None)
async def get_filtered_data(request: Request, response: Response) -> Union[List[dict], JSONResponse, str]:
    filter_field = request.query_params.get("filter_field")
    filter_value = request.query_params.get("filter_value")
    export = request.query_params.get("export", "")

    if not filter_value:
        response.status_code = 400
        return JSONResponse(content={"error": "Missing filter value"})

    if not filter_field or filter_field == "All":
        if not export:
            return [result.to_dict() for result in filter_all_fields(filter_value)]
        elif export == "csv":
            response.headers["Content-Disposition"] = "attachment; filename=export.csv"
            response.headers["Content-Type"] = "text/csv"
            response_csv = export_csv(filter_all_fields(filter_value))
            return Response(content=response_csv)
        elif export == "json":
            response.headers["Content-Disposition"] = "attachment; filename=export.json"
            response.headers["Content-Type"] = "application/json"
            response_json = export_json(filter_all_fields(filter_value))
            return Response(content=response_json)

    if filter_field not in FILTER_TO_FIELD_MAPPING:
        response.status_code = 400
        return JSONResponse(content={"error": f"Invalid filter field: {filter_field}"})

    model_field, model_cls = FILTER_TO_FIELD_MAPPING[filter_field]
    model_field_type = typing.get_type_hints(model_cls).get(model_field)

    try:
        filter_value = model_field_type(filter_value)
    except ValueError:
        response.status_code = 400
        return JSONResponse(
            content={"error": f"Invalid filter value type: {filter_value} (expected {model_field_type})"}
        )

    if model_cls == GPUModel:
        results = filter_gpu_model(model_field, filter_value)
    elif model_cls == GPUChip:
        results = filter_gpu_chip(model_field, filter_value)
    else:
        raise ValueError(f"Invalid model class: {model_cls}")

    if not results:
        return []

    if not export:
        return [result.to_dict() for result in results]
    elif export == "csv":
        response.headers["Content-Disposition"] = "attachment; filename=export.csv"
        response.headers["Content-Type"] = "text/csv"
        response_csv = export_csv(results)
        return Response(content=response_csv)
    elif export == "json":
        response.headers["Content-Disposition"] = "attachment; filename=export.json"
        response.headers["Content-Type"] = "application/json"
        response_json = export_json(results)
        return Response(content=response_json)


@api_v2_router.get("/all", response_model=None)
async def get_all_data(request: Request, response: Response) -> List[dict]:
    export = request.query_params.get("export", "")
    if not export:
        return [result.to_dict() for result in GPUModel.filter()]
    elif export == "csv":
        response.headers["Content-Disposition"] = "attachment; filename=export.csv"
        response.headers["Content-Type"] = "text/csv"
        response_csv = export_csv(GPUModel.filter())
        return Response(content=response_csv)
    elif export == "json":
        response.headers["Content-Disposition"] = "attachment; filename=export.json"
        response.headers["Content-Type"] = "application/json"
        response_json = export_json(GPUModel.filter())
        return Response(content=response_json)
