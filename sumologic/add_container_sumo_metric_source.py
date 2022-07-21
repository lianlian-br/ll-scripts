#!/usr/bin/env python3

import os

from sumo_functions import write_sources, write_user_properties

alias = os.environ['APPLICATION_NAME'].replace(" ", "-")
env = os.environ['ENVIRONMENT'].replace(" ", "-")
modifier = os.environ['MODIFIER'].replace(" ", "-")
vpc = os.environ['VPC_ALIAS'].replace(" ", "-")
service_type = os.environ['SERVICE_TYPE'].replace(" ", "-")
access_id = os.environ['SUMO_ACCESS_ID']
access_key = os.environ['SUMO_ACCESS_KEY']

metric_sources = {
    "Carbon2": 8125
}

fields = {
    "application": alias,
    "environment": env,
    "vpc": vpc,
    "modifier": modifier
}

write_sources(f'{env}/{service_type}/{vpc}/{alias}/{modifier}', metric_sources)
write_user_properties(f'{env}-{vpc}-{alias}-{modifier}', access_id, access_key, fields, ephemeral=True)
