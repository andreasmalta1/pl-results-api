import os
import sys
import csv
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from contextlib import contextmanager

sys.path.append(os.path.dirname(os.path.dirname(sys.path[0])))

from app.database import get_db
from app.models import Team, Match, LastRow, Season, Nation, Manager, Stints
import new_matches

CARETAKER_MANAGER = "‡"
INCUMBENT_MANAGER = "†"


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


def get_pl_managers():
    source = requests.get(os.getenv("PL_MANAGERS_URL")).text
    page = BeautifulSoup(source, "lxml")
    table = page.find("table", class_="sortable")
    body = table.find("tbody")
    rows = body.find_all("tr")[1:]

    list_stints = []

    for row in rows:
        name = row.find("th").get_text().strip()
        if CARETAKER_MANAGER in name:
            continue

        name = name.replace(INCUMBENT_MANAGER, "")
        cells = row.find_all("td")

        country = cells[0].find("a").find("img")["alt"]
        with contextmanager(get_db)() as db:
            country_obj = db.query(Nation).filter(Nation.name == country).first()

        if not country_obj:
            country_dict = {"name": country}
            country_obj = Nation(**country_dict)

            with contextmanager(get_db)() as db:
                db.add(country_obj)
                db.commit()
                country_id = country_obj.id
        else:
            country_id = country_obj.id

        with contextmanager(get_db)() as db:
            manager_obj = db.query(Manager).filter(Manager.name == name).first()

        if not manager_obj:
            manager_dict = {"name": name, "nation_id": country_id}
            manager_obj = Manager(**manager_dict)

            with contextmanager(get_db)() as db:
                db.add(manager_obj)
                db.commit()
                manager_id = manager_obj.id

        else:
            manager_id = manager_obj.id

        team_name = cells[1].get_text().strip()

        with contextmanager(get_db)() as db:
            team_obj = (
                db.query(Team).filter(Team.name.like("%" + team_name + "%")).first()
            )

        date_start = cells[2].find("span").get_text().strip()
        date_start = datetime.strptime(date_start, "%d %B %Y")
        date_end = cells[3].get_text().strip()
        if "Present" not in date_end:
            current = False
            date_end = datetime.strptime(date_end, "%d %B %Y")
        else:
            current = True
            date_end = None

        stint_dict = {
            "manager_id": manager_id,
            "team_id": team_obj.id,
            "date_start": date_start,
            "date_end": date_end,
            "current": current,
        }
        stint_obj = Stints(**stint_dict)
        list_stints.append(stint_obj)

    if list_stints:
        with contextmanager(get_db)() as db:
            db.add_all(list_stints)
            db.commit()


def main():
    set_details()
    create_teams()
    get_pl_matches()
    new_matches.main()
    get_pl_managers()


if __name__ == "__main__":
    main()
