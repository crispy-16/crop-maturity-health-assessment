"""
Crop Maturity & Health Assessment
A Digital Image Processing application for analyzing crop health and maturity
using computer vision techniques.
 
Main application entry point with sidebar navigation and page routing.
"""
 
import streamlit as st
from src.ui import load_global_css
from src.ui.components import (
    analysis_card,
    render_quick_overview,
    render_project_info,
    image_processing_page,
    feature_analysis_page,
    maturity_assessment_page,
    health_assessment_page,
    final_report_page,
)
 
 
# Page configuration
st.set_page_config(
    page_title="CropVision - Maturity & Health Assessment",
    layout="wide",
    initial_sidebar_state="expanded",
)
 
# Load global CSS styling
load_global_css()
 
# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================
 
with st.sidebar:
    # Sidebar header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem; padding-top: 1rem;">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;"></div>
        <h1 style="margin: 0; font-size: 1.5rem; color: #FFFFFF; font-family: 'Space Grotesk', sans-serif;">CropVision</h1>
        <p style="margin: 0.25rem 0 0 0; font-size: 0.85rem; color: #94A3B8; letter-spacing: 0.5px; font-family: 'DM Sans', sans-serif;">
            DIGITAL IMAGE PROCESSING<br>AGRICULTURAL INTELLIGENCE
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border-color: rgba(255, 255, 255, 0.1); margin: 1.5rem 0;'>", unsafe_allow_html=True)
    
    # Navigation sections
    st.markdown("""
    <div style="font-size: 0.75rem; font-weight: 700; letter-spacing: 1px; color: #64748B; text-transform: uppercase; margin-top: 1.5rem; margin-bottom: 0.75rem; font-family: 'DM Sans', sans-serif;">
        OVERVIEW
    </div>
    """, unsafe_allow_html=True)
    
    page = st.radio(
        "Navigation",
        ["Dashboard", "Image Processing", "Feature Analysis", "Maturity Assessment", "Health Assessment", "Final Report"],
        label_visibility="collapsed",
        key="main_nav",
    )
    
    st.markdown("""
    <div style="font-size: 0.75rem; font-weight: 700; letter-spacing: 1px; color: #64748B; text-transform: uppercase; margin-top: 1.5rem; margin-bottom: 0.75rem; font-family: 'DM Sans', sans-serif;">
        ANALYSIS
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="font-size: 0.75rem; font-weight: 700; letter-spacing: 1px; color: #64748B; text-transform: uppercase; margin-top: 1.5rem; margin-bottom: 0.75rem; font-family: 'DM Sans', sans-serif;">
        REPORTING
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border-color: rgba(255, 255, 255, 0.1); margin: 2rem 0;'>", unsafe_allow_html=True)
    
    # System status card
    st.markdown("""
    <div style="background: rgba(22, 163, 74, 0.1); border: 1px solid rgba(22, 163, 74, 0.2); border-radius: 10px; padding: 1rem; margin-top: 1.5rem;">
        <div style="font-size: 0.75rem; font-weight: 700; letter-spacing: 1px; color: #94A3B8; text-transform: uppercase; margin-bottom: 0.75rem; font-family: 'DM Sans', sans-serif;">
            System Status
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.75rem;">
            <span style="width: 8px; height: 8px; background: #22C55E; border-radius: 50%; display: inline-block;"></span>
            <span style="color: #E2E8F0; font-weight: 500; font-size: 0.9rem; font-family: 'DM Sans', sans-serif;">Prototype Active</span>
        </div>
        <div style="border-top: 1px solid rgba(255, 255, 255, 0.1); padding-top: 0.75rem;">
            <div style="font-size: 0.8rem; color: #94A3B8; font-family: 'DM Sans', sans-serif;">DIP Pipeline</div>
            <div style="color: #22C55E; font-weight: 600; font-size: 0.9rem; font-family: 'Space Grotesk', sans-serif;">Ready for analysis</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
 
 
# ============================================================================
# MAIN CONTENT AREA
# ============================================================================
 
if page == "Dashboard":
    # Dashboard header
    st.markdown("""
    <div style="margin-bottom: 2.5rem;">
        <div style="font-size: 0.75rem; font-weight: 700; letter-spacing: 1px; color: #94A3B8; text-transform: uppercase; margin-bottom: 0.75rem; font-family: 'DM Sans', sans-serif;">
            Digital Image Processing • Agricultural Analytics
        </div>
        <h1 style="margin: 0.75rem 0 0 0; font-size: 3rem; font-weight: 700; background: linear-gradient(135deg, #86EFAC 0%, #22C55E 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-family: 'Space Grotesk', sans-serif;">
            Crop Maturity<br>& Health Assessment
        </h1>
        <p style="margin-top: 1.25rem; color: #94A3B8; font-size: 1rem; line-height: 1.7; font-family: 'DM Sans', sans-serif;">
            Analyze crop images using digital image processing techniques to estimate maturity and identify visible health abnormalities.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Status badge
    st.markdown("""
    <div style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.6rem 1.25rem; background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 24px; margin-bottom: 2.5rem;">
        <span style="width: 8px; height: 8px; background: #22C55E; border-radius: 50%;"></span>
        <span style="color: #16A34A; font-weight: 600; font-size: 0.9rem; font-family: 'DM Sans', sans-serif;">DIP SYSTEM READY</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 2.5rem 0;'>", unsafe_allow_html=True)
    
    # Analysis card with upload
    uploaded_file = analysis_card()
    crop_type = st.session_state.get("crop_type", "Select crop")
    
    # Analyze button
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("Analyze Image", use_container_width=True, key="analyze_btn"):
            if uploaded_file and crop_type != "Select crop":
                st.success("Analysis initiated. Processing pipeline connecting...")
                st.info("DIP pipeline will process: preprocessing → segmentation → feature extraction → maturity/health assessment")
            elif not uploaded_file:
                st.warning("Please upload an image first")
            else:
                st.warning("Please select a crop type")
    
    st.markdown("<div style='margin: 3.5rem 0; border-top: 1px solid #334155;'></div>", unsafe_allow_html=True)
    
    # Quick overview cards
    render_quick_overview()
    
    st.markdown("<div style='margin: 3.5rem 0;'></div>", unsafe_allow_html=True)
    
    # Project information
    render_project_info()
 
 
elif page == "Image Processing":
    image_processing_page()
 
 
elif page == "Feature Analysis":
    feature_analysis_page()
 
 
elif page == "Maturity Assessment":
    maturity_assessment_page()
 
 
elif page == "Health Assessment":
    health_assessment_page()
 
 
elif page == "Final Report":
    final_report_page()
 
 
# ============================================================================
# FOOTER
# ============================================================================
 
st.markdown("""
<hr style='margin-top: 3rem; border-color: #334155;'>
<div style='text-align: center; padding: 1.5rem 0; color: #94A3B8; font-size: 0.85rem; font-family: "DM Sans", sans-serif; box-sizing: border-box; width: 100%; max-width: 100%;'>
    <p style='margin: 0.5rem 0;'>Crop Maturity & Health Assessment v1.0</p>
    <p style='margin: 0.5rem 0;'>Digital Image Processing System • Agricultural Intelligence</p>
</div>
""", unsafe_allow_html=True)