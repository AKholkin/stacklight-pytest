import subprocess
import socket

import yaml
from pprint import pprint

from stacklight_tests import settings
from stacklight_tests import utils


class LOG(object):
    @staticmethod
    def info(msg):
        pprint(msg)


class NoApplication(Exception):
    pass


class MKConfig(object):
    def __init__(self, cluster_name=None):

        if cluster_name is None:
            cluster_name = socket.getfqdn().split('.', 1)[-1]
            LOG.info("No domain/cluster_name passed, use generated: {}"
                     .format(cluster_name))

        inventory = subprocess.Popen("reclass --inventory",
                                     shell=True,
                                     stdout=subprocess.PIPE).stdout.read()
        inventory = yaml.load(inventory)
        LOG.info("Try to load nodes for domain {}".format(cluster_name))
        self.nodes = {k: v for k, v in inventory["nodes"].items()
                      if cluster_name in k}
        LOG.info("Load nodes: {}".format(self.nodes.keys()))

    def get_application_node(self, application):
        for fqdn, node in self.nodes.items():
            # LOG.info("Check application {} for node {}".
            #          format(application, fqdn))
            if application in node["applications"]:
                LOG.info("Found application {} for node {}".
                         format(application, fqdn))
                return node
        raise NoApplication()

    def generate_nodes_config(self):
        nodes_config = []
        private_key = open("/root/.ssh/id_rsa").read()

        def parse_roles_from_classes(node):
            roles_mapping = {
                "openstack.control": "controller",
                "openstack.compute": "compute",
                "stacklight.server": "monitoring",
                "galera.master": "galera.master",
                "galera.slave": "galera.slave",
                "kubernetes.control": "k8s_controller",
                "kubernetes.compute": "k8s_compute",
            }
            cls_based_roles = [
                role for role_name, role in roles_mapping.items()
                if any(role_name in c for c in node["classes"])
            ]
            # Avoid simultaneous existence of k8s_controller
            # and k8s_compute roles
            if ("k8s_compute" in cls_based_roles and
                    "k8s_controller" in cls_based_roles):
                cls_based_roles.remove("k8s_compute")
            return cls_based_roles

        for current_node in self.nodes.values():
            node_params = current_node["parameters"]
            roles = current_node["applications"]
            roles.extend(parse_roles_from_classes(current_node))
            nodes_config.append({
                "address": node_params['_param']['cluster_local_address'],
                "hostname": node_params['linux']['network']['fqdn'],
                "username": "root",
                "private_key": private_key,
                "roles": roles,
            })

        return nodes_config

    def generate_influxdb_config(self):
        _param = self.get_application_node("influxdb")['parameters']['_param']
        return {
            "influxdb_vip": _param['grafana_influxdb_host'],
            "influxdb_port": _param['influxdb_port'],
            "influxdb_username": _param['influxdb_user'],
            "influxdb_password": _param['influxdb_password'],
            "influxdb_db_name": _param['influxdb_database'],
        }

    def generate_elasticsearch_config(self):
        _param = (
            self.get_application_node("elasticsearch")['parameters']['_param'])
        return {
            "elasticsearch_vip": _param['kibana_elasticsearch_host'],
            "elasticsearch_port": _param['elasticsearch_port'],
            "kibana_port": _param['cluster_kibana_port'],
        }

    def generate_grafana_config(self):
        _param = self.get_application_node("grafana")['parameters']['_param']
        return {
            "grafana_vip": _param['grafana_influxdb_host'],
            "grafana_port": _param['grafana_port'],
            "grafana_username": _param['grafana_user'],
            "grafana_password": _param['grafana_password'],
        }

    def generate_nagios_config(self):
        _param = self.get_application_node("nagios")['parameters']['_param']
        return {
            "nagios_vip": _param['nagios_host'],
            "nagios_port": 80,
            "nagios_tls": False,
            "nagios_username": _param['nagios_username'],
            "nagios_password": _param['nagios_password'],
        }

    def generate_keystone_config(self):
        _param = (
            self.get_application_node("keystone")['parameters']['keystone'])
        return {
            "admin_name": _param['server']['admin_name'],
            "admin_password": _param['server']['admin_password'],
            "admin_tenant": _param['server']['admin_tenant'],
            "private_address": _param['server']['bind']['private_address'],
            "public_address": _param['server']['bind']['public_address'],
        }

    def generate_mysql_config(self):
        _param = self.get_application_node("galera")['parameters']['_param']
        return {
            "mysql_user": _param['mysql_admin_user'],
            "mysql_password": _param['mysql_admin_password']
        }

    def generate_prometheus_config(self):
        _param = self.get_application_node("prometheus")['parameters']
        expose_params = (
            _param["docker"]["client"]["stack"]["monitoring"]["service"])
        get_port = lambda x: x["ports"][0].split(":")[0]
        return {
            "use_prometheus_query_alert": True,
            "prometheus_vip": _param["_param"]["prometheus_control_address"],
            "prometheus_server_port":
                get_port(expose_params["server"]),
            "prometheus_alertmanager":
                get_port(expose_params["alertmanager"]),
            "prometheus_pushgateway":
                get_port(expose_params["pushgateway"]),
        }

    def main(self):
        config = {
            "env": {"type": "mk"},
        }
        for application in settings.CONFIGURE_APPS:
            try:
                method = getattr(self, "generate_{}_config".
                                 format(application))
                config.update({
                    application: method()
                })
                LOG.info("INFO: {} configured".format(application))
            except NoApplication:
                LOG.info("INFO: No {} installed, skip".format(application))

        config_filename = utils.get_fixture("config.yaml",
                                            check_existence=False)
        LOG.info("INFO: Saving config to {}".format(config_filename))
        with open(config_filename, "w") as f:
            yaml.safe_dump(config, f, default_flow_style=False)


def main():
    MKConfig(cluster_name=settings.ENV_CLUSTER_NAME).main()


if __name__ == '__main__':
    main()
