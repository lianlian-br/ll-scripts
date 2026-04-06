#!/bin/bash
set -e
echo "Installing New Relic agent..."
mkdir -p /var/app/newrelic
curl -L https://download.newrelic.com/newrelic/java-agent/newrelic-agent/current/newrelic-java.zip -o /tmp/newrelic-java.zip

dnf install -y unzip
unzip -o /tmp/newrelic-java.zip -d /var/app/
chmod -R 755 /var/app/newrelic
cp /var/app/staging/scripts/newrelic/newrelic.yml /var/app/newrelic/

echo "New Relic installed successfully"
