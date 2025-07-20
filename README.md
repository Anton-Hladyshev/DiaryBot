# DiaryBot

A Telegram bot that prints today's schedule from the Informatics Department of IUT of Limoges.  
This project uses the API developed by [@Vexcited](https://github.com/Vexcited).  
Big thanks to him! 🎉

📎 Source of the API:  
https://github.com/Vexcited/EDT-IUT-Info-Limoges/blob/main/packages/website/README.md

---

## 🚀 Launching Guide

1. **Get a Telegram bot token from [@BotFather](https://t.me/BotFather):**  
   - Talk to BotFather on Telegram and create a new bot.  
   - Copy the generated token for later use.

2. **Install dependencies:**  
   Run this command in the root of the project to install all required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file in the root of the project:**  
   - You can use `.env.example` as a template:
     ```bash
     cp .env.example .env
     ```
   - Then open `.env` and paste your Telegram bot token:
     ```env
     BOT_TOKEN=your-telegram-bot-token-here
     ```

4. **Run the bot:**
   ```bash
   python aiogram_run.py
   ```

---

## 📝 Notes

- Make sure your `.env` file is **not committed** to GitHub. It's already included in `.gitignore`.
- This bot uses [Aiogram](https://docs.aiogram.dev/) for Telegram integration.
