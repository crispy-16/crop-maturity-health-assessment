"""
Bridge between the Streamlit UI and the MATLAB pipeline.

The uploaded image is saved to outputs/dashboard/<id>/, MATLAB's
crop_pipeline.m is called through the MATLAB Engine for Python, and the
results.json it writes is read back into a plain dict. crop_pipeline.m runs
the stages as a chain and lists them, in order, under "stages".

Folder layout this expects (the project root is found automatically):

    Crop_Assessment/                      <- project root (has matlab/)
    ├── matlab/                           <- crop_pipeline.m, ...
    ├── outputs/dashboard/                <- written by each analysis
    └── crop-maturity-health-assessment/  <- this repo

Set the environment variable CROPVISION_ROOT to override the project root.
"""

import hashlib
import json
import os
from pathlib import Path
from typing import Optional

import streamlit as st


REPO_DIR = Path(__file__).resolve().parents[2]

# Bump together with out.version in crop_pipeline.m; older saved results are re-run.
PIPELINE_VERSION = 3
PIPELINE_FILE = "crop_pipeline.m"


class BackendError(RuntimeError):
    """Raised with a message that can be shown to the user as-is."""


def project_root() -> Optional[Path]:
    """Folder that contains matlab/crop_pipeline.m, or None if not found."""
    env = os.environ.get("CROPVISION_ROOT")
    if env:
        root = Path(env)
        return root if (root / "matlab" / PIPELINE_FILE).is_file() else None
    for folder in [REPO_DIR, *REPO_DIR.parents]:
        if (folder / "matlab" / PIPELINE_FILE).is_file():
            return folder
    return None


@st.cache_resource(show_spinner="Starting MATLAB (first run only)...")
def _engine(matlab_dir: str):
    """Start one MATLAB session and keep it for the whole Streamlit server."""
    try:
        import matlab.engine
    except ImportError as exc:
        raise BackendError(
            "MATLAB Engine for Python is not installed in this environment."
        ) from exc
    eng = matlab.engine.start_matlab()
    eng.addpath(matlab_dir, nargout=0)
    return eng


def run_analysis(image_bytes: bytes, image_name: str) -> dict:
    """
    Run the MATLAB pipeline on one image and return its results:
    {"ok": bool, "stages": [{key, title, operation, input, path}, ...],
     "images": {stage key: absolute path}, "features": {name: float}}
    Results for an image that was already analysed are reused.
    """
    root = project_root()
    if root is None:
        raise BackendError(
            "Could not find matlab/crop_pipeline.m. Put this repo inside the folder "
            "that contains matlab/, or set CROPVISION_ROOT."
        )
    matlab_dir = root / "matlab"

    run_id = hashlib.sha1(image_bytes).hexdigest()[:12]
    out_dir = root / "outputs" / "dashboard" / run_id
    json_path = out_dir / "results.json"

    if not _is_current(json_path):
        out_dir.mkdir(parents=True, exist_ok=True)
        ext = Path(image_name).suffix.lower() or ".png"
        input_path = out_dir / f"input{ext}"
        input_path.write_bytes(image_bytes)
        try:
            eng = _engine(str(matlab_dir))
            json_path = Path(eng.crop_pipeline(str(input_path), str(out_dir), nargout=1))
        except BackendError:
            raise
        except Exception as exc:
            raise BackendError(f"MATLAB reported an error: {exc}") from exc

    data = json.loads(json_path.read_text(encoding="utf-8"))
    images = {
        key: str(out_dir / name)
        for key, name in data.get("images", {}).items()
        if (out_dir / name).is_file()
    }
    stages = data.get("stages") or []
    if isinstance(stages, dict):  # jsonencode writes a 1x1 struct array as an object
        stages = [stages]
    stages = [
        {**stage, "path": str(out_dir / stage["file"])}
        for stage in stages
        if (out_dir / stage.get("file", "")).is_file()
    ]
    features = data.get("features") or {}
    if isinstance(features, list):  # jsonencode writes an empty struct as []
        features = {}
    return {
        "ok": bool(data.get("ok")),
        "stages": stages,
        "images": images,
        "features": features,
        "output_dir": str(out_dir),
    }


def _is_current(json_path: Path) -> bool:
    """True if results.json exists and was written by this pipeline version."""
    if not json_path.is_file():
        return False
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except ValueError:
        return False
    return data.get("version") == PIPELINE_VERSION
