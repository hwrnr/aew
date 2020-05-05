#!/usr/bin/env python3
import sys
import sqlite3

if len(sys.argv)<3:
    print(f"Usage: {sys.argv[0]} [DISTRO] [BASE] [DEPS...]")
    sys.exit(1)

distro = sys.argv[1]
base = sys.argv[2]
deps = sys.argv[3:]

connection = sqlite3.connect(base)
cursor = connection.cursor()

for i in deps:
	cursor.execute("SELECT {} FROM packages WHERE arch=?".format(distro), deps)
	print(cursor.fetchone()[0])

connection.close()