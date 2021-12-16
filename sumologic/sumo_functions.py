#!/bin/bash python3

import json


def generate_source(prefix: str, source: str, path_expression: str) -> dict:
    return {
        "sourceType": "LocalFile",
        "category": f'{prefix}/{source}'.lower(),
        "name": source,
        "pathExpression": path_expression
    }


def generate_sources_file(prefix: str, sources: dict) -> dict:
    return {
        "api.version": "v1",
        "sources": list(map(lambda source: generate_source(prefix, source[0], source[1]), sources.items()))
    }


def generate_user_file(content: dict) -> list:
    return list(map(lambda line: f'{line[0]}={line[1]}', content.items()))


def write_user_properties(
        name: str,
        sumo_access_id: str,
        sumo_access_key: str,
        fields: dict,
        ephemeral: bool = False
):
    with open('/opt/SumoCollector/config/user.properties', 'w') as new_file:
        variables = {
            "name": name.lower(),
            "accessid": sumo_access_id,
            "accesskey": sumo_access_key,
            "fields": ",".join(map(lambda field: f'{field[0]}={field[1]}', fields.items())).lower(),
            "wrapper.java.command": "java",
            "syncSources": "/opt/SumoCollector/config/sumo_sources.json",
            "ephemeral": f'{ephemeral}'.lower(),
            "skipAccessKeyRemoval": "true"
        }

        file_lines = generate_user_file(variables)
        print("\n".join(file_lines))
        new_file.writelines("\n".join(file_lines))


def write_sources(prefix: str, sources: dict):
    with open('/opt/SumoCollector/config/sumo_sources.json', 'w') as new_file:
        file_content = generate_sources_file(prefix, sources)

        print(json.dumps(file_content, indent=4))
        new_file.write(json.dumps(file_content, indent=4))
