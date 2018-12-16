from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
from flask import Flask, render_template, Response, request, redirect, url_for

    
app = Flask(__name__)

@app.route('/ceny/', methods=['GET', 'POST'])
def getvalue():
    if request.method == 'POST':
        if request.form['submit_button'] == 'etl':
            cena_p = request.form['od']
            cena_k = request.form['do']

            csv_file = open('cms_scrape.csv', 'w', encoding='utf-8', errors = 'ignore')
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['nazwa', 'dzielnica', 'pokoj', 'metry', 'cena_metr', 'cena'])

            nazwy=[]
            dzielnice=[]
            pokoje=[]
            metryy=[]
            cena_metryy=[]
            ceny=[]


            for i in range(1, 10):
                page = "https://www.otodom.pl/sprzedaz/mieszkanie/krakow/?search%5Bfilter_float_price%3Afrom%5D="+ cena_p +"&search%5Bfilter_float_price%3Ato%5D="+ cena_k +"&page={}".format(i)
                html = requests.get(page)
                soup = BeautifulSoup(html.text, 'lxml')
                
                for mieszkanie in soup.find_all('div', class_='offer-item-details'):
                    cenka = mieszkanie.find('li', class_='offer-item-price')

                    
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
                

                df = pd.DataFrame({'Nazwa':nazwy, 'Dzielnica':dzielnice, 'Pokoj':pokoje, 'Metry':metryy, 'Cena za metr':cena_metryy, 'Cena':ceny})
            
            csv_file.close()

            return render_template('wynik.html', c1=cena_p, c2=cena_k, data=df)

        if request.form['submit_button'] == 'extract':    #TYLKO WYKONANIE TRANSFORM
            cena_p = request.form['od']
            cena_k = request.form['do']

            csv_file = open('cms_scrape.csv', 'w', encoding='utf-8', errors = 'ignore')
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['nazwa', 'dzielnica', 'pokoj', 'metry', 'cena_metr', 'cena'])

            nazwy=[]
            dzielnice=[]
            pokoje=[]
            metryy=[]
            cena_metryy=[]
            ceny=[]


            for i in range(1, 10):
                page = "https://www.otodom.pl/sprzedaz/mieszkanie/krakow/?search%5Bfilter_float_price%3Afrom%5D="+ cena_p +"&search%5Bfilter_float_price%3Ato%5D="+ cena_k +"&page={}".format(i)
                html = requests.get(page)
                soup = BeautifulSoup(html.text, 'lxml')
                
                for mieszkanie in soup.find_all('div', class_='offer-item-details'):

                    nazwa = mieszkanie.find('span', class_='offer-item-title')
                    nazwy.append(nazwa)

                    podpis = mieszkanie.find('p', class_='text-nowrap hidden-xs')
                    dzielnice.append(podpis)

                    pokoj = mieszkanie.find('li', class_='offer-item-rooms hidden-xs')
                    pokoje.append(pokoj)

                    metry = mieszkanie.find('li', class_='hidden-xs offer-item-area')
                    metryy.append(metry)

                    cena_metr = mieszkanie.find('li', class_='hidden-xs offer-item-price-per-m')
                    cena_metryy.append(cena_metr)

                    cena = mieszkanie.find('li', class_='offer-item-price')
                    ceny.append(cena)

                    #print(nazwa, podpis, pokoj, metry, cena_metr, cena)

                    df = (nazwy, dzielnice, pokoje, metryy, cena_metryy, ceny)

            return render_template('extract.html', data=df)
        
        if request.form['submit_button'] == 'transform':

            return render_template('transform.html')


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()



