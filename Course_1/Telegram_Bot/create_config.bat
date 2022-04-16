@echo off

chcp 65001

set /p TOKEN="TOKEN: "

set /p Admin="Admin: "
 
echo TOKEN = r'%TOKEN%' > config.py

mkdir Admin

cd Admin

echo %Admin%, > admins.txt
