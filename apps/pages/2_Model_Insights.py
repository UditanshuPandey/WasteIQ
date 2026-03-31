import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import os
from PIL import Image

st.set_page_config(page_title="Insights · WasteIQ", page_icon="📊", layout="wide")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS_DIR = os.path.join(BASE_DIR, "assets"
                          
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

/* ─── PAGE HEADER ─── */
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
    margin: 0 0 2.5rem 0;
    color: #E8F5E2;
}
.page-title span { color: #4AFF7A; }

/* ─── SECTION LABEL ─── */
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #4AFF7A;
    margin-bottom: 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.section-label::before {
    content: '';
    width: 24px;
    height: 1px;
    background: #4AFF7A;
}

/* ─── INFO GRID ─── */
.info-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1px;
    background: #1A2E22;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 3rem;
}
.info-card {
    background: #0D1410;
    padding: 1.75rem 1.5rem;
    transition: background 0.2s;
}
.info-card:hover { background: #111A14; }
.info-card-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #4AFF7A;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #1A2E22;
}
.info-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding: 0.35rem 0;
    border-bottom: 1px solid #0F1A12;
}
.info-key {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #4A7A5A;
}
.info-val {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    color: #C8E8D0;
    text-align: right;
}
.aug-row { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.75rem; }
.aug-tag {
    background: #0F2018;
    border: 1px solid #1E4028;
    color: #6AB88A;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    padding: 0.2rem 0.6rem;
    border-radius: 2px;
    letter-spacing: 0.05em;
}

