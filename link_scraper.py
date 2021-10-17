import json, psycopg2, datetime, secret

# This file is used to add a new chain to bb db

BB_ID = "36"
NAME = "Market of Choice"
SCRAPER = "market_of_choice"
with open('chains.json', 'r') as f:
    data = json.load(f)

def rewind_time():
    return datetime.datetime(2002, 4, 9).strftime('%Y-%m-%d %H:%M:%S')

if BB_ID == '':
    # Empty id means it's a new chains
    conn = psycopg2.connect(host=secret.DB_HOST, database=secret.DB_NAME, user=secret.DB_USER, password=secret.DB_PASS)
    cur = conn.cursor()
    bb_name = NAME.replace("'", "''")

    sql_command = ""
    sql_command += f"INSERT INTO chains (name, created_at, updated_at)"
    sql_command += f" VALUES ( '{bb_name}', now(), '{rewind_time()}' )"
    cur.execute(sql_command)
    conn.commit()

    cur.execute(f"SELECT id FROM chains WHERE name='{bb_name}'")
    BB_ID = str(cur.fetchone()[0])

    conn.close()

data[BB_ID] = {'name': NAME, 'scraper': SCRAPER}

with open('chains.json', 'w') as f:
    json.dump(data, f, indent=2)
