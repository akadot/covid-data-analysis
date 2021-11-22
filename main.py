import requests as req
import datetime as dt
import csv
from PIL import Image
from IPython.display import display

# Creating Request
url = "https://api.covid19api.com/dayone/country/brazil"
res = req.get(url)
raw_data = res.json()

# Cleaning data and populating data array
data = []

for obs in raw_data:
    data.append([obs["Confirmed"], obs["Deaths"],
                obs["Recovered"], obs["Active"], obs["Date"]])

data.insert(0, ["Confirmados", "Óbitos", "Recuperados", "Ativos", "Data"])

# Constants
CONFIRMADOS = 0
OBITOS = 1
RECUPERADOS = 2
ATIVOS = 3
DATA = 4

# Removing timezones
for i in range(1, len(data)):
    data[i][DATA] = data[i][DATA][:10]

# Writing CSV file
with open("brasil-covid.csv", "w", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(data)

for i in range(1, len(data)):
    data[i][DATA] = dt.datetime.strptime(data[i][DATA], '%Y-%m-%d')


def getDatasets(y, labels):
    if type(y[0]) == list:
        datasets = []
        for i in range(len(y)):
            datasets.append({
                "label": labels[i],
                "data": y[i]
            })
        return datasets
    else:
        return [{
            "label": labels[0],
            "data":y
        }]


def setTitle(title=""):
    if title != "":
        display = "true"
    else:
        display = "false"
    return {
        "title": title,
        "display": display
    }


def createChart(x, y, labels, kind="bar", title=""):

    datasets = getDatasets(y, labels)
    options = setTitle(title)

    chart = {
        "type": kind,
        "data": {
            "labels": x,
            "datasets": datasets
        },
        "options": options
    }
    return chart


def getApiChart(chart):
    url_base = "https://quickchart.io/chart"
    res = req.get(f"{url_base}?c={str(chart)}")
    return res.content


def saveImage(path, content):
    with open(path, "wb") as image:
        image.write(content)


def displayImage(path):
    imgPil = Image.open(path)
    display(imgPil)


y_data_1 = []
for obs in data[1::10]:
    y_data_1.append(obs[CONFIRMADOS])

y_data_2 = []
for obs in data[1::10]:
    y_data_2.append(obs[RECUPERADOS])

labels = ["Confirmados", "Recuperados"]

x = []
for obs in data[1::10]:
    x.append(obs[DATA].strftime("%d/%m/%Y"))

chart = createChart(x, [y_data_1, y_data_2], labels,
                    title="Gráfico Confirmados x Recuperados")

chartContent = getApiChart(chart)

saveImage("firstGraph.png", chartContent)

displayImage("firstGraph.png")
