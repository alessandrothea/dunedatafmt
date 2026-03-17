"""Smoke tests for datafmt package imports."""


def test_version():
    import importlib.metadata
    version = importlib.metadata.version("datafmt")
    assert version == "4.2.1"


def test_import_daqdataformats():
    import daqdataformats  # noqa: F401


def test_import_detdataformats():
    import detdataformats  # noqa: F401


def test_import_fddetdataformats():
    import fddetdataformats  # noqa: F401


def test_import_trgdataformats():
    import trgdataformats  # noqa: F401


def test_import_rawdatautils():
    import rawdatautils  # noqa: F401


if __name__ == "__main__":
    test_version()
    test_import_daqdataformats()
    test_import_detdataformats()
    test_import_fddetdataformats()
    test_import_trgdataformats()
    test_import_rawdatautils()
    print("All tests passed.")
