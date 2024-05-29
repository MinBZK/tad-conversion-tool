#!/usr/bin/env bash

if [ "$1" ]
then
    poetry run conversion_utils --action split_algoritmeregister --path $1

else
    poetry run conversion_utils --action split_algoritmeregister
fi

mkdir -p out/
yq -p=csv -o=yaml --csv-auto-parse=f --from-file transformations/algoritmeregister/v010_to_systemcard_v01a3.yq  input/algoritmeregister_v010.csv | yq '.[]' -s '"out/"+(.owners[0].organization|downcase|sub("[^a-zA-Z0-9]"; "_")) + "_" + (.name|downcase|sub("[^a-zA-Z0-9]"; "_"))'
yq -p=csv -o=yaml --csv-auto-parse=f --from-file transformations/algoritmeregister/v040_to_systemcard_v01a3.yq  input/algoritmeregister_v040.csv | yq '.[]' -s '"out/"+(.owners[0].organization|downcase|sub("[^a-zA-Z0-9]"; "_")) + "_" + (.name|downcase|sub("[^a-zA-Z0-9]"; "_"))'
yq -p=csv -o=yaml --csv-auto-parse=f --from-file transformations/algoritmeregister/v100_to_systemcard_v01a3.yq  input/algoritmeregister_v100.csv | yq '.[]' -s '"out/"+(.owners[0].organization|downcase|sub("[^a-zA-Z0-9]"; "_")) + "_" + (.name|downcase|sub("[^a-zA-Z0-9]"; "_"))'