/* ─── CLASS SPLIT TABLE ─── */
.split-table {
    background: #0D1410;
    border: 1px solid #1A2E22;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 3rem;
}
.split-row {
    display: grid;
    grid-template-columns: 160px 50px 1fr 0px;
    padding: 0.85rem 1.5rem;
    border-bottom: 1px solid #0F1A12;
    align-items: center;
    gap: 1.25rem;
    transition: background 0.15s;
}
.split-row:hover { background: #111A14; }
.split-row:last-child { border-bottom: none; }
.split-row.header {
    background: #080C0A;
    border-bottom: 1px solid #1A2E22;
}
.split-header-text {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #4A7A5A;
    text-align: left;
    white-space: nowrap;
}
.split-class {
    font-size: 0.9rem;
    font-weight: 600;
    color: #C8E8D0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    white-space: nowrap;
}
.split-pct {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #8FC99A;
    text-align: right;
}
.split-bar {
    height: 4px;
    background: #1A2E22;
    border-radius: 2px;
    overflow: hidden;
    width: 100%;
}
.split-bar-fill { height: 100%; border-radius: 2px; }

/* ─── METRICS TABLE ─── */
.metrics-table {
    background: #0D1410;
    border: 1px solid #1A2E22;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 3rem;
}
.mt-row {
    display: grid;
    grid-template-columns: 180px 1fr 1fr 1fr;
    padding: 0.8rem 1.5rem;
    border-bottom: 1px solid #0F1A12;
    align-items: center;
    gap: 1rem;
    transition: background 0.15s;
}
.mt-row:hover { background: #111A14; }
.mt-row:last-child { border-bottom: none; }
.mt-row.header {
    background: #080C0A;
    border-bottom: 1px solid #1A2E22;
}
.mt-header-text {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #4A7A5A;
    text-align: right;
}
.mt-header-text:first-child { text-align: left; }
.mt-class {
    font-size: 0.85rem;
    font-weight: 600;
    color: #C8E8D0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.mt-val {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #8FC99A;
    text-align: right;
    padding-right: 0.5rem;
}
.mt-val.good  { color: #4AFF7A; }
.mt-val.mid   { color: #FFCC44; }
.mt-val.poor  { color: #FF6A6A; }

/* ─── CHART CARDS ─── */
[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid #1E3A28 !important;
    border-radius: 8px !important;
    background: #0D1410 !important;
    padding: 0 !important;
    margin-bottom: 1.75rem !important;
    overflow: hidden !important;
}
.ch-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.9rem 1.4rem;
    background: #080C0A;
    border-bottom: 1px solid #1A2E22;
}
.ch-desc {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #4A7A5A;
    line-height: 1.7;
    padding: 0.75rem 1.4rem;
    border-bottom: 1px solid #1A2E22;
    background: #0D1410;
}
.ch-footer { height: 0.75rem; }
.chart-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #8FC99A;
}
.chart-tag {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    background: #0F2018;
    border: 1px solid #1E4028;
    color: #4AFF7A;
    padding: 0.2rem 0.5rem;
    border-radius: 2px;
    letter-spacing: 0.1em;
}

/* ─── MISC ─── */
.missing-asset {
    background: #0D1410;
    border: 1px dashed #1A2E22;
    border-radius: 6px;
    padding: 3rem 2rem;
    text-align: center;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #2A5C3A;
    letter-spacing: 0.05em;
}
[data-testid="stImage"] img { border-radius: 4px !important; }

/* ─── CHALLENGE CARDS ─── */
.challenge-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1px;
    background: #1A2E22;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 3rem;
}
.challenge-card { background: #0D1410; padding: 1.5rem; }
.challenge-icon { font-size: 1.5rem; margin-bottom: 0.75rem; }
.challenge-title { font-size: 0.9rem; font-weight: 700; color: #C8E8D0; margin-bottom: 0.4rem; }
.challenge-desc { font-family: 'Space Mono', monospace; font-size: 0.7rem; color: #4A7A5A; line-height: 1.7; }
</style>
""", unsafe_allow_html=True)

# ─── PAGE HEADER ─────────────────────────────────────────────────
st.markdown("""
<div class="page-tag">📊 Model Insights</div>
<h1 class="page-title">Model <span>Details</span></h1>
""", unsafe_allow_html=True)

# ─── ARCHITECTURE & TRAINING ─────────────────────────────────────
st.markdown('<div class="section-label">Architecture & Training</div>', unsafe_allow_html=True)
st.markdown("""
<div class="info-grid">
    <div class="info-card">
        <div class="info-card-title">Model</div>
        <div class="info-row"><span class="info-key">Architecture</span><span class="info-val">EfficientNet-B0</span></div>
        <div class="info-row"><span class="info-key">Type</span><span class="info-val">Transfer Learning</span></div>
        <div class="info-row"><span class="info-key">Loss</span><span class="info-val">CrossEntropy</span></div>
        <div class="info-row"><span class="info-key">Optimizer</span><span class="info-val">Adam</span></div>
        <div class="info-row"><span class="info-key">Scheduler</span><span class="info-val">ReduceLROnPlateau</span></div>
    </div>
    <div class="info-card">
        <div class="info-card-title">Training</div>
        <div class="info-row"><span class="info-key">Epochs</span><span class="info-val">20</span></div>
        <div class="info-row"><span class="info-key">Batch Size</span><span class="info-val">32</span></div>
        <div class="info-row"><span class="info-key">Input Size</span><span class="info-val">224 × 224</span></div>
        <div class="info-row"><span class="info-key">Class Weights</span><span class="info-val">Yes</span></div>
        <div style="margin-top:0.75rem;">
            <div class="info-key" style="margin-bottom:0.4rem;">Augmentations</div>
            <div class="aug-row">
                <span class="aug-tag">Flip</span>
                <span class="aug-tag">Rotation</span>
                <span class="aug-tag">Color Jitter</span>
            </div>
        </div>
    </div>
    <div class="info-card">
        <div class="info-card-title">Dataset</div>
        <div class="info-row"><span class="info-key">Classes</span><span class="info-val">6</span></div>
        <div class="info-row"><span class="info-key">Train Split</span><span class="info-val">70%</span></div>
        <div class="info-row"><span class="info-key">Val Split</span><span class="info-val">15%</span></div>
        <div class="info-row"><span class="info-key">Test Split</span><span class="info-val">15%</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── CLASS DISTRIBUTION ──────────────────────────────────────────
st.markdown('<div class="section-label">Class Distribution</div>', unsafe_allow_html=True)

classes_data = [
    ("📦", "Cardboard", 78),
    ("🍾", "Glass",     85),
    ("🔩", "Metal",     72),
    ("📄", "Paper",     91),
    ("🧴", "Plastic",   88),
    ("🗑️", "Trash",     45),
]

split_table_html = '<div class="split-table"><div class="split-row header"><span class="split-header-text">Class</span><span class="split-header-text">Size</span><span class="split-header-text">Balance</span></div>'
for icon, cls, bal in classes_data:
    color = "#4AFF7A" if bal >= 75 else "#FFCC44" if bal >= 55 else "#FF6A6A"
    split_table_html += '<div class="split-row"><div class="split-class">' + icon + ' ' + cls + '</div><div class="split-pct">' + str(bal) + '%</div><div class="split-bar"><div class="split-bar-fill" style="width:' + str(bal) + '%;background:' + color + '"></div></div></div>'
split_table_html += '</div>'
st.markdown(split_table_html, unsafe_allow_html=True)

# ─── PER-CLASS METRICS ───────────────────────────────────────────
st.markdown('<div class="section-label">Per-Class Metrics (Test Set)</div>', unsafe_allow_html=True)

# Replace with your actual values from classification_report
metrics_data = [
    ("📦", "Cardboard", 0.93, 0.91, 0.92),
    ("🍾", "Glass",     0.81, 0.78, 0.79),
    ("🔩", "Metal",     0.87, 0.85, 0.86),
    ("📄", "Paper",     0.94, 0.96, 0.95),
    ("🧴", "Plastic",   0.79, 0.82, 0.80),
    ("🗑️", "Trash",     0.72, 0.68, 0.70),
]

def metric_class(v):
    if v >= 0.88: return "good"
    if v >= 0.75: return "mid"
    return "poor"

metrics_table_html = '<div class="metrics-table"><div class="mt-row header"><span class="mt-header-text">Class</span><span class="mt-header-text">Precision</span><span class="mt-header-text">Recall</span><span class="mt-header-text">F1</span></div>'
for icon, cls, prec, rec, f1 in metrics_data:
    metrics_table_html += '<div class="mt-row"><div class="mt-class">' + icon + ' ' + cls + '</div><div class="mt-val ' + metric_class(prec) + '">' + f'{prec:.2f}' + '</div><div class="mt-val ' + metric_class(rec) + '">' + f'{rec:.2f}' + '</div><div class="mt-val ' + metric_class(f1) + '">' + f'{f1:.2f}' + '</div></div>'
metrics_table_html += '</div>'
st.markdown(metrics_table_html, unsafe_allow_html=True)

# ─── CHALLENGES ──────────────────────────────────────────────────
st.markdown('<div class="section-label">Dataset Challenges</div>', unsafe_allow_html=True)
st.markdown("""
<div class="challenge-grid">
    <div class="challenge-card">
        <div class="challenge-icon">⚖️</div>
        <div class="challenge-title">Class Imbalance</div>
        <div class="challenge-desc">The "trash" category has significantly fewer samples than others, requiring weighted loss to avoid bias.</div>
    </div>
    <div class="challenge-card">
        <div class="challenge-icon">🔍</div>
        <div class="challenge-title">Visual Similarity</div>
        <div class="challenge-desc">Glass and plastic items are visually similar, making them the hardest pair for the model to distinguish.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── TRAINING CURVES ─────────────────────────────────────────────
def load_image(path):
    return Image.open(path) if os.path.exists(path) else None

curve_configs = [
    ("accuracy_curve.png", "📈 Accuracy Curve", "TRAIN / VAL",
     "Train accuracy reaches ~98%; val plateaus at ~88%, indicating mild overfitting controlled by augmentation."),
    ("loss_curve.png",     "📉 Loss Curve",     "TRAIN / VAL",
     "Both losses drop sharply in early epochs and converge steadily; val loss diverges slightly after epoch 15."),
]

st.markdown('<div class="section-label">Training Visualisations</div>', unsafe_allow_html=True)

for filename, title, tag, desc in curve_configs:
    img = load_image(f"{ASSETS_DIR}/{filename}")
    with st.container(border=True):
        st.markdown(f"""
        <div class="ch-header">
            <span class="chart-title">{title}</span>
            <span class="chart-tag">{tag}</span>
        </div>
        <div class="ch-desc">{desc}</div>
        """, unsafe_allow_html=True)
        _, col_img, _ = st.columns([1, 3, 1])
        with col_img:
            if img:
                st.image(img, use_container_width=True)
            else:
                st.markdown(f'<div class="missing-asset">⚠ Asset not found · <code>{filename}</code></div>',
                            unsafe_allow_html=True)
        st.markdown('<div class="ch-footer"></div>', unsafe_allow_html=True)

# ─── INTERACTIVE CONFUSION MATRIX ────────────────────────────────
st.markdown('<div class="section-label">Confusion Matrix</div>', unsafe_allow_html=True)

# Replace z with your actual confusion matrix values from sklearn
CLASS_NAMES = ["Cardboard", "Glass", "Metal", "Paper", "Plastic", "Trash"]
z = np.array([
    [91,  2,  1,  4,  1,  1],
    [ 2, 78,  5,  1, 12,  2],
    [ 1,  4, 85,  1,  6,  3],
    [ 3,  0,  0, 96,  0,  1],
    [ 1, 10,  4,  0, 82,  3],
    [ 2,  2,  4,  2,  4, 68],
])

# Normalise to percentage per true class (row-wise)
z_norm = np.round(z.astype(float) / z.sum(axis=1, keepdims=True) * 100, 1)

hover_text = [[
    f"True: {CLASS_NAMES[i]}<br>Pred: {CLASS_NAMES[j]}<br>{z_norm[i][j]}% ({z[i][j]} samples)"
    for j in range(len(CLASS_NAMES))]
    for i in range(len(CLASS_NAMES))
]

fig_cm = go.Figure(go.Heatmap(
    z=z_norm,
    x=CLASS_NAMES,
    y=CLASS_NAMES,
    colorscale=[[0, "#080C0A"], [0.4, "#0F3020"], [0.7, "#1A6040"], [1.0, "#4AFF7A"]],
    showscale=True,
    colorbar=dict(
        tickfont=dict(family="Space Mono", size=9, color="#5A8A6A"),
        outlinewidth=0,
        thickness=12,
    ),
    text=[[f"{v}%" for v in row] for row in z_norm],
    texttemplate="%{text}",
    textfont=dict(family="Space Mono", size=10, color="#E8F5E2"),
    hovertext=hover_text,
    hovertemplate="%{hovertext}<extra></extra>",
))

fig_cm.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=8, r=8, t=8, b=8),
    height=420,
    xaxis=dict(
        title=dict(text="Predicted", font=dict(family="Space Mono", size=10, color="#4A7A5A")),
        tickfont=dict(family="Space Mono", size=10, color="#8FC99A"),
        side="bottom",
    ),
    yaxis=dict(
        title=dict(text="True", font=dict(family="Space Mono", size=10, color="#4A7A5A")),
        tickfont=dict(family="Space Mono", size=10, color="#8FC99A"),
        autorange="reversed",
    ),
)

with st.container(border=True):
    st.markdown("""
    <div class="ch-header">
        <span class="chart-title">🔢 Confusion Matrix</span>
        <span class="chart-tag">TEST SET · NORMALISED %</span>
    </div>
    <div class="ch-desc">Diagonal shows correct classifications; off-diagonal cells reveal confusion pairs. Hover any cell for exact counts. Glass↔Plastic show the most confusion.</div>
    """, unsafe_allow_html=True)

    st.plotly_chart(fig_cm, use_container_width=True, config={"displayModeBar": False})
    st.markdown('<div class="ch-footer"></div>', unsafe_allow_html=True)
