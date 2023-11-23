import os
import pandas as pd
from contextlib import contextmanager

from database import get_db
from models import Team, Match, LastRow, Season


def get_last_row():
    with contextmanager(get_db)() as db:
        last_row = db.query(LastRow).first().last_row
    return last_row


def set_last_row(last_row):
    last_row_dict = {"last_row": last_row}
    with contextmanager(get_db)() as db:
        row_query = db.query(LastRow).filter(LastRow.id == 1)
        row_query.update(last_row_dict, synchronize_session=False)
        db.commit()


def get_season():
    with contextmanager(get_db)() as db:
        season = db.query(Season).first().season
    return season


def get_teams():
    list_teams = []
    with contextmanager(get_db)() as db:
        teams = db.query(Team).all()
        for team in teams:
            list_teams.append({"id": team.id, "name": team.alternative_name})
    return list_teams


def get_current_results(last_row, season, teams):
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
        match_dict = {}

        score = row["Score"].split("–")
        home_score = int(score[0])
        away_score = int(score[1])
        home_team = next(team for team in teams if team["name"] == row["Home"])
        home_id = home_team["id"]
        away_team = next(team for team in teams if team["name"] == row["Away"])
        away_id = away_team["id"]

        match_dict["home_id"] = home_id
        match_dict["home_score"] = home_score
        match_dict["away_id"] = away_id
        match_dict["away_score"] = away_score
        match_dict["match_date"] = row["Date"]
        match_dict["season"] = season
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
    teams = get_teams()
    get_current_results(last_row, season, teams)


if __name__ == "__main__":
    main()
