#!/usr/bin/env python3
"""Script to test my regular expressions"""
import re

message = "name=egg;email=eggmin@eggsample.com;password=e112@gc$llent;date_of_birth=12/12/1986;"
fields = ['password', 'date_of_birth']
redaction = 'xxxx'
for field in fields:
    re.search(f'{field}=([^;\\s]+)', message, flags=0)
    message = re.sub(f'{field}=([^;\\s]+)', f'{field}={redaction}', message)
print(message)