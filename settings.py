import os

# FUEL connection options
ENV_FUEL_IP = os.environ.get("ENV_FUEL_IP", "10.109.0.2")
ENV_FUEL_LOGIN = os.environ.get("ENV_FUEL_LOGIN", "root")
ENV_FUEL_PASSWORD = os.environ.get("ENV_FUEL_PASSWORD", "r00tme")

# Plugins info
INFLUXDB_GRAFANA_PLUGIN_VERSION = os.environ.get(
    "INFLUXDB_GRAFANA_PLUGIN_VERSION", "1.0")
