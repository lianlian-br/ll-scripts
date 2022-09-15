#!/usr/bin/env python3

import os
import sys

from sumo_functions import write_sources, write_user_properties

alias = os.environ['APPLICATION_NAME'].replace(" ", "-")
env = os.environ['ENVIRONMENT'].replace(" ", "-")
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
    "vpc": vpc
}

path = sys.argv[0] if len(sys.argv) > 0 else '/opt/SumoCollector/config'

write_sources(f'{env}/{service_type}/{vpc}/{alias}', metricSources=metric_sources, path=path)
write_user_properties(
    f'{env}-{service_type}-{vpc}-{alias}',
    access_id,
    access_key,
    fields,
    ephemeral=True,
    java_wrapper="/opt/SumoCollector/jre/bin/java",
    path=path
)
