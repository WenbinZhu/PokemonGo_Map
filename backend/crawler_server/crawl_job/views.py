import os
import json
import logging

from django.shortcuts import render
from django.http import HttpResponse

from my_pokemon_api import *
from mock_pgoapi import *

from db_accessor import *

logger = logging.getLogger("worker")

class Config():
    pass

# Create your views here.
def add_crawl_point(request):
    logger.info("I'm in add_crawl_point")

    # crawl pokemon data

    # get cell id from request
    request_obj = json.loads(request.body)
    cell_id = request_obj['cell_id']

    # call my search api
    config = Config()
    config.auth_service = 'ptc'
    config.username = os.environ['PG_USER']
    config.password = os.environ['PG_PASSWORD']
    config.proxy = 'socks5://127.0.0.1:9050'

    api = init_api(config)
    search_response = search_cell(cell_id, api)
    result = parse_pokemon(search_response)

    logger.info('cell_id: {0}'.format(cell_id))
    logger.info('Crawl result: {0}'.format(json.dumps(result, indent=2)))

    # strore search result into database
    for pokemon in result:
        add_pokemon_to_db(pokemon['encounter_id'],
                          pokemon['expiration_timestamp_ms'],
                          pokemon['pokemon_id'],
                          pokemon['latitude'],
                          pokemon['longitude'])

    return HttpResponse("Successful Result")
