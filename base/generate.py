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
    "gentoo": ["/bin/cat", "/tmp/gentoo"], 
    "redhat": ["/usr/bin/yum", "list", "all"], # Don't use this, not tested
    "alpine": ["/usr/bin/apk", "search"], # Don't use this, not tested
    "debian": ["/usr/bin/apt", "list"] # Don't use this, not tested
}

if not distro in distros.keys():
    sys.exit(1)


distro_rows = [dis+" varchar(32)" for dis in distros.keys()]

connection = sqlite3.connect("packages.db")
cursor = connection.cursor()
cursor.execute(TABLE_QUERY.format(distro_rows))

process = subprocess.Popen(distros[distro], stdout=subprocess.PIPE)
packages = process.stdout.read().decode("utf-8").splitlines()

cursor.execute("SELECT arch FROM packages")
arch_packages = cursor.fetchall()

if distro == "arch":
    for package in packages:
        cursor.execute(ADD_ARCH_QUERY, (package, ))
else:
    for arch_package in arch_packages:
        print(arch_package)
        for host_package in packages:
            if arch_package[0] in host_package:
                cursor.execute(UPDATE_QUERY.format(distro), (host_package, arch_package[0]))

connection.commit()
connection.close()
