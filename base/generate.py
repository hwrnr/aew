#!/usr/bin/env python3
"""Generate database of arch dependencies on other distributions."""
import fileinput
import sys
import sqlite3
from difflib import SequenceMatcher
from tqdm import tqdm

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

    for raw_package in tqdm(cursor.fetchall()):
        arch_package = raw_package[0]
        for raw_host_pkg in packages:
            if '/' in raw_host_pkg:
                host_package = raw_host_pkg.split('/')[1]

            if host_package == arch_package:
                cursor.execute(UPDATE_QUERY.format(distro),
                               (raw_host_pkg, arch_package))
                break


# Save and exit the session
connection.commit()
connection.close()
