#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import serial

print('参数个数为:', len(sys.argv), '个参数。')
print('参数列表:', str(sys.argv))
print('参数1:', str(sys.argv[1]))
ted = serial.Serial(port="/dev/ttyAMA1", baudrate=9600)
ted.write(str(sys.argv[1]).encode("gbk"))
ted.read(3)
ted.write("Hello World".encode("gbk"))
ted.read(11)