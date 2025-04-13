import sqlite3

DATABASE = "./task.db"

conn = sqlite3.connect(DATABASE)
print(f"{DATABASE} created")


query_create = """
CREATE TABLE restaurant (
    id INT PRIMARY KEY,
    address VARCHAR(100) NOT NULL,
    number_of_Michelin_stars TINYINT UNSIGNED NOT NULL,
    rating TINYINT UNSIGNED NOT NULL,
    culinary_tradition_of_the_restaurant VARCHAR(100) NOT NULL
    );
"""

conn.execute(query_create)
conn.commit()

conn.close()
