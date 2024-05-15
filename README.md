# TAD Conversion Tool

This repository contains transformations to the TAD System Card. Currently supported transformations:
1. Algoritmeregister (v0.1.0, v0.4.0, v1.0.0) --> TAD System Card (v0.1a3).
1. Toetsingskader algoritmes (v1) --> TAD Assessment Card (v0.1a3).

## Prerequisites
The following are required:
- [yq](https://mikefarah.gitbook.io/yq). On MacOs install yq by executing the following command
in the terminal:
    ```shell
    brew install yq
    ```
- Python and Poetry. To install Python, follow
[these](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation) instructions. To install
Poetry follow, [these](https://python-poetry.org/docs/#installing-with-pipx) instruction.

Before using the conversion scripts run:
```shell
poetry install
```

## Usage
The directory `transformations/` contains the transformation files. These transformation files
can be loaded by `yq` to transform a given input format to TAD System Cards. One can add transformations
for new input formats.

The directory `scripts` contains shells scripts for converting the algoritmeregister and the toetsingskader
algoritmes to TAD System Cards and Assessment Cards respectively.
The command
```shell
./scripts/convert_algoritmeregister.sh
```
will load the whole algoritmeregister from this [resource](https://algoritmes.overheid.nl/api/downloads/ENG?filetype=csv).
This will create a directory `out/` in which TAD System Cards will be generated from the entries from the
algoritmeregsiter. The System Cards will have filenames `{organization}_{name}.yml`.
Furthermore, it is also possible to provide an explicit file to this script, which will convert a csv
file containing entries from the algoritmeregister to System Cards by executing:
```shell
./scripts/convert_algoritmeregister.sh <PATH_TO_ALGORITMEREGISTER_CSV>
```
The command
```shell
./scripts/convert_toetsingskader_v1.sh
```
will load the empty toetsingskader algoritmes v1 from this [resource](https://www.rekenkamer.nl/binaries/rekenkamer/documenten/publicaties/2021/01/28/download-het-toetsingskader/Toetsingskader+algoritmes+v1.0.xlsx).
This will create an Assessment Card in `out/toetsingskader_algoritmes_v1.yml`.
Furthermore, it is also possible to provide an explicit file to this script, which will convert a xlsx
file of a toetsingskader algoritmes to a Assesment Card by executing:
```shell
./scripts/convert_toetsingskader_v1.sh <PATH_TO_TOETSINGSKADER_XLSX>
```

## Tests
To test the algoritmeregister transformations, run:
```shell
./scripts/tests/test_algoritmeregister_transform.sh
```
To test the toetsingskader transformation, run:
```shell
./scripts/tests/test_toetsingskader_transform.sh
```
