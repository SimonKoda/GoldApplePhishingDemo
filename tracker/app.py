import os
import sqlite3
import requests

from flask import Flask
from flask import request
from flask import redirect
from datetime import datetime


app = Flask(__name__)

DATABASE = "/data/phishing.db"
#TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
#TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_TOKEN = "8764667229:AAHr91hcF7I-lXCuzoIPi_HaT9ysoLYTsIU"
TELEGRAM_CHAT_ID = "8965212146"


def send_telegram_notification(email, ip, click_time, token):

    message = f"""
Phishing Transition
    
Email:
{email}

IP:
{ip}

Date:
{click_time}

Token:
{token}
"""

    url = (
            f"https://api.telegram.org/"
            f"bot{TELEGRAM_TOKEN}"
            f"/sendMessage"
            )

    data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
            }

    try:
        response = requests.post(
            url,
            json=data,
            timeout=10
            )
        print(response.status_code,response.text)
    
    except Exception as e:
        print(
                "Telegram error:",
                e
                )


def init_database():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        token TEXT NOT NULL UNIQUE,
        status TEXT DEFAULT 'sent',
        send_time TEXT

        )

    """)

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS click_logs(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        token TEXT NOT NULL,
        ip TEXT,
        click_time TEXT

        )

    """)

    conn.commit()

    conn.close()

def save_click(email,token,ip):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    click_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""

        INSERT INTO click_logs(
        email,
        token,
        ip,
        click_time

        )

        VALUES(?,?,?,?)

    """,

    (

        email,
        token,
        ip,
        click_time

    )

    )

    conn.commit()

    conn.close()

    return click_time

def update_user_status(token):

    conn = sqlite3.connect(DATABASE)
    
    cursor = conn.cursor()
    
    cursor.execute("""

        UPDATE users

        SET status='clicked'

        WHERE token=?
                   
    """,

    (token,)

    )

    conn.commit()

    conn.close()


def verify_user(email, token):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute(

        """
        SELECT id

        FROM users

        WHERE email=?
        AND token=?

        """,

        (email, token)

    )

    result = cursor.fetchone()

    conn.close()

    return result is not None

@app.route("/")

def phishing_tracker():

    email = request.args.get("email")

    token = request.args.get("token")

    if not verify_user(email,token):

        return "Invalid request",400

    ip = request.headers.get(
            "X-Real-IP"
            )
    if not ip:

        ip = request.remote_addr

    click_time = save_click(
            email,
            token,
            ip
            )

    update_user_status(token)
    
    send_telegram_notification(
            email,
            ip,
            click_time,
            token
            )

    return redirect(
            "/phishing.html",
            code=302
                    )

if __name__ == "__main__":

    os.makedirs("/data",exist_ok=True)

    init_database()

    app.run(

        host="0.0.0.0",
        port=5000

    )
