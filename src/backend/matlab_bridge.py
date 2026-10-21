"""
Bridge between the Streamlit UI and the MATLAB pipeline.

The uploaded image is saved to outputs/dashboard/<id>/, MATLAB's
run_dashboard.m is called through the MATLAB Engine for Python, and the
results.json it writes is read back into a plain dict.

Folder layout this expects (the project root is found automatically):

    Crop_Assessment/                      <- project root (has matlab/)
    ├── matlab/                           <- process_image.m, run_dashboard.m, ...
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


class BackendError(RuntimeError):
    """Raised with a message that can be shown to the user as-is."""


def project_root() -> Optional[Path]:
    """Folder that contains matlab/process_image.m, or None if not found."""
    env = os.environ.get("CROPVISION_ROOT")
    if env:
        root = Path(env)
        return root if (root / "matlab" / "process_image.m").is_file() else None
    for folder in [REPO_DIR, *REPO_DIR.parents]:
        if (folder / "matlab" / "process_image.m").is_file():
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
    {"ok": bool, "images": {name: absolute path}, "features": {name: float}}
    Results for an image that was already analysed are reused.
    """
    root = project_root()
    if root is None:
        raise BackendError(
            "Could not find the MATLAB folder. Put this repo inside the folder "
            "that contains matlab/, or set CROPVISION_ROOT."
        )
    matlab_dir = root / "matlab"
    if not (matlab_dir / "run_dashboard.m").is_file():
        raise BackendError(f"run_dashboard.m is missing from {matlab_dir}.")

    run_id = hashlib.sha1(image_bytes).hexdigest()[:12]
    out_dir = root / "outputs" / "dashboard" / run_id
    json_path = out_dir / "results.json"

    if not json_path.is_file():
        out_dir.mkdir(parents=True, exist_ok=True)
        ext = Path(image_name).suffix.lower() or ".png"
        input_path = out_dir / f"input{ext}"
        input_path.write_bytes(image_bytes)
        try:
            eng = _engine(str(matlab_dir))
            json_path = Path(eng.run_dashboard(str(input_path), str(out_dir), nargout=1))
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
    features = data.get("features") or {}
    if isinstance(features, list):  # jsonencode writes an empty struct as []
        features = {}
    return {
        "ok": bool(data.get("ok")),
        "images": images,
        "features": features,
        "output_dir": str(out_dir),
    }
