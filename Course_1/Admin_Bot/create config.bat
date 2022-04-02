@echo off

chcp 65001

set /p TOKEN="TOKEN: "

set /p Admin="Admin: "
 
echo TOKEN = r'%TOKEN%' > config.py

echo Admin = ['%Admin%',] >> config.py

