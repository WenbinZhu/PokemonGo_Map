import os
import time
import psycopg2


table_name = "pokemon_map"


def get_pokemons_from_db(north, south, west, east):
    # open connection
    conn = psycopg2.connect(host=os.environ['DB_HOST'],
                            port=os.environ['DB_PORT'],
                            user=os.environ['DB_USER'],
                            password=os.environ['DB_PASSWORD'],
                            database=os.environ['DB_NAME'])

    # execute sql
    with conn.cursor() as cur:
        cur.execute("SELECT expire, pokemon_id, latitude, longitude FROM %s " % (table_name,) + 
                    "WHERE expire >= %s " + 
                    "AND latitude > %s " +
                    "AND latitude < %s " +
                    "AND longitude > %s " + 
                    "AND longitude < %s " +
                    "LIMIT 100",
                    (time.time() * 1000, south, north, west, east))

        rows = cur.fetchall()
    
    result = []
    for row in rows:
        result.append({
                          "expire": row[0],
                          "pokemon_id": row[1],
                          "latitude": row[2],
                          "longitude": row[3]
                     })
       
    # connection commit
    # conn.commit()

    return result

