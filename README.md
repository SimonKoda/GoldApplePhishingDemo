# GoldApplePhishingDemo
# Phishing Awareness Training System

A containerized phishing awareness training platform built with Docker Compose.

## Features

* Send personalized phishing awareness emails via SMTP.
* Generate unique tracking tokens for each recipient.
* Track user click events.
* Record user email, token, source IP address and click time.
* Store training records in SQLite.
* Display a phishing awareness training page after users click the link.
* One-command deployment using Docker Compose.

## Project Structure

Phishing_Training/
│
├── README.md
├── .gitignore
├── database/
├── docker-compose.yml
├── mailservice/
├── nginx/
└── tracker/

## Requirements

* Docker
* Docker Compose

## Configuration

Create the following file before sending emails:

mailer/.env

Example:

SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
BASE_URL=http://localhost:8084

Create your user list:

mailer/users.csv

Example:

email,name
alice@example.com,Alice
bob@example.com,Bob
charlie@example.com,Charlie

## Running the Project

Build and start the services:

bash:
docker compose up -d --build

Check running containers:

bash:
docker ps

The phishing awareness page will be available at:

http://localhost:8084

## Sending Emails

Run the mailer service manually:

bash:
docker compose run --rm mailservice

The mailer will:

* Read users from users.csv.
* Generate a unique token.
* Store user information in SQLite.
* Generate a personalized phishing link.
* Send emails via SMTP.

## Checking the Database

The SQLite database is stored under:

database/phishing.db

Open the database:

bash:
sqlite3 database/phishing.db

Show all tables:

sql:
.tables

View user records:

sql:
SELECT * FROM users;

View click logs:

sql:
SELECT * FROM click_logs;

## Click Tracking Flow

User
 |
Click Email Link
 |
nginx (8084)
 |
tracker (5000)
 |
Record Click Information
 |
Update User Status
 |
Redirect to phishing.html
 |
Training Completed

## Disclaimer

This project is intended for phishing awareness training and educational purposes only. It should only be used in authorized environments.
