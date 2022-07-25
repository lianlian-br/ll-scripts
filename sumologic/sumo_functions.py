#!/bin/bash python3

import json

def generate_metric_source(prefix: str, source: str, port: int) -> dict:
    return {
        "sourceType": "StreamingMetrics",
        "category": f'{prefix}/{source}'.lower(),
        "name": source,
        "port": port,
        "protocol": "UDP",
        "contentType": "Carbon2"
    }


def generate_file_source(prefix: str, source: str, path_expression: str) -> dict:
    return {
        "sourceType": "LocalFile",
        "category": f'{prefix}/{source}'.lower(),
        "name": source,
        "pathExpression": path_expression
    }


def generate_sources_file(prefix: str, pathSources: dict = {}, metricSources: dict = {}) -> dict:
    allPathSources = list(map(lambda source: generate_file_source(prefix, source[0], source[1]), pathSources.items()))
    allMetricSources = list(map(lambda source: generate_metric_source(prefix, source[0], source[1]), metricSources.items()))

    return { "api.version": "v1", "sources": allPathSources + allMetricSources }


def generate_user_file(content: dict) -> list:
    return list(map(lambda line: f'{line[0]}={line[1]}', content.items()))


def write_user_properties(
        name: str,
        sumo_access_id: str,
        sumo_access_key: str,
        fields: dict,
        ephemeral: bool = False,
        java_wrapper: str = "java",
        path: str = '/opt/SumoCollector/config'
):
    with open(f'{path}/user.properties', 'w') as new_file:
        variables = {
            "name": name.lower(),
            "accessid": sumo_access_id,
            "accesskey": sumo_access_key,
            "fields": ",".join(map(lambda field: f'{field[0]}={field[1]}', fields.items())).lower(),
            "wrapper.java.command": java_wrapper,
            "syncSources": f'{path}/sumo_sources.json',
            "ephemeral": f'{ephemeral}'.lower(),
            "skipAccessKeyRemoval": "true"
        }

        file_lines = generate_user_file(variables)
        print("\n".join(file_lines))
        new_file.writelines("\n".join(file_lines))


def write_sources(prefix: str, pathSources: dict = {}, metricSources: dict = {}, path: str = '/opt/SumoCollector/config'):
    with open(f'{path}/sumo_sources.json', 'w') as new_file:
        file_content = generate_sources_file(prefix, pathSources, metricSources)

        print(json.dumps(file_content, indent=4))
        new_file.write(json.dumps(file_content, indent=4))
