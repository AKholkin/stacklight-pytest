from tests import base_test

import logging


logger = logging.getLogger(__name__)


class TestAlerts(base_test.BaseLMATest):
    def test_check_mysql_fs_alarms(self):
        """Check that mysql-fs-warning and mysql-fs-critical alarms work as
        expected.

        Scenario:
            1. Fill up /var/lib/mysql filesystem to 91 percent.
            2. Check the last value of the warning alarm in InfluxDB.
            3. Clean the filesystem.
            4. Fill up /var/lib/mysql filesystem to 96 percent.
            5. Check the last value of the critical alarm in InfluxDB.
            6. Clean the filesystem.

        Duration 10m
        """
        controller = self.cluster.get_random_controller()
        self.check_filesystem_alarms(
            controller, "/dev/mapper/mysql-root", "mysql-fs",
            "/var/lib/mysql/test/bigfile", "mysql-nodes")

    def test_check_rabbitmq_disk_alarm(self):
        """Check that rabbitmq-disk-limit-warning and
        rabbitmq-disk-limit-critical alarms work as expected.

        Scenario:
            1. Check the last value of the okay alarm in InfluxDB.
            2. Set RabbitMQ disk limit to 99.99 percent of available space.
            3. Check the last value of the warning alarm in InfluxDB.
            4. Set RabbitMQ disk limit to the default value.
            5. Check the last value of the okay alarm in InfluxDB.
            6. Set RabbitMQ disk limit to 100 percent of available space.
            7. Check the last value of the critical alarm in InfluxDB.
            8. Set RabbitMQ disk limit to the default value.
            9. Check the last value of the okay alarm in InfluxDB.

        Duration 10m
        """
        controller = self.cluster.get_random_controller()
        self.check_rabbit_mq_disk_alarms(controller, self.WARNING_STATUS,
                                         self.RABBITMQ_DISK_WARNING_PERCENT)
        self.check_rabbit_mq_disk_alarms(controller, self.CRITICAL_STATUS,
                                         self.RABBITMQ_DISK_CRITICAL_PERCENT)

    def test_check_rabbitmq_memory_alarm(self):
        """Check that rabbitmq-memory-limit-warning and
        rabbitmq-memory-limit-critical alarms work as expected.

        Scenario:
            1. Check the last value of the okay alarm in InfluxDB.
            2. Set RabbitMQ memory limit to 101 percent of currently
            used memory.
            3. Check the last value of the warning alarm in InfluxDB.
            4. Set RabbitMQ memory limit to the default value.
            5. Check the last value of the okay alarm in InfluxDB.
            6. Set RabbitMQ memory limit to 100.01 percent of currently
            used memory.
            7. Check the last value of the critical alarm in InfluxDB.
            8. Set RabbitMQ memory limit to the default value.
            9. Check the last value of the okay alarm in InfluxDB.

        Duration 10m
        """
        controller = self.cluster.get_random_controller()
        self.check_rabbit_mq_memory_alarms(controller, self.WARNING_STATUS,
                                           self.RABBITMQ_MEMORY_WARNING_VALUE)
        self.check_rabbit_mq_memory_alarms(controller, self.CRITICAL_STATUS,
                                           self.RABBITMQ_MEMORY_CRITICAL_VALUE)

    # def check_rabbitmq_pacemaker_alarms(self):
    #     """Check that rabbitmq-pacemaker-* alarms work as expected.
    #
    #     Scenario:
    #         1. Stop one slave RabbitMQ instance.
    #         2. Check that the status of the RabbitMQ cluster is warning.
    #         3. Stop the second slave RabbitMQ instance.
    #         4. Check that the status of the RabbitMQ cluster is critical.
    #         5. Stop the master RabbitMQ instance.
    #         6. Check that the status of the RabbitMQ cluster is down.
    #         7. Clear the RabbitMQ resource.
    #         8. Check that the status of the RabbitMQ cluster is okay.
    #
    #     Duration 10m
    #     """
    #     def ban_and_check_status(node, status, wait=None):
    #         with self.fuel_web.get_ssh_for_node(node.name) as remote:
    #             logger.info("Ban rabbitmq resource on {}".format(node.name))
    #             self.remote_ops.ban_resource(remote,
    #                                          'master_p_rabbitmq-server',
    #                                          wait=wait)
    #         self.check_alarms('service', 'rabbitmq-cluster', 'pacemaker',
    #                           None, status)
    #
    #     self.env.revert_snapshot("deploy_ha_toolchain")
    #
    #     self.check_alarms('service', 'rabbitmq-cluster', 'pacemaker',
    #                       None, OKAY_STATUS)
    #
    #     controllers = self.fuel_web.get_nailgun_cluster_nodes_by_roles(
    #         self.helpers.cluster_id, ["controller"])
    #
    #     controller = controllers[0]
    #     controller_node = self.fuel_web.get_devops_node_by_nailgun_node(
    #         controller)
    #     rabbitmq_master = self.fuel_web.get_rabbit_master_node(
    #         controller_node.name)
    #     rabbitmq_slaves = self.fuel_web.get_rabbit_slaves_node(
    #         controller_node.name)
    #     ban_and_check_status(rabbitmq_slaves[0], WARNING_STATUS, 120)
    #     ban_and_check_status(rabbitmq_slaves[1], CRITICAL_STATUS, 120)
    #     # Don't wait for the pcs operation to complete as it will fail since
    #     # the resource isn't running anywhere
    #     ban_and_check_status(rabbitmq_master, DOWN_STATUS)
    #
    #     logger.info("Clear rabbitmq resource")
    #     with self.fuel_web.get_ssh_for_node(rabbitmq_master.name) as remote:
    #         self.remote_ops.clear_resource(remote,
    #                                        'master_p_rabbitmq-server',
    #                                        wait=240)
    #     self.check_alarms('service', 'rabbitmq-cluster', 'pacemaker',
    #                       None, OKAY_STATUS)

    def test_check_root_fs_alarms(self):
        """Check that root-fs-warning and root-fs-critical alarms work as
        expected.

        Scenario:
            1. Fill up root filesystem to 91 percent.
            2. Check the last value of the warning alarm in InfluxDB.
            3. Clean the filesystem.
            4. Fill up root filesystem to 96 percent.
            5. Check the last value of the critical alarm in InfluxDB.
            6. Clean the filesystem.

        Duration 10m
        """
        controller = self.cluster.get_random_controller()
        self.check_filesystem_alarms(
            controller, "/$", "root-fs", "/bigfile", "controller")

    def test_check_log_fs_alarms(self):
        """Check that log-fs-warning and log-fs-critical alarms work as
        expected.

        Scenario:
            1. Fill up /var/log filesystem to 91 percent.
            2. Check the last value of the warning alarm in InfluxDB.
            3. Clean the filesystem.
            4. Fill up /var/log filesystem to 96 percent.
            5. Check the last value of the critical alarm in InfluxDB.
            6. Clean the filesystem.

        Duration 10m
        """
        controller = self.cluster.get_random_controller()
        self.check_filesystem_alarms(
            controller, "/var/log", "log-fs", "/var/log/bigfile", "controller")

    def test_check_nova_fs_alarms(self):
        """Check that nova-fs-warning and nova-fs-critical alarms work as
        expected.

        Scenario:
            1. Fill up /var/lib/nova filesystem to 91 percent.
            2. Check the last value of the warning alarm in InfluxDB.
            3. Clean the filesystem.
            4. Fill up /var/lib/nova filesystem to 96 percent.
            5. Check the last value of the critical alarm in InfluxDB.
            6. Clean the filesystem.

        Duration 10m
        """
        compute = self.cluster.filter_by_role("compute").first()
        self.check_filesystem_alarms(compute, "/var/lib/nova", "nova-fs",
                                     "/var/lib/nova/bigfile", "compute")

    # def check_nova_api_logs_errors_alarms(self):
    #     """Check that nova-logs-error and nova-api-http-errors alarms work as
    #     expected.
    #
    #     Scenario:
    #         1. Rename all nova tables to UPPERCASE.
    #         2. Run some nova list command repeatedly.
    #         3. Check the last value of the nova-logs-error alarm in InfluxDB.
    #         4. Check the last value of the nova-api-http-errors alarm
    #            in InfluxDB.
    #         5. Revert all nova tables names to lowercase.
    #
    #     Duration 10m
    #     """
    #     def get_servers_list():
    #         try:
    #             self.helpers.os_conn.get_servers()
    #         except Exception:
    #             pass
    #     self.env.revert_snapshot("deploy_toolchain")
    #
    #     controller = self.fuel_web.get_nailgun_cluster_nodes_by_roles(
    #         self.helpers.cluster_id, ["controller"])[0]
    #
    #     with self.helpers.make_logical_db_unavailable("nova", controller):
    #         metrics = {"nova-logs": "error",
    #                    "nova-api": "http_errors"}
    #         self._verify_service_alarms(
    #             get_servers_list, 100, metrics, WARNING_STATUS)
    #
    # @test(depends_on_groups=["deploy_toolchain"],
    #       groups=["check_neutron_api_logs_errors_alarms",
    #               "http_logs_errors_alarms", "toolchain", "alarms"])
    # @log_snapshot_after_test
    # def check_neutron_api_logs_errors_alarms(self):
    #     """Check that neutron-logs-error and neutron-api-http-errors
    #     alarms work as expected.
    #
    #     Scenario:
    #         1. Rename all neutron tables to UPPERCASE.
    #         2. Run some neutron agents list command repeatedly.
    #         3. Check the last value of the neutron-logs-error alarm
    #            in InfluxDB.
    #         4. Check the last value of the neutron-api-http-errors alarm
    #            in InfluxDB.
    #         5. Revert all neutron tables names to lowercase.
    #
    #     Duration 10m
    #     """
    #     def get_agents_list():
    #         try:
    #             self.helpers.os_conn.list_agents()
    #         except Exception:
    #             pass
    #
    #     self.env.revert_snapshot("deploy_toolchain")
    #
    #     controller = self.fuel_web.get_nailgun_cluster_nodes_by_roles(
    #         self.helpers.cluster_id, ["controller"])[0]
    #
    #     with self.helpers.make_logical_db_unavailable("neutron", controller):
    #         metrics = {"neutron-logs": "error",
    #                    "neutron-api": "http_errors"}
    #         self._verify_service_alarms(
    #             get_agents_list, 100, metrics, WARNING_STATUS)
    #
    # @test(depends_on_groups=["deploy_toolchain"],
    #       groups=["check_glance_api_logs_errors_alarms",
    #               "http_logs_errors_alarms", "toolchain", "alarms"])
    # @log_snapshot_after_test
    # def check_glance_api_logs_errors_alarms(self):
    #     """Check that glance-logs-error and glance-api-http-errors alarms
    #     work as expected.
    #
    #     Scenario:
    #         1. Rename all glance tables to UPPERCASE.
    #         2. Run some glance image list command repeatedly.
    #         3. Check the last value of the glance-logs-error alarm
    #            in InfluxDB.
    #         4. Check the last value of the glance-api-http-errors alarm
    #            in InfluxDB.
    #         5. Revert all glance tables names to lowercase.
    #
    #     Duration 10m
    #     """
    #     def get_images_list():
    #         try:
    #             # NOTE(rpromyshlennikov): List is needed here
    #             # because glance image list is lazy method
    #             return list(self.helpers.os_conn.get_image_list())
    #         except Exception:
    #             pass
    #
    #     self.env.revert_snapshot("deploy_toolchain")
    #
    #     controller = self.fuel_web.get_nailgun_cluster_nodes_by_roles(
    #         self.helpers.cluster_id, ["controller"])[0]
    #
    #     with self.helpers.make_logical_db_unavailable("glance", controller):
    #         metrics = {"glance-logs": "error",
    #                    "glance-api": "http_errors"}
    #         self._verify_service_alarms(
    #             get_images_list, 100, metrics, WARNING_STATUS)
    #
    # @test(depends_on_groups=["deploy_toolchain"],
    #       groups=["check_heat_api_logs_errors_alarms",
    #               "http_logs_errors_alarms", "toolchain", "alarms"])
    # @log_snapshot_after_test
    # def check_heat_api_logs_errors_alarms(self):
    #     """Check that heat-logs-error and heat-api-http-errors alarms work as
    #     expected.
    #
    #     Scenario:
    #         1. Rename all heat tables to UPPERCASE.
    #         2. Run some heat stack list command repeatedly.
    #         3. Check the last value of the heat-logs-error alarm in InfluxDB.
    #         4. Check the last value of the heat-api-http-errors alarm
    #            in InfluxDB.
    #         5. Revert all heat tables names to lowercase.
    #
    #     Duration 10m
    #     """
    #     def get_stacks_list():
    #         try:
    #             with self.fuel_web.get_ssh_for_nailgun_node(
    #                     controller) as remote:
    #                 return remote.execute(
    #                     ". openrc && heat stack-list > /dev/null 2>&1")
    #         except Exception:
    #             pass
    #
    #     self.env.revert_snapshot("deploy_toolchain")
    #
    #     controller = self.fuel_web.get_nailgun_cluster_nodes_by_roles(
    #         self.helpers.cluster_id, ["controller"])[0]
    #
    #     with self.helpers.make_logical_db_unavailable("heat", controller):
    #         metrics = {"heat-logs": "error",
    #                    "heat-api": "http_errors"}
    #         self._verify_service_alarms(
    #             get_stacks_list, 100, metrics, WARNING_STATUS)
    #
    # @test(depends_on_groups=["deploy_toolchain"],
    #       groups=["check_cinder_api_logs_errors_alarms",
    #               "http_logs_errors_alarms", "toolchain", "alarms"])
    # @log_snapshot_after_test
    # def check_cinder_api_logs_errors_alarms(self):
    #     """Check that cinder-logs-error and cinder-api-http-errors alarms
    #     work as expected.
    #
    #     Scenario:
    #         1. Rename all cinder tables to UPPERCASE.
    #         2. Run some cinder list command repeatedly.
    #         3. Check the last value of the cinder-logs-error alarm
    #            in InfluxDB.
    #         4. Check the last value of the cinder-api-http-errors alarm
    #            in InfluxDB.
    #         5. Revert all cinder tables names to lowercase.
    #
    #     Duration 10m
    #     """
    #
    #     def get_volumes_list():
    #         try:
    #             self.helpers.os_conn.cinder.volumes.list()
    #         except Exception:
    #             pass
    #
    #     self.env.revert_snapshot("deploy_toolchain")
    #
    #     controller = self.fuel_web.get_nailgun_cluster_nodes_by_roles(
    #         self.helpers.cluster_id, ["controller"])[0]
    #
    #     with self.helpers.make_logical_db_unavailable("cinder", controller):
    #         metrics = {"cinder-logs": "error",
    #                    "cinder-api": "http_errors"}
    #         self._verify_service_alarms(
    #             get_volumes_list, 100, metrics, WARNING_STATUS)
    #
    # @test(depends_on_groups=["deploy_toolchain"],
    #       groups=["check_keystone_api_logs_errors_alarms",
    #               "http_logs_errors_alarms", "toolchain", "alarms"])
    # @log_snapshot_after_test
    # def check_keystone_api_logs_errors_alarms(self):
    #     """Check that keystone-logs-error, keystone-public-api-http-errors and
    #     keystone-admin-api-http-errors alarms work as expected.
    #
    #     Scenario:
    #         1. Rename all keystone tables to UPPERCASE.
    #         2. Run some keystone stack list command repeatedly.
    #         3. Check the last value of the keystone-logs-error alarm
    #            in InfluxDB.
    #         4. Check the last value of the keystone-public-api-http-errors
    #            alarm in InfluxDB.
    #         5. Check the last value of the keystone-admin-api-http-errors
    #            alarm in InfluxDB.
    #         6. Revert all keystone tables names to lowercase.
    #
    #     Duration 10m
    #     """
    #
    #     def get_users_list(level):
    #         additional_cmds = {
    #             "user": ("&& export OS_AUTH_URL="
    #                      "`(echo $OS_AUTH_URL "
    #                      "| sed 's%:5000/%:5000/v2.0%')` "),
    #             "admin": ("&& export OS_AUTH_URL="
    #                       "`(echo $OS_AUTH_URL "
    #                       "| sed 's%:5000/%:35357/v2.0%')` ")
    #         }
    #
    #         def get_users_list_parametrized():
    #             try:
    #                 with self.fuel_web.get_ssh_for_nailgun_node(
    #                         controller) as remote:
    #                     return remote.execute(
    #                         ". openrc {additional_cmd}"
    #                         "&& keystone user-list > /dev/null 2>&1".format(
    #                             additional_cmd=additional_cmds[level]
    #                         )
    #                     )
    #             except Exception:
    #                 pass
    #         return get_users_list_parametrized
    #
    #     self.env.revert_snapshot("deploy_toolchain")
    #
    #     controller = self.fuel_web.get_nailgun_cluster_nodes_by_roles(
    #         self.helpers.cluster_id, ["controller"])[0]
    #
    #     with self.helpers.make_logical_db_unavailable("keystone", controller):
    #         metrics = {"keystone-logs": "error",
    #                    "keystone-public-api": "http_errors"}
    #         self._verify_service_alarms(
    #             get_users_list("user"), 100, metrics, WARNING_STATUS)
    #
    #         metrics = {"keystone-admin-api": "http_errors"}
    #         self._verify_service_alarms(
    #             get_users_list("admin"), 100, metrics, WARNING_STATUS)
    #
    # @test(depends_on_groups=["deploy_toolchain"],
    #       groups=["check_swift_api_logs_errors_alarms",
    #               "http_logs_errors_alarms", "toolchain", "alarms"])
    # @log_snapshot_after_test
    # def check_swift_api_logs_errors_alarms(self):
    #     """Check that swift-logs-error and swift-api-http-error alarms
    #     work as expected.
    #
    #     Scenario:
    #         1. Stop swift-account service on controller.
    #         2. Run some swift stack list command repeatedly.
    #         3. Check the last value of the swift-logs-error alarm
    #            in InfluxDB.
    #         4. Check the last value of the swift-api-http-errors alarm
    #            in InfluxDB.
    #         5. Start swift-account service on controller.
    #
    #     Duration 15m
    #     """
    #
    #     def get_objects_list():
    #         try:
    #             with self.fuel_web.get_ssh_for_nailgun_node(
    #                     controller) as remote:
    #                 return remote.execute(
    #                     ". openrc "
    #                     "&& export OS_AUTH_URL="
    #                     "`(echo $OS_AUTH_URL | sed 's%:5000/%:5000/v2.0%')` "
    #                     "&& swift list > /dev/null 2>&1")
    #         except Exception:
    #             pass
    #
    #     self.env.revert_snapshot("deploy_toolchain")
    #
    #     controller = self.fuel_web.get_nailgun_cluster_nodes_by_roles(
    #         self.helpers.cluster_id, ["controller"])[0]
    #
    #     with self.fuel_web.get_ssh_for_nailgun_node(
    #             controller) as remote:
    #         self.remote_ops.manage_service(
    #             remote, "swift-account", "stop")
    #
    #     metrics = {"swift-logs": "error",
    #                "swift-api": "http_errors"}
    #     self._verify_service_alarms(
    #         get_objects_list, 10, metrics, WARNING_STATUS)
    #
    #     with self.fuel_web.get_ssh_for_nailgun_node(controller) as remote:
    #         self.remote_ops.manage_service(
    #             remote, "swift-account", "start")
