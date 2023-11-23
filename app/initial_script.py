import os
import csv
import requests
from bs4 import BeautifulSoup
from contextlib import contextmanager

from database import get_db
from models import Team, Match, LastRow, Season


def set_details():
    last_row_dict = {"last_row": -1}
    season_dict = {"season": "2023/2024"}

    last_row_obj = LastRow(**last_row_dict)
    season_obj = Season(**season_dict)
    with contextmanager(get_db)() as db:
        db.add(last_row_obj)
        db.add(season_obj)
        db.commit()


def create_teams():
    team_list = []
    with open("csvs/team_ids.csv") as teams:
        reader = csv.DictReader(teams)
        for team in reader:
            team["id"] = int(team["id"])
            if team["current_team"] == "true":
                team["current_team"] = True
            else:
                team["current_team"] = False
            team_obj = Team(**team)
            team_list.append(team_obj)

    with contextmanager(get_db)() as db:
        db.add_all(team_list)
        db.commit()


def get_pl_matches():
    """
    A utility to scrape PL matches information
    """
    list_matches = []
    list_teams = []
    with contextmanager(get_db)() as db:
        teams = db.query(Team).all()
        for team in teams:
            list_teams.append({"id": team.id, "name": team.name})

    num_rounds = 42
    start_year = int(os.getenv("START_YEAR"))

    for year in range(start_year, 2023):
        if year > 1994:
            num_rounds = 38

        for round in range(1, num_rounds + 1):
            link = f"{os.getenv('PL_MATCHES_URL')}{year}-{year+1}-spieltag/{round}"
            source = requests.get(link).text
            page = BeautifulSoup(source, "lxml")
            table = page.find("table", class_="standard_tabelle")
            rows = table.find_all("tr")

            date = None

            for row in rows:
                match_dict = {}
                cells = row.find_all("td")
                if cells[0].get_text():
                    date = cells[0].get_text()
                home_team = cells[2].get_text().strip()
                home_team = next(
                    team for team in list_teams if team["name"] == home_team
                )
                home_id = home_team["id"]

                away_team = cells[4].get_text().strip()
                away_team = next(
                    team for team in list_teams if team["name"] == away_team
                )
                away_id = away_team["id"]
                score = cells[-2].get_text().strip().split()[0].split(":")

                match_dict["home_id"] = home_id
                match_dict["home_score"] = score[0]
                match_dict["away_id"] = away_id
                match_dict["away_score"] = score[1]
                match_dict["match_date"] = date
                match_dict["season"] = f"{year}/{year+1}"
                match_obj = Match(**match_dict)
                list_matches.append(match_obj)

    with contextmanager(get_db)() as db:
        db.add_all(list_matches)
        db.commit()


def main():
    set_details()
    create_teams()
    get_pl_matches()


if __name__ == "__main__":
    main()
