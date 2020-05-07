#! /bin/bash

if [[ -z $1 ]]; then
  echo "Give PKGBUILD file as argument to this command"
  echo "Like this: $0 PKGBUILD"
  exit 1
fi

source $1 #semi safe
<<<<<<< HEAD:bin/get_deps.sh
printf '%s\n' "${depends[@]}"
printf '%s\n' "${makedepends[@]}"
=======
>>>>>>> 8a6d8a3d3c04ed230717ccd6f2c1d274acefd841:bin/get_odeps.sh
printf '%s\n' "${optdepends[@]}" | sed 's/:.*//g'
