import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from os import getenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from re import sub

page = requests.get("https://www.worldometers.info/coronavirus/")
soup = BeautifulSoup(page.content, "html.parser")


def update_data():
    print("Updating data...")
    global world
    global countries
    global continents

    data = get_data()
    countries = data[0]
    world = data[1]
    continents = data[2]


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(update_data, "interval", hours=3)
scheduler.start()


def to_int(num: str) -> int:
    return 0 if num.strip() == "" else int(sub(r"(\+|\,)", "", num))


def get_data():

    world = {}
    countries = []
    continents = {}

    table = soup.find("table", {"id": "main_table_countries_today"}).find("tbody")
    i = 0
    for col in table.find_all("tr"):
        result = col.find_all("td")

        if not col.has_attr("data-continent"):
            if i == 0:
                world["total_cases"] = to_int(result[2].get_text())
                world["new_cases"] = to_int(result[3].get_text())
                world["total_deaths"] = to_int(result[4].get_text())
                world["new_deaths"] = to_int(result[5].get_text())
                world["total_recovered"] = to_int(result[6].get_text())
                world["active_cases"] = to_int(result[8].get_text())
                world["critical_cases"] = to_int(result[9].get_text())

            else:
                temp = {
                    "country": result[1].get_text(),
                    "total_cases": to_int(result[2].get_text()),
                    "new_cases": to_int(result[3].get_text()),
                    "total_deaths": to_int(result[4].get_text()),
                    "new_deaths": to_int(result[5].get_text()),
                    "total_recovered": to_int(result[6].get_text()),
                    "active_cases": to_int(result[8].get_text()),
                    "critical_cases": to_int(result[9].get_text()),
                    "total_tests": to_int(result[12].get_text()),
                    "population": to_int(result[14].get_text()),
                    "continent": result[15].get_text(),
                }

                countries.append(temp)
            i += 1
        elif result[1].get_text().strip() != "":
            continent = {
                "continent": result[1].get_text().replace("\n", ""),
                "total_cases": to_int(result[2].get_text()),
                "new_cases": to_int(result[3].get_text()),
                "total_deaths": to_int(result[4].get_text()),
                "new_deaths": to_int(result[5].get_text()),
                "total_recovered": to_int(result[6].get_text()),
                "active_cases": to_int(result[8].get_text()),
                "critical_cases": to_int(result[9].get_text()),
            }

            continents[continent["continent"].lower().replace(" ", "_")] = continent

    return [countries, world, continents]


app = Flask(__name__)

limiter = Limiter(app, key_func=get_remote_address, default_limits=["120 per minutes"])


@app.route("/countries")
def get_countries():
    return jsonify(countries)


@app.route("/world")
def get_world_stat():
    return jsonify(world)


@app.route("/countries/<country>")
def get_country(country: str):
    return jsonify(
        next(
            (
                x
                for x in countries
                if x["country"].lower() == sub(r"(-|_)", " ", country.lower()).strip()
            ),
            {"error": "Not Found"},
        )
    )


@app.route("/continents")
def get_continents():
    return jsonify(continents)


@app.route("/continents/<continent>")
def get_continent(continent):
    ccontinent = sub(r"(\s|-)", "_", continent.lower())
    return (
        jsonify(continents[ccontinent])
        if ccontinent in continents
        else {"error": "Not Found"}
    )


@app.route("/")
@limiter.exempt
def home():
    return render_template("index.html")


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"})


if __name__ == "__main__":
    data = get_data()
    countries = data[0]
    world = data[1]
    continents = data[2]
    app.run(port=getenv("PORT") or 8000, debug=False)
