from stacklight_tests.tests.prometheus import base_test


class TestAlerts(base_test.BaseLMAPrometheusTest):
    def test_system_load_alerts(self):
        """Check that alert for load overage and idle on node can be fired.

        Scenario:
            1. Check that alert is not fired
            2. Make high load on compute node during 5 minutes
            3. Wait until and check that alert was fired
            4. Unload compute node
            5. Wait until and check that alert was ended

        Duration 15m
        """
        def check_status(is_fired=True):
            alert_names = ["SystemLoad5", "AvgCPUUsageIdle"]
            for alert_name in alert_names:
                criteria = {
                    "name": alert_name,
                    "host": compute.hostname,
                }
                self.prometheus_alerting.check_alert_status(
                    criteria, is_fired=is_fired, timeout=6 * 60)

        load_processes_count = 20

        # TODO(rpromyshlennikov): use ".get_random_compute" method
        # instead of current filter after roles config of hosts will be fixed
        compute = [host for host in self.cluster.hosts
                   if host.fqdn.startswith("cmp")][0]

        check_status(is_fired=False)
        with compute.os.make_temporary_load(load_processes_count):
            check_status()
        check_status(is_fired=False)
