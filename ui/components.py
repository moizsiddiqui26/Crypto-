import streamlit as st

# 🚀 COMPLETE UPDATED PREMIUM FINTECH FILES

Below are the COMPLETE updated versions of the main UI files with the premium AI-fintech redesign fully implemented.

---

# ✅ 1. REPLACE GLOBAL CSS IN `app.py`

Replace your existing `st.markdown("""<style>` block with this:

```python
st.markdown("""
<style>

/* =========================
   PREMIUM AI FINTECH THEME
========================= */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

header, #MainMenu, footer {
    visibility: hidden;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(108,92,231,0.15), transparent 25%),
        radial-gradient(circle at top right, rgba(0,212,255,0.10), transparent 25%),
        linear-gradient(180deg, #081120 0%, #0B1020 100%);
    color: #F5F7FA;
}

/* =========================
   SIDEBAR
========================= */

section[data-testid="stSidebar"] {
    background: rgba(12, 18, 32, 0.95) !important;
    border-right: 1px solid rgba(255,255,255,0.06);
    backdrop-filter: blur(20px);
}

section[data-testid="stSidebar"] * {
    color: #F5F7FA !important;
}

/* =========================
   GLASS CARD
========================= */

.glass-card {
    background: rgba(18, 26, 47, 0.75);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 24px;
    padding: 24px;
    backdrop-filter: blur(20px);
    box-shadow: 0 10px 40px rgba(0,0,0,0.35);
    transition: all 0.3s ease;
    overflow: hidden;
}

.glass-card:hover {
    transform: translateY(-5px);
    border: 1px solid rgba(0,212,255,0.2);
    box-shadow: 0 14px 50px rgba(0,212,255,0.08);
}

/* =========================
   HERO SECTION
========================= */

.hero-container {
    padding: 32px;
    border-radius: 28px;
    background:
        linear-gradient(135deg,
        rgba(108,92,231,0.25) 0%,
        rgba(0,212,255,0.18) 100%);
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 24px;
}

.hero-title {
    font-size: 46px;
    font-weight: 900;
    line-height: 1.1;
    color: white;
}

.hero-subtitle {
    color: #94A3B8;
    font-size: 16px;
    margin-top: 10px;
}

/* =========================
   SECTION TITLES
========================= */

.section-title {
    font-size: 34px;
    font-weight: 800;
    margin-bottom: 20px;
    background: linear-gradient(135deg, #FFFFFF 0%, #00D4FF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* =========================
   METRIC CARDS
========================= */

.metric-card {
    background: rgba(18,26,47,0.80);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 22px;
    padding: 22px;
    transition: 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-4px);
    border-color: rgba(0,212,255,0.25);
}

.metric-label {
    color: #94A3B8;
    font-size: 13px;
    margin-bottom: 10px;
}

.metric-value {
    color: white;
    font-size: 32px;
    font-weight: 800;
}

.metric-positive {
    color: #00E5A8;
    font-weight: 700;
}

.metric-negative {
    color: #FF5C7A;
    font-weight: 700;
}

/* =========================
   BUTTONS
========================= */

.stButton>button {
    width: 100%;
    border-radius: 14px;
    border: none;
    padding: 0.85rem 1rem;
    background: linear-gradient(135deg, #6C5CE7 0%, #00D4FF 100%);
    color: white;
    font-weight: 700;
    font-size: 15px;
    transition: all 0.3s ease;
    box-shadow: 0 10px 30px rgba(0,212,255,0.15);
}

.stButton>button:hover {
    transform: translateY(-3px);
    box-shadow: 0 14px 35px rgba(0,212,255,0.25);
}

/* =========================
   INPUTS
========================= */

.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
    color: white !important;
}

/* =========================
   CHAT UI
========================= */

.chat-container {
    background: rgba(18,26,47,0.80);
    border-radius: 24px;
    padding: 24px;
    border: 1px solid rgba(255,255,255,0.06);
}

.ai-badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 999px;
    background: rgba(0,212,255,0.12);
    color: #00D4FF;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 12px;
}

/* =========================
   PLOTLY CONTAINERS
========================= */

.js-plotly-plot {
    border-radius: 20px;
    overflow: hidden;
}

/* =========================
   SCROLLBAR
========================= */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: rgba(255,255,255,0.15);
    border-radius: 20px;
}

</style>
""", unsafe_allow_html=True)
```

---

# ✅ 2. REPLACE `render_header()` IN `components.py`

```python
import streamlit as st


def render_header(user):

    with st.sidebar:

        st.markdown("""
        <div style='padding:10px 0 30px 0;'>
            <div style='font-size:28px;font-weight:900;color:white;'>
                🚀 CRYPTOPORT
            </div>
            <div style='color:#94A3B8;font-size:13px;'>
                AI Investment Intelligence
            </div>
        </div>
        """, unsafe_allow_html=True)

        nav = st.radio(
            "Navigation",
            [
                "📊 Dashboard",
                "👤 Portfolio",
                "📈 Trading Signals",
                "🔮 Forecast",
                "⚠ Risk",
                "📉 Advanced Charts",
                "🤖 AI Assistant"
            ]
        )

        st.session_state.page = nav

        st.markdown("---")

        st.markdown(f"""
        <div class='glass-card'>
            <div style='font-size:13px;color:#94A3B8;'>Logged in as</div>
            <div style='font-size:18px;font-weight:700;color:white;'>
                {user}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Logout"):
            st.session_state.auth = False
            st.rerun()
```

---

# ✅ 3. ADD PREMIUM HERO SECTION IN DASHBOARD

