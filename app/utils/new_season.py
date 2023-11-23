import os
import sys
import json
from contextlib import contextmanager

sys.path.append(os.path.dirname(os.path.dirname(sys.path[0])))


from app.database import get_db
from app.models import Team, LastRow, Season


def set_last_row():
    with contextmanager(get_db)() as db:
        last_row = db.query(LastRow).filter(LastRow.id == 1).first()
        last_row.last_row = -1
        db.commit()


def set_new_season():
    with open("app/utils/new_season.json") as json_file:
        new_season = json.load(json_file)

    season = new_season["season"]
    set_season(season)

    new_teams = new_season["new_teams"]
    if new_teams:
        team_list = []
        for team in new_teams:
            team_obj = Team(**team)
            team_obj.current_team = True
            team_list.append(team_obj)

    with contextmanager(get_db)() as db:
        db.add_all(team_list)
        db.commit()

    promoted_teams = new_season["promotion"]
    for team in promoted_teams:
        with contextmanager(get_db)() as db:
            team = db.query(Team).filter(Team.name == team).first()
            team.current_team = True
            db.commit()

    relegated_teams = new_season["relegation"]
    for team in relegated_teams:
        with contextmanager(get_db)() as db:
            team = db.query(Team).filter(Team.name == team).first()
            team.current_team = False
            db.commit()


def set_season(new_season):
    with contextmanager(get_db)() as db:
        season = db.query(Season).filter(Season.id == 1).first()
        season.season = new_season
        db.commit()


def main():
    set_last_row()
    set_new_season()


if __name__ == "__main__":
    main()
