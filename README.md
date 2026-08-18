# Voltify — Telegram Shop Bot

A Telegram bot for an electronics store, built with aiogram.

## Stack
- Python, aiogram
- SQLite (via SQLAlchemy)

## Features
- Product catalog with categories
- Order placement flow (FSM-based)
- Customer provides phone number or username for contact
- Admin receives a notification message when a new order is placed

## Project structure

shop_bot/
├── database/ # models and DB queries
├── handlers/ # command and message handlers
├── keyboards/ # inline/reply keyboards
├── states/ # FSM states for the order flow
├── bot.py # entry point
└── config.py # loads config from .env



## Setup
1. Clone the repository
2. Install dependencies:
   pip install -r requirements.txt
3. Create a `.env` file in the root:
   BOT_TOKEN=your_bot_token
   ADMIN_ID=your_telegram_id
4. Run:
   python bot.py



## Limitations
- No payment integration — orders are collected and forwarded to the admin manually
- No order history for customers
- No admin panel — order management happens via direct Telegram notifications
