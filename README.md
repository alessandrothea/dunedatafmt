DUNE DAQ Data Format Python Package
====================================

`datafmt` provides Python bindings for the core DUNE-DAQ data format libraries, enabling
unpacking and inspection of DUNE-DAQ detector fragments from Python.

## Included packages

| Package | Description |
|---|---|
| `daqdataformats` | Core DAQ data format types |
| `detdataformats` | Detector data format types |
| `fddetdataformats` | Far detector data format types |
| `trgdataformats` | Trigger data format types |
| `rawdatautils` | Utilities for unpacking raw data |

The C++ sources are pulled in as git submodules from the [DUNE-DAQ](https://github.com/DUNE-DAQ)
organisation and compiled as pybind11 extensions at install time.

## Installation

```bash
git clone <this-repo>
pip install ./dunedatafmt
```

Submodules are initialised automatically during the build.

## Requirements

- Python >= 3.7
- A C++ compiler (GCC or Clang)
- pybind11 >= 2.10.0

## Testing

```bash
pip install pytest
pytest tests/
```

## Building the docs

```bash
cd docs
make html
```

## License

BSD-style — see [LICENSE](LICENSE).
