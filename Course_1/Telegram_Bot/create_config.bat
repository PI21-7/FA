@echo off

chcp 65001

set /p TOKEN="TOKEN: "

set /p ADMIN_BOT="Admin_bot_token: "

set /p Admin="Admin: "
 
echo TOKEN = r'%TOKEN%' > config.py

echo ADMIN_BOT_TOKEN = r'%ADMIN_BOT%' >> config.py

echo ADMIN = None  # Admin's user_id >> config.py

mkdir Admin

cd Admin

echo %Admin%, > admins.txt
