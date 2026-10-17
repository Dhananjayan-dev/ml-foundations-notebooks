import json
from pathlib import Path


def test_notebooks_are_valid_json():
    for nb in Path("notebooks").glob("*.ipynb"):
        assert json.loads(nb.read_text(encoding="utf-8"))["nbformat"] == 4
