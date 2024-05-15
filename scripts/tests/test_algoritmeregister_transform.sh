#!/usr/bin/env bash

echo "Testing conversion algoritmeregister v010 to systemcard v01a3"
./scripts/convert_algoritmeregister.sh "mock_data/algoritmeregister_v010_entry.csv"
difference=$(diff  out/organization_value_name_value.yml mock_data/expected_algoritmeregister_v010_model_card.yaml)
if [[ $difference !=  "" ]];
then
    echo "Conversion algoritmeregister v010 to system card v01a3 unsuccessfull:"
    echo "$difference"
    exit 1
else
    echo "Conversion algoritmeregister v010 to system card v01a3 successfull"
fi
rm -rf input
rm -rf out

echo "Testing conversion algoritmeregister v040 to systemcard v01a3"
./scripts/convert_algoritmeregister.sh "mock_data/algoritmeregister_v040_entry.csv"
difference=$(diff  out/organization_value_name_value.yml mock_data/expected_algoritmeregister_v040_model_card.yaml)
if [[ $difference !=  "" ]];
then
    echo "Conversion algoritmeregister v040 to system card v01a3 unsuccessfull:"
    echo "$difference"
    exit 1
else
    echo "Conversion algoritmeregister v040 to system card v01a3 successfull"
fi
rm -rf input
rm -rf out

echo "Testing conversion algoritmeregister v100 to systemcard v01a3"
./scripts/convert_algoritmeregister.sh "mock_data/algoritmeregister_v100_entry.csv"
difference=$(diff  out/organization_value_name_value.yml mock_data/expected_algoritmeregister_v100_model_card.yaml)
if [[ $difference !=  "" ]];
then
    echo "Conversion algoritmeregister v100 to system card v01a3 unsuccessfull:"
    echo "$difference"
    exit 1
else
    echo "Conversion algoritmeregister v100 to system card v01a3 successfull"
fi
rm -rf input
rm -rf out
