#!/usr/bin/env python3

from sumo_functions import write_sources, write_user_properties
import os

alias = os.environ['APPLICATION_NAME'].replace(" ", "-")
env = os.environ['ENVIRONMENT'].replace(" ", "-")
modifier = os.environ['MODIFIER'].replace(" ", "-")
vpc = os.environ['VPC_ALIAS'].replace(" ", "-")
access_id = os.environ['SUMO_ACCESS_ID']
access_key = os.environ['SUMO_ACCESS_KEY']

file_sources = {
    "Application": "/var/log/web.stdout.log"
}

metric_sources = {
    "Carbon2": 8125
}

fields = {
    "application": alias,
    "environment": env,
    "vpc": vpc,
    "modifier": modifier
}

write_sources('/opt/SumoCollector/config', f'{env}/eb/{vpc}/{alias}/{modifier}', file_sources, metric_sources)
write_user_properties('/opt/SumoCollector/config', f'{env}-{vpc}-{alias}-{modifier}', access_id, access_key, fields, ephemeral=True)
