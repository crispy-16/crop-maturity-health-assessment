"""
CropVision — Crop Maturity & Health Assessment
Digital Image Processing mini project (Streamlit front end).

Main entry point: page config, global styles, sidebar navigation, routing.
"""

import streamlit as st

from src.ui import load_global_css
from src.ui.components import (
    init_state,
    render_sidebar,
    render_footer,
    dashboard_page,
    image_processing_page,
    feature_analysis_page,
    maturity_assessment_page,
    health_assessment_page,
    final_report_page,
)


st.set_page_config(
    page_title="CropVision - Maturity & Health Assessment",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_global_css()
init_state()

page = render_sidebar()

ROUTES = {
    "Dashboard": dashboard_page,
    "Image Processing": image_processing_page,
    "Feature Analysis": feature_analysis_page,
    "Maturity Assessment": maturity_assessment_page,
    "Health Assessment": health_assessment_page,
    "Final Report": final_report_page,
}

ROUTES[page]()
render_footer()
