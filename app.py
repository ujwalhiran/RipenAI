"""
RipenAI - Banana Ripeness & Freshness Analysis System
Vibrant Yellow Fun & Fresh Edition ✨
Featuring Animated Mascot, Creators Section & Interactive Banana Fun Facts
"""

import streamlit as st
import numpy as np
from PIL import Image
import plotly.graph_objects as go
import os
import base64

from ripeness_detector import BananaRipenessDetector

try:
    from cnn_detector import DeepBananaClassifier
    CNN_AVAILABLE = True
except Exception:
    CNN_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="RipenAI - Fresh & Fun Banana Ripeness Analyzer",
    page_icon="🍌",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return f"data:image/jpeg;base64,{base64.b64encode(img_file.read()).decode()}"
    return ""

ujwal_b64 = get_base64_image(os.path.join(BASE_DIR, "assets", "ujwal.jpg"))
if not ujwal_b64:
    ujwal_b64 = get_base64_image(os.path.join(BASE_DIR, "ujwal.jpg"))
if not ujwal_b64:
    ujwal_b64 = get_base64_image("e:/hackathon1/assets/ujwal.jpg")

riyan_b64 = get_base64_image(os.path.join(BASE_DIR, "assets", "riyan.jpg"))
if not riyan_b64:
    riyan_b64 = get_base64_image(os.path.join(BASE_DIR, "riyan.jpg"))
if not riyan_b64:
    riyan_b64 = get_base64_image("e:/hackathon1/assets/riyan.jpg")

BANANA_FACTS = [
    "Did you know? Botanically speaking, bananas are classified as berries, while strawberries are not!",
    "Humans share approximately 50% of our DNA with bananas!",
    "Bananas curve upwards against gravity as they grow towards the sun — a phenomenon called negative geotropism!",
    "A cluster of bananas on a tree is officially called a 'hand', and an individual banana is called a 'finger'!",
    "Bananas float in water because their natural microscopic air chambers make them less dense than water!",
    "Eating a banana boosts your mood! They are loaded with Vitamin B6, which helps your brain produce serotonin (the happiness hormone).",
    "Those brown freckles that develop on ripe bananas are called 'sugar spots' — proof of maximum sweetness and rich antioxidants!",
    "More than 100 billion bananas are eaten around the globe every single year!",
    "Rubbing the inside of a banana peel on mosquito bites can naturally relieve the itch due to soothing polysaccharides!"
]

if "fact_index" not in st.session_state:
    st.session_state.fact_index = 0

