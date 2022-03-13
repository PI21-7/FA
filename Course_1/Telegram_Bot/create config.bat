@echo off
 
set /p TOKEN="TOKEN: "
set /p ADMIN="Администратор: "
echo TOKEN = r'%TOKEN%' > config.py
echo ADMIN = [r'%ADMIN%']>>config.py