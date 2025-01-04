from ...tools.model import GPUModel, GPUChip


FILTER_TO_FIELD_MAPPING = {
    "Model name": ("modelName", GPUModel),
    "Manufacturer": ("manufacturer", GPUModel),
    "Launch date": ("launchDate", GPUModel),
    "Launch price": ("launchPrice", GPUModel),
    "Memory": ("memory", GPUModel),
    "Compute units": ("computeUnits", GPUModel),
    "Performance": ("performance", GPUModel),
    "Chip name": ("chipName", GPUChip),
    "Architecture": ("architecture", GPUChip),
    "Fab": ("fab", GPUChip),
    "Transistors": ("transistors", GPUChip),
    "Die size": ("dieSize", GPUChip),
}
