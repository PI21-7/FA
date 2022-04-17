import asyncio
from datetime import timedelta, datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound
from transliterate import translit
from Buttons.Exactly_Buttons.Buttons import *
from Utils.Groups import *
from Utils.Miscellaneous import *
from Utils.date import week_definition
from Utils.debug import Debugger

