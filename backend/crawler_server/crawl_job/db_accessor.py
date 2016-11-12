import os
import psycopg2


table_name = "pokemon_map"

def add_pokemon_to_db(encounter_id, expire, pokemon_id, latitude, longitude):
    # open connection
    conn = psycopg2.connect(host=os.environ['DB_HOST'],
                            port=os.environ['DB_PORT'],
                            user=os.environ['DB_USER'],
                            password=os.environ['DB_PASSWORD'],
                            database=os.environ['DB_NAME'])

    # execute sql
    with conn.cursor() as cur:
        cur.execute("INSERT INTO %s (encounter_id, expire, pokemon_id, latitude, longitude) " % (table_name,) + 
                    "VALUES (%s, %s, %s, %s, %s) " + 
                    "ON CONFLICT (encounter_id) DO NOTHING", (encounter_id, expire, pokemon_id, latitude, longitude))

    # connection commit
    conn.commit()

    return

