# GoldApplePhishingDemo

## Phishing Awareness Training System

A containerized phishing awareness training platform built with Docker Compose.

This project simulates phishing awareness exercises by sending personalized training emails, tracking user interactions, recording security awareness metrics, and providing real-time administrator notifications through Telegram.

## Features

* Send personalized phishing awareness emails via SMTP.
* Generate unique tracking tokens for each recipient.
* Generate personalized phishing links.
* Track user click events through a tracking service.
* Record user email, token, source IP address, and click time.
* Store training records in SQLite database.
* Update user training status after interaction.
* Display a phishing awareness training page after users click the link.
* Send real-time phishing click notifications through Telegram Bot API.
* Fully containerized deployment using Docker Compose.

---

## System Architecture

                    User
                      |
                      |
              Phishing Email Link
                      |
                      v
                Nginx (8084)
                      |
                      v
              Tracker Service
              (Flask/Python)
                /          \
               /            \
              v              v
     SQLite Database     Telegram Bot API
                              |
                              v
                    Administrator Alert


              Mail Service
                   |
                   v
                 SMTP
                   |
                   v
             Recipient Email

---

## Project Structure

Phishing_Training/

├── README.md
├── .gitignore
├── .env
├── database/
│
├── docker-compose.yml
│
├── mailservice/
│   ├── Dockerfile
│   ├── send_email.py
│   └── users.csv
│
├── nginx/
│   ├── Dockerfile
│   └── nginx.conf
│
└── tracker/
    ├── Dockerfile
    ├── app.py
    └── requirements.txt

---

## Requirements

* Docker
* Docker Compose

---

# Configuration

## Environment Variables

Create a `.env` file in the project root directory.

Example:
env
TELEGRAM_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

The tracker service loads these variables automatically through Docker Compose.

For email sending configuration, create:

mailservice/.env

Example:
env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
BASE_URL=http://localhost:8084

---

# User List Configuration

Create the recipient list:

mailservice/users.csv

Example:
csv
email,name
alice@example.com,Alice
bob@example.com,Bob
charlie@example.com,Charlie

---

# Running the Project

Build and start all services:

bash
docker compose up -d --build

Check running containers:
bash
docker ps

The phishing awareness page will be available at:

http://localhost:8084

---

# Sending Phishing Awareness Emails

Run the mail service manually:
bash
docker compose run --rm mailservice

The mail service will:

1. Read recipients from `users.csv`.
2. Generate a unique tracking token.
3. Store user information in SQLite.
4. Generate a personalized phishing URL.

Example:

http://localhost:8084/?email=user@example.com&token=8f34d2...

5. Send the personalized email through SMTP.

---

# Click Tracking Flow

When a user clicks the phishing link:

User Clicks Email Link

        |
        v

Nginx (8084)

        |
        v

Tracker Service (5000)

        |
        +----------------+
        |                |
        v                v

Save Click Event    Update User Status

        |
        v

Send Telegram Notification

        |
        v

Redirect to phishing.html

        |
        v

Training Completed

---

# Telegram Notification

The tracker service sends a Telegram notification after every phishing link click.

Example notification:

Phishing Transition

Email:
ivan@test.ru

IP:
10.10.10.15

Date:
2026-08-15 10:15:23

Token:
8f34d2...

The notification contains:

* User email address.
* Source IP address.
* Click timestamp.
* Unique tracking token.

---

# Database

The SQLite database is stored at:

database/phishing.db

Open the database:
bash
sqlite3 database/phishing.db

Show tables:
sql
.tables

View users:
sql
SELECT * FROM users;

View click events:
sql
SELECT * FROM click_logs;

---

# Disclaimer

This project is intended for phishing awareness training and educational purposes only.

It should only be deployed and used in authorized environments with proper permission from system owners and users.
