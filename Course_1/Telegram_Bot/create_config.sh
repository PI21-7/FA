#!/bin/bash

@echo off

set /p TOKEN="TOKEN: "

set /p Admin="Admin: "

echo TOKEN = r'$TOKEN$' > config.py

mkdir Admin

cd Admin || exit

echo %Admin%, > admins.txt