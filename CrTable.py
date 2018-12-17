import psycopg2

connection = psycopg2.connect(user = "postgres",
                                  password = "haslo",
                                  database = "postgres")
cursor = connection.cursor()
sql="""CREATE TABLE otodom
    (
        "Tytul" text,
        "Dzielnica" text,
        "Liczba pokoi" text,
        "Metraz" text,
        "Cena za metr" text,
        "Cena" text,
        PRIMARY KEY ("Tytul")
    )"""
cursor.execute(sql)

connection.commit()
connection.close()
cursor.close()