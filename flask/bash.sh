#!/bin/bash
mysql -uroot -proot -e "drop database weatherstation;"
python3 database.py
python3 database_handler.py