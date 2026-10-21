"""
Reusable UI Components for Crop Maturity & Health Assessment
Cards, stat tiles, image slots, sidebar, and page layouts.

Image slots accept an optional `source` (file path, bytes, PIL image or
numpy array). Results from the MATLAB backend (src/backend) are stored in
st.session_state.results and passed into the matching slots and tiles.
"""

import io
import json
from html import escape
from typing import Optional

import streamlit as st
from PIL import Image

from src.backend import BackendError, run_analysis
from .styles import section_label


CROPS = ["Select crop", "Coffee", "Tomato", "Mango"]
PAGES = [
    "Dashboard",
    "Image Processing",
    "Feature Analysis",
    "Maturity Assessment",
    "Health Assessment",
    "Final Report",
]


# ============================================================================
# HELPERS
# ============================================================================

def _html(markup: str):
    """Render HTML. Lines are stripped so Markdown never treats them as code."""
    flat = "".join(line.strip() for line in markup.splitlines())
    st.markdown(flat, unsafe_allow_html=True)


def init_state():
    """Create the session keys the UI relies on."""
    defaults = {
        "image_bytes": None,
        "image_name": None,
        "crop_type": "Select crop",
        "analysis_requested": False,
        "uploader_id": 0,
        # Filled in later by the processing backend:
        "results": {},
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)

    # Sync widget values early so the sidebar is never one step behind
    if "_crop_select" in st.session_state:
        st.session_state.crop_type = st.session_state["_crop_select"]

    uploaded = st.session_state.get(f"uploader_{st.session_state.uploader_id}")
    if uploaded is not None:
        data = uploaded.getvalue()
        if data != st.session_state.image_bytes:
            st.session_state.image_bytes = data
            st.session_state.image_name = uploaded.name
            st.session_state.analysis_requested = False
            st.session_state.results = {}


def _clear_image():
    st.session_state.image_bytes = None
    st.session_state.image_name = None
    st.session_state.analysis_requested = False
    st.session_state.results = {}
    st.session_state.uploader_id += 1


def _request_analysis():
    if st.session_state.image_bytes is not None and st.session_state.crop_type != "Select crop":
        st.session_state.analysis_requested = True


def _image_info() -> Optional[str]:
    """Return 'W x H px · size' for the stored image."""
    data = st.session_state.get("image_bytes")
    if not data:
        return None
    try:
        w, h = Image.open(io.BytesIO(data)).size
        return f"{w} x {h} px · {len(data) / 1024:.0f} KB"
    except Exception:
        return f"{len(data) / 1024:.0f} KB"


def _result(key: str) -> Optional[str]:
    """Read a backend result value, or None if not available yet."""
    return st.session_state.get("results", {}).get(key)


def _output(key: str) -> Optional[str]:
    """Path of a MATLAB output image, or None if not available yet."""
    return st.session_state.get("results", {}).get("images", {}).get(key)


def _fmt(value, spec: str = ".2f") -> str:
    return "n/a" if value is None else format(value, spec)


def _summarise(raw: dict) -> dict:
    """Turn the MATLAB results into the short strings the tiles display."""
    f = raw["features"]
    res = {
        "ok": raw["ok"],
        "images": raw["images"],
        "features": f,
        "output_dir": raw["output_dir"],
        "crop": st.session_state.crop_type,
    }
    if not (raw["ok"] and f):
        return res

    res["color_features"] = _fmt(f.get("mean_L"), ".1f")
    res["color_features_sub"] = (
        f"Mean L* · a* {_fmt(f.get('mean_a'))} · b* {_fmt(f.get('mean_b'))}"
    )
    res["texture_features"] = _fmt(f.get("mean_entropy"))
    res["texture_features_sub"] = f"Mean entropy · GLCM contrast {_fmt(f.get('glcm_contrast'))}"
    res["shape_features"] = _fmt(f.get("solidity"))
    res["shape_features_sub"] = f"Solidity · eccentricity {_fmt(f.get('eccentricity'))}"
    if f.get("edge_density") is not None:
        res["edge_features"] = f"{f['edge_density'] * 100:.1f}%"
        res["edge_features_sub"] = "Canny edge pixels in fruit"

    hues = {
        "green": f.get("frac_green"),
        "yellow": f.get("frac_yellow"),
        "red-orange": f.get("frac_red"),
    }
    hues = {k: v for k, v in hues.items() if v is not None}
    if hues:
        name = max(hues, key=hues.get)
        res["maturity_evidence"] = f"{hues[name] * 100:.0f}% {name}"
        res["maturity_evidence_sub"] = "Largest hue class in fruit"
    return res


