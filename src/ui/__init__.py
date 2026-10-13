"""
UI Module for Crop Maturity & Health Assessment
Provides styles, components, and page layouts
"""

from .styles import THEME, load_global_css, section_divider, section_label, status_badge
from .components import (
    init_state,
    render_sidebar,
    render_footer,
    page_header,
    section_header,
    stat_tile,
    image_slot,
    notice,
    dashboard_page,
    image_processing_page,
    feature_analysis_page,
    maturity_assessment_page,
    health_assessment_page,
    final_report_page,
)

__all__ = [
    "THEME",
    "load_global_css",
    "section_divider",
    "section_label",
    "status_badge",
    "init_state",
    "render_sidebar",
    "render_footer",
    "page_header",
    "section_header",
    "stat_tile",
    "image_slot",
    "notice",
    "dashboard_page",
    "image_processing_page",
    "feature_analysis_page",
    "maturity_assessment_page",
    "health_assessment_page",
    "final_report_page",
]
