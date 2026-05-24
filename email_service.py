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
    Requires an App Password if using 2FA.
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
# 📝 TRANSACTION RECEIPT (BUY/SELL)
# ======================================================
def send_transaction_notification(to_email, coin, action, amount):
    """
    Sends an immediate receipt after a Buy or Sell order.
    """
    subject = f"✅ Transaction Confirmed: {action} {coin}"
    
    # Visual cues for Buy (Green) vs Sell (Red)
    accent_color = "#00ffcc" if action == "Buy" else "#ff4b4b"
    header_text = "Purchase Confirmed" if action == "Buy" else "Sale Confirmed"

    html = f"""
    <html>
    <body style="font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color:#0f0c29; color:#ffffff; padding:40px;">
        <div style="max-width:600px; margin:0 auto; background-color:#1a1a3a; border-radius:15px; overflow:hidden; border:1px solid #302b63;">
            <div style="background-color:{accent_color}; padding:20px; text-align:center;">
                <h1 style="color:#0f0c29; margin:0; font-size:24px;">{header_text}</h1>
            </div>
            <div style="padding:30px;">
                <p style="font-size:16px; color:#94A3B8;">Hello,</p>
                <p style="font-size:16px; line-height:1.6;">Your recent transaction has been successfully processed and updated in your <b>CryptoPort AI</b> portfolio.</p>
                
                <div style="background-color:#0f0c29; padding:20px; border-radius:10px; margin:20px 0; border-left:4px solid {accent_color};">
                    <table style="width:100%; border-spacing:0 10px;">
                        <tr><td style="color:#94A3B8;">Asset:</td><td style="text-align:right; font-weight:bold;">{coin}</td></tr>
                        <tr><td style="color:#94A3B8;">Action:</td><td style="text-align:right; font-weight:bold; color:{accent_color};">{action.upper()}</td></tr>
                        <tr><td style="color:#94A3B8;">Amount:</td><td style="text-align:right; font-weight:bold;">${amount:,.2f}</td></tr>
                        <tr><td style="color:#94A3B8;">Status:</td><td style="text-align:right; font-weight:bold; color:#00ffcc;">COMPLETED</td></tr>
                    </table>
                </div>
                
                <p style="font-size:14px; color:#94A3B8; text-align:center; margin-top:30px;">
                    Thank you for using CryptoPort AI Elite.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    return send_email(to_email, subject, html)

# ======================================================
# 📊 WEEKLY/DAILY PORTFOLIO SUMMARY
# ======================================================
def send_portfolio_summary_email(to_email, portfolio_df):
    """
    Sends a complete breakdown of current holdings and total profit.
    """
    subject = "📊 Your CryptoPort AI Portfolio Statement"
    
    total_invested = portfolio_df["Total Invested"].sum()
    total_value = portfolio_df["Current Value"].sum()
    total_profit = total_value - total_invested
    profit_pct = (total_profit / total_invested * 100) if total_invested != 0 else 0

    # Build the table rows dynamically
    table_rows = ""
    for _, row in portfolio_df.iterrows():
        p_color = "#00ffcc" if row["P/L ($)"] >= 0 else "#ff4b4b"
        table_rows += f"""
        <tr style="border-bottom:1px solid #302b63;">
            <td style="padding:12px; border-bottom:1px solid #302b63;">{row['Asset']}</td>
            <td style="padding:12px; border-bottom:1px solid #302b63;">{row['Quantity']}</td>
            <td style="padding:12px; border-bottom:1px solid #302b63; text-align:right;">${row['Current Value']:,.2f}</td>
            <td style="padding:12px; border-bottom:1px solid #302b63; text-align:right; color:{p_color}; font-weight:bold;">{row['ROI (%)']:.2f}%</td>
        </tr>
        """

    html = f"""
    <html>
    <body style="font-family:sans-serif; background-color:#0f0c29; color:white; padding:20px;">
        <h2 style="color:#00ffcc;">Executive Summary</h2>
        <div style="background:#1a1a3a; padding:20px; border-radius:12px; margin-bottom:20px;">
            <table style="width:100%;">
                <tr>
                    <td><b>Total Value:</b></td><td style="font-size:24px; color:#00ffcc;">${total_value:,.2f}</td>
                </tr>
                <tr>
                    <td><b>Total Profit:</b></td><td style="color:{'#00ffcc' if total_profit >= 0 else '#ff4b4b'};">${total_profit:,.2f} ({profit_pct:.2f}%)</td>
                </tr>
            </table>
        </div>
        
        <h3>Asset Breakdown</h3>
        <table style="width:100%; border-collapse:collapse; background:#1a1a3a;">
            <tr style="background:#302b63; color:#94A3B8; text-align:left;">
                <th style="padding:12px;">Asset</th><th style="padding:12px;">Qty</th><th style="padding:12px; text-align:right;">Value</th><th style="padding:12px; text-align:right;">ROI</th>
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
    Sends an alert when a coin hits a specific price target.
    """
    subject = f"🚨 ALERT: {coin} target reached!"
    color = "#00ffcc" if condition == "above" else "#ff4b4b"
    direction = "surpassed" if condition == "above" else "dropped below"

    html = f"""
    <div style="background:#0f0c29; color:white; padding:30px; border-radius:15px; border:2px solid {color};">
        <h2 style="color:{color};">Target Triggered!</h2>
        <p>Your price alert for <b>{coin}</b> has been triggered.</p>
        <p>{coin} has {direction} your target of <b>${target_price:,.2f}</b>.</p>
        <hr style="border:0; border-top:1px solid #302b63;">
        <p>Current Market Price: <span style="font-size:20px; font-weight:bold;">${current_price:,.2f}</span></p>
    </div>
    """
    return send_email(to_email, subject, html)