def _sub(key: str, default: str) -> str:
    """Tile caption from the results, falling back to the static text."""
    return _result(f"{key}_sub") or default


def _run_backend():
    """Run the MATLAB pipeline on the stored image and save the results."""
    try:
        with st.spinner("Running MATLAB pipeline..."):
            raw = run_analysis(
                st.session_state.image_bytes,
                st.session_state.image_name or "input.png",
            )
    except BackendError as exc:
        st.session_state.analysis_requested = False
        st.error(str(exc))
        return
    st.session_state.results = _summarise(raw)
    st.session_state.analysis_requested = False
    if raw["ok"]:
        st.toast("Analysis complete.")
    else:
        st.toast("Segmentation did not find a plausible fruit region.")
    st.rerun()


# ============================================================================
# BUILDING BLOCKS
# ============================================================================

def page_header(eyebrow: str, title: str, subtitle: str = "", small: bool = True):
    """Animated page header. `title` may contain a <span class='cv-grad'>."""
    size = " cv-title-sm" if small else ""
    sub = f"<p class='cv-subtitle'>{subtitle}</p>" if subtitle else ""
    _html(f"""
        <div class="cv-eyebrow"><span class="cv-dot on"></span>{eyebrow}</div>
        <h1 class="cv-title{size}">{title}</h1>
        {sub}
    """)


def section_header(title: str, subtitle: str = "", label: str = ""):
    """Backward-compatible wrapper around page_header."""
    page_header(label or "CropVision", title, subtitle)


def stat_tile(label: str, value: Optional[str], sub: str = "", tone: str = ""):
    """Small metric tile. value=None shows a pending dash."""
    shown = escape(value) if value else "&mdash;"
    pending = "" if value else " pending"
    tone_cls = f" tone-{tone}" if (tone and value) else ""
    _html(f"""
        <div class="cv-stat{tone_cls}">
            <div class="cv-stat-label">{label}</div>
            <div class="cv-stat-value{pending}">{shown}</div>
            <div class="cv-stat-sub">{sub}</div>
        </div>
    """)


def image_slot(title: str, key: str, source=None, empty_text: str = "Awaiting output"):
    """
    Card that shows an image, or an animated placeholder if source is None.
    `key` must be unique on the page.
    """
    with st.container(key=f"card_{key}"):
        tag = "<span class='cv-tag live'>Ready</span>" if source is not None else "<span class='cv-tag'>Pending</span>"
        _html(f"""
            <div class="cv-slot-head">
                <span class="cv-slot-title">{title}</span>{tag}
            </div>
        """)
        if source is not None:
            st.image(source, width="stretch")
        else:
            _html(f"""
                <div class="cv-placeholder">
                    <div class="cv-frame"></div>
                    <div>{empty_text}</div>
                </div>
            """)


def notice(title: str, body: str, kind: str = "warning"):
    """Inline notice with a coloured bar. kind: warning | info."""
    cls = "info" if kind == "info" else ""
    _html(f"""
        <div class="cv-notice {cls}">
            <div class="cv-bar"></div>
            <div><b>{title}</b>&nbsp; {body}</div>
        </div>
    """)


def _chips():
    """Status chips summarising the current session."""
    has_img = st.session_state.image_bytes is not None
    crop = st.session_state.crop_type
    has_crop = crop != "Select crop"
    queued = st.session_state.analysis_requested
    done = bool(st.session_state.results)
    _html(f"""
        <div class="cv-chips">
            <span class="cv-chip"><span class="cv-dot {'on' if has_img else ''}"></span>
                {'Image loaded' if has_img else 'No image'}</span>
            <span class="cv-chip"><span class="cv-dot {'on' if has_crop else ''}"></span>
                {escape(crop) if has_crop else 'No crop selected'}</span>
            <span class="cv-chip"><span class="cv-dot {'on' if done else 'wait' if queued else ''}"></span>
                {'Analysis complete' if done else 'Analysis queued' if queued else 'Idle'}</span>
        </div>
    """)


