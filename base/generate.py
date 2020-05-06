#!/usr/bin/env python3
"""Generate database of arch dependencies on other distributions."""
import fileinput
import sys
import sqlite3
import re

# SQLite3 queries
ADD_TABLE_QUERY = 'CREATE TABLE IF NOT EXISTS packages (arch varchar(24));'
ADD_ARCH_QUERY = 'INSERT INTO PACKAGES (arch) VALUES (?);'
ADD_COLUMN_QUERY = 'ALTER TABLE packages ADD COLUMN {} varchar(24);'
GET_PACKAGES_QUERY = 'SELECT arch FROM packages;'
UPDATE_QUERY = 'UPDATE packages SET {}=? WHERE arch=?'


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
    cursor.execute(ADD_COLUMN_QUERY.format(distro))
    cursor.execute(GET_PACKAGES_QUERY)

    for raw_package in cursor.fetchall():
        package = raw_package[0]
        keywords = re.split('-|_', package)
        alternative = None

        for host_package in packages:

            if package in host_package or host_package in package:
                cursor.execute(UPDATE_QUERY.format(distro),
                               (host_package, package))
                packages.pop(packages.index(host_package))
                break
            for keyword in keywords:
                if keyword in host_package:
                    alternative = host_package
        else:
            cursor.execute(UPDATE_QUERY.format(distro),
                           (alternative, package))
            packages.pop(packages.index(host_package))


# Save and exit the session
connection.commit()
connection.close()
