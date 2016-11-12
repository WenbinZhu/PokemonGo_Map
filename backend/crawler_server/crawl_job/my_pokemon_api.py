import os
import sys
import time
import json
import logging
import argparse

import s2sphere
from s2sphere import CellId, math

#from pgoapi import pgoapi
from mock_pgoapi import mock_pgoapi as pgoapi

log = logging.getLogger(__name__)


def break_area_to_cells(north, south, west, east):
    region = s2sphere.RegionCoverer()
    region.min_level = 15
    region.max_level = 15
    p1 = s2sphere.LatLng.from_degrees(north,west)
    p2 = s2sphere.LatLng.from_degrees(south, east)
    cell_ids = region.get_covering(s2sphere.LatLngRect.from_point_pair(p1, p2))

    return [cell_id.id() for cell_id in cell_ids]


def get_position_from_cell_id(cell_id):
    cell = CellId(id_ = cell_id).to_lat_lng()
    return (math.degrees(cell._LatLng__coords[0]), math.degrees(cell._LatLng__coords[1]), 0)


def search_cell(cell_id, api):
    position = get_position_from_cell_id(cell_id)

    api.set_position(*position)

    cell_ids = [cell_id]
    timestamps = [0]
    response_dict = api.get_map_objects(latitude=position[0], 
                                        longitude=position[1], 
                                        since_timestamp_ms=timestamps, 
                                        cell_id=cell_ids)

    return response_dict


def parse_pokemon(search_response):
    map_cells = search_response["responses"]["GET_MAP_OBJECTS"]["map_cells"]
    map_cell = map_cells[0]
    catchable_pokemons = map_cell["catchable_pokemons"]

    return catchable_pokemons


def scan_area(north, south, west, east, api):
    result = []

    cell_ids = break_area_to_cells(north, south, west, east)
    
    for cell_id in cell_ids:
        print cell_id
        response = search_cell(cell_id, api)

        pokemon = parse_pokemon(response)
        result += pokemon

    return result


def init_config():
    parser = argparse.ArgumentParser()
    config_file = "config.json"
    
    # If config file exists, load variables from json
    load = {}
    if os.path.isfile(config_file):
        with open(config_file) as data:
            load.update(json.load(data))
            
    # Read passed in Arguments
    required = lambda x: not x in load
    parser.add_argument("-a", "--auth_service", help="Auth Service ('ptc' or 'google')",
    required=required("auth_service"))
    parser.add_argument("-u", "--username", help="Username", required=required("username"))
    parser.add_argument("-p", "--password", help="Password")
    parser.add_argument("-l", "--location", help="Location", required=required("location"))
    parser.add_argument("-d", "--debug", help="Debug Mode", action='store_true')
    parser.add_argument("-t", "--test", help="Only parse the specified location", action='store_true')
    parser.add_argument("-px", "--proxy", help="Specify a socks5 proxy url")
    parser.set_defaults(DEBUG=False, TEST=False)
    config = parser.parse_args()
            
    # Passed in arguments shoud trump
    for key in config.__dict__:
        if key in load and config.__dict__[key] == None:
            config.__dict__[key] = str(load[key])
                    
    if config.__dict__["password"] is None:
        log.info("Secure Password Input (if there is no password prompt, use --password <pw>):")
        config.__dict__["password"] = getpass.getpass()
                        
    if config.auth_service not in ['ptc', 'google']:
        log.error("Invalid Auth service specified! ('ptc' or 'google')")
        return None

    return config


def init_api(config):
    api = pgoapi.PGoApi()
    
    if config.proxy:
        api.set_proxy({'http': config.proxy, 'https': config.proxy })
    
    if config.proxy:
        api.set_authentication(provider = config.auth_service, username = config.username, password =  config.password, proxy_config = {'http': config.proxy, 'https': config.proxy})
    else:
        api.set_authentication(provider = config.auth_service, username = config.username, password =  config.password)

    api.activate_signature("mock_pgoapi/libencrypt.so")

    return api


if __name__  == "__main__":
    config = init_config()
    if not config:
        exit(1)

    api = init_api(config)

    # for i in scan_area(41.7565138, 40.7473342, -74.0003176, -73.997958, api):
        # print i
