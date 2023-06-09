from fastapi import FastAPI, Response
from scrapping import database, update_year
import datetime
from fastapi_utils.tasks import repeat_every

app = FastAPI()


@app.on_event("startup")
@repeat_every(seconds=3600, wait_first=True)
def pull_new_data():
    update_year(datetime.date.today().year, database)


@app.get("/")
def welcome():
    return {"Welcome": "Bienvenido a UF-API", "Author": "Duvan García", "How to use?": "Haz una petición como esta /uf?date=20230207"}


@app.get("/uf", status_code=200)
def get_uf_value(date: str, response: Response):

    try:
        parsed_date = datetime.datetime.strptime(date, '%Y%m%d')

        year = parsed_date.year
        month = parsed_date.month
        day = parsed_date.day

        value = database[year][day-1][month-1]

        return {"index": "UF", "date": parsed_date.strftime("%Y-%m-%d"), "value": value}

    except ValueError:
        response.status_code = 400
        return {"error": "Bad input"}

    except KeyError:
        response.status_code = 406
        return {"error": "The data for the requested year is not available"}
