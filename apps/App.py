import streamlit as st

st.set_page_config(
    page_title="WasteIQ",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

/* ─── GLOBAL RESET ─────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #080C0A;
    color: #E8F5E2;
}

/* ─── HIDE STREAMLIT CHROME ─────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ─── SIDEBAR ───────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #0D1410;
    border-right: 1px solid #1E3A28;
    padding-top: 2rem;
}
[data-testid="stSidebar"] .stMarkdown p {
    color: #5A8A6A;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}
[data-testid="stSidebarNav"] a {
    color: #8FC99A !important;
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    letter-spacing: 0.05em;
    border-radius: 6px;
    transition: all 0.2s;
}
[data-testid="stSidebarNav"] a:hover {
    background: #1A2E22 !important;
    color: #4AFF7A !important;
}

/* ─── MAIN AREA ─────────────────────────────────── */
.main .block-container {
    padding: 3rem 4rem;
    max-width: 1100px;
}

/* ─── HERO SECTION ──────────────────────────────── */
.hero-wrap {
    position: relative;
    padding: 4rem 0 3rem 0;
    overflow: hidden;
}
.hero-badge {
    display: inline-block;
    background: #0F2018;
    border: 1px solid #2A5C3A;
    color: #4AFF7A;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    padding: 0.35rem 1rem;
    border-radius: 2px;
    margin-bottom: 1.5rem;
    text-transform: uppercase;
}
.hero-title {
    font-size: clamp(3rem, 7vw, 5.5rem);
    font-weight: 800;
    line-height: 1.0;
    letter-spacing: -0.03em;
    margin: 0 0 1rem 0;
    color: #E8F5E2;
}
.hero-title span {
    color: #4AFF7A;
}
.hero-subtitle {
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    color: #5A8A6A;
    letter-spacing: 0.05em;
    line-height: 1.8;
    max-width: 480px;
    margin-bottom: 3rem;
}
.hero-grid-line {
    position: absolute;
    right: -2rem;
    top: 0;
    width: 40%;
    height: 100%;
    background-image:
        linear-gradient(#1E3A28 1px, transparent 1px),
        linear-gradient(90deg, #1E3A28 1px, transparent 1px);
    background-size: 40px 40px;
    opacity: 0.4;
    pointer-events: none;
}
.hero-orb {
    position: absolute;
    right: 10%;
    top: 50%;
    transform: translateY(-50%);
    width: 220px;
    height: 220px;
    border-radius: 50%;
    background: radial-gradient(circle, #1A4D2A 0%, #080C0A 70%);
    border: 1px solid #2A5C3A;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 5rem;
    box-shadow: 0 0 80px rgba(74,255,122,0.08), inset 0 0 40px rgba(74,255,122,0.05);
}

/* ─── STAT CARDS ────────────────────────────────── */
.stat-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1px;
    background: #1E3A28;
    border: 1px solid #1E3A28;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 3rem;
}
.stat-card {
    background: #0D1410;
    padding: 1.75rem 2rem;
    transition: background 0.2s;
}
.stat-card:hover { background: #111A14; }
.stat-num {
    font-size: 2.5rem;
    font-weight: 800;
    color: #4AFF7A;
    letter-spacing: -0.04em;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.stat-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #4A7A5A;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

/* ─── FEATURE SECTION ───────────────────────────── */
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #4AFF7A;
    margin-bottom: 1.5rem;
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
.feature-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1px;
    background: #1A2E22;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 2rem;
}
.feature-card {
    background: #0D1410;
    padding: 2rem;
    transition: background 0.3s;
    position: relative;
    overflow: hidden;
}
.feature-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0;
    width: 100%; height: 2px;
    background: linear-gradient(90deg, #4AFF7A, transparent);
    opacity: 0;
    transition: opacity 0.3s;
}
.feature-card:hover { background: #111A14; }
.feature-card:hover::after { opacity: 1; }
.feat-icon {
    font-size: 1.75rem;
    margin-bottom: 1rem;
    display: block;
}
.feat-title {
    font-size: 1rem;
    font-weight: 700;
    color: #C8E8D0;
    margin-bottom: 0.4rem;
    letter-spacing: -0.01em;
}
.feat-desc {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: #4A7A5A;
    line-height: 1.7;
}

/* ─── CLASS CHIPS ───────────────────────────────── */
.chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 1rem;
}
.chip {
    background: #0F2018;
    border: 1px solid #2A5C3A;
    color: #8FC99A;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    padding: 0.35rem 0.85rem;
    border-radius: 2px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ─── BOTTOM CTA ────────────────────────────────── */
.cta-bar {
    background: linear-gradient(135deg, #0F2018 0%, #152A1E 100%);
    border: 1px solid #2A5C3A;
    border-radius: 8px;
    padding: 2rem 2.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 3rem;
}
.cta-text {
    font-size: 1.1rem;
    font-weight: 700;
    color: #C8E8D0;
}
.cta-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #4A7A5A;
    margin-top: 0.25rem;
    letter-spacing: 0.05em;
}
.cta-arrow {
    font-size: 2rem;
    color: #4AFF7A;
}
</style>
""", unsafe_allow_html=True)

# ─── HERO ────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-grid-line"></div>
    <div class="hero-badge">♻ AI-Powered Waste Classification</div>
    <h1 class="hero-title">Waste<span>IQ</span></h1>
    <p class="hero-subtitle">
        EfficientNet-B0 deep learning model that identifies waste categories
        and recommends optimal disposal methods — instantly.
    </p>
    <div class="hero-orb">♻️</div>
</div>
""", unsafe_allow_html=True)

# ─── STATS ───────────────────────────────────────────────────────
st.markdown("""
<div class="stat-row">
    <div class="stat-card">
        <div class="stat-num">6</div>
        <div class="stat-label">Waste Categories</div>
    </div>
    <div class="stat-card">
        <div class="stat-num">B0</div>
        <div class="stat-label">EfficientNet Model</div>
    </div>
    <div class="stat-card">
        <div class="stat-num">224²</div>
        <div class="stat-label">Input Resolution</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── FEATURES ────────────────────────────────────────────────────
st.markdown('<div class="section-label">Core Features</div>', unsafe_allow_html=True)

st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <span class="feat-icon">📸</span>
        <div class="feat-title">Instant Classification</div>
        <div class="feat-desc">Upload one or multiple images and get real-time predictions with confidence scores.</div>
    </div>
    <div class="feature-card">
        <span class="feat-icon">🗑️</span>
        <div class="feat-title">Disposal Guidance</div>
        <div class="feat-desc">Each prediction comes with actionable disposal recommendations tailored to the waste type.</div>
    </div>
    <div class="feature-card">
        <span class="feat-icon">📊</span>
        <div class="feat-title">Model Insights</div>
        <div class="feat-desc">Explore training curves, confusion matrices, and architecture details on the Insights page.</div>
    </div>
    <div class="feature-card">
        <span class="feat-icon">⚡</span>
        <div class="feat-title">GPU Accelerated</div>
        <div class="feat-desc">Runs on CUDA when available, falling back gracefully to CPU for universal compatibility.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── CLASSES ─────────────────────────────────────────────────────
st.markdown('<div class="section-label">Recognizable Classes</div>', unsafe_allow_html=True)

st.markdown("""
<div class="chip-row">
    <span class="chip">📦 Cardboard</span>
    <span class="chip">🍾 Glass</span>
    <span class="chip">🔩 Metal</span>
    <span class="chip">📄 Paper</span>
    <span class="chip">🧴 Plastic</span>
    <span class="chip">🗑️ Trash</span>
</div>
""", unsafe_allow_html=True)

# ─── GRAD-CAM EXPLAINABILITY ─────────────────────────────────────
st.markdown('<div style="margin-top:2rem;"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">Model Explainability</div>', unsafe_allow_html=True)

st.markdown("""
<div style="background:#0D1410;border:1px solid #1E3A28;border-radius:8px;overflow:hidden;margin-bottom:2rem;">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1px;background:#1E3A28;">
        <div style="background:#0D1410;padding:2rem;">
            <span style="font-size:1.5rem;display:block;margin-bottom:0.75rem;">🔬</span>
            <div style="font-family:'Syne',sans-serif;font-size:0.95rem;font-weight:700;color:#C8E8D0;margin-bottom:0.5rem;">What is Grad-CAM?</div>
            <div style="font-family:'Space Mono',monospace;font-size:0.72rem;color:#4A7A5A;line-height:1.75;">
                Gradient-weighted Class Activation Mapping highlights the image regions that most influenced the model's prediction — turning the black box into a transparent decision map.
            </div>
        </div>
        <div style="background:#0D1410;padding:2rem;">
            <span style="font-size:1.5rem;display:block;margin-bottom:0.75rem;">🌡️</span>
            <div style="font-family:'Syne',sans-serif;font-size:0.95rem;font-weight:700;color:#C8E8D0;margin-bottom:0.5rem;">Reading the Heatmap</div>
            <div style="font-family:'Space Mono',monospace;font-size:0.72rem;color:#4A7A5A;line-height:1.75;">
                <span style="color:#FF4444;">■</span> <span style="color:#5A8A6A;">Red = high importance</span> &nbsp;·&nbsp;
                <span style="color:#FFAA44;">■</span> <span style="color:#5A8A6A;">Orange = medium</span> &nbsp;·&nbsp;
                <span style="color:#4A7ABF;">■</span> <span style="color:#5A8A6A;">Blue = low.</span><br><br>
                <span style="color:#4A7A5A;">The model focuses on object texture and edges to classify waste type.</span>
            </div>
        </div>
    </div>
    <div style="padding:0.85rem 2rem;background:#080C0A;border-top:1px solid #1A2E22;
                font-family:'Space Mono',monospace;font-size:0.65rem;color:#2A5C3A;
                letter-spacing:0.05em;display:flex;align-items:center;gap:0.75rem;">
        <span style="color:#4AFF7A;font-size:0.5rem;">●</span>
        Grad-CAM runs on the last conv layer of EfficientNet-B0 · Toggle it per-image on the Predict page
    </div>
</div>
""", unsafe_allow_html=True)

# ─── CTA ─────────────────────────────────────────────────────────
st.markdown("""
<div class="cta-bar">
    <div>
        <div class="cta-text">Ready to classify waste?</div>
        <div class="cta-sub">Navigate to Predict in the sidebar →</div>
    </div>
    <div class="cta-arrow">→</div>
</div>
""", unsafe_allow_html=True)