@echo off
 
set /p TOKEN="TOKEN: "
set /p ADMIN="Администратор: "
echo TOKEN = r'%TOKEN%' > config.p
echo ADMIN = [r'%ADMIN%']>>config.py