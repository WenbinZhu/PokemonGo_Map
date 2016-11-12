import os
import json
import boto3
import logging
import s2sphere

from django.shortcuts import render
from django.http import HttpResponse
from db_accessor import get_pokemons_from_db

SQS_QUEUE_NAME = os.environ['SQS_NAME']

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
    if rect.area() * 1e8 > 7:
        return []

    cell_ids = region.get_covering(rect)

    return [cell_id.id() for cell_id in cell_ids]


def scan_area(north, south, west, east):
    result = []

    cell_ids = break_area_to_cells(north, south, west, east)

    work_queue = boto3.resource('sqs', region_name=os.environ['SQS_REGION']).get_queue_by_name(QueueName=SQS_QUEUE_NAME)
    
    for cell_id in cell_ids:
        print cell_id
        work_queue.send_message(MessageBody=json.dumps({'cell_id': cell_id}))

    return result
