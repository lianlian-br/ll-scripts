#!/usr/bin/env python3

from sumo_functions import write_sources, write_user_properties
import os

alias = os.environ['APPLICATION_NAME']
env = os.environ['ENVIRONMENT']
modifier = os.environ['MODIFIER']
vpc = os.environ['VPC_ALIAS']
access_id = os.environ['SUMO_ACCESS_ID']
access_key = os.environ['SUMO_ACCESS_KEY']

sources = {
    "Application": "/var/log/web.stdout.log"
}

fields = {
    "application": alias,
    "environment": env,
    "vpc": vpc,
    "modifier": modifier
}

write_sources(f'{env}/eb/{vpc}/{alias}/{modifier}', sources)
write_user_properties(f'{env}-{vpc}-{alias}-{modifier}', access_id, access_key, fields, ephemeral=True)

