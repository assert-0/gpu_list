import csv
import io
import json
from typing import List, Any

from ..tools.model import GPUModel, GPUChip


def filter_gpu_model(model_field: str, filter_value: Any) -> List[GPUModel]:
    if isinstance(filter_value, str):
        return GPUModel.filter({model_field: {"$regex": filter_value}})
    elif isinstance(filter_value, int) or isinstance(filter_value, float):
        return GPUModel.filter({model_field: filter_value})


def filter_gpu_chip(model_field: str, filter_value: Any) -> List[GPUModel]:
    results = []

    models = GPUModel.filter()
    for model in models:
        model_dict = model.to_dict()
        if model_dict["chip"][model_field] == filter_value:
            results.append(model)

    return results


def filter_all_fields(filter_value: Any) -> List[GPUModel]:
    results = []

    models = GPUModel.filter()
    for model in models:
        model_dict = model.to_dict()
        selected = False

        for key, value in model_dict.items():
            if filter_value in str(value):
                results.append(model)
                selected = True
                break

        if selected:
            continue
        for key, value in model_dict["chip"].items():
            if filter_value in str(value):
                results.append(model)
                break

    return results


def export_json(models: List[GPUModel]) -> str:
    return json.dumps([model.to_dict() for model in models])


def export_csv(models: List[GPUModel]) -> str:
    model_dicts = [model.to_dict() for model in models]

    first_dict = model_dicts[0]
    chip_keys = list(first_dict["chip"].keys())
    model_keys = list(first_dict.keys())
    model_keys.remove("chip")

    header = model_keys + chip_keys

    with io.StringIO() as f:
        csv.DictWriter(f, header).writeheader()

        for model_dict in model_dicts:
            chip = model_dict.pop("chip")
            model_dict.update(chip)
            csv.DictWriter(f, header).writerow(model_dict)

        return f.getvalue()
