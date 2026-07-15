import os
import sqlite3

from flask import Flask
from flask import request
from flask import redirect
from datetime import datetime


app = Flask(__name__)

DATABASE = "/data/phishing.db"

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

    save_click(
        email,
        token,
        ip
    )

    update_user_status(token)
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
