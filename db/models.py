from db.database import get_connection
import sqlite3

# =========================
# USER MODELS (Authentication)
# =========================

def create_user(name, email, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def fetch_user(email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cur.fetchone()
    conn.close()
    return user

def update_user_password(email, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET password=? WHERE email=?",
        (password, email)
    )
    conn.commit()
    conn.close()


# =========================
# PORTFOLIO MODELS (Buy/Sell)
# =========================

def add_holding(email, crypto, amount, date):
    """Records a buy transaction."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO holdings (email, crypto, amount, date) VALUES (?, ?, ?, ?)",
        (email, crypto, amount, date)
    )
    conn.commit()
    conn.close()

def sell_holding(email, crypto, amount, date):
    """Records a sell transaction by storing the amount as negative."""
    conn = get_connection()
    cur = conn.cursor()
    # Using negative abs() ensures it's always stored as a subtraction
    cur.execute(
        "INSERT INTO holdings (email, crypto, amount, date) VALUES (?, ?, ?, ?)",
        (email, crypto, -abs(amount), date)
    )
    conn.commit()
    conn.close()

def get_holdings(email):
    """Fetches all transactions for a user to calculate portfolio status."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT crypto, amount, date FROM holdings WHERE email=? ORDER BY date ASC",
        (email,)
    )
    data = cur.fetchall()
    conn.close()
    return data

def get_total_investment(email):
    """Calculates net cash put into the portfolio (Buys - Sells)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT SUM(amount) FROM holdings WHERE email=?",
        (email,)
    )
    total = cur.fetchone()[0]
    conn.close()
    return total if total else 0


# =========================
# PRICE ALERT MODELS
# =========================

def add_alert(email, coin, condition, target_price):
    """Saves a new price alert."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO alerts (email, coin, condition, target_price, active)
        VALUES (?, ?, ?, ?, 1)
    """, (email, coin, condition, target_price))
    conn.commit()
    conn.close()

def get_alerts(email):
    """Fetches alerts for a specific user."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, coin, condition, target_price, active
        FROM alerts WHERE email = ?
    """, (email,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_all_active_alerts():
    """Used by background services to check all pending alerts."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, email, coin, condition, target_price
        FROM alerts WHERE active = 1
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def deactivate_alert(alert_id):
    """Turns off an alert once it has been triggered."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE alerts SET active = 0 WHERE id = ?", (alert_id,))
    conn.commit()
    conn.close()