# ============================================================================
# SIDEBAR
# ============================================================================

def render_sidebar() -> str:
    """Brand, navigation and session card. Returns the selected page."""
    with st.sidebar:
        _html("""
            <div class="cv-brand">
                <div class="cv-logo"></div>
                <div>
                    <div class="cv-brand-name">CropVision</div>
                    <div class="cv-brand-sub">Maturity &amp; health</div>
                </div>
            </div>
            <div class="cv-side-label">Navigate</div>
        """)

        page = st.radio(
            "Navigation",
            PAGES,
            label_visibility="collapsed",
            key="main_nav",
        )

        name = st.session_state.image_name or "None"
        crop = st.session_state.crop_type
        crop = crop if crop != "Select crop" else "None"
        if st.session_state.results:
            status = "Complete"
        else:
            status = "Queued" if st.session_state.analysis_requested else "Idle"
        _html(f"""
            <div class="cv-session">
                <div class="cv-side-label" style="margin-left:0">Session</div>
                <div class="cv-session-row"><span>Image</span><b>{escape(name)}</b></div>
                <div class="cv-session-row"><span>Crop</span><b>{escape(crop)}</b></div>
                <div class="cv-session-row"><span>Status</span><b>{status}</b></div>
            </div>
        """)
    return page


# ============================================================================
# DASHBOARD
# ============================================================================

def _upload_card():
    """Upload card. Image bytes persist in session state across pages."""
    with st.container(key="card_upload"):
        _html("""
            <div class="cv-card-head">
                <span class="cv-step">01</span>
                <span class="cv-card-title">Upload image</span>
                <span class="cv-card-meta">JPG · JPEG · PNG</span>
            </div>
        """)
        st.file_uploader(
            "Crop image",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed",
            key=f"uploader_{st.session_state.uploader_id}",
        )
        # (stored into session state by init_state on each run)

        if st.session_state.image_bytes is not None:
            st.image(st.session_state.image_bytes, width="stretch")
            info_col, btn_col = st.columns([3, 1], vertical_alignment="center")
            with info_col:
                _html(f"""
                    <div class="cv-stat-sub">
                        <b style="color:var(--cv-text)">{escape(st.session_state.image_name or '')}</b><br>
                        {_image_info() or ''}
                    </div>
                """)
            with btn_col:
                st.button("Clear", key="clear_img", type="tertiary", on_click=_clear_image)


def _configure_card():
    """Crop selection, readiness checklist and the Analyze button."""
    with st.container(key="card_config"):
        _html("""
            <div class="cv-card-head">
                <span class="cv-step">02</span>
                <span class="cv-card-title">Configure and run</span>
            </div>
        """)

        # Mirror into a widget key so the choice survives page switches
        if "_crop_select" not in st.session_state:
            st.session_state["_crop_select"] = st.session_state.crop_type
        crop = st.selectbox("Crop type", CROPS, key="_crop_select")
        st.session_state.crop_type = crop

        has_img = st.session_state.image_bytes is not None
        has_crop = crop != "Select crop"
        _html(f"""
            <div class="cv-checklist">
                <div class="cv-check {'done' if has_img else ''}"><i></i>Image uploaded</div>
                <div class="cv-check {'done' if has_crop else ''}"><i></i>Crop type selected</div>
            </div>
        """)

        st.write("")
        if st.button("Analyze image", key="analyze_btn", type="primary", width="stretch",
                     on_click=_request_analysis):
            if has_img and has_crop:
                _run_backend()
            elif not has_img:
                st.warning("Upload an image first.")
            else:
                st.warning("Select a crop type.")


