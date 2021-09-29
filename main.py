import importlib, psycopg2, requests, json, time, sys, datetime, traceback, secret
import pdb

# Geocodio can handle 1000 addresses reliably
ADDRESS_LIM = 1000

# Amount of days until a chain will be updated
UPDATE_THRESH = 30

# Time of executing script
NOW = datetime.datetime.now()

# API Info
API_KEY = f'api_key={secret.GEO_KEY}'
BASE_URL = 'https://api.geocod.io/v1.6/'
API_URL = f'{BASE_URL}geocode?{API_KEY}'

# Open connection to the database
conn = psycopg2.connect(host=secret.DB_HOST, database=secret.DB_NAME, user=secret.DB_USER, password=secret.DB_PASSWORD)
cur = conn.cursor()

# Get info on previous api calls
#! IMPORTANT global variable
with open('api_calls.json', 'r') as f:
    api_calls = json.load(f)


# Returns all chain objects
def get_chains(cur):
    cur.execute("SELECT * FROM chains")
    return cur.fetchall()

# Does the chain need to be updated?
def needs_update(chain):
    updated_at = chain[3]
    days_old = (NOW - updated_at).days
    if days_old >= UPDATE_THRESH:
        return True
    else:
        return False

# Returns ID's of chains needing an update
def get_updatable_ids(chains):
    result = []
    for chain in chains:
        if needs_update(chain):
            result.append(chain[0])
    return result

# Returns amount of calls available
# 2500 available max
def calculate_remaining_calls():
    api_data = api_calls['geocodio']
    time_passed = time.time() - api_data['time']
    days_passed = time_passed / 86400
    remaining_calls = 2500 - api_data['count']
    if days_passed < 1:
        return remaining_calls
    else:
        api_calls['geocodio']['count'] = 0
        return 2500

# Are all locations geocoded?
def is_geocoded(chain_id):
    chain = api_calls['queue'][chain_id]
    if len(chain) == 0:
        return False
    last_entry = chain[-1]
    return 'lat' in last_entry

# Updates a store row in the database
def update_store(store, chain_id):
    sql_command = ""
    sql_command += f"UPDATE STORES SET"
    sql_command += f" address='{store['address']}'"
    sql_command += f", phone='{store['phone']}'"
    sql_command += f", lat='{store['lat']}'"
    sql_command += f", lng='{store['lng']}'"
    sql_command += f", updated_at=now()"
    sql_command += f" WHERE remote_id='{store['id']}'"
    sql_command += f" AND chain_id='{chain_id}'"
    cur.execute(sql_command)
    return

# Adds a new store row to the database
def add_store(store, chain_id):
    sql_command = ""
    sql_command += f"INSERT INTO stores"
    sql_command += f" (chain_id, address, phone, remote_id"
    sql_command += f", lat, lng"
    sql_command += f", created_at, updated_at, checked_at)"
    sql_command += f" VALUES ({chain_id}, '{store['address']}', '{store['phone']}', '{store['id']}'"
    sql_command += f", '{store['lat']}', '{store['lng']}'"
    sql_command += f", now(), now(), now() )"
    cur.execute(sql_command)
    return

# Removes a store row from the database
def remove_store(store_id, chain_id):
    sql_command = ""
    sql_command += f"DELETE FROM stores"
    sql_command += f" WHERE chain_id ='{chain_id}'"
    sql_command += f" AND id='{store_id}'"
    cur.execute(sql_command)
    return

# Can we make more API calls?
def is_calling(call_count, call_length, chain_count, chain_pos):
    if call_count <= call_length:
        # Not enough calls left this 24 hour period
        return False
    elif call_length >= ADDRESS_LIM:
        # Limit to 1000 addresses a time
        return False
    elif chain_count <= chain_pos:
        # Reached the end
        return False
    return True

# returns [address]
# correct amount of addresses to geocode
def get_non_geocoded_addresses(call_count, chain_ids):
    result = []
    addr_ndx = 0
    chain_ndx = 0
    while is_calling(call_count, len(result), len(chain_ids), chain_ndx):
        stores = api_calls['queue'][chain_ids[chain_ndx]]
        if len(stores) == 0:
            print(f'{chain_ids[chain_ndx]} returned 0 stores')
            chain_ndx += 1
            continue
        store = stores[addr_ndx]
        if 'lat' not in store:
            result.append(store['address'])

        if addr_ndx == len(stores) - 1:
            # Start getting addresses for next chain
            chain_ndx += 1
            addr_ndx = 0
        else:
            # Get next address
            addr_ndx += 1

    return result

