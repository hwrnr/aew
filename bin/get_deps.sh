#! /bin/bash

if [[ -z $1 ]]; then
  echo "Give PKGBUILD file as argument to this command"
  echo "Like this: $0 PKGBUILD"
  exit 1
fi

source $1 #semi safe
printf '%s\n' "${depends[@]}"
printf '%s\n' "${makedepends[@]}"
printf '%s\n' "${optdepends[@]}" | sed 's/:.*//g'
