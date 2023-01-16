# %%
import os
import sys
import csv
import yaml
from argparse import ArgumentParser

from match import Match

# %%


def parse_args():
    parser = ArgumentParser(prog="Sportchemy Match Importer",
                            description="Import matches from CSV file.")
    parser.add_argument("--csv", type=str, help="CSV file path.")
    parser.add_argument(
        "-d", "--dst", default="content/match/", help="Folder to save imported matches ['content/match/'].")
    parser.add_argument("--season", default=None,
                        help="Season for the matches in the CSV.")
    parser.add_argument("--league", default=None,
                        help="League for the matches in the CSV.")

    args = parser.parse_args()
    return vars(args)

# %%


def main(args):
    matches = []
    with open(args["csv"], "r") as f:
        header = next(f).rstrip().split(",")
        data = csv.DictReader(f, fieldnames=header, delimiter=",", quotechar='"',
                              skipinitialspace=True)
        for row in data:
            matches.append(Match.from_csv(
                row, season=args["season"], league=args["league"]))

    os.makedirs(args["dst"], exist_ok=True)

    for match in matches:
        match.save(folder=args["dst"])


# %%


if __name__ == "__main__":
    args = parse_args()
    sys.exit(main(args))
