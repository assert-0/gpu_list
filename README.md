# GPU list

## Description
This repository contains an open-access list of GPU models from Nvidia and AMD. This list is not exhaustive and only
provides a small sample of all GPU models produced by these companies. The data is distributed in JSON and CSV,
along with a MongoDB database dump. All data is sourced from the respective Wikipedia pages, and release under the
Creative Commons Attribution Share-Alike (CC BY-SA) license.

## Repository metadata
**License:**  
Shield: [![CC BY-SA 4.0][cc-by-sa-shield]][cc-by-sa]

This work is licensed under a
[Creative Commons Attribution-ShareAlike 4.0 International License][cc-by-sa].

[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg

**Data sources**:
- https://en.wikipedia.org/wiki/List_of_Nvidia_graphics_processing_units
- https://en.wikipedia.org/wiki/List_of_AMD_graphics_processing_units

**Repository Author:** Nikola Sočec  
**Version:** v1.0  
**Language:** English  
**Release date:** 2024-10-24  
**Export MIME types:** text/csv, application/json, application/bson  
**Date format:** YYYY-MM-DD  
**Currency:** USD  
**Data fields:**
- `GPUModel` class 
  - `modelName`: GPU model name
  - `manufacturer`: GPU manufacturer (Nvidia or AMD)
  - `chip`: instance of associated `GPUChip` class (column not present in CSV)
  - `launchDate`: GPU launch date
  - `launchPrice`: GPU launch price
  - `memory`: GPU memory size (GB)
  - `computeUnits`: enabled GPU compute units (CU/SM)
  - `performance`: GPU FP32 performance (TFLOPS)
  
- `GPUChip` class 
  - `chipName`: GPU chip name
  - `architecture`: GPU chip architecture
  - `fab`: GPU chip fabrication process
  - `transistors`: GPU chip transistor count (billions)
  - `dieSize`: GPU chip die size (mm^2)
