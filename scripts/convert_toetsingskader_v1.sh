#!/usr/bin/env bash

if [ "$1" ]
then
    poetry run conversion_utils --action convert_toetsingskader --path $1

else
    poetry run conversion_utils --action convert_toetsingskader
fi
mkdir -p out
yq -p=csv -o=yaml --csv-auto-parse=f --from-file transformations/toetsingskader_algoritmes/v1_to_systemcard_v01a3.yq  input/toetsingskader_algoritmes_v1.csv > out/toetsingskader_algoritmes_v1.yml
