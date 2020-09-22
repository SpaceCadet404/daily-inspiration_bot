#!/bin/bash
if [[ ! $(pgrep -f telegram_bot.py) ]]; then
        echo "Starting telegram_bot.py"
        python3 telegram_bot.py
else
        echo "telegram_bot.py already running. Nothing to do!"
fi

if [[ ! $(pgrep -f inspirobot_bot_daily.py) ]]; then
        echo "Starting inspirobot_bot_daily.py"
        python3 inspirobot_bot_daily.py
else
        echo "inspirobot_bot_daily.py already running. Nothing to do!"
fi