# Custom Styling: Warm Yellow Theme & Smooth Animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Fredoka', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    @keyframes bounce-slow {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-8px) rotate(3deg); }
    }
    @keyframes wiggle {
        0%, 100% { transform: rotate(-6deg); }
        50% { transform: rotate(6deg); }
    }
    @keyframes pop {
        0% { transform: scale(0.96); opacity: 0.7; }
        100% { transform: scale(1); opacity: 1; }
    }

    .banana-mascot {
        display: inline-block;
        animation: bounce-slow 2.5s ease-in-out infinite;
        cursor: pointer;
    }
    .banana-mascot:hover {
        animation: wiggle 0.5s ease-in-out infinite;
    }

    .header-box {
        background: linear-gradient(135deg, #FFFBEB 0%, #FEF08A 40%, #FDE047 100%);
        border: 3px solid #EAB308;
        border-radius: 24px;
        padding: 22px 28px;
        box-shadow: 0 10px 25px -5px rgba(234, 179, 8, 0.3);
        margin-bottom: 20px;
    }

    .app-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #78350F;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .app-subtitle {
        font-size: 1.1rem;
        color: #92400E;
        font-weight: 600;
        margin-top: 4px;
    }

    .fun-badge {
        background: #FEF3C7;
        color: #92400E;
        border: 2px solid #FCD34D;
        padding: 4px 14px;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 700;
        display: inline-block;
        box-shadow: 0 2px 6px rgba(245, 158, 11, 0.15);
    }

    /* Creators Card */
    .creators-box {
        background: #FFFFFF;
        border: 2.5px solid #FDE047;
        border-radius: 20px;
        padding: 16px 22px;
        box-shadow: 0 8px 20px -4px rgba(234, 179, 8, 0.2);
        margin-bottom: 22px;
    }
    .creators-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1C1917;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 12px;
    }
    .creator-card {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 8px 14px;
        background: #FFFBEB;
        border-radius: 16px;
        border: 1.5px solid #FEF08A;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .creator-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 14px rgba(234, 179, 8, 0.2);
        border-color: #FACC15;
    }
    .avatar-wrapper {
        width: 110px;
        height: 110px;
        border-radius: 50%;
        overflow: hidden;
        border: 2.5px solid #FACC15;
        box-shadow: 0 4px 10px rgba(234, 179, 8, 0.3);
        flex-shrink: 0;
    }
    .creator-avatar {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transform-origin: center 15%;
        transform: scale(2.2);
    }
    .creator-name {
        font-size: 1.05rem;
        font-weight: 700;
        color: #1C1917;
        margin: 0;
    }
    .creator-role {
        font-size: 0.78rem;
        font-weight: 600;
        color: #B45309;
        margin-top: 2px;
    }

    /* Fun Facts Box */
    .facts-box {
        background: linear-gradient(135deg, #FFFBEB 0%, #FEF08A 100%);
        border: 2px solid #FCD34D;
        border-radius: 18px;
        padding: 16px;
        box-shadow: 0 6px 16px -3px rgba(234, 179, 8, 0.18);
        margin-top: 14px;
    }
    .facts-title {
        font-size: 0.88rem;
        font-weight: 700;
        color: #78350F;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 8px;
    }
    .facts-content {
        background: rgba(255, 255, 255, 0.88);
        border: 1.5px solid #FDE047;
        border-radius: 12px;
        padding: 12px 14px;
        font-size: 0.88rem;
        font-weight: 600;
        color: #78350F;
        line-height: 1.45;
        animation: pop 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* Yellow Metric Cards */
    .yellow-card {
        background: #FFFFFF;
        border: 2px solid #FDE047;
        border-radius: 20px;
        padding: 18px;
        box-shadow: 0 8px 20px -4px rgba(234, 179, 8, 0.2);
        text-align: center;
        margin-bottom: 14px;
        transition: transform 0.2s ease;
    }
    .yellow-card:hover {
        transform: translateY(-3px);
    }
    .card-label {
        font-size: 0.82rem;
        font-weight: 700;
        color: #B45309;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .card-val {
        font-size: 1.8rem;
        font-weight: 700;
        color: #78350F;
        margin-top: 4px;
    }

    .chef-box {
        background: linear-gradient(135deg, #FEF9C3 0%, #FEF08A 100%);
        border: 2px dashed #EAB308;
        border-radius: 20px;
        padding: 20px;
        margin-top: 18px;
        box-shadow: 0 4px 14px rgba(234, 179, 8, 0.15);
    }

    div.stButton > button {
        background: linear-gradient(135deg, #FACC15 0%, #EAB308 100%) !important;
        color: #78350F !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        border: 2px solid #CA8A04 !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 12px rgba(202, 138, 4, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_engines():
    cv_engine = BananaRipenessDetector()
    cnn_engine = DeepBananaClassifier() if CNN_AVAILABLE else None
    return cv_engine, cnn_engine

cv_detector, cnn_detector = load_engines()

def fuse_predictions(cv_res, cnn_res):
    if not cnn_res:
        return cv_res["category"], cv_res["ripeness_percentage"], cv_res["color_breakdown"]

    cv_color = cv_res["color_breakdown"]
    cnn_probs = cnn_res["probabilities"]

    cv_unripe = cv_color["Green"] / 100.0
    cv_ripe = cv_color["Yellow"] / 100.0
    cv_overripe = cv_color["Brown"] / 100.0

    cnn_unripe = cnn_probs.get("Unripe", 0.0) / 100.0
    cnn_ripe = cnn_probs.get("Ripe", 0.0) / 100.0
    cnn_overripe = cnn_probs.get("Overripe", 0.0) / 100.0

    if cv_color["Green"] >= 45.0:
        fused_unripe = 0.7 * cv_unripe + 0.3 * cnn_unripe
        fused_ripe = 0.5 * cv_ripe + 0.5 * cnn_ripe
        fused_overripe = 0.5 * cv_overripe + 0.5 * cnn_overripe
    elif cv_color["Brown"] >= 30.0:
        fused_overripe = 0.7 * cv_overripe + 0.3 * cnn_overripe
        fused_ripe = 0.5 * cv_ripe + 0.5 * cnn_ripe
        fused_unripe = 0.5 * cv_unripe + 0.5 * cnn_unripe
    else:
        fused_unripe = 0.45 * cv_unripe + 0.55 * cnn_unripe
        fused_ripe = 0.5 * cv_ripe + 0.5 * cnn_ripe
        fused_overripe = 0.5 * cv_overripe + 0.5 * cnn_overripe

    total = fused_unripe + fused_ripe + fused_overripe
    if total > 0:
        fused_unripe /= total
        fused_ripe /= total
        fused_overripe /= total

    scores = {
        "Unripe": round(fused_unripe * 100, 1),
        "Ripe": round(fused_ripe * 100, 1),
        "Overripe": round(fused_overripe * 100, 1)
    }

    best_cat = max(scores, key=scores.get)
    confidence = scores[best_cat]
    return best_cat, confidence, scores

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 10px;">
        <span style="font-size: 3rem;">🍌</span>
        <h2 style="color: #78350F; margin: 0;">RipenAI Control</h2>
        <p style="color: #B45309; font-size: 0.85rem; font-weight: 600;">Fun & Fresh Edition ✨</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #FEF9C3; border: 2px solid #FDE047; border-radius: 16px; padding: 14px; margin-bottom: 15px;">
        <strong style="color: #78350F; font-size: 0.9rem;">💛 Why this AI is special:</strong>
        <ul style="color: #92400E; font-size: 0.82rem; margin-top: 6px; padding-left: 18px;">
            <li>Auto-White Balancing in LAB space</li>
            <li>CLAHE Sugar-Spot Enhancer</li>
            <li>MobileNetV2 Deep Neural Network</li>
            <li>USDA 7-Stage Agricultural Index</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# 1. Header with Animated Mascot
st.markdown("""
<div class="header-box">
    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 15px;">
        <div style="display: flex; align-items: center; gap: 18px;">
            <div class="banana-mascot">
                <svg width="74" height="74" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M22 75C28 85 45 92 68 82C84 75 92 56 86 34C81 18 70 10 65 6C64 5 62 7 62 9C62 13 65 24 64 36C62 52 48 70 22 75Z" fill="#FACC15" stroke="#CA8A04" stroke-width="3.5" stroke-linecap="round"/>
                    <path d="M65 6C66 4 64 2 61 3C58 4 56 7 57 9L62 9" fill="#65A30D" stroke="#4D7C0F" stroke-width="2.5"/>
                    <circle cx="21" cy="76" r="3.5" fill="#78350F"/>
                    <circle cx="62" cy="42" r="4" fill="#1C1917"/>
                    <circle cx="63.5" cy="40.5" r="1.5" fill="#FFFFFF"/>
                    <circle cx="73" cy="40" r="4" fill="#1C1917"/>
                    <circle cx="74.5" cy="38.5" r="1.5" fill="#FFFFFF"/>
                    <ellipse cx="58" cy="46" rx="3.5" ry="2" fill="#F87171" opacity="0.6"/>
                    <ellipse cx="77" cy="44" rx="3.5" ry="2" fill="#F87171" opacity="0.6"/>
                    <path d="M64 47C66 52 71 51 73 46" stroke="#1C1917" stroke-width="2.5" stroke-linecap="round"/>
                    <ellipse cx="46" cy="87" rx="5.5" ry="3.5" fill="#EAB308" stroke="#CA8A04" stroke-width="2"/>
                    <ellipse cx="58" cy="86" rx="5.5" ry="3.5" fill="#EAB308" stroke="#CA8A04" stroke-width="2"/>
                </svg>
            </div>
            <div>
                <div class="app-title">RipenAI 🍌</div>
                <div class="app-subtitle">Your Friendly AI Fruit Detective • Check Sweetness & Spot Sugar Freckles!</div>
            </div>
        </div>
        <div style="display: flex; gap: 8px;">
            <span class="fun-badge">🎯 95%+ Precision</span>
            <span class="fun-badge">🌿 Zero Food Waste</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 2. Try a Mood Reference Section
st.markdown("##### 🎮 Try an Instant Reference Mood:")
col_s1, col_s2, col_s3 = st.columns(3)
sample_dir = "samples"
if not os.path.exists(sample_dir):
    sample_dir = "e:/hackathon1/samples"

green_sample = os.path.join(sample_dir, "sample_green.jpg")
ripe_sample = os.path.join(sample_dir, "sample_ripe.jpg")
spotted_sample = os.path.join(sample_dir, "sample_spotted.jpg")

sample_image_to_load = None

with col_s1:
    if st.button("🟢 Crunchy Green (Unripe)", use_container_width=True):
        if os.path.exists(green_sample):
            sample_image_to_load = Image.open(green_sample)
with col_s2:
    if st.button("⭐ Golden Sweet (Peak)", use_container_width=True):
        if os.path.exists(ripe_sample):
            sample_image_to_load = Image.open(ripe_sample)
with col_s3:
    if st.button("🐆 Sugar Spots (Bake Time!)", use_container_width=True):
        if os.path.exists(spotted_sample):
            sample_image_to_load = Image.open(spotted_sample)

# 3. CREATORS SECTION (Placed JUST BELOW Try a Mood)
st.markdown(f"""
<div class="creators-box">
    <div class="creators-title">
        <span style="background: linear-gradient(135deg, #F59E0B, #EAB308); color: white; padding: 4px 9px; border-radius: 10px; font-size: 0.95rem;">✨</span>
        <span>Creators</span>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 14px;">
        <!-- Ujwal Hiran -->
        <div class="creator-card">
            <div class="avatar-wrapper">
                <img src="{ujwal_b64}" class="creator-avatar" alt="Ujwal Hiran"/>
            </div>
            <div>
                <p class="creator-name">Ujwal Hiran</p>
                <p class="creator-role">Project Creator</p>
            </div>
        </div>
        <!-- Riyan VT -->
        <div class="creator-card">
            <div class="avatar-wrapper">
                <img src="{riyan_b64}" class="creator-avatar" style="transform-origin: center 25%; transform: scale(1.7);" alt="Riyan VT"/>
            </div>
            <div>
                <p class="creator-name">Riyan VT</p>
                <p class="creator-role">Project Creator</p>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 4. Input Section: Upload & Live Camera
tab_upload, tab_camera = st.tabs(["📁 Drop Banana Photo", "📸 Live Camera Snap"])

image_to_analyze = sample_image_to_load

with tab_upload:
    uploaded_file = st.file_uploader("Choose a banana photo from your phone or PC...", type=["jpg", "jpeg", "png", "webp"])
    if uploaded_file is not None:
        image_to_analyze = Image.open(uploaded_file)

with tab_camera:
    camera_file = st.camera_input("Hold a banana in front of your camera:")
    if camera_file is not None:
        image_to_analyze = Image.open(camera_file)

# 5. FUN FACTS ABOUT BANANA (Placed right below upload with refresh button right below text!)
col_fact, col_space = st.columns([1.2, 0.8])
with col_fact:
    current_fact = BANANA_FACTS[st.session_state.fact_index % len(BANANA_FACTS)]
    st.markdown(f"""
    <div class="facts-box">
        <div class="facts-title">
            <span>💡</span> Fun Facts About Banana
        </div>
        <div class="facts-content">
            "{current_fact}"
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_btn_l, col_btn_r = st.columns([1, 1])
    with col_btn_r:
        if st.button("🔄 Refresh Fact", use_container_width=True):
            st.session_state.fact_index = (st.session_state.fact_index + 1) % len(BANANA_FACTS)
            st.rerun()

st.divider()

# Main Processing Section
if image_to_analyze is not None:
    with st.spinner("Analyzing banana sweetness and spot patterns..."):
        cv_result = cv_detector.analyze(image_to_analyze)
        
        cnn_result = None
        if cnn_detector:
            try:
                cnn_result = cnn_detector.predict(image_to_analyze)
            except Exception:
                pass

        final_category, confidence, fused_scores = fuse_predictions(cv_result, cnn_result)

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)

    with col_m1:
        st.markdown(f"""
        <div class="yellow-card">
            <div class="card-label">Ripeness Mood</div>
            <div class="card-val" style="color: #B45309;">{final_category} ✨</div>
        </div>
        """, unsafe_allow_html=True)

    with col_m2:
        st.markdown(f"""
        <div class="yellow-card">
            <div class="card-label">AI Confidence</div>
            <div class="card-val" style="color: #059669;">{confidence}% 🎯</div>
        </div>
        """, unsafe_allow_html=True)

    with col_m3:
        st.markdown(f"""
        <div class="yellow-card">
            <div class="card-label">USDA Stage</div>
            <div class="card-val" style="color: #D97706; font-size: 1.5rem;">Stage {cv_result['stage_number']} / 7</div>
        </div>
        """, unsafe_allow_html=True)

    with col_m4:
        st.markdown(f"""
        <div class="yellow-card">
            <div class="card-label">Estimated Shelf Life</div>
            <div class="card-val" style="color: #2563EB; font-size: 1.5rem;">~{cv_result['estimated_shelf_life_days']} Days ⏳</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    col_img1, col_img2 = st.columns(2)
    with col_img1:
        st.markdown("#### 📷 Your Banana Photo")
        st.image(cv_result["original_image"], use_container_width=True)

    with col_img2:
        st.markdown("#### 🔬 AI Vision Segmentation Mask")
        st.image(cv_result["overlay_image"], use_container_width=True)
        st.markdown("""
        <div style="margin-top: 8px; text-align: center;">
            <span class="fun-badge" style="background:#D1FAE5; color:#065F46; border-color:#6EE7B7;">🟢 Green (Prebiotic Starch)</span>
            <span class="fun-badge" style="background:#FEF3C7; color:#92400E; border-color:#FCD34D;">🟡 Yellow (Natural Sugars)</span>
            <span class="fun-badge" style="background:#FEE2E2; color:#991B1B; border-color:#FCA5A5;">🔴 Red (Sugar Spots)</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown("#### 📊 Sweetness & Ripeness Probabilities")
        fig_bar = go.Figure(go.Bar(
            x=list(fused_scores.values()),
            y=list(fused_scores.keys()),
            orientation='h',
            marker=dict(color=['#10B981', '#F59E0B', '#EF4444']),
            text=[f"{v}%" for v in fused_scores.values()],
            textposition='auto',
        ))
        fig_bar.update_layout(
            xaxis_title="AI Confidence Score (%)",
            height=250,
            margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#78350F', family='Fredoka')
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_chart2:
        st.markdown("#### ⏱️ Ripeness Sweet-o-Meter")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=cv_result["ripeness_percentage"],
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': "#78350F"},
                'bar': {'color': "#D97706"},
                'steps': [
                    {'range': [0, 40], 'color': '#A7F3D0'},
                    {'range': [40, 80], 'color': '#FDE68A'},
                    {'range': [80, 100], 'color': '#FECACA'},
                ],
            }
        ))
        fig_gauge.update_layout(
            height=250,
            margin=dict(t=30, b=10, l=30, r=30),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#78350F', family='Fredoka')
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    st.markdown(f"""
    <div class="chef-box">
        <h4 style="margin: 0 0 8px 0; color: #78350F; font-size: 1.25rem;">
            🍌 Chef Banana's Recommendation: {cv_result['stage_name']}
        </h4>
        <p style="color: #92400E; margin: 4px 0;"><strong>🍴 Best Way to Enjoy:</strong> {cv_result['recommended_use']}</p>
        <p style="color: #92400E; margin: 4px 0;"><strong>👅 Texture & Taste:</strong> {cv_result['taste_profile']}</p>
        <p style="color: #92400E; margin: 4px 0;"><strong>🧊 Freshness Keeper:</strong> {cv_result['storage_tip']} ({cv_result['shelf_life_desc']})</p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.info("👆 Upload a banana photo, take a camera snap, or choose a mood sample above to begin!")
