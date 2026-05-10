# ============================================================
# 💰 PREMIUM LIVE TICKER
# ============================================================
def render_ticker(prices):

    import streamlit as st

    st.markdown("""
    <div style="
        font-size:34px;
        font-weight:900;
        margin-bottom:22px;
        color:white;
    ">
        💰 Live Market Overview
    </div>
    """, unsafe_allow_html=True)

    if not prices:
        st.info("Fetching live market prices...")
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

                    background:
                        linear-gradient(
                            135deg,
                            rgba(18,26,47,0.92) 0%,
                            rgba(10,16,32,0.88) 100%
                        );

                    border: 1px solid rgba(255,255,255,0.06);

                    border-radius: 24px;

                    padding: 24px;

                    position:relative;

                    overflow:hidden;

                    backdrop-filter: blur(18px);

                    box-shadow:
                        0 10px 35px rgba(0,0,0,0.25);

                ">

                    <div style="
                        position:absolute;

                        top:-40px;
                        right:-40px;

                        width:120px;
                        height:120px;

                        background:rgba(0,212,255,0.08);

                        border-radius:50%;

                        filter: blur(24px);
                    "></div>

                    <div style="
                        color:#94A3B8;
                        font-size:13px;
                        margin-bottom:12px;
                    ">
                        {symbol}
                    </div>

                    <div style="
                        font-size:34px;
                        font-weight:900;
                        color:white;
                        margin-bottom:14px;
                    ">
                        ${price:.2f}
                    </div>

                    <div style="
                        display:inline-flex;

                        align-items:center;

                        gap:6px;

                        padding:6px 12px;

                        border-radius:999px;

                        background:rgba(0,229,168,0.10);

                        color:#00E5A8;

                        font-size:12px;

                        font-weight:700;
                    ">

                        ● LIVE MARKET

                    </div>

                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