# Updates api_calls.json with data from api call
def save_geocode_data(api_response, chain_ids):
    print('Geocoding Chains')
    api_calls['geocodio']['time'] = time.time()
    api_calls['geocodio']['count'] += len(api_response)
    write_api_calls() # Save time and count incase error

    chain_ndx = 0 # index of api_calls['queue']
    store_ndx = 0 # index of api_calls['queue'][chain_ndx]
    addr_ndx  = 0 # index of non geocoded address
    chain_count = len(chain_ids)

    for response in api_response:
        # Get next lat/long
        try:
            coords = response['response']['results'][0]['location']
        except IndexError:
            coords = {'lat': None, 'lng': None}

        # stores = list(api_calls['queue'][chain_ids[chain_ndx]])
        # store_count = len(stores)
        while chain_ndx < chain_count:

            stores = list(api_calls['queue'][chain_ids[chain_ndx]])
            store_count = len(stores)

            if store_ndx == store_count:
                store_ndx = 0
                chain_ndx += 1
            elif 'lat' not in stores[store_ndx]:
                stores[store_ndx].update(coords)
                store_ndx += 1
            else:
                store_ndx += 1
    print()
    write_api_calls() # Write lat and lng
    return

# Returns response from api call
# Updates time and count values in api_calls.json
def make_api_call(addresses):
    api_calls['geocodio']['count'] += len(addresses)
    api_calls['geocodio']['time'] = time.time()
    return requests.post(API_URL, json=addresses).json()['results']


# Execute locations in the queue
def geocode_queue():
    call_count = calculate_remaining_calls()
    chain_ids = list(api_calls['queue'].keys()) # chains in queue
    not_geocoded = get_non_geocoded_addresses(call_count, chain_ids)
    print(f'{len(not_geocoded)} stores to geocode')
    if len(not_geocoded) == 0:
        # Empty geocode queue
        return
    response = make_api_call(not_geocoded)
    save_geocode_data(response, chain_ids)
    return

# Scrape stores that havent in over THRESHOLD
def add_to_queue():
    with open('chains.json', 'r') as f:
        scrapers = json.load(f)
    chains = get_chains(cur)
    update_ids = [str(v) for v in get_updatable_ids(chains)] # cast to string
    print(f'{len(update_ids)} chains outdated')
    scraper_ids = list(scrapers.keys())
    for iden in update_ids:
        if iden not in scraper_ids:
            print(f'Scraper not found for chain#{iden}')
            continue
        elif iden in list(api_calls['queue'].keys()):
            # Already queue'd
            continue

        try:
            # Import and execute scraper
            scraper_name = scrapers[iden]['scraper']
            exec(f'import scrapers.{scraper_name}_scraper as chain', globals())
            scraper = chain.execute()
            print(f'{scraper.name} located {len(scraper.stores)} stores')
        except Exception as e:
            print(f'scraper {scraper_name} failed', e)
            traceback.print_exc()
            continue

        # Save in api_calls.json
        try:
            if len(scraper.stores) > 0:
                api_calls['queue'][iden] = scraper.stores
                write_api_calls()
        except Exception as e:
            print(f'scraper#{iden}:{scraper.name} failed', e)

    return


# Send new data to Database
def clear_queue():
    print('Uploading to database')
    chain_ids = list(api_calls['queue'].keys())
    for chain_id in chain_ids:
        if not is_geocoded(chain_id):
            # Out of geocoded chains
            break
        print('Uploading', chain_id)
        stores = api_calls['queue'][chain_id]


        # Find current remote ids
        cur.execute(f"SELECT remote_id FROM stores WHERE chain_id='{chain_id}'")
        known_ids = [r[0] for r in cur.fetchall()]

        # Update known ids
        known_stores = [s for s in stores if s['id'] in known_ids]
        for store in known_stores:
            print('.', end='', flush=True)
            update_store(store, chain_id)

        # create new ids
        unknown_stores = [s for s in stores if s['id'] not in known_ids]
        for store in unknown_stores:
            print('n', end='', flush=True)
            add_store(store, chain_id)

        # remove unused ids
        scraper_ids = [s['id'] for s in stores]
        unused_ids = [iden for iden in known_ids if iden not in scraper_ids]
        for iden in unused_ids:
            print('d', end='', flush=True)
            remove_store(iden, chain_id)

        # Update checked_at time
        cur.execute(f"UPDATE chains SET updated_at=now() WHERE id='{chain_id}'")

        # remove from queue
        api_calls['queue'].pop(chain_id)
    conn.commit() #batch commit
    print()
    return

def write_api_calls():
    with open('api_calls.json', 'w') as f:
        json.dump(api_calls, f, indent=2)

if __name__ == '__main__':
    geocode_queue() # Adds coordinates to stores in queue
    add_to_queue() # Adds stores to queue
    geocode_queue()
    clear_queue() # Moves queue data to database
    write_api_calls() # Save json file
    conn.close() #close database connection
