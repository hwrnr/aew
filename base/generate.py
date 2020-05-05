import sqlite3
import sys
import subprocess
import time

TABLE_QUERY = "CREATE TABLE IF NOT EXISTS packages ({})"
ADD_ARCH_QUERY = "INSERT INTO PACKAGES (arch) VALUES (?)"
UPDATE_QUERY = "UPDATE packages SET {}=? WHERE arch=?"

distro = sys.argv[1]
distros = {
    "arch": ["/usr/bin/pacman", "-Qq"],
    "gentoo": ["EIX_LIMIT=0", "/usr/bin/eix", "'*'", "-#"], 
    "redhat": ["/usr/bin/yum", "list", "all"], # Don't use this, not tested
    "alpine": ["apk search"], # Don't use this, not tested
    "debian": ["apt list"] # Don't use this, not tested
}

if not distro in distros.keys():
	sys.exit(1)


distro_rows = [dis+" varchar(32)" for dis in distros.keys()]

connection = sqlite3.connect("packages.db")
cursor = connection.cursor()
cursor.execute(TABLE_QUERY.format(distro_rows))

process = subprocess.Popen(distros[distro], stdout=subprocess.PIPE)

packages = process.stdout.read().decode('utf-8').splitlines()
if distro == "arch":
	for package in packages:
		cursor.execute(ADD_ARCH_QUERY, (package, ))
else:
	for arch_package in cursor.execute("SELECT arch FROM packages"):
		for host_package in packages:
			if arch_package in host_package:
				cursor.execute(UPDATE_QUERY.format(distro), arch_package)
				continue

connection.commit()
connection.close()