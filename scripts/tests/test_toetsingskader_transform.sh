#!/usr/bin/env bash

echo "Testing conversion toetsingskader v1 to systemcard v01a3"
./scripts/convert_toetsingskader_v1.sh "mock_data/mock_toetsingskader.xlsx"
difference=$(diff  out/toetsingskader_algoritmes_v1.yml mock_data/expected_toetsingskader_algoritmes_v1_model_card.yaml)
if [[ $difference !=  "" ]];
then
    echo "Conversion toetsingskader algoritmes v1 to system card v01a3 unsuccessfull:"
    echo "$difference"
else
    echo "Conversion toetsingskader algoritmes v1 to system card v01a3 successfull"
fi
rm -rf input
rm -rf out
