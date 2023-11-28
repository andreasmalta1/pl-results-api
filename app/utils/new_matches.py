import os
import sys
import pandas as pd
from contextlib import contextmanager

sys.path.append(os.path.dirname(os.path.dirname(sys.path[0])))

from app.database import get_db
from app.models import Team, Match, LastRow, Season


def get_last_row():
    with contextmanager(get_db)() as db:
        last_row = db.query(LastRow).first().last_row
    return last_row


def set_last_row(last_row):
    with contextmanager(get_db)() as db:
        last_row_obj = db.query(LastRow).filter(LastRow.id == 1).first()
        last_row_obj.last_row = last_row
        db.commit()


def get_season():
    with contextmanager(get_db)() as db:
        season = db.query(Season).first().season
    return season


def get_current_results(last_row, season):
    html = pd.read_html(os.getenv("PL_CURRENT_SEASON_URL"), header=0)
    df = (
        html[0][["Date", "Home", "Score", "Away"]]
        .dropna()
        .reset_index()
        .iloc[last_row + 1 :, :]
    )

    list_matches = []

    for index, row in df.iterrows():
        last_row += 1

        score = row["Score"].split("–")
        home_score = int(score[0])
        away_score = int(score[1])
        home_name = (
            row["Home"]
            .replace("Utd", "United")
            .replace("Nott'", "Notting")
            .replace("Wolves", "Wolverhampton")
        )
        away_name = (
            row["Away"]
            .replace("Utd", "United")
            .replace("Nott'", "Notting")
            .replace("Wolves", "Wolverhampton")
        )

        with contextmanager(get_db)() as db:
            home_team = (
                db.query(Team).filter(Team.name.like("%" + home_name + "%")).first()
            )

            away_team = (
                db.query(Team).filter(Team.name.like("%" + away_name + "%")).first()
            )

        match_dict = {
            "home_id": home_team.id,
            "home_score": home_score,
            "away_id": away_team.id,
            "away_score": away_score,
            "match_date": row["Date"],
            "season": season,
        }
        match_obj = Match(**match_dict)
        list_matches.append(match_obj)

    if list_matches:
        with contextmanager(get_db)() as db:
            db.add_all(list_matches)
            db.commit()

    set_last_row(last_row)


def main():
    last_row = get_last_row()
    season = get_season()
    get_current_results(last_row, season)


if __name__ == "__main__":
    main()
