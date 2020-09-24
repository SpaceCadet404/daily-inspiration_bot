#!/bin/bash
kill $(pgrep -f telegram_bot.py)
echo "telegram_bot.py has been stopped."
kill $(pgrep -f inspirobot_bot_daily.py)
echo "inspirobot_bot_daily.py has been stopped."
