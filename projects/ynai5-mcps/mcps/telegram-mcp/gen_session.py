"""Run this ONCE to generate your Telegram session string.
Then paste the output into your .env file as TELEGRAM_SESSION_STRING"""
import os
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

API_ID   = int(input("Enter your API_ID from my.telegram.org: "))
API_HASH = input("Enter your API_HASH from my.telegram.org: ")

with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    print("\n✅ Your session string (paste into .env):")
    print(client.session.save())
