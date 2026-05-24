import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import EMAIL_USER, EMAIL_PASS

# ======================================================
# 🚀 CORE EMAIL SENDER ENGINE
# ======================================================
def send_email(to_email: str, subject: str, html_content: str):
    """
    Base engine to send HTML emails via Gmail SMTP.
    Requires a Google App Password (16 characters) to work.
    """
    try:
        msg = MIMEMultipart()
        msg["From"] = f"CryptoPort AI <{EMAIL_USER}>"
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(html_content, "html"))

        # Connection to Google SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()

        return True
    except Exception as e:
        print(f"CRITICAL EMAIL ERROR: {e}")
        return False

# ======================================================
# 📝 TRANSACTION NOTIFICATION (BUY/SELL RECEIPT)
# ======================================================
def send_transaction_notification(to_email, coin, action, amount):
    """
    Sends an immediate receipt after a Buy or Sell transaction.
    This provides a 'banking app' experience for the user.
    """
    subject = f"✅ Transaction Confirmed: {action} {coin}"
    
    # Dynamic styling based on transaction type
    accent_color = "#00ffcc" if action == "Buy" else "#ff4b4b"
    header_title = "Purchase Receipt" if action == "Buy" else "Sale Confirmation"

    html = f"""
    <html>
    <body style="font-family: 'Segoe UI', Tahoma, sans-serif; background-color:#0f0c29; color:#ffffff; padding:20px;">
        <div style="max-width:600px; margin:0 auto; background-color:#1a1a3a; border-radius:15px; border:1px solid #302b63; overflow:hidden;">
            <div style="background-color:{accent_color}; padding:20px; text-align:center;">
                <h1 style="color:#0f0c29; margin:0; font-size:22px;">{header_title}</h1>
            </div>
            <div style="padding:30px;">
                <p style="color:#94A3B8; font-size:16px;">Order Details:</p>
                <div style="background-color:#0f0c29; padding:20px; border-radius:10px; border-left:4px solid {accent_color};">
                    <table style="width:100%; border-spacing: 0 10px;">
                        <tr><td style="color:#94A3B8;">Asset:</td><td style="text-align:right; font-weight:bold;">{coin}</td></tr>
                        <tr><td style="color:#94A3B8;">Type:</td><td style="text-align:right; font-weight:bold; color:{accent_color};">{action.upper()}</td></tr>
                        <tr><td style="color:#94A3B8;">Cash Value:</td><td style="text-align:right; font-weight:bold;">${amount:,.2f}</td></tr>
                        <tr><td style="color:#94A3B8;">Status:</td><td style="text-align:right; font-weight:bold; color:#00ffcc;">SETTLED</td></tr>
                    </table>
                </div>
                <p style="text-align:center; color:#94A3B8; font-size:12px; margin-top:20px;">
                    Your portfolio weighted average price has been updated automatically.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    return send_email(to_email, subject, html)

# ======================================================
# 📊 PORTFOLIO SUMMARY STATEMENT
# ======================================================
def send_portfolio_summary_email(to_email, portfolio_df):
    """
    Sends a full breakdown of current holdings and net profit/loss.
    """
    subject = "📊 Your CryptoPort AI Portfolio Statement"
    
    total_invested = portfolio_df["Total Invested"].sum()
    total_value = portfolio_df["Current Value"].sum()
    total_profit = total_value - total_invested
    roi = (total_profit / total_invested * 100) if total_invested != 0 else 0

    # Build the HTML table rows
    table_rows = ""
    for _, row in portfolio_df.iterrows():
        p_color = "#00ffcc" if row["P/L ($)"] >= 0 else "#ff4b4b"
        table_rows += f"""
        <tr style="border-bottom:1px solid #302b63;">
            <td style="padding:12px;">{row['Asset']}</td>
            <td style="padding:12px;">{row['Quantity']:.4f}</td>
            <td style="padding:12px; text-align:right;">${row['Current Value']:,.2f}</td>
            <td style="padding:12px; text-align:right; color:{p_color}; font-weight:bold;">{row['ROI (%)']:.2f}%</td>
        </tr>
        """

    html = f"""
    <html>
    <body style="font-family:sans-serif; background-color:#0f0c29; color:white; padding:20px;">
        <h2 style="color:#00ffcc;">Portfolio Performance Summary</h2>
        <div style="background:#1a1a3a; padding:20px; border-radius:12px; margin-bottom:20px; border:1px solid #302b63;">
            <p><b>Current Portfolio Value:</b> <span style="font-size:22px; color:#00ffcc;">${total_value:,.2f}</span></p>
            <p><b>Net P/L:</b> <span style="color:{'#00ffcc' if total_profit >= 0 else '#ff4b4b'};">${total_profit:,.2f} ({roi:.2f}%)</span></p>
        </div>
        
        <table style="width:100%; border-collapse:collapse; background:#1a1a3a; border-radius:10px; overflow:hidden;">
            <tr style="background:#302b63; color:#94A3B8; text-align:left;">
                <th style="padding:12px;">Asset</th><th style="padding:12px;">Quantity</th><th style="padding:12px; text-align:right;">Value</th><th style="padding:12px; text-align:right;">ROI</th>
            </tr>
            {table_rows}
        </table>
    </body>
    </html>
    """
    return send_email(to_email, subject, html)

# ======================================================
# 🚨 PRICE ALERT NOTIFICATION
# ======================================================
def send_alert_email(to_email, coin, condition, target_price, current_price):
    """
    Sends an alert when a user-defined price target is hit.
    """
    subject = f"🚨 Price Alert: {coin} Target Reached!"
    color = "#00ffcc" if condition == "above" else "#ff4b4b"

    html = f"""
    <div style="background-color:#0f0c29; color:white; padding:30px; border-radius:15px; border:2px solid {color}; font-family:sans-serif;">
        <h2 style="color:{color};">Target Triggered!</h2>
        <p>Your alert for <b>{coin}</b> has been triggered.</p>
        <p>Condition: {coin} price is <b>{condition} ${target_price:,.2f}</b>.</p>
        <hr style="border:0; border-top:1px solid #302b63; margin:20px 0;">
        <p style="font-size:18px;">Current Market Price: <b style="color:{color};">${current_price:,.2f}</b></p>
        <p style="font-size:12px; color:#94A3B8; margin-top:20px;">This alert has now been deactivated. Log in to set a new one.</p>
    </div>
    """
    return send_email(to_email, subject, html)
