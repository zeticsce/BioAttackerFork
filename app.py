import pymysql
from pymysql.cursors import DictCursor

import os
import sys


from libs.mysql_connect import query

from aiogram import Bot, Dispatcher
import asyncio

