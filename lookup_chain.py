import psycopg2, sys, secret

conn = psycopg2.connect(host=secret.DB_HOST, database=secret.DB_NAME, user=secret.DB_USER, password=secret.DB_PASS)
cur = conn.cursor()

name = ''
args = sys.argv
if len(args) > 1:
    name = sys.argv[-1]

print('searching', name)
sql_command = f"SELECT name, id FROM chains WHERE name ILIKE '%{name}%'"
cur.execute(sql_command)
result = cur.fetchall()
[print(r[1], r[0]) for r in result]
conn.close()
