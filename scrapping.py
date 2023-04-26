import requests
from bs4 import BeautifulSoup
from datetime import date


class HTMLTable:
    def __init__(self, url, table_id):
        self.url = url
        self.table_id = table_id

    def scraping(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, 'lxml')
        rows = soup.find(id=self.table_id).find_all('tr')

        data = []
        for row in rows[1:]:
            new_row = []
            for cell in row.find_all('td'):
                str_value = cell.string.replace(".", "").replace(",", ".")
                try:
                    new_row.append(float(str_value))
                except:
                    new_row.append(None)
            data.append(new_row)

        return data


database = {}


def update_year(year, database):
    url = f"https://www.sii.cl/valores_y_fechas/uf/uf{year}.htm"
    table = HTMLTable(url, "table_export")
    data = table.scraping()
    database[year] = data


for year in range(2013, date.today().year + 1):
    update_year(year, database)