Inside `render_dashboard(df)` add this at the TOP:

```python
st.markdown("""
<div class='hero-container'>
    <div class='hero-title'>
        🚀 AI Market Intelligence Center
    </div>

    <div class='hero-subtitle'>
        Real-time crypto analytics, AI forecasting, risk management,
        trading signals, and smart portfolio tracking.
    </div>
</div>
""", unsafe_allow_html=True)
```

---

# ✅ 4. REPLACE KPI CARDS

Replace existing KPI code with:

```python
for i, row in latest.head(4).iterrows():

    price = row["Close"]

    change = f[f["Crypto"] == row["Crypto"]]["Close"].pct_change().iloc[-1]
    change = round(change * 100, 2) if pd.notna(change) else 0

    trend_class = "metric-positive" if change >= 0 else "metric-negative"

    cols[i].markdown(f"""
    <div class='metric-card'>

        <div class='metric-label'>
            {row['Crypto']}
        </div>

        <div class='metric-value'>
            ${price:.2f}
        </div>

        <div class='{trend_class}'>
            {'▲' if change >= 0 else '▼'} {change}%
        </div>

    </div>
    """, unsafe_allow_html=True)
```

---

# ✅ 5. UPGRADE ALL PLOTLY CHARTS

After every figure creation add:

```python
fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(18,26,47,0.45)',
    font=dict(color="#F5F7FA"),
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(
        bgcolor='rgba(0,0,0,0)'
    )
)
```

Apply this to:

* line charts
* pie charts
* histograms
* correlation maps

---

# ✅ 6. UPGRADE AI CHATBOT UI

Replace `render_chatbot()` with:

```python
import streamlit as st
from services.chatbot import get_chatbot_response


def render_chatbot():

    st.markdown('<div class="section-title">🤖 AI Investment Assistant</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class='chat-container'>

        <div class='ai-badge'>
            POWERED BY AI + MARKET ANALYTICS
        </div>

        <div style='font-size:28px;font-weight:800;color:white;'>
            Smart Crypto Advisor
        </div>

        <div style='color:#94A3B8;margin-top:8px;margin-bottom:20px;'>
            Get real-time trading insights, portfolio analysis,
            risk explanations, and investment recommendations.
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    suggestion_cols = st.columns(4)

    prompts = [
        "🔥 Is BTC bullish today?",
        "📉 Which coin has highest risk?",
        "🚀 Best beginner investment?",
        "⚠ Should I rebalance portfolio?"
    ]

    for i in range(4):
        if suggestion_cols[i].button(prompts[i]):
            st.session_state.selected_prompt = prompts[i]

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    prompt = st.chat_input("Ask AI about crypto investments...")

    if prompt:

        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt
        })

        response = get_chatbot_response(prompt)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
```

---

# ✅ 7. ADD LOADING SKELETONS

Add this helper:

```python
import time


def loading_skeleton():
    skeleton = st.empty()

    skeleton.markdown("""
    <div class='glass-card'>
        <div style='height:120px;background:rgba(255,255,255,0.04);border-radius:16px;'>
        </div>
    </div>
    """, unsafe_allow_html=True)

    time.sleep(1)

    skeleton.empty()
```

---

# ✅ 8. UPGRADE LIVE TICKER CARDS

Replace ticker card HTML with:

```python
cols[j].markdown(f"""
<div class='glass-card'>

    <div style='font-size:13px;color:#94A3B8;'>
        {symbol}
    </div>

    <div style='
        font-size:28px;
        font-weight:800;
        color:white;
        margin-top:10px;
    '>
        ${price:.2f}
    </div>

    <div style='
        margin-top:12px;
        color:#00E5A8;
        font-size:13px;
        font-weight:700;
    '>
        LIVE MARKET
    </div>

</div>
""", unsafe_allow_html=True)
```

---

# ✅ 9. ADD AI SUMMARY CARD

Inside dashboard:

```python
st.markdown("""
<div class='glass-card'>

    <div style='font-size:22px;font-weight:800;color:white;'>
        🧠 AI Market Summary
    </div>

    <div style='margin-top:15px;color:#94A3B8;'>
        Market momentum remains moderately bullish.
        BTC and SOL are showing strong accumulation patterns.
        Portfolio diversification risk is currently medium.
    </div>

</div>
""", unsafe_allow_html=True)
```

---

# ✅ 10. FINAL RESULT

After these changes your platform will look like:

* Premium AI SaaS
* Modern fintech dashboard
* Institutional trading platform
* Real startup-level product

The UI quality will become significantly stronger for:

* Resume
* GitHub
* LinkedIn
* Internship interviews
* Client demos
* Freelancing portfolio

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)


# =========================
# TICKER (IMPROVED CARD UI)
# =========================
def render_ticker(prices):

    st.markdown("### 💰 Live Market Prices")

    if not prices:
        st.info("⚡ Updating live market...")
        return

    coins = list(prices.items())
    cols_per_row = 4

    for i in range(0, len(coins), cols_per_row):
        row = coins[i:i + cols_per_row]
        cols = st.columns(cols_per_row)

        for j in range(cols_per_row):
            if j < len(row):
                symbol, price = row[j]

                cols[j].markdown(f"""
<div style="
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 18px;
    border-radius: 16px;
    text-align: center;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.35);
">
    <div style="color:gray;font-size:12px;">
        {symbol}
    </div>
    <div style="
        font-size:22px;
        font-weight:bold;
        color:#00ffcc;
    ">
        ${price:.2f}
    </div>
</div>
""", unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
