import streamlit as st


# =========================
# 🎨 GLOBAL UI STYLES
# =========================
st.markdown("""
<style>

/* ===== HEADER ===== */
.header {
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(14px);
    background: rgba(15,12,41,0.85);
    padding: 12px 20px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

/* LOGO */
.logo {
    font-size: 22px;
    font-weight: bold;
    color: #00ffcc;
    letter-spacing: 1px;
}

/* NAV */
div[role="radiogroup"] > label {
    padding: 8px 14px;
    border-radius: 10px;
    transition: 0.2s ease;
}

div[role="radiogroup"] > label:hover {
    background: rgba(255,255,255,0.08);
}

div[role="radiogroup"] > label[aria-checked="true"] {
    background: rgba(0,255,204,0.15);
    border: 1px solid rgba(0,255,204,0.35);
}

/* ===== GLASS CARD ===== */
.card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 18px;
    border-radius: 16px;
    text-align: center;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.35);
}

/* PRICE TEXT */
.price {
    font-size: 22px;
    font-weight: bold;
    color: #00ffcc;
}

/* LABEL TEXT */
.label {
    color: gray;
    font-size: 12px;
}

/* ===== MOBILE RESPONSIVE ===== */
@media (max-width: 768px) {

    .logo {
        font-size: 18px;
    }

    div[role="radiogroup"] {
        flex-wrap: wrap !important;
    }

    div[data-testid="column"] {
        width: 100% !important;
    }

    .card {
        padding: 12px;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================
# 🚀 HEADER (CRYPTOPORT)
# =========================
def render_header(user):

    st.markdown('<div class="header">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2,6,2])

    # LOGO
    with col1:
        st.markdown('<div class="logo">🚀 CRYPTOPORT</div>', unsafe_allow_html=True)

    # NAVIGATION
    with col2:
        nav = st.radio(
            "",
            [
                "📊 Market",
                "💰 AI Portfolio",
                "⚠ Risk",
                "🔮 AI Forecast",
                "👤 Portfolio",
                "🤖 AI"
            ],
            horizontal=True,
            label_visibility="collapsed"
        )
        st.session_state.page = nav

    # USER + LOGOUT
    with col3:
        st.markdown(f"👤 {user}")
        if st.button("Logout"):
            st.session_state.auth = False
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # spacing
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)


# =========================
# 💰 MARKET TICKER (CARDS)
# =========================
def render_ticker(prices):

    st.markdown("### 💰 Live Market")

    if not prices:
        st.info("Loading prices...")
        return

    coins = list(prices.items())
    cols_per_row = 5  # trading style grid

    for i in range(0, len(coins), cols_per_row):

        row = coins[i:i + cols_per_row]
        cols = st.columns(cols_per_row)

        for j in range(cols_per_row):

            if j < len(row):
                symbol, price = row[j]

                cols[j].markdown(f"""
                <div class="card">
                    <div class="label">{symbol}</div>
                    <div class="price">${price:.2f}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)


# =========================
# 📊 MARKET GRID (ADVANCED)
# =========================
def render_market_cards(prices):

    st.markdown("### 📊 Market Snapshot")

    cols = st.columns(len(prices))

    for i, (coin, price) in enumerate(prices.items()):
        cols[i].markdown(f"""
        <div class="card">
            <div class="label">{coin}</div>
            <div class="price">${price:.2f}</div>
        </div>
        """, unsafe_allow_html=True)


# =========================
# 🔔 NOTIFICATION HELPER
# =========================
def show_notification(message, type="info"):

    if type == "success":
        st.success(message)
    elif type == "warning":
        st.warning(message)
    elif type == "error":
        st.error(message)
    else:
        st.info(message)
