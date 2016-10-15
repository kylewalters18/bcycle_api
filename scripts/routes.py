import csv
import itertools
import json
import random
import time
import requests
import logging

# configure log
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# color code log
logging.addLevelName(logging.WARNING, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
logging.addLevelName(logging.ERROR, "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.ERROR))


base_url = 'http://www.yournavigation.org/api/1.0/gosmore.php'

with open('data/geocode_stations.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')

    combinations = itertools.combinations([row for row in reader], 2)

    routes = []
    for source, target in list(combinations):
        try:
            logger.info("Combo: " + source['name'] + ', ' + target['name'])

            payload = {
                'format': 'geojson',
                'flat': source['lat'],
                'flon': source['lng'],
                'tlat': target['lat'],
                'tlon': target['lng'],
                'v': 'bicycle'
            }

            headers = {'X-Yours-client': 'https://github.com/kylewalters18'}

            response = requests.get(base_url, params=payload, headers=headers)
            data = response.json()

            routes.append({
                'source': source,
                'target': target,
                'coordinates': data['coordinates'],
                'distance': data['properties']['distance'],
                'traveltime': data['properties']['traveltime']
            })
        except Exception as e:
            logger.warning("Combo Failed: " + source['name'] + ', ' + target['name'])

        time.sleep(random.randint(2, 4))

    with open('data/routes.json', 'w') as f:
        json.dump(routes, f, indent=4, sort_keys=True, separators=(',', ':'))
