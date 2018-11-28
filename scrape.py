from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd

source = requests.get('https://www.otodom.pl/sprzedaz/mieszkanie/krakow/')

soup = BeautifulSoup(source.text, 'html.parser')

csv_file = open('cms_scrape.csv', 'w', encoding='utf-8', errors = 'ignore')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['nazwa', 'podpis', 'pokoj', 'metry', 'cena_metr', 'cena'])

for mieszkanie in soup.find_all('div', class_='offer-item-details'):

    nazwa = mieszkanie.find('span', class_='offer-item-title').text
    podpis = mieszkanie.find('p', class_='text-nowrap hidden-xs').text
    pokoj = mieszkanie.find('li', class_='offer-item-rooms hidden-xs').text
    metry = mieszkanie.find('li', class_='hidden-xs offer-item-area').text
    cena_metr = mieszkanie.find('li', class_='hidden-xs offer-item-price-per-m').text
    cena = mieszkanie.find('li', class_='offer-item-price').text.replace(' ','').replace('\n','')

    csv_writer.writerow([nazwa, podpis, pokoj, metry, cena_metr, cena])

    data = [[nazwa, podpis, pokoj, metry, cena_metr, cena]]
    df = pd.DataFrame(data, columns=['Nazwa', 'Podpis', 'Pokoj', 'Metry', 'Cena za metr', 'Cena'])
    print(df)

csv_file.close()

from flask import Flask, render_template
    
app = Flask(__name__)

@app.route('/')
def homepage():

    return render_template("index.html", data=df)

if __name__ == "__main__":
    app.run()

    csv_writer.writerow([nazwa, podpis, pokoj])
csv_file.close()