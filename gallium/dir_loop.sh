#!/bin/bash

for path in $PWD/conf_files/*
  do
    (
    [ -d "${path}" ] || continue # if not a directory, skip
    dirname="$(basename "${path}")"
    echo $path
    cd $path || exit
    phonopy --quiet mesh.conf
    )
  done