def dashboard_page():
    """Main dashboard: upload, configure, quick results."""
    page_header(
        "Digital image processing",
        "Crop maturity<br><span class='cv-grad'>&amp; health</span>",
        "Upload a still image, choose the crop, and run the assessment.",
        small=False,
    )
    _chips()

    left, right = st.columns([1.35, 1], gap="large")
    with left:
        _upload_card()
    with right:
        _configure_card()

    section_label("Results at a glance")
    c1, c2, c3, c4 = st.columns(4, gap="medium")
    crop = st.session_state.crop_type
    with c1:
        stat_tile("Crop", crop if crop != "Select crop" else None, "Selected type", "accent")
    with c2:
        stat_tile("Maturity", _result("maturity"), "Not ready · Ready · Overripe", "accent")
    with c3:
        stat_tile("Health", _result("health"), "Visible condition", "warning")
    with c4:
        stat_tile("Affected area", _result("affected_area"), "Of crop region", "danger")


# ============================================================================
# OTHER PAGES
# ============================================================================

def image_processing_page():
    """Original image and preprocessing outputs."""
    page_header(
        "Preprocessing",
        "Image <span class='cv-grad'>processing</span>",
    )
    _chips()

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        image_slot("Original", "ip_original", st.session_state.image_bytes, "Upload an image on the dashboard")
    with c2:
        image_slot("Denoised", "ip_denoised", _output("denoised"))
    c3, c4 = st.columns(2, gap="medium")
    with c3:
        image_slot("Contrast enhanced", "ip_contrast", _output("enhanced"))
    with c4:
        image_slot("Colour space (L* a* b*)", "ip_colorspace", _output("colorspace"))


def feature_analysis_page():
    """Extracted features and segmentation outputs."""
    page_header(
        "Segmentation and features",
        "Feature <span class='cv-grad'>analysis</span>",
    )
    _chips()

    c1, c2, c3, c4 = st.columns(4, gap="medium")
    with c1:
        stat_tile("Colour", _result("color_features"), _sub("color_features", "Colour moments"))
    with c2:
        stat_tile("Texture", _result("texture_features"), _sub("texture_features", "Texture analysis"))
    with c3:
        stat_tile("Shape", _result("shape_features"), _sub("shape_features", "Shape descriptors"))
    with c4:
        stat_tile("Edges", _result("edge_features"), _sub("edge_features", "Edge detection"))

    section_label("Visual outputs")
    c5, c6 = st.columns(2, gap="medium")
    with c5:
        image_slot("Segmentation mask", "fa_mask", _output("mask"))
    with c6:
        image_slot("Edge map", "fa_edges", _output("edges"))


def maturity_assessment_page():
    """Maturity stage scale and evidence."""
    page_header(
        "Maturity",
        "Maturity <span class='cv-grad'>assessment</span>",
    )
    _chips()

    current = _result("maturity")
    stages = [
        ("s-not", "Not ready", "Early development"),
        ("s-ready", "Ready", "Harvest window"),
        ("s-over", "Overripe", "Past optimal window"),
    ]
    cards = "".join(
        f"""<div class="cv-stage {cls} {'active' if current == name else ''}">
                <div class="cv-stage-bar"></div>
                <div class="cv-stage-name">{name}</div>
                <div class="cv-stage-hint">{hint}</div>
            </div>"""
        for cls, name, hint in stages
    )
    _html(f"<div class='cv-scale'>{cards}</div>")

    section_label("Results")
    tab1, tab2, tab3 = st.tabs(["Overview", "Visual evidence", "Details"])
    with tab1:
        c1, c2, c3 = st.columns(3, gap="medium")
        with c1:
            stat_tile("Stage", current, "Assessed maturity", "accent")
        with c2:
            stat_tile("Crop", _result("crop"), "Analysed crop")
        with c3:
            stat_tile("Evidence", _result("maturity_evidence"), _sub("maturity_evidence", "Key measurement"))
    with tab2:
        c1, c2 = st.columns(2, gap="medium")
        with c1:
            image_slot("Input", "mt_input", st.session_state.image_bytes, "Upload an image on the dashboard")
        with c2:
            image_slot("Ripeness map", "mt_map", _output("ripeness_map"))
    with tab3:
        with st.container(key="card_mt_details"):
            features = _result("features")
            if features:
                rows = "".join(
                    f"<div class='cv-row'><span>{escape(name)}</span><b>{_fmt(value, '.4f')}</b></div>"
                    for name, value in features.items()
                )
                _html(f"""
                    <div class="cv-slot-head"><span class="cv-slot-title">Measurements</span>
                    <span class="cv-tag live">Ready</span></div>
                    <div class="cv-rows">{rows}</div>
                """)
            else:
                _html("""
                    <div class="cv-slot-head"><span class="cv-slot-title">Measurements</span>
                    <span class="cv-tag">Pending</span></div>
                    <div class="cv-stat-sub">Detailed measurements appear here after analysis.</div>
                """)


