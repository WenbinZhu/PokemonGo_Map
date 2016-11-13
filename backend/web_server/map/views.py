import os
import json
import boto3
import redis
import logging
import s2sphere

from django.shortcuts import render
from django.http import HttpResponse
from db_accessor import get_pokemons_from_db

SQS_QUEUE_NAME = os.environ['SQS_NAME']
REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = os.environ['REDIS_PORT']

def pokemons(request):
    # get latitude and longitude info
    north = request.GET['north']
    south = request.GET['south']
    west = request.GET['west']
    east = request.GET['east']

    # query database
    result = get_pokemons_from_db(north, south, west, east)

    # publish crawl jobs to message queue
    # scan_area(float(north), float(south), float(west), float(east))
    scan_area(*map(float, [north, south, west, east]))

    return HttpResponse(json.dumps(result))


def break_area_to_cells(north, south, west, east):
    region = s2sphere.RegionCoverer()
    region.min_level = 15
    region.max_level = 15

    p1 = s2sphere.LatLng.from_degrees(north, west)
    p2 = s2sphere.LatLng.from_degrees(south, east)
    rect = s2sphere.LatLngRect.from_point_pair(p1, p2)
    if rect.area() * 1e8 > 10:
        return []

    cell_ids = region.get_covering(rect)

    return [cell_id.id() for cell_id in cell_ids]


def scan_area(north, south, west, east):
    cell_ids = break_area_to_cells(north, south, west, east)
    if cell_ids == []:
        return

    work_queue = boto3.resource('sqs', region_name=os.environ['SQS_REGION']).get_queue_by_name(QueueName=SQS_QUEUE_NAME)
    redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)

    # query redis server for cell_ids
    redis_response = redis_client.mget(cell_ids)

    # for i, cell_id in enumerate(cell_ids):
    #     print cell_id
    #     work_queue.send_message(MessageBody=json.dumps({'cell_id': cell_id}))

    for i, cell_id in enumerate(cell_ids):
        if redis_response[i] == None:
            print cell_id, 'already existes in redis'
            work_queue.send_message(MessageBody=json.dumps({'cell_id': cell_id}))
            redis_client.setex(cell_id, 30, "1")
        else:
            print cell_id, 'not in redis'
