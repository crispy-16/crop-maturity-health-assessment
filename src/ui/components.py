"""
Reusable UI Components for Crop Maturity & Health Assessment
Provides styled cards, metrics, and layout elements
"""

import streamlit as st
from typing import Optional


def metric_card(title: str, value: str, subtitle: str = "", icon: str = ""):
    """
    Render a modern metric card.
    
    Args:
        title: Card title
        value: Main value to display
        subtitle: Optional subtitle text
        icon: Optional emoji/icon
    """
    col = st.columns(1)[0]
    with col:
        card_html = f"""
        <div class="modern-card">
            <div class="card-header">
                {f'<span style="font-size: 1.5rem; margin-right: 0.5rem;">{icon}</span>' if icon else ''}
                <h3 style="margin: 0; font-family: 'Space Grotesk', sans-serif;">{title}</h3>
            </div>
            <div style="font-size: 2rem; font-weight: 700; color: #16A34A; margin: 1rem 0; font-family: 'Space Grotesk', sans-serif;">
                {value}
            </div>
            {f'<div class="card-subtitle">{subtitle}</div>' if subtitle else ''}
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)


def section_header(title: str, subtitle: str = "", label: str = ""):
    """
    Render a professional section header.
    
    Args:
        title: Main heading
        subtitle: Optional subtitle
        label: Optional label above title
    """
    if label:
        st.markdown(f'<div class="section-label">{label}</div>', unsafe_allow_html=True)
    st.markdown(f"# {title}")
    if subtitle:
        st.markdown(f"<p style='color: #94A3B8; font-size: 0.95rem; margin-top: -0.75rem; line-height: 1.6;'>{subtitle}</p>", unsafe_allow_html=True)


def feature_card(number: str, title: str, value: str, description: str = ""):
    """
    Render a feature/capability card.
    
    Args:
        number: Card number (01, 02, etc.)
        title: Card title
        value: Main value/metric
        description: Optional description text
    """
    card_html = f"""
    <div class="feature-card">
        <div style="font-size: 0.85rem; font-weight: 700; color: #16A34A; margin-bottom: 0.75rem; letter-spacing: 0.5px; font-family: 'Space Grotesk', sans-serif;">
            {number}
        </div>
        <div class="feature-card-title">{title}</div>
        <div class="feature-card-value">{value}</div>
        {f'<div class="feature-card-description">{description}</div>' if description else ''}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def render_pipeline():
    """Render the complete DIP processing pipeline as numbered stage cards only."""
    st.markdown("<div class='section-label'>DIP Processing Pipeline</div>", unsafe_allow_html=True)
    
    pipeline_stages = [
        ("01", "", "Image Input", "Upload crop image"),
        ("02", "", "Preprocessing", "Prepare image"),
        ("03", "", "Segmentation", "Isolate regions"),
        ("04", "", "Feature Extraction", "Analyze visual features"),
        ("05", "", "Maturity + Health", "Assess crop condition"),
        ("06", "", "Report", "Generate results"),
    ]
    
    pipeline_html = '<div class="pipeline-container">'
    
    for number, icon, title, description in pipeline_stages:
        pipeline_html += f'''
        <div class="pipeline-step">
            <div class="pipeline-step-box">
                <div class="pipeline-step-icon">{icon}</div>
                <div class="pipeline-step-number">{number}</div>
                <div class="pipeline-step-title">{title}</div>
            </div>
        </div>
        '''
    
    pipeline_html += '</div>'
    
    st.markdown(pipeline_html, unsafe_allow_html=True)


