from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd

source = requests.get('https://www.otodom.pl/sprzedaz/mieszkanie/krakow/')

soup = BeautifulSoup(source.text, 'html.parser')


csv_file = open('cms_scrape.csv', 'w', encoding='utf-8', errors = 'ignore')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['nazwa', 'podpis', 'pokoj', 'metry', 'cena_metr', 'cena'])

nazwy=[]
podpisy=[]
pokoje=[]
metryy=[]
cena_metryy=[]
ceny=[]

for i in range(1, 10):
    page = "https://www.otodom.pl/sprzedaz/mieszkanie/krakow/?page={}".format(i)
    html = requests.get(page)
    soup = BeautifulSoup(html.text, 'lxml')
    
    for mieszkanie in soup.find_all('div', class_='offer-item-details'):

        nazwa = mieszkanie.find('span', class_='offer-item-title').text
        nazwy.append(nazwa)

        podpis = mieszkanie.find('p', class_='text-nowrap hidden-xs').text
        podpisy.append(podpis)

        pokoj = mieszkanie.find('li', class_='offer-item-rooms hidden-xs').text
        pokoje.append(pokoj)

        metry = mieszkanie.find('li', class_='hidden-xs offer-item-area').text
        metryy.append(metry)

        cena_metr = mieszkanie.find('li', class_='hidden-xs offer-item-price-per-m').text
        cena_metryy.append(cena_metr)

        cena = mieszkanie.find('li', class_='offer-item-price').text.replace(' ','').replace('\n','')
        ceny.append(cena)


        csv_writer.writerow([nazwa, podpis, pokoj, metry, cena_metr, cena])

        #data = [[nazwa, podpis, pokoj, metry, cena_metr, cena]]
        #df = pd.DataFrame(data, columns=['Nazwa', 'Podpis', 'Pokoj', 'Metry', 'Cena za metr', 'Cena'])

df = pd.DataFrame({'Nazwa':nazwy, 'Podpis':podpisy, 'Pokoj':pokoje, 'Metry':metryy, 'Cena za metr':cena_metryy, 'Cena':ceny})
    
csv_file.close()

print(df)

from flask import Flask, render_template
    
app = Flask(__name__)

@app.route('/')
def homepage():

    return render_template("index.html", data=df)

if __name__ == "__main__":
    app.run()

    csv_writer.writerow([nazwa, podpis, pokoj])
csv_file.close()