# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

output = ""
file_name = "landingtext.txt"
string_to_add = "+01:00"

with open(file_name, 'r') as f:
    file_lines = [''.join([x.strip(), string_to_add, '\n']) for x in f.readlines()]

with open(file_name, 'w') as f:
    f.writelines(file_lines) 