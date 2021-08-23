#!/usr/bin/env python3

from sumo_functions import write_sources, write_user_properties

alias = input("Enter Instance Alias: ")
env = input("Enter AWS Env Alias: ")
vpc = input("Enter AWS VPC Alias: ")

access_id = input("Enter Sumo Logic Access Id: ")
access_key = input("Enter Sumo Logic Access Key: ")

sources = {
    "Aide": "/var/log/aide/aide.log*",
    "Audit": "/var/log/audit/audit.log",
    "Secure": "/var/log/secure*",
    "Messages": "/var/log/messages",
    "Yum": "/var/log/yum.log"
}

fields = {
    "application": alias.lower(),
    "environment": env.lower(),
    "vpc": vpc.lower()
}

write_sources(f'{env.lower()}/ec2/linux/{vpc.lower()}/{alias.lower()}', sources)
write_user_properties(f'{alias}-{env}-{vpc}', access_id, access_key, fields)
