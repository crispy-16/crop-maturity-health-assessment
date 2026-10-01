"""
UI Module for Crop Maturity & Health Assessment
Provides styles, components, and page layouts
"""

from .styles import load_global_css, section_divider, section_label, status_badge
from .components import (
    metric_card,
    section_header,
    feature_card,
    render_pipeline,
    analysis_card,
    render_quick_overview,
    render_project_info,
    image_processing_page,
    feature_analysis_page,
    maturity_assessment_page,
    health_assessment_page,
    final_report_page,
)

__all__ = [
    "load_global_css",
    "section_divider",
    "section_label",
    "status_badge",
    "metric_card",
    "section_header",
    "feature_card",
    "render_pipeline",
    "analysis_card",
    "render_quick_overview",
    "render_project_info",
    "image_processing_page",
    "feature_analysis_page",
    "maturity_assessment_page",
    "health_assessment_page",
    "final_report_page",
]