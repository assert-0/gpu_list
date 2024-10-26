import csv
import json
from typing import List

from model import GPUModel


def export_json(model_dicts: List[dict]) -> None:
    with open("gpu_models.json", "w") as f:
        json.dump(model_dicts, f)


def export_csv(model_dicts: List[dict]) -> None:
    if not model_dicts:
        raise ValueError("No model data to export")

    first_dict = model_dicts[0]
    chip_keys = list(first_dict["chip"].keys())
    model_keys = list(first_dict.keys())
    model_keys.remove("chip")

    header = model_keys + chip_keys

    with open("gpu_models.csv", "w") as f:
        csv.DictWriter(f, header).writeheader()

        for model_dict in model_dicts:
            chip = model_dict.pop("chip")
            model_dict.update(chip)
            csv.DictWriter(f, header).writerow(model_dict)


def main() -> None:
    gpu_models = GPUModel.filter()
    model_dicts = [model.to_dict() for model in gpu_models]

    for model_dict in model_dicts:
        model_dict["chip"].pop("id")

    export_json(model_dicts)
    export_csv(model_dicts)


if __name__ == '__main__':
    main()