def analysis_card():
    """Render the main analysis card with upload and crop selection."""
    st.markdown("<div class='section-label'>Analysis Workflow</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div class="modern-card">
            <div class="card-header">
                <span style="font-size: 1.5rem;"></span>
                <h3 style="margin: 0; font-family: 'Space Grotesk', sans-serif;">Upload Crop Image</h3>
            </div>
            <p style="color: #94A3B8; margin-bottom: 1rem;">JPG / JPEG / PNG</p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
        
        if uploaded_file:
            st.image(uploaded_file, use_column_width=True, caption=f"{uploaded_file.name}")
            st.markdown(f"""
            <div style="margin-top: 0.75rem; padding: 1rem; background: #052E16; border-radius: 8px; border-left: 4px solid #16A34A; box-sizing: border-box;">
                <div style="font-weight: 600; color: #86EFAC; font-size: 0.9rem; font-family: 'DM Sans', sans-serif;">Image Loaded</div>
                <div style="font-size: 0.85rem; color: #16A34A; margin-top: 0.25rem; font-family: 'DM Sans', sans-serif;">Ready for analysis</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 2.5rem 1rem; color: #94A3B8; box-sizing: border-box;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;"></div>
                <div style="font-weight: 500; font-family: 'DM Sans', sans-serif;">Drag and drop or click to upload</div>
            </div>
            """, unsafe_allow_html=True)
        
        return uploaded_file
    
    with col2:
        st.markdown("""
        <div class="modern-card">
            <div class="card-header">
                <span style="font-size: 1.5rem;"></span>
                <h3 style="margin: 0; font-family: 'Space Grotesk', sans-serif;">Crop Selection</h3>
            </div>
            <p style="color: #94A3B8; margin-bottom: 1rem;">Select the crop type for analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        crop_type = st.selectbox(
            "Crop Type",
            ["Select crop", "Coffee", "Tomato", "Mango"],
            label_visibility="collapsed"
        )
        
        st.markdown(f"""
        <div style="margin-top: 1rem; padding: 1rem; background: #0F172A; border-radius: 8px; border: 1px solid #334155; box-sizing: border-box;">
            <div style="font-size: 0.85rem; color: #94A3B8; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px; margin-bottom: 0.5rem; font-family: 'DM Sans', sans-serif;">Selected Crop</div>
            <div style="font-size: 1.25rem; font-weight: 700; color: #16A34A; font-family: 'Space Grotesk', sans-serif;">{crop_type}</div>
        </div>
        """, unsafe_allow_html=True)
        
        return crop_type


def render_quick_overview():
    """Render quick overview capability cards."""
    st.markdown("<div class='section-label'>Key Capabilities</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        feature_card("01", "Image Processing", "Preprocessing", "Noise reduction & enhancement")
    
    with col2:
        feature_card("02", "Segmentation", "Region Analysis", "Identify crop areas")
    
    with col3:
        feature_card("03", "Feature Extraction", "Data Analysis", "Compute quantitative metrics")
    
    col4, col5, col6 = st.columns(3, gap="medium")
    
    with col4:
        feature_card("04", "Maturity Estimation", "Development Stage", "Growth prediction model")
    
    with col5:
        feature_card("05", "Health Detection", "Abnormality Scan", "Identify visible defects")
    
    with col6:
        feature_card("06", "Comprehensive Report", "Documentation", "Export & analysis summary")


def render_project_info():
    """Render project information and technical details."""
    st.markdown("<div class='section-label'>About This System</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div class="modern-card">
            <div class="card-header">
                <span style="font-size: 1.5rem;"></span>
                <h3 style="margin: 0; font-family: 'Space Grotesk', sans-serif;">Purpose</h3>
            </div>
            <p style="color: #94A3B8; line-height: 1.7; font-family: 'DM Sans', sans-serif;">
                This Digital Image Processing system applies computer vision techniques to analyze crop images and estimate maturity stages while identifying visible health abnormalities.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="modern-card">
            <div class="card-header">
                <span style="font-size: 1.5rem;"></span>
                <h3 style="margin: 0; font-family: 'Space Grotesk', sans-serif;">Technology</h3>
            </div>
            <p style="color: #94A3B8; line-height: 1.7; font-family: 'DM Sans', sans-serif;">
                Built with Python, Streamlit, and image processing libraries. Implements DIP pipeline stages for preprocessing, segmentation, and feature extraction.
            </p>
        </div>
        """, unsafe_allow_html=True)


def image_processing_page():
    """Render the Image Processing page."""
    section_header(
        "Image Processing",
        "Preprocessing and enhancement techniques for crop analysis",
        "IMAGE PROCESSING • PREPROCESSING"
    )
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div class="modern-card">
            <div class="card-header">
                <span style="font-size: 1.5rem;"></span>
                <h3 style="margin: 0; font-family: 'Space Grotesk', sans-serif;">Preprocessing Steps</h3>
            </div>
            <div style="margin-top: 1rem; display: flex; flex-direction: column; gap: 0.75rem;">
                <div style="padding: 0.75rem; background: #0F172A; border-radius: 6px; border-left: 3px solid #16A34A; box-sizing: border-box;">
                    <div style="font-weight: 600; color: #86EFAC; font-size: 0.9rem; font-family: 'DM Sans', sans-serif;">Noise Reduction</div>
                </div>
                <div style="padding: 0.75rem; background: #0F172A; border-radius: 6px; border-left: 3px solid #16A34A; box-sizing: border-box;">
                    <div style="font-weight: 600; color: #86EFAC; font-size: 0.9rem; font-family: 'DM Sans', sans-serif;">Contrast Enhancement</div>
                </div>
                <div style="padding: 0.75rem; background: #0F172A; border-radius: 6px; border-left: 3px solid #16A34A; box-sizing: border-box;">
                    <div style="font-weight: 600; color: #86EFAC; font-size: 0.9rem; font-family: 'DM Sans', sans-serif;">Color Space Conversion</div>
                </div>
                <div style="padding: 0.75rem; background: #0F172A; border-radius: 6px; border-left: 3px solid #16A34A; box-sizing: border-box;">
                    <div style="font-weight: 600; color: #86EFAC; font-size: 0.9rem; font-family: 'DM Sans', sans-serif;">Histogram Equalization</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="modern-card">
            <div class="card-header">
                <span style="font-size: 1.5rem;"></span>
                <h3 style="margin: 0; font-family: 'Space Grotesk', sans-serif;">Processing Results</h3>
            </div>
            <div style="margin-top: 1rem; text-align: center; padding: 2rem; background: #0F172A; border-radius: 8px; color: #94A3B8; box-sizing: border-box;">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;"></div>
                <div style="font-weight: 500; font-family: 'DM Sans', sans-serif;">Awaiting image analysis</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def feature_analysis_page():
    """Render the Feature Analysis page."""
    section_header(
        "Feature Analysis",
        "Quantitative metrics and feature extraction results",
        "FEATURE ANALYSIS • QUANTIFICATION"
    )
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div class="modern-card">
            <div class="card-header">
                <span style="font-size: 1.5rem;"></span>
                <h3 style="margin: 0; font-family: 'Space Grotesk', sans-serif;">Extracted Features</h3>
            </div>
            <div style="margin-top: 1rem; display: flex; flex-direction: column; gap: 0.75rem;">
                <div>
                    <div style="font-weight: 600; color: #E2E8F0; font-size: 0.9rem; margin-bottom: 0.25rem; font-family: 'DM Sans', sans-serif;">Color Moments</div>
                    <div style="padding: 0.75rem; background: #0F172A; border-radius: 6px; color: #94A3B8; font-size: 0.9rem; font-family: 'DM Sans', sans-serif; box-sizing: border-box;">Awaiting analysis</div>
                </div>
                <div>
                    <div style="font-weight: 600; color: #E2E8F0; font-size: 0.9rem; margin-bottom: 0.25rem; font-family: 'DM Sans', sans-serif;">Texture Analysis</div>
                    <div style="padding: 0.75rem; background: #0F172A; border-radius: 6px; color: #94A3B8; font-size: 0.9rem; font-family: 'DM Sans', sans-serif; box-sizing: border-box;">Awaiting analysis</div>
                </div>
                <div>
                    <div style="font-weight: 600; color: #E2E8F0; font-size: 0.9rem; margin-bottom: 0.25rem; font-family: 'DM Sans', sans-serif;">Shape Descriptors</div>
                    <div style="padding: 0.75rem; background: #0F172A; border-radius: 6px; color: #94A3B8; font-size: 0.9rem; font-family: 'DM Sans', sans-serif; box-sizing: border-box;">Awaiting analysis</div>
                </div>
                <div>
                    <div style="font-weight: 600; color: #E2E8F0; font-size: 0.9rem; margin-bottom: 0.25rem; font-family: 'DM Sans', sans-serif;">Edge Detection</div>
                    <div style="padding: 0.75rem; background: #0F172A; border-radius: 6px; color: #94A3B8; font-size: 0.9rem; font-family: 'DM Sans', sans-serif; box-sizing: border-box;">Awaiting analysis</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="modern-card">
            <div class="card-header">
                <span style="font-size: 1.5rem;"></span>
                <h3 style="margin: 0; font-family: 'Space Grotesk', sans-serif;">Feature Vector</h3>
            </div>
            <div style="margin-top: 1rem; text-align: center; padding: 2rem; background: #0F172A; border-radius: 8px; color: #94A3B8; box-sizing: border-box;">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;"></div>
                <div style="font-weight: 500; font-family: 'DM Sans', sans-serif;">Awaiting image analysis</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def maturity_assessment_page():
    """Render the Maturity Assessment page."""
    section_header(
        "Maturity Assessment",
        "Estimate development stage and ripeness level",
        "MATURITY ANALYSIS • GROWTH STAGE"
    )
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.markdown("""
        <div class="modern-card" style="border-left: 4px solid #94A3B8; background: rgba(148, 163, 184, 0.05);">
            <div style="font-weight: 700; color: #94A3B8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem; font-family: 'DM Sans', sans-serif;">Status</div>
            <div style="font-size: 2rem; font-weight: 700; color: #94A3B8; margin: 0.75rem 0; font-family: 'Space Grotesk', sans-serif;">UNRIPE</div>
            <p class="card-subtitle">Early development stage</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="modern-card" style="border-left: 4px solid #F59E0B; background: rgba(245, 158, 11, 0.08);">
            <div style="font-weight: 700; color: #D97706; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem; font-family: 'DM Sans', sans-serif;">Status</div>
            <div style="font-size: 2rem; font-weight: 700; color: #D97706; margin: 0.75rem 0; font-family: 'Space Grotesk', sans-serif;">READY</div>
            <p class="card-subtitle">Optimal harvest window</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="modern-card" style="border-left: 4px solid #EF4444; background: rgba(239, 68, 68, 0.08);">
            <div style="font-weight: 700; color: #EF4444; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem; font-family: 'DM Sans', sans-serif;">Status</div>
            <div style="font-size: 2rem; font-weight: 700; color: #DC2626; margin: 0.75rem 0; font-family: 'Space Grotesk', sans-serif;">OVERRIPE</div>
            <p class="card-subtitle">Recommend immediate harvest</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-label' style='margin-top: 2rem;'>Analysis Results</div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Overview", "Visual Evidence", "Details"])
    
    with tab1:
        st.markdown("""
        <div class="modern-card">
            <div style="text-align: center; padding: 2rem; color: #94A3B8; box-sizing: border-box;">
                <div style="font-size: 2rem; margin-bottom: 1rem;"></div>
                <div style="font-weight: 500; font-family: 'DM Sans', sans-serif;">Awaiting image analysis</div>
                <p style="font-family: 'DM Sans', sans-serif;">Upload an image and click "Analyze Image" to begin</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div class="modern-card">
            <div style="text-align: center; padding: 2rem; color: #94A3B8; box-sizing: border-box;">
                <div style="font-size: 2rem; margin-bottom: 1rem;"></div>
                <div style="font-weight: 500; font-family: 'DM Sans', sans-serif;">Awaiting image analysis</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("""
        <div class="modern-card">
            <div style="text-align: center; padding: 2rem; color: #94A3B8; box-sizing: border-box;">
                <div style="font-size: 2rem; margin-bottom: 1rem;"></div>
                <div style="font-weight: 500; font-family: 'DM Sans', sans-serif;">Awaiting image analysis</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def health_assessment_page():
    """Render the Health Assessment page."""
    section_header(
        "Health Assessment",
        "Detect visible abnormalities and health indicators",
        "HEALTH ANALYSIS • ABNORMALITY DETECTION"
    )
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div class="modern-card">
            <div class="card-header">
                <span style="font-size: 1.5rem;"></span>
                <h3 style="margin: 0; font-family: 'Space Grotesk', sans-serif;">Visible Assessment</h3>
            </div>
            <div style="margin-top: 1rem; display: flex; flex-direction: column; gap: 0.75rem;">
                <div>
                    <div style="font-weight: 600; color: #E2E8F0; font-size: 0.9rem; margin-bottom: 0.25rem; font-family: 'DM Sans', sans-serif;">Detected Condition</div>
                    <div style="padding: 0.75rem; background: #0F172A; border-radius: 6px; color: #94A3B8; font-size: 0.9rem; font-family: 'DM Sans', sans-serif; box-sizing: border-box;">Awaiting analysis</div>
                </div>
                <div>
                    <div style="font-weight: 600; color: #E2E8F0; font-size: 0.9rem; margin-bottom: 0.25rem; font-family: 'DM Sans', sans-serif;">Likelihood</div>
                    <div style="padding: 0.75rem; background: #0F172A; border-radius: 6px; color: #94A3B8; font-size: 0.9rem; font-family: 'DM Sans', sans-serif; box-sizing: border-box;">—</div>
                </div>
                <div>
                    <div style="font-weight: 600; color: #E2E8F0; font-size: 0.9rem; margin-bottom: 0.25rem; font-family: 'DM Sans', sans-serif;">Affected Area</div>
                    <div style="padding: 0.75rem; background: #0F172A; border-radius: 6px; color: #94A3B8; font-size: 0.9rem; font-family: 'DM Sans', sans-serif; box-sizing: border-box;">—</div>
                </div>
                <div>
                    <div style="font-weight: 600; color: #E2E8F0; font-size: 0.9rem; margin-bottom: 0.25rem; font-family: 'DM Sans', sans-serif;">Severity</div>
                    <div style="padding: 0.75rem; background: #0F172A; border-radius: 6px; color: #94A3B8; font-size: 0.9rem; font-family: 'DM Sans', sans-serif; box-sizing: border-box;">—</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="modern-card">
            <div class="card-header">
                <span style="font-size: 1.5rem;"></span>
                <h3 style="margin: 0; font-family: 'Space Grotesk', sans-serif;">Detected Regions</h3>
            </div>
            <div style="margin-top: 1rem; text-align: center; padding: 2rem; background: #0F172A; border-radius: 8px; color: #94A3B8; box-sizing: border-box;">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;"></div>
                <div style="font-weight: 500; font-family: 'DM Sans', sans-serif;">Awaiting analysis</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-top: 2rem; padding: 1.25rem; background: #451A03; border-left: 4px solid #F59E0B; border-radius: 8px; box-sizing: border-box;">
        <div style="font-weight: 600; color: #FDE68A; margin-bottom: 0.5rem; font-family: 'Space Grotesk', sans-serif;">Important Disclaimer</div>
        <p style="margin: 0; color: #FBBF24; font-size: 0.9rem; font-family: 'DM Sans', sans-serif;">
            This system is intended for image-based assessment of visible abnormalities and does not provide medical, pesticide, or treatment recommendations. Results should be validated by agricultural experts.
        </p>
    </div>
    """, unsafe_allow_html=True)


def final_report_page():
    """Render the Final Report page."""
    section_header(
        "Analysis Report",
        "Complete assessment summary and export options",
        "FINAL REPORT • DOCUMENTATION"
    )
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div class="modern-card">
            <div class="card-header">
                <span style="font-size: 1.5rem;"></span>
                <h3 style="margin: 0; font-family: 'Space Grotesk', sans-serif;">Report Contents</h3>
            </div>
            <div style="margin-top: 1rem; display: flex; flex-direction: column; gap: 0.75rem;">
                <div style="padding: 0.75rem; background: #0F172A; border-radius: 6px; border-left: 3px solid #16A34A; box-sizing: border-box;">
                    <div style="font-weight: 600; color: #86EFAC; font-size: 0.9rem; font-family: 'DM Sans', sans-serif;">Input Image</div>
                </div>
                <div style="padding: 0.75rem; background: #0F172A; border-radius: 6px; border-left: 3px solid #16A34A; box-sizing: border-box;">
                    <div style="font-weight: 600; color: #86EFAC; font-size: 0.9rem; font-family: 'DM Sans', sans-serif;">Crop Information</div>
                </div>
                <div style="padding: 0.75rem; background: #0F172A; border-radius: 6px; border-left: 3px solid #16A34A; box-sizing: border-box;">
                    <div style="font-weight: 600; color: #86EFAC; font-size: 0.9rem; font-family: 'DM Sans', sans-serif;">Maturity Assessment</div>
                </div>
                <div style="padding: 0.75rem; background: #0F172A; border-radius: 6px; border-left: 3px solid #16A34A; box-sizing: border-box;">
                    <div style="font-weight: 600; color: #86EFAC; font-size: 0.9rem; font-family: 'DM Sans', sans-serif;">Health Assessment</div>
                </div>
                <div style="padding: 0.75rem; background: #0F172A; border-radius: 6px; border-left: 3px solid #16A34A; box-sizing: border-box;">
                    <div style="font-weight: 600; color: #86EFAC; font-size: 0.9rem; font-family: 'DM Sans', sans-serif;">Affected Area Estimation</div>
                </div>
                <div style="padding: 0.75rem; background: #0F172A; border-radius: 6px; border-left: 3px solid #16A34A; box-sizing: border-box;">
                    <div style="font-weight: 600; color: #86EFAC; font-size: 0.9rem; font-family: 'DM Sans', sans-serif;">Visual Evidence</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="modern-card">
            <div class="card-header">
                <span style="font-size: 1.5rem;"></span>
                <h3 style="margin: 0; font-family: 'Space Grotesk', sans-serif;">Export Options</h3>
            </div>
            <div style="margin-top: 1rem; display: flex; flex-direction: column; gap: 0.75rem;">
        """, unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.button("Download Report", key="download_btn", disabled=True, use_container_width=True)
        with col_b:
            st.button(" Export Results", key="export_btn", disabled=True, use_container_width=True)
        
        st.markdown("""
            </div>
            <p class="card-subtitle" style="margin-top: 1rem;">Buttons enabled after analysis completes</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-top: 2rem; padding: 1.25rem; background: #052E16; border-left: 4px solid #16A34A; border-radius: 8px; box-sizing: border-box;">
        <div style="font-weight: 600; color: #86EFAC; margin-bottom: 0.5rem; font-family: 'Space Grotesk', sans-serif;">Report Status</div>
        <p style="margin: 0; color: #16A34A; font-size: 0.9rem; font-family: 'DM Sans', sans-serif;">
            No analysis performed yet. Upload an image and select a crop type to generate a comprehensive report.
        </p>
    </div>
    """, unsafe_allow_html=True)