import argparse
import logging
from enum import StrEnum
from io import BytesIO
from pathlib import Path

import pandas as pd
import requests


def convert_toetsingskader_to_csv(df: pd.DataFrame | pd.Series) -> None:
    """
    Converts the second tab in the toetsingskader algoritmes excel to
    csv.
    """
    out_dir = Path("input")
    out_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_dir / "toetsingskader_algoritmes_v1.csv", index=False)


def messy_date_to_iso8601(input: str) -> str:
    """
    Converts messy date (e.g. 10-2022, 2022-10) to ISO 8601 dates.
    If day is not specified, day is set to 01.
    If month is not specified, month is set to 01.
    """

    # Pandas to_datetime does a pretty exhaustive job at
    # parsing (incomplete) dates with different formats. If to_datetime
    # cannot parse, we can assume the date is illegible or not filled in
    # so we return an empty string in this case.
    try:
        return pd.to_datetime(input).date().isoformat()
    except (pd.errors.ParserError, ValueError):
        return ""


def split_algoritmeregister(df: pd.DataFrame) -> None:
    """
    Split algoritmeregister csv file into multiple csv files, where
    each file contains entries with the same schema version.
    """
    # Arguably this section should be removed and done in the yq transformations.
    # Cleanup messy dates to ISO 8601 date without timezone.
    df["begin_date"] = df["begin_date"].apply(lambda x: messy_date_to_iso8601(x))
    df["end_date"] = df["end_date"].apply(lambda x: messy_date_to_iso8601(x))

    out_dir = Path("input")
    out_dir.mkdir(parents=True, exist_ok=True)

    standard_versions = ("0.1.0", "0.4.0", "1.0.0")
    for standard_version in standard_versions:
        df_v = df[df["standard_version"] == standard_version]

        # Save as for example: out_dir/algoritmeregister_v010.csv
        save_path = out_dir / Path(f'algoritmeregister_v{standard_version.replace(".", "")}.csv')
        df_v.to_csv(save_path, index=False)


class Resources(StrEnum):
    ToetsingskaderV1 = "https://www.rekenkamer.nl/binaries/rekenkamer/documenten/publicaties/2021/01/28/download-het-toetsingskader/Toetsingskader+algoritmes+v1.0.xlsx"
    Algoritmeregister = "https://algoritmes.overheid.nl/api/downloads/ENG?filetype=csv"


def load_toetsingskader(path: Path | None) -> pd.Series | pd.DataFrame:
    if path is None:
        logging.info(f"loading toetsingskader from source with url {Resources.ToetsingskaderV1}")
        try:
            request = requests.get(Resources.ToetsingskaderV1)
            request.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"request error: {e}")
            raise SystemExit(f"Unable to get toetsingskader from {Resources.ToetsingskaderV1}") from e

        file = BytesIO(request.content)

        # The toetsingskader questions are on the 1st sheet (first index is 0) of the Excel file, so we
        # only need to load the 1st sheet.
        df = pd.read_excel(file, sheet_name=1)
    else:
        logging.info(f"loading toetsingskader with path {path}")

        # The toetsingskader questions are on the 1st sheet (first index is 0) of the Excel file, so we
        # only need to load the 1st sheet.
        df = pd.read_excel(path, sheet_name=1)

    # Use the first row as column names, and then drop the first row.
    headers = df.iloc[0]
    df = pd.DataFrame(df.values[1:], columns=headers)
    df = df[df["Onderzoeksvraag"].notnull()]

    return df


def load_algoritmeregister(path: Path | None) -> pd.DataFrame:
    if path is None:
        logging.info(f"loading algoritmeregister from source with url {Resources.Algoritmeregister}")
        try:
            request = requests.get(Resources.Algoritmeregister)
            request.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"request error: {e}")
            raise SystemExit(f"Unable to get toetsingskader from {Resources.Algoritmeregister}") from e

        file = BytesIO(request.content)
        df = pd.read_csv(file, skipinitialspace=True)
    else:
        logging.info(f"splitting algoritmeregister with path {path}")
        df = pd.read_csv(path, skipinitialspace=True)

    return df


class Action(StrEnum):
    ConvertToetsingskader = "convert_toetsingskader"
    SplitAlgoritmeregister = "split_algoritmeregister"


def main() -> int:
    """
    Peforms ConvertToetsingskader or SplitAlgoritmeregister. If a path
    is provided use the resource given in the path. If a path is not provided get the
    resource from a remote URL specified in the Resources enum.
    """

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s [%(name)s:%(lineno)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("--action", type=Action, choices=list(Action), required=True)
    parser.add_argument("--path", type=Path, help="Input file", required=False)
    args = parser.parse_args()
    logging.info(f"conversion utils started with args: {args}")

    if args.path is not None and args.path.is_dir():
        raise ValueError(f"{args.path} is a directory, not a file")

    match args.action:
        case Action.ConvertToetsingskader:
            df = load_toetsingskader(args.path)
            convert_toetsingskader_to_csv(df)
            logging.info("successfully converted toetsingskader to csv.")
        case Action.SplitAlgoritmeregister:
            df = load_algoritmeregister(args.path)
            split_algoritmeregister(df)
            logging.info("successfully splitted algoritmeregister to csv.")
        case _:
            raise ValueError(f"{args.action} is an invalid action")

    return 0


if __name__ == "__main__":
    main()