def health_assessment_page():
    """Visible abnormality results."""
    page_header(
        "Health",
        "Health <span class='cv-grad'>assessment</span>",
    )
    _chips()

    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        stat_tile("Condition", _result("health"), "Detected condition", "warning")
    with c2:
        stat_tile("Affected area", _result("affected_area"), "Of crop region", "danger")
    with c3:
        stat_tile("Severity", _result("severity"), "Visible extent")

    section_label("Detected regions")
    c4, c5 = st.columns(2, gap="medium")
    with c4:
        image_slot("Abnormal region mask", "ha_mask", empty_text="Not produced by the MATLAB pipeline yet")
    with c5:
        image_slot("Overlay", "ha_overlay", empty_text="Not produced by the MATLAB pipeline yet")

    notice(
        "Disclaimer",
        "Image-based assessment of visible characteristics only. No pesticide, "
        "medication, or treatment recommendations. Validate results with an expert.",
    )


def final_report_page():
    """Summary of all results and export actions."""
    page_header(
        "Report",
        "Analysis <span class='cv-grad'>report</span>",
    )
    _chips()

    crop = st.session_state.crop_type
    rows = [
        ("Input image", st.session_state.image_name),
        ("Crop", crop if crop != "Select crop" else None),
        ("Maturity", _result("maturity")),
        ("Health", _result("health")),
        ("Affected area", _result("affected_area")),
        ("Severity", _result("severity")),
    ]
    row_html = "".join(
        f"<div class='cv-row'><span>{label}</span>"
        f"<b class='{'' if value else 'pending'}'>{escape(value) if value else 'Pending'}</b></div>"
        for label, value in rows
    )

    left, right = st.columns([1.5, 1], gap="large")
    with left:
        _html(f"""
            <div class="cv-card">
                <div class="cv-card-head"><span class="cv-card-title">Summary</span></div>
                <div class="cv-rows">{row_html}</div>
            </div>
        """)
    with right:
        with st.container(key="card_export"):
            _html("""
                <div class="cv-card-head"><span class="cv-card-title">Export</span></div>
            """)
            done = bool(st.session_state.results)
            if done:
                st.download_button("Download report", _report_text(rows), "cropvision_report.txt",
                                   mime="text/plain", key="download_btn", width="stretch")
                st.download_button("Export results", json.dumps(_result("features") or {}, indent=2),
                                   "cropvision_features.json", mime="application/json",
                                   key="export_btn", width="stretch")
            else:
                st.button("Download report", key="download_btn", disabled=True, width="stretch")
                st.button("Export results", key="export_btn", disabled=True, width="stretch")
            hint = "Report and MATLAB measurements." if done else "Available after analysis completes."
            _html(f"<div class='cv-stat-sub' style='margin-top:0.5rem'>{hint}</div>")

        section_label("Input")
        image_slot("Input image", "rp_input", st.session_state.image_bytes, "No image uploaded")


def _report_text(rows) -> str:
    """Plain-text report: the summary rows plus every MATLAB measurement."""
    lines = ["CropVision - Crop maturity and health assessment", ""]
    lines += [f"{label}: {value or 'Pending'}" for label, value in rows]
    features = _result("features") or {}
    if features:
        lines += ["", "Measurements (MATLAB)"]
        lines += [f"  {name}: {_fmt(value, '.4f')}" for name, value in features.items()]
    lines += ["", "Image-based assessment of visible characteristics only."]
    return "\n".join(lines) + "\n"


def render_footer():
    """Small footer line."""
    _html("""
        <div class="cv-footer">
            <span>CropVision · Crop maturity &amp; health assessment</span>
            <span>Digital Image Processing mini project</span>
        </div>
    """)
