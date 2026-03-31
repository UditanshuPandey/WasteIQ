import streamlit as st
import plotly.graph_objects as go
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import load_model, predict, get_disposal, safe_open_image, confidence_level
from utils import generate_gradcam, overlay_gradcam

st.set_page_config(page_title="Predict · WasteIQ", page_icon="🔍", layout="wide")

# ─── STYLES ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #080C0A;
    color: #E8F5E2;
}
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

[data-testid="stSidebar"] {
    background: #0D1410;
    border-right: 1px solid #1E3A28;
}
[data-testid="stSidebarNav"] a {
    color: #8FC99A !important;
    font-family: 'Syne', sans-serif;
    font-weight: 600;
}
[data-testid="stSidebarNav"] a:hover {
    background: #1A2E22 !important;
    color: #4AFF7A !important;
}
.main .block-container {
    padding: 3rem 4rem;
    max-width: 1100px;
}

/* Page Header */
.page-tag {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: #4AFF7A;
    text-transform: uppercase;
    background: #0F2018;
    border: 1px solid #2A5C3A;
    padding: 0.3rem 0.75rem;
    border-radius: 2px;
    margin-bottom: 0.5rem;
    display: inline-block;
}
.page-title {
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1;
    margin: 0 0 2rem 0;
    color: #E8F5E2;
}
.page-title span { color: #4AFF7A; }

/* Controls Section */
.controls-container {
    background: linear-gradient(135deg, #0D1410 0%, #111A14 100%);
    border: 1px solid #1E3A28;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 2rem;
}

.controls-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #1E3A28;
    flex-wrap: wrap;
    gap: 1rem;
}

.controls-title {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.controls-title h3 {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    margin: 0;
    color: #E8F5E2;
}

.controls-badge {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: #4AFF7A;
    background: #0F2018;
    padding: 0.25rem 0.6rem;
    border-radius: 4px;
    border: 1px solid #2A5C3A;
}

.activation-preview {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: #080C0A;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    border: 1px solid #1A2E22;
}

.activation-preview span {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: #4A7A5A;
}

.color-scale {
    display: flex;
    gap: 2px;
    height: 20px;
    border-radius: 3px;
    overflow: hidden;
}

.color-low { background: #2A5C8A; width: 20px; }
.color-mid { background: #FFAA44; width: 20px; }
.color-high { background: #FF4444; width: 20px; }

/* Control Cards */
.control-card {
    background: #0F2018;
    border: 1px solid #1E3A28;
    border-radius: 8px;
    padding: 1rem;
    transition: all 0.2s ease;
}

.control-card:hover {
    border-color: #4AFF7A;
}

/* Checkbox Style */
.stCheckbox > label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: #E8F5E2 !important;
}

/* Slider Style */
.stSlider > label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: #8FC99A !important;
}

/* Divider */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #4AFF7A, #2A8A4A, #4AFF7A, transparent);
    margin: 2rem 0;
    opacity: 0.3;
}

/* Upload Zone */
[data-testid="stFileUploader"] {
    background: #0D1410 !important;
    border: 1px dashed #2A5C3A !important;
    border-radius: 8px !important;
    padding: 1.5rem !important;
}
[data-testid="stFileUploader"]:hover { 
    border-color: #4AFF7A !important;
}
[data-testid="stFileUploader"] label {
    color: #5A8A6A !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
}

/* Batch Summary */
.batch-bar {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    background: #0D1410;
    border: 1px solid #1E3A28;
    border-radius: 8px;
    padding: 1rem 1.5rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}
.batch-stat {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: #5A8A6A;
}
.batch-stat strong { color: #C8E8D0; font-size: 0.9rem; }
.batch-divider { width: 1px; height: 1.2rem; background: #1E3A28; }

/* Result Card */
.result-card {
    border: 1px solid #1E3A28;
    border-radius: 12px;
    background: #0D1410;
    margin-bottom: 1.75rem;
    overflow: hidden;
}
.result-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.9rem 1.4rem;
    background: #080C0A;
    border-bottom: 1px solid #1A2E22;
}
.result-filename {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #4A7A5A;
}
.result-status {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #4AFF7A;
}

/* Prediction Info */
.pred-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #4A7A5A;
    margin-bottom: 0.3rem;
}
.pred-class {
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: #4AFF7A;
    margin-bottom: 0.1rem;
}
.conf-value {
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    color: #8FC99A;
    margin-bottom: 0.75rem;
}
.conf-bar-wrap {
    background: #0F1A12;
    border-radius: 2px;
    height: 4px;
    margin-bottom: 1rem;
    overflow: hidden;
    border: 1px solid #1A2E22;
}
.conf-bar-fill {
    height: 100%;
    border-radius: 2px;
    background: linear-gradient(90deg, #2A8A4A, #4AFF7A);
    transition: width 0.6s ease;
}

/* Confidence Warning */
.conf-warn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #FFAA00;
    background: #1A1200;
    border: 1px solid #4A3200;
    border-radius: 4px;
    padding: 0.35rem 0.75rem;
    margin-bottom: 1rem;
}
.conf-medium {
    color: #FFCC44;
    background: #141000;
    border-color: #3A2A00;
}

/* Disposal Badge */
.disposal-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.6rem 1.2rem;
    border-radius: 4px;
    font-weight: 700;
    font-size: 0.85rem;
    margin-bottom: 1.25rem;
}
.disposal-blue { background: #0A1820; border: 1px solid #1A4060; color: #60BFFF; }
.disposal-green { background: #0A1A10; border: 1px solid #1A4A28; color: #4AFF7A; }
.disposal-yellow { background: #1A1400; border: 1px solid #4A3A00; color: #FFCC44; }

/* Image Section */
.image-section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #4A7A5A;
    margin-bottom: 0.75rem;
}
.image-caption {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: #4A7A5A;
    text-align: center;
    margin-top: 0.5rem;
}

/* Empty State */
.empty-state {
    text-align: center;
    padding: 5rem 2rem;
    color: #3A5A48;
    background: #0D1410;
    border-radius: 12px;
    border: 1px dashed #1E3A28;
}
.empty-icon { font-size: 3.5rem; margin-bottom: 1rem; }
.empty-text {
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
}

/* Error Card */
.err-card {
    background: #1A0A0A;
    border: 1px solid #5A1A1A;
    border-radius: 8px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1.5rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #FF6A6A;
}

@media (max-width: 768px) {
    .main .block-container {
        padding: 2rem 1rem;
    }
    .controls-header {
        flex-direction: column;
        align-items: flex-start;
    }
}
</style>
""", unsafe_allow_html=True)

# ─── LOAD MODEL ──────────────────────────────────────────────────
@st.cache_resource
def get_model():
    return load_model()

model, class_names = get_model()

# ─── HELPERS ─────────────────────────────────────────────────────
CLASS_ICONS = {
    "cardboard": "📦", "glass": "🍾", "metal": "🔩",
    "paper": "📄", "plastic": "🧴", "trash": "🗑️"
}

def prob_chart(all_probs: dict, top_class: str):
    labels = [f"{CLASS_ICONS.get(c,'◾')} {c.capitalize()}" for c in all_probs]
    values = [round(v * 100, 1) for v in all_probs.values()]
    colors = ["#4AFF7A" if c == top_class else "#162A1E" for c in all_probs]
    borders = ["#4AFF7A" if c == top_class else "#1E3A28" for c in all_probs]

    fig = go.Figure(go.Bar(
        x=values, y=labels,
        orientation="h",
        marker=dict(color=colors, line=dict(color=borders, width=1)),
        text=[f"{v}%" for v in values],
        textposition="outside",
        textfont=dict(family="Space Mono", size=10, color="#5A8A6A"),
        hovertemplate="%{y}: %{x}%<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=48, t=4, b=4),
        height=210,
        xaxis=dict(range=[0, 115], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(
            showgrid=False, zeroline=False, autorange="reversed",
            tickfont=dict(family="Space Mono", size=10, color="#8FC99A"),
        ),
        showlegend=False,
    )
    return fig

# ─── PAGE HEADER ─────────────────────────────────────────────────
st.markdown("""
<div class="page-tag">🔍 Prediction Engine</div>
<h1 class="page-title">Classify <span>Waste</span></h1>
""", unsafe_allow_html=True)

import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device_label = "CUDA GPU" if str(device) == "cuda" else "CPU"
device_icon = "⚡" if str(device) == "cuda" else "💻"
st.markdown(f"""
<div style="font-family:'Space Mono',monospace;font-size:0.7rem;color:#4A7A5A;
     background:#0D1410;border:1px solid #1E3A28;border-radius:4px;
     display:inline-flex;align-items:center;gap:0.5rem;
     padding:0.4rem 0.9rem;margin-bottom:2rem;">
    {device_icon} Running on <strong style="color:#8FC99A">{device_label}</strong>
</div>
""", unsafe_allow_html=True)

# ─── CONTROLS SECTION ────────────────────────────────────────────
with st.container(border=True):
    # Header row
    head_left, head_right = st.columns([1, 1])
    with head_left:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:0.75rem;padding:0.25rem 0 0.75rem 0;
                    border-bottom:1px solid #1E3A28;margin-bottom:0.75rem;">
            <span style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#E8F5E2;">
                🔬 Model Explainability
            </span>
            <span style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#4AFF7A;
                         background:#0F2018;padding:0.25rem 0.6rem;border-radius:4px;
                         border:1px solid #2A5C3A;">Grad-CAM</span>
        </div>
        """, unsafe_allow_html=True)
    with head_right:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:0.75rem;padding:0.25rem 0 0.75rem 0;
                    border-bottom:1px solid #1E3A28;margin-bottom:0.75rem;justify-content:flex-end;">
            <span style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#4A7A5A;">
                Activation Map
            </span>
            <div style="display:flex;gap:2px;height:18px;border-radius:3px;overflow:hidden;">
                <div style="background:#2A5C8A;width:18px;"></div>
                <div style="background:#FFAA44;width:18px;"></div>
                <div style="background:#FF4444;width:18px;"></div>
            </div>
            <span style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#4A7A5A;">
                Low → High Importance
            </span>
        </div>
        """, unsafe_allow_html=True)

    # Controls row
    ctrl_left, ctrl_right = st.columns(2)
    with ctrl_left:
        show_gradcam = st.checkbox(
            "🔬 Show Grad-CAM",
            value=True,
            help="Visualize which regions influenced the model's decision"
        )
    with ctrl_right:
        alpha = st.slider(
            "🔥 Heatmap Intensity",
            min_value=0.0,
            max_value=1.0,
            value=0.4,
            step=0.05,
            help="Control the opacity of the Grad-CAM overlay"
        )
        alpha_percentage = int(alpha * 100)
        st.markdown(
            f'<div style="text-align:right;margin-top:-0.5rem;">'
            f'<span style="font-family:\'Space Mono\',monospace;font-size:0.7rem;color:#4AFF7A;">'
            f'🔥 {alpha_percentage}% opacity</span></div>',
            unsafe_allow_html=True
        )

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ─── UPLOADER ────────────────────────────────────────────────────
uploaded_files = st.file_uploader(
    "Drop images here — JPG, PNG, JPEG",
    type=["jpg", "png", "jpeg"],
    accept_multiple_files=True,
    label_visibility="visible"
)

# ─── RESULTS ─────────────────────────────────────────────────────
if uploaded_files:

    # Run inference on all files
    results, errors = [], []
    with st.spinner("🧠 Classifying waste using EfficientNet..."):
        progress = st.progress(0, text="Analysing images…")

        for i, file in enumerate(uploaded_files):
            img, err = safe_open_image(file)
            if err:
                errors.append((file.name, err))
            else:
                top_class, top_conf, all_probs = predict(model, class_names, img)
                class_idx = class_names.index(top_class)
                
                # Only generate Grad-CAM if toggle is ON
                gradcam_img = None
                if show_gradcam:
                    cam = generate_gradcam(model, img, class_idx)
                    gradcam_img = overlay_gradcam(img, cam, alpha)
                
                results.append((file, img, top_class, top_conf, all_probs, gradcam_img))
            progress.progress((i + 1) / len(uploaded_files))

        progress.empty()

    # Batch summary bar
    if results:
        total = len(results)
        recyclable = sum(1 for _, _, c, _, _, _ in results if c in ["glass", "metal", "cardboard", "paper", "plastic"])
        general = sum(1 for _, _, c, _, _, _ in results if c == "trash")
        low_n = sum(1 for _, _, _, cf, _, _ in results if confidence_level(cf) == "low")
        
        st.markdown(f"""
        <div class="batch-bar">
            <div class="batch-stat">📂 <strong>{total}</strong> image{"s" if total > 1 else ""} processed</div>
            <div class="batch-divider"></div>
            <div class="batch-stat">♻️ <strong>{recyclable}</strong> recyclable</div>
            <div class="batch-divider"></div>
            <div class="batch-stat">🗑️ <strong>{general}</strong> general waste</div>
            {f'<div class="batch-divider"></div><div class="batch-stat" style="color:#FFAA00">⚠ <strong style="color:#FFAA00">{low_n}</strong> low confidence</div>' if low_n else ''}
        </div>
        """, unsafe_allow_html=True)

    # Per-image result cards
    for file, image, top_class, top_conf, all_probs, gradcam_img in results:
        disposal_label, disposal_icon, disposal_cls = get_disposal(top_class)
        conf_pct = int(top_conf * 100)
        conf_lvl = confidence_level(top_conf)

        if conf_lvl == "low":
            warn_html = '<div class="conf-warn">⚠ Low confidence — verify manually</div>'
        elif conf_lvl == "medium":
            warn_html = '<div class="conf-warn conf-medium">◈ Moderate confidence</div>'
        else:
            warn_html = ""

        st.markdown(f"""
        <div class="result-card">
            <div class="result-header">
                <span class="result-filename">📄 {file.name}</span>
                <span class="result-status">PROCESSED ✓</span>
            </div>
        """, unsafe_allow_html=True)
        
        col_img, col_info = st.columns([1, 2])

        with col_img:
            if show_gradcam and gradcam_img is not None:
                st.markdown('<div class="image-section-label">📸 Model Analysis</div>', unsafe_allow_html=True)
                img_col1, img_col2 = st.columns(2)
                
                with img_col1:
                    st.image(image, use_container_width=True)
                    st.markdown('<div class="image-caption">Original Image</div>', unsafe_allow_html=True)
                
                with img_col2:
                    st.image(gradcam_img, use_container_width=True)
                    st.markdown(f'<div class="image-caption">Grad-CAM · α={alpha:.2f}</div>', unsafe_allow_html=True)
            else:
                st.image(image, use_container_width=True)
                if not show_gradcam:
                    st.markdown('<div class="image-caption">Original Image</div>', unsafe_allow_html=True)

        with col_info:
            st.markdown(f"""
            <div style="padding: 1rem 1rem 0 0.5rem">
                <div class="pred-label">Detected Class</div>
                <div class="pred-class">{top_class.upper()}</div>
                <div class="conf-value">Confidence · {conf_pct}%</div>
                <div class="conf-bar-wrap">
                    <div class="conf-bar-fill" style="width:{conf_pct}%"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if warn_html:
                st.markdown(warn_html, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="padding: 0 1rem">
                <div class="pred-label" style="margin-bottom:0.5rem">Disposal Method</div>
                <div class="disposal-badge {disposal_cls}">{disposal_icon} {disposal_label}</div>
                <div class="prob-section-label">All-Class Probabilities</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.plotly_chart(
                prob_chart(all_probs, top_class),
                use_container_width=True,
                config={"displayModeBar": False}
            )
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Errors
    for fname, msg in errors:
        st.markdown(f'<div class="err-card">⚠ <strong>{fname}</strong> — {msg}</div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">📂</div>
        <div class="empty-text">No images uploaded yet.<br>Drop your waste images above to begin.</div>
    </div>
    """, unsafe_allow_html=True)