from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd

source = requests.get('https://www.otodom.pl/sprzedaz/mieszkanie/krakow/').text

soup = BeautifulSoup(source, 'lxml')

csv_file = open('cms_scrape.csv', 'w', encoding='utf-8', errors = 'ignore')  # zapis

csv_writer = csv.writer(csv_file)
csv_writer.writerow(['nazwa', 'podpis', 'pokoj', 'metry', 'cena_metr', 'cena'])

nazwy=[]
dzielnice=[]
pokoje=[]
metryy=[]
cena_metryy=[]
ceny=[]

for mieszkanie in soup.find_all(class_='offer-item-details'):

    nazwa = mieszkanie.find('span', class_='offer-item-title').text
    nazwy.append(nazwa)

    podpis = mieszkanie.find('p', class_='text-nowrap hidden-xs').text
    dzielnica = podpis.split(':')[1]
    dzielnice.append(dzielnica)

    pokoj = mieszkanie.find('li', class_='offer-item-rooms hidden-xs').text
    pokoje.append(pokoj)

    metry = mieszkanie.find('li', class_='hidden-xs offer-item-area').text
    metryy.append(metry)

    cena_metr = mieszkanie.find('li', class_='hidden-xs offer-item-price-per-m').text
    cena_metryy.append(cena_metr)

    cena = mieszkanie.find('li', class_='offer-item-price').text.replace(' ','').replace('\n','')
    ceny.append(cena)

    csv_writer.writerow([nazwa, dzielnica, pokoj, metry, cena_metr, cena])



#data = [[nazwa, dzielnica, pokoj, metry, cena_metr, cena]]
#df = pd.DataFrame(data,columns=['Nazwa','Dzielnica', 'Pokoj', 'Metry', 'Cena za metr', 'Cena'])
    
df = pd.DataFrame({'Nazwa':nazwy,'Dzielnica':dzielnice, 'Pokoje':pokoje, 'Metry':metryy, 'Cena za metr':cena_metryy, 'Cena':ceny})


csv_file.close()



print(df)


from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def homepage():
        return render_template("wynik.html", data=df)

if __name__ == "__main__":
    app.run()

# pandas dataframe 