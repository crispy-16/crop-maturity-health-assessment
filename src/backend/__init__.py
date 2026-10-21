"""
Processing backend: runs the MATLAB pipeline and returns its outputs.
"""

from .matlab_bridge import BackendError, project_root, run_analysis

__all__ = ["BackendError", "project_root", "run_analysis"]
