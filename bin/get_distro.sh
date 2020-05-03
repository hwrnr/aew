#! /bin/bash
DISTRO=$(cat /etc/*release | grep '^NAME' | cut -d '=' -f 2 | sed 's/"//g')
echo ${DISTRO}
