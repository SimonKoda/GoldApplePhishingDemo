import os
import sqlite3
import secrets
import smtplib
import pandas as pd

from datetime import datetime
from email.message import EmailMessage

DATABASE = "/data/phishing.db"

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

BASE_URL = os.getenv("BASE_URL")

def read_users():

    return pd.read_csv("users.csv")

def generate_token():

    return secrets.token_hex(16)

def user_exists(email):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(

        """
        SELECT id
    
        FROM users

        WHERE email=?

        """,

        (email,)
        )

    result = cursor.fetchone()

    conn.close()

    return result is not None

def save_user(email, token):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    send_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute(

        """
        INSERT INTO users(

            email,
            token,
            status,
            send_time

        )   

        VALUES(?,?,?,?)

        """,

        (

            email,
            token,
            "sent",
            send_time

        )
        )

    conn.commit()
    conn.close()

def build_link(email, token):

    return (

        f"{BASE_URL}"
        f"/?email={email}"
        f"&token={token}"
        )

def build_message(name, link):

    return f"""

    Dear {name},

    Please review the latest security policy update.

    Click the following link:

    {link}

    Regards,

    IT Department
    """

def send_email(receiver, name, link):

    message = EmailMessage()

    message["Subject"] = "Security Policy Update"
    message["From"] = SMTP_USER
    message["To"] = receiver

    text_content = f"""
Dear {name},

Please review the latest security policy update.

Click the following link:

{link}

Regards,

IT Department
"""

    message.set_content(text_content)

    html_content = f"""
<html>

<body>

<p>Dear {name},</p>

<p>
Please review the latest security policy update.
</p>

<p>
<a href="{link}">
Click here to review the update.
</a>
</p>

<p>
Regards,<br>
IT Department
</p>

</body>

</html>
"""

    message.add_alternative(
        html_content,
        subtype="html"
    )

    with smtplib.SMTP(
        SMTP_SERVER,
        SMTP_PORT
    ) as smtp:

        smtp.starttls()

        smtp.login(
            SMTP_USER,
            SMTP_PASSWORD
        )

        smtp.send_message(message)

"""def send_email(receiver, content):

    message = EmailMessage()

    message["Subject"] = "Security Policy Update"
    message["From"] = SMTP_USER
    message["To"] = receiver

    message.set_content(content)

    with smtplib.SMTP(
        SMTP_SERVER,
        SMTP_PORT

        ) as smtp:

        smtp.starttls()

        smtp.login(
        SMTP_USER,
        SMTP_PASSWORD
        )

        smtp.send_message(message)
"""

def main():

    users = read_users()

    success = 0
    failed = 0

    print("\n===================================")
    print("Security Awareness Training")
    print("===================================\n")

    print(f"{len(users)} users loaded.\n")

    for _, row in users.iterrows():

        email = row["email"]
        name = row["name"]

        print("-----------------------------------")
        print(f"Processing : {email}")

        try:

            if user_exists(email):

                print("Status : SKIPPED")
                print("Reason : User already exists.\n")

                continue

            token = generate_token()

            save_user(
                email,
                token
            )

            link = build_link(
                email,
                token
            )

            send_email(
                email,
                name,
                link
            )

            success += 1

            print("Status : SUCCESS")
            print(f"Token  : {token}\n")

        except Exception as error:

            failed += 1

            print("Status : FAILED")
            print(f"Error  : {error}\n")

        print("===================================")
        print(f"Success : {success}")
        print(f"Failed  : {failed}")
        print("===================================\n")

if __name__ == "__main__":

    main()

