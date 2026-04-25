import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import EMAIL_USER, EMAIL_PASS


# =========================
# SAFE EMAIL CONNECTION
# =========================
def get_smtp_server():
    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls(context=context)
        server.login(EMAIL_USER, EMAIL_PASS)
        return server
    except Exception as e:
        print("SMTP Connection Error:", e)
        return None


# =========================
# CORE EMAIL SENDER
# =========================
def send_email(to_email: str, subject: str, html_content: str):

    if not EMAIL_USER or not EMAIL_PASS:
        print("❌ Email credentials not set in .env")
        return False

    server = get_smtp_server()

    if not server:
        return False

    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(html_content, "html"))

        server.send_message(msg)
        server.quit()

        print(f"✅ Email sent to {to_email}")
        return True

    except Exception as e:
        print("❌ Email Send Error:", e)
        return False


# =========================
# PRICE ALERT EMAIL
# =========================
def send_alert_email(to_email, coin, condition, target_price, current_price):

    subject = f"🚨 {coin} Alert Triggered"

    arrow = "📈" if condition == "above" else "📉"
    color = "#00ffcc" if condition == "above" else "#ff4b4b"

    html = f"""
    <html>
    <body style="font-family:Arial;background:#0f0c29;color:white;padding:20px;">
        <h2 style="color:#4cc9f0;">🚨 Price Alert</h2>

        <div style="background:#302b63;padding:15px;border-radius:10px;">
            <p>{arrow} <b>{coin}</b> is now <b>{condition}</b> your target</p>

            <p><b>Current:</b> <span style="color:{color}">${current_price:.2f}</span></p>
            <p><b>Target:</b> ${target_price:.2f}</p>
        </div>

        <p style="margin-top:20px;">📊 Check your dashboard for details</p>
    </body>
    </html>
    """

    return send_email(to_email, subject, html)


# =========================
# WELCOME EMAIL
# =========================
def send_welcome_email(to_email):

    subject = "🎉 Welcome to Crypto SaaS Platform"

    html = """
    <html>
    <body style="font-family:Arial;background:#0f0c29;color:white;padding:20px;">
        <h2 style="color:#4cc9f0;">🚀 Welcome!</h2>

        <p>Your account has been successfully created.</p>

        <div style="background:#302b63;padding:15px;border-radius:10px;">
            <p>✔ Track your portfolio</p>
            <p>✔ AI insights</p>
            <p>✔ Real-time prices</p>
        </div>

        <p style="margin-top:20px;">Happy Investing 💰</p>
    </body>
    </html>
    """

    return send_email(to_email, subject, html)


# =========================
# OTP EMAIL
# =========================
def send_otp_email(to_email, otp):

    subject = "🔐 Your OTP Code"

    html = f"""
    <html>
    <body style="font-family:Arial;background:#0f0c29;color:white;padding:20px;">
        <h2 style="color:#4cc9f0;">🔐 OTP Verification</h2>

        <p>Your OTP:</p>

        <h1 style="
            background:#00ffcc;
            color:black;
            padding:10px;
            border-radius:8px;
            text-align:center;
            letter-spacing:5px;">
            {otp}
        </h1>

        <p>Valid for limited time only.</p>
    </body>
    </html>
    """

    return send_email(to_email, subject, html)


# =========================
# RISK ALERT EMAIL
# =========================
def send_risk_alert_email(to_email, risk_data):

    subject = "⚠ Portfolio Risk Alert"

    rows = ""

    for _, row in risk_data.iterrows():
        color = "red" if row["Risk"] == "High" else "orange" if row["Risk"] == "Medium" else "green"

        rows += f"""
        <tr>
            <td>{row['Crypto']}</td>
            <td>{round(row['Volatility'], 4)}</td>
            <td style="color:{color};">{row['Risk']}</td>
        </tr>
        """

    html = f"""
    <html>
    <body style="font-family:Arial;background:#0f0c29;color:white;padding:20px;">
        <h2 style="color:#ff4d4d;">⚠ Risk Alert</h2>

        <table style="width:100%;border-collapse:collapse;">
            <tr style="background:#302b63;">
                <th>Crypto</th>
                <th>Volatility</th>
                <th>Risk</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """

    return send_email(to_email, subject, html)


# =========================
# PORTFOLIO SUMMARY EMAIL
# =========================
def send_portfolio_summary_email(to_email, df):

    subject = "📊 Portfolio Summary"

    if df.empty:
        return send_email(to_email, subject, "<h3>No portfolio data</h3>")

    total_invested = df["Amount"].sum()
    total_value = df["Current Value"].sum()
    profit = total_value - total_invested

    rows = ""

    for _, row in df.iterrows():
        color = "green" if row["Profit ($)"] >= 0 else "red"

        rows += f"""
        <tr>
            <td>{row['Crypto']}</td>
            <td>${row['Amount']}</td>
            <td>${row['Current Value']:.2f}</td>
            <td style="color:{color};">${row['Profit ($)']:.2f}</td>
        </tr>
        """

    html = f"""
    <html>
    <body style="font-family:Arial;background:#0f0c29;color:white;padding:20px;">
        <h2>📊 Portfolio Summary</h2>

        <p><b>Total Invested:</b> ${total_invested:.2f}</p>
        <p><b>Current Value:</b> ${total_value:.2f}</p>
        <p><b>Profit:</b> ${profit:.2f}</p>

        <table style="width:100%;border-collapse:collapse;margin-top:15px;">
            <tr style="background:#302b63;">
                <th>Crypto</th>
                <th>Invested</th>
                <th>Current</th>
                <th>Profit</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """

    return send_email(to_email, subject, html)
