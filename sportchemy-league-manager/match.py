# %%

import os
from collections import defaultdict
from yaml import dump as ydump
from datetime import datetime

# %%

DATETIME_FORMAT = "%Y-%m-%d %H:%M"
HUGO_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# %%


class Match():
    def __init__(self, **kwargs) -> None:
        self.title = None
        self.summary = None
        self.date = None
        self.season = None
        self.league = None
        self.matchDay = None
        self.court = {
            "name": None,
            "address": None,
            "link": None,
            "lat": None,
            "long": None
        }
        self.home = {
            "name": None,
            "logo": None
        }
        self.away = {
            "name": None,
            "logo": None
        }
        self.score = {
            "home": None,
            "away": None
        }
        self.publishDate = datetime.now()
        self.tags = []
        self.featured = False

        for k, v in kwargs.items():
            if hasattr(self, k):
                if isinstance(getattr(self, k), dict):
                    getattr(self, k).update(v)
                else:
                    setattr(self, k, v)

    @classmethod
    def from_csv(cls, csv, **kwargs):
        records = defaultdict(dict)
        # construct match datetime form date and time columns if present
        try:
            date = f"{csv.pop('date')} {csv.pop('time')}"
            date = datetime.strptime(date, DATETIME_FORMAT)
            records["date"] = date
        except:
            pass
        # loop over other attributes in the csv:
        # home, away, court, score, ...
        for k, v in csv.items():
            if k in ["home", "away", "court"]:
                records[k].update({"name": v})
            elif k in ["address", "link"]:
                records["court"].update({k: v})
            elif k == "score":
                home, away = v.split("-")
                records[k].update({"home": home, "away": away})
            else:
                records[k] = v

        return cls(**records, **kwargs)

    def get_dict(self):
        return {
            "title": self.title,
            "summary": self.summary,
            "date": self.date if self.date is None else self.date.strftime(HUGO_DATETIME_FORMAT),
            "home": self.home,
            "away": self.away,
            "score": self.score,
            "season": self.season,
            "league": self.league,
            "matchDay": self.matchDay,
            "court": self.court,
            "publishDate": self.publishDate.strftime(HUGO_DATETIME_FORMAT),
            "tags": self.tags,
            "featured": self.featured
        }

    def save(self, fname=None, folder="", season_folder=True, league_folder=True):
        if fname is None:
            fname = f"{self.date.strftime(DATETIME_FORMAT)}_{self.home['name']}-{self.away['name']}.md"
        if season_folder and self.season is not None:
            folder = os.path.join(folder, self.season)
        if league_folder and self.league is not None:
            folder = os.path.join(folder, self.league)

        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

        fname = os.path.join(folder, fname)

        frontmatter = "---\n" + \
            ydump(self.get_dict(), indent=2, sort_keys=False) + "---\n"

        with open(fname, "w") as f:
            f.write(frontmatter)
