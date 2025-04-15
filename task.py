import sqlite3

DATABASE = "./task.db"

conn = sqlite3.connect(DATABASE)
print(f"{DATABASE} created")


query_create = """
CREATE TABLE restaurants (
    id INT PRIMARY KEY,
    address VARCHAR(100) NOT NULL,
    number_of_Michelin_stars TINYINT UNSIGNED NOT NULL,
    rating TINYINT UNSIGNED NOT NULL,
    culinary_tradition_of_the_restaurant VARCHAR(100) NOT NULL
    );
"""

query_insert = """
INSERT INTO restaurants (id, address, number_of_Michelin_stars, rating, culinary_tradition_of_the_restaurant)
VALUES (1, 'Via Stella, 22, 41121 Modena MO, Італія', 3, '4,4', 'Італійська'),
(2, '9 Pl. des Vosges, 75004 Paris, Франція', 3, '4,1', 'Французька'),
(3, 'Carrer de Can Sunyer, 48, 17007 Girona, Іспанія', 3, '4,8', 'Іспанська')
"""

conn.execute(query_create)
conn.execute(query_insert)
conn.commit()

conn.close()
