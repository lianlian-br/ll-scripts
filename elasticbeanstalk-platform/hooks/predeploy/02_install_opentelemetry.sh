#!/bin/bash
set -e

DEST="/opt/opentelemetry/opentelemetry-javaagent.jar"
URL="https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/download/v1.10.0/opentelemetry-javaagent.jar"

mkdir -p /opt/opentelemetry
curl -L "$URL" -o "$DEST"

chmod 755 "$DEST"
chown root:root "$DEST"
