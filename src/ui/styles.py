"""
UI Styles for Crop Maturity & Health Assessment
Handles all CSS, theme customization, and visual styling
"""

import streamlit as st


def load_global_css():
    """Load global CSS styling for the entire application."""
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
        font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* ==================== COLOR PALETTE ==================== */
    :root {
        --color-primary-dark: #86EFAC;
        --color-primary: #22C55E;
        --color-primary-light: #4ADE80;
        --color-primary-lighter: #052E16;
        --color-bg-dark: #0F172A;
        --color-slate: #334155;
        --color-slate-light: #1E293B;
        --color-white: #111827;
        --color-warning: #F59E0B;
        --color-error: #EF4444;
        --color-border: #334155;
        --color-text-primary: #E5E7EB;
        --color-text-secondary: #94A3B8;
        --color-shadow: rgba(0, 0, 0, 0.35);
        --color-shadow-lg: rgba(0, 0, 0, 0.5);
    }
    
    /* ==================== MAIN LAYOUT ==================== */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0B1220 0%, #0F172A 100%);
        color: var(--color-text-primary);
        width: 100%;
        max-width: 100%;
        box-sizing: border-box;
        overflow-x: hidden;
    }
    
    [data-testid="stMainBlockContainer"] {
        padding: 2.5rem 2rem;
        max-width: 100%;
        width: 100%;
        box-sizing: border-box;
        margin: 0 auto;
    }
    
    /* ==================== SIDEBAR ==================== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        box-sizing: border-box;
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlockBigContainer"] {
        padding: 1.5rem 1rem;
        box-sizing: border-box;
    }
    
    /* ==================== SIDEBAR COLLAPSE CONTROL ==================== */
    /*
       Keep Streamlit's native sidebar toggle functional. The previous
       rule hid the entire control, which made the sidebar impossible
       to close. We hide only the leaked icon-label text and provide a
       clean visual chevron while preserving the native button action.
    */
    [data-testid="stSidebarCollapseButton"] {
        display: block !important;
    }

    [data-testid="stSidebarCollapseButton"] button,
    button[aria-label*="Close sidebar"],
    button[aria-label*="Open sidebar"],
    button[title*="Close sidebar"],
    button[title*="Open sidebar"] {
        position: relative !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 2.25rem !important;
        min-width: 2.25rem !important;
        height: 2.25rem !important;
        min-height: 2.25rem !important;
        padding: 0 !important;
        margin: 0 !important;
        border: 1px solid rgba(148, 163, 184, 0.25) !important;
        border-radius: 8px !important;
        background: rgba(15, 23, 42, 0.75) !important;
        color: transparent !important;
        font-size: 0 !important;
        line-height: 0 !important;
        box-shadow: none !important;
        z-index: 999999 !important;
    }

    [data-testid="stSidebarCollapseButton"] button:hover,
    button[aria-label*="Close sidebar"]:hover,
    button[aria-label*="Open sidebar"]:hover,
    button[title*="Close sidebar"]:hover,
    button[title*="Open sidebar"]:hover {
        background: rgba(22, 163, 74, 0.18) !important;
        border-color: rgba(34, 197, 94, 0.45) !important;
    }

    /* Hide Streamlit/material icon text inside the native control. */
    [data-testid="stSidebarCollapseButton"] button > span,
    [data-testid="stSidebarCollapseButton"] button > div,
    [data-testid="stSidebarCollapseButton"] button > svg,
    button[aria-label*="Close sidebar"] > span,
    button[aria-label*="Open sidebar"] > span {
        display: none !important;
    }

    /* Render a simple, reliable visual indicator without replacing the button. */
    [data-testid="stSidebarCollapseButton"] button::before,
    button[aria-label*="Close sidebar"]::before,
    button[aria-label*="Open sidebar"]::before {
        content: "‹";
        display: block !important;
        color: #E2E8F0 !important;
        font-family: Arial, sans-serif !important;
        font-size: 1.65rem !important;
        font-weight: 400 !important;
        line-height: 1 !important;
        width: auto !important;
        height: auto !important;
    }

    button[aria-label*="Open sidebar"]::before {
        content: "›";
    }

    /* ==================== TEXT STYLING ==================== */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: var(--color-text-primary);
    }
    
    h1 {
        font-size: 3rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        line-height: 1.2;
        margin-bottom: 0.75rem;
    }
    
    h2 {
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin-top: 2rem;
        margin-bottom: 1rem;
        line-height: 1.3;
    }
    
    h3 {
        font-size: 1.375rem;
        font-weight: 600;
        letter-spacing: -0.01em;
        margin-bottom: 0.75rem;
        line-height: 1.3;
    }
    
    h4, h5, h6 {
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    p {
        color: var(--color-text-secondary);
        line-height: 1.7;
        font-size: 0.95rem;
        font-weight: 400;
    }
    
    /* ==================== BUTTONS ==================== */
    button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        font-family: 'DM Sans', sans-serif;
        box-sizing: border-box;
    }
    
    [data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
        color: white !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(22, 163, 74, 0.25);
    }
    
    [data-testid="baseButton-primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(22, 163, 74, 0.35);
    }
    
    [data-testid="baseButton-secondary"] {
        background: var(--color-slate-light);
        color: var(--color-text-primary) !important;
        border: 1px solid var(--color-border) !important;
    }
    
    [data-testid="baseButton-secondary"]:hover {
        background: #1E293B;
        border-color: var(--color-primary) !important;
    }
    
    /* ==================== INPUT ELEMENTS ==================== */
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stSelectbox"] div {
        border-radius: 8px !important;
        border: 1px solid var(--color-border) !important;
        background: var(--color-white) !important;
        font-family: 'DM Sans', sans-serif !important;
        box-sizing: border-box !important;
    }
    
    [data-testid="stTextInput"] input:focus,
    [data-testid="stNumberInput"] input:focus {
        border-color: var(--color-primary) !important;
        box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.1) !important;
    }
    
    /* ==================== SELECTBOX ==================== */
    [data-testid="stSelectbox"] {
        margin-top: 0.5rem;
    }
    
    [role="combobox"] {
        border-radius: 8px !important;
        border: 1px solid var(--color-border) !important;
        padding: 0.75rem 1rem !important;
        background: var(--color-white) !important;
        color: var(--color-text-primary) !important;
        font-weight: 500;
        font-family: 'DM Sans', sans-serif !important;
        box-sizing: border-box !important;
    }
    
    [role="combobox"]:hover {
        border-color: var(--color-primary) !important;
    }
    
    /* ==================== FILE UPLOADER ==================== */
    [data-testid="stFileUploadDropzone"] {
        border: 2px dashed var(--color-primary) !important;
        border-radius: 12px !important;
        background: rgba(22, 163, 74, 0.05) !important;
        padding: 2rem 1rem !important;
        text-align: center;
        transition: all 0.3s ease;
        box-sizing: border-box !important;
    }
    
    [data-testid="stFileUploadDropzone"]:hover {
        border-color: var(--color-primary-dark) !important;
        background: rgba(22, 163, 74, 0.1) !important;
    }
    
    [data-testid="stFileUploadDropzone"] div {
        color: var(--color-primary) !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    
    /* ==================== TABS ==================== */
    [data-testid="stTabs"] {
        margin-top: 1.5rem;
    }
    
    button[data-testid="stTabBarButton"] {
        background: transparent !important;
        color: var(--color-text-secondary) !important;
        border-bottom: 2px solid transparent !important;
        border-radius: 0 !important;
        padding: 0.75rem 1.25rem !important;
        font-weight: 500;
        transition: all 0.3s ease;
        font-family: 'DM Sans', sans-serif !important;
        box-sizing: border-box !important;
    }
    
    button[data-testid="stTabBarButton"]:hover {
        color: var(--color-primary) !important;
    }
    
    button[aria-selected="true"][data-testid="stTabBarButton"] {
        color: var(--color-primary) !important;
        border-bottom-color: var(--color-primary) !important;
    }
    
    /* ==================== CARDS & CONTAINERS ==================== */
    [data-testid="stVerticalBlockBigContainer"] > [data-testid="stVerticalBlock"] > [data-testid="stColumn"] {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-sizing: border-box;
    }
    
    .modern-card {
        background: var(--color-white);
        border-radius: 12px;
        border: 1px solid var(--color-border);
        padding: 1.75rem;
        box-shadow: 0 1px 3px var(--color-shadow);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-sizing: border-box;
    }
    
    .modern-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px var(--color-shadow-lg);
        border-color: rgba(22, 163, 74, 0.2);
    }
    
    .card-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }
    
    .card-header h3 {
        margin: 0;
        font-size: 1.25rem;
        font-weight: 600;
    }
    
    .card-subtitle {
        color: var(--color-text-secondary);
        font-size: 0.9rem;
        margin-top: 0.5rem;
        line-height: 1.6;
    }
    
    /* ==================== BADGES & STATUS ==================== */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: rgba(22, 163, 74, 0.1);
        color: var(--color-primary-dark);
        border-radius: 24px;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        font-family: 'DM Sans', sans-serif;
    }
    
    .status-badge.ready {
        background: rgba(34, 197, 94, 0.1);
        color: var(--color-primary);
    }
    
    .status-badge.warning {
        background: rgba(245, 158, 11, 0.1);
        color: var(--color-warning);
    }
    
    .status-badge.error {
        background: rgba(239, 68, 68, 0.1);
        color: var(--color-error);
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: currentColor;
        display: inline-block;
    }
    
    /* ==================== SECTION LABELS ==================== */
    .section-label {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1.2px;
        color: var(--color-text-secondary);
        text-transform: uppercase;
        margin-bottom: 1.25rem;
        margin-top: 2rem;
        font-family: 'DM Sans', sans-serif;
    }
    
    /* ==================== DIVIDER ==================== */
    hr {
        border: none;
        border-top: 1px solid var(--color-border);
        margin: 2rem 0;
        box-sizing: border-box;
    }
    
    /* ==================== FEATURE CARDS ==================== */
    .feature-card {
        background: var(--color-white);
        border: 1px solid var(--color-border);
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        box-sizing: border-box;
    }
    
    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 12px var(--color-shadow);
        border-color: var(--color-primary);
    }
    
    .feature-card-icon {
        font-size: 2.25rem;
        margin-bottom: 0.75rem;
    }
    
    .feature-card-title {
        font-weight: 600;
        font-size: 0.95rem;
        color: var(--color-text-primary);
        margin-bottom: 0.5rem;
        font-family: 'DM Sans', sans-serif;
    }
    
    .feature-card-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--color-primary);
        margin: 0.75rem 0;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .feature-card-description {
        font-size: 0.8rem;
        color: var(--color-text-secondary);
        font-family: 'DM Sans', sans-serif;
    }
    
    /* ==================== PIPELINE VISUALIZATION ==================== */
    .pipeline-container {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 1rem;
        margin: 2.5rem 0;
        width: 100%;
        max-width: 100%;
        box-sizing: border-box;
    }
    
    .pipeline-step {
        width: 100%;
        min-width: 0;
        box-sizing: border-box;
    }
    
    .pipeline-step-box {
        background: var(--color-white);
        border: 2px solid var(--color-border);
        border-radius: 12px;
        padding: 1.25rem 1rem;
        transition: all 0.3s ease;
        text-align: center;
        box-sizing: border-box;
        width: 100%;
    }
    
    .pipeline-step-box:hover {
        border-color: var(--color-primary);
        box-shadow: 0 4px 16px rgba(22, 163, 74, 0.15);
        transform: translateY(-3px);
    }
    
    .pipeline-step-number {
        font-weight: 700;
        color: var(--color-primary);
        font-size: 1.25rem;
        margin-bottom: 0.75rem;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .pipeline-step-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    .pipeline-step-title {
        font-weight: 600;
        font-size: 0.85rem;
        color: var(--color-text-primary);
        font-family: 'DM Sans', sans-serif;
        line-height: 1.4;
    }
    
    @media (max-width: 1200px) {
        .pipeline-container {
            grid-template-columns: repeat(3, minmax(0, 1fr));
        }
    }
    
    @media (max-width: 768px) {
        .pipeline-container {
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 1rem;
        }
    }
    
    @media (max-width: 480px) {
        .pipeline-container {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
    }
    
    /* ==================== ANIMATIONS ==================== */
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    [data-testid="stAppViewContainer"] {
        animation: fadeIn 0.5s ease-out;
    }
    
    .modern-card {
        animation: slideUp 0.5s ease-out;
    }
    
    /* Respect prefers-reduced-motion */
    @media (prefers-reduced-motion: reduce) {
        * {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
    
    /* ==================== SIDEBAR TEXT COLORS ==================== */
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] p {
        color: #E2E8F0;
        font-family: 'DM Sans', sans-serif;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #FFFFFF;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    /* ==================== SIDEBAR BUTTON ==================== */
    [data-testid="stSidebar"] [data-testid="baseButton-primary"] {
        width: 100%;
        background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
        margin-top: 0.5rem;
    }
    
    /* ==================== EXPANDER ==================== */
    [data-testid="stExpander"] {
        border: 1px solid var(--color-border) !important;
        border-radius: 8px !important;
        box-sizing: border-box !important;
    }
    
    [data-testid="stExpander"] button {
        color: var(--color-text-primary) !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    
    /* ==================== METRIC ELEMENTS ==================== */
    [data-testid="stMetric"] {
        background: var(--color-white);
        border: 1px solid var(--color-border);
        border-radius: 12px;
        padding: 1.5rem;
        box-sizing: border-box;
    }
    
    [data-testid="stMetric"] label {
        color: var(--color-text-secondary);
        font-weight: 500;
        font-family: 'DM Sans', sans-serif;
    }
    
    /* ==================== SCROLLBAR ==================== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--color-primary);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--color-primary-dark);
    }
    
    /* ==================== RESPONSIVE ==================== */
    @media (max-width: 768px) {
        h1 {
            font-size: 2rem;
            line-height: 1.2;
        }
        
        h2 {
            font-size: 1.5rem;
            line-height: 1.3;
        }
        
        [data-testid="stMainBlockContainer"] {
            padding: 1.5rem 1rem;
        }
    }
    
    @media (max-width: 480px) {
        h1 {
            font-size: 1.75rem;
        }
        
        h2 {
            font-size: 1.25rem;
        }
        
        [data-testid="stMainBlockContainer"] {
            padding: 1rem 0.75rem;
        }
    }

    /* ==================== DARK MODE BASE ==================== */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"],
    [data-testid="stHeader"], [data-testid="stToolbar"] {
        background-color: #0B1220 !important;
        color: #E5E7EB !important;
    }

    [data-testid="stMainBlockContainer"] {
        background: #0B1220 !important;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0B1220 0%, #111827 100%) !important;
    }

    [data-testid="stSidebar"] [data-testid="stVerticalBlockBigContainer"] {
        background: transparent !important;
    }

    [data-testid="stFileUploadDropzone"],
    [data-testid="stFileUploadDropzone"] section {
        background: #111827 !important;
        color: #E5E7EB !important;
    }

    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stSelectbox"] > div,
    [role="combobox"] {
        background: #111827 !important;
        color: #E5E7EB !important;
        border-color: #334155 !important;
    }

    [data-testid="stSelectbox"] svg,
    [role="combobox"] svg {
        color: #94A3B8 !important;
        fill: #94A3B8 !important;
    }

    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {
        color: inherit;
    }

    /* ==================== END DARK MODE BASE ==================== */
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def section_divider():
    """Render a styled section divider."""
    st.markdown("<hr>", unsafe_allow_html=True)


def section_label(text: str):
    """Render a section label with uppercase styling."""
    st.markdown(f'<div class="section-label">{text}</div>', unsafe_allow_html=True)


def status_badge(text: str, status: str = "ready"):
    """Render a status badge."""
    status_classes = {
        "ready": "ready",
        "warning": "warning",
        "error": "error",
        "neutral": ""
    }
    status_class = status_classes.get(status, "")
    dot_html = f'<span class="status-dot"></span> {text}'
    st.markdown(
        f'<div class="status-badge {status_class}">{dot_html}</div>',
        unsafe_allow_html=True
    )