#!/usr/bin/env python3
"""Generate database of arch dependencies on other distributions."""
import fileinput
import sys
import sqlite3
import re

# SQLite3 queries
ADD_TABLE_QUERY = 'CREATE TABLE IF NOT EXISTS packages (arch varchar(24));'
ADD_ARCH_QUERY = 'INSERT INTO PACKAGES (arch) VALUES (?);'
ADD_COLUMN_QUERY = 'ALTER TABLE packages ADD COLUMN ? varchar(24);'
GET_PACKAGES_QUERY = 'SELECT arch FROM packages;'
UPDATE_QUERY = 'UPDATE packages SET ?=? WHERE arch=?'


# Get packages and distro variables
if len(sys.argv) == 3:
    with open(sys.argv[2], 'r') as file:
        packages = file.read().splitlines()
        distro = sys.argv[1]

elif len(sys.argv) == 2:
    packages = list(fileinput.input(files='-'))
    distro = sys.argv[1]
else:
    sys.exit(1)


packages = [package.replace('\n', '') for package in packages]


# Instantiate database
connection = sqlite3.connect('packages.db')
cursor = connection.cursor()

# Create database if doesn't exist
cursor.execute(ADD_TABLE_QUERY)

# Arch packages
if distro == 'arch':
    for package in packages:
        cursor.execute(ADD_ARCH_QUERY, (package, ))
else:
    cursor.execute(ADD_COLUMN_QUERY, (distro, ))
    cursor.execute(GET_PACKAGES_QUERY)
    for package in cursor.fetchall():
        for host_package in packages:
            if host_package in package:
                cursor.execute(UPDATE_QUERY, (distro, host_package, package))
        else:
            keywords = re.split('_|-', package)
            for keyword in keywords:
                if keyword in package:
                    cursor.execute(
                        UPDATE_QUERY, (distro, host_package, package))


# Save and exit the session
connection.commit()
connection.close()
