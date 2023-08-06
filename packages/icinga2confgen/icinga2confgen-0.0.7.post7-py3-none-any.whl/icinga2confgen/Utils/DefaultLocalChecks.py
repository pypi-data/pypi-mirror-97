#!/usr/bin/python3
# -*- coding: utf-8

#  Icinga2 configuration generator
#
#  Icinga2 configuration file generator for hosts, commands, checks, ... in python
#
#  Copyright (c) 2020 Fabian Fröhlich <mail@icinga2.confgen.org> https://icinga2.confgen.org
#
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#  For all license terms see README.md and LICENSE Files in root directory of this Project.

from icinga2confgen.Checks.HariSekhonNagiosPlugins.CheckYum import CheckYum
from icinga2confgen.Checks.MonitoringPlugins.CheckExistingUsers import CheckExistingUsers
from icinga2confgen.Checks.MonitoringPlugins.CheckGroupMembers import CheckGroupMembers
from icinga2confgen.Checks.MonitoringPlugins.CheckRebootRequired import CheckRebootRequired
from icinga2confgen.Checks.MonitoringPlugins.CheckSSHDSecurity import CheckSSHDSecurity
from icinga2confgen.Checks.MonitoringPlugins.CheckUFWStatus import CheckUFWStatus
from icinga2confgen.Checks.NagiosPlugins.CheckApt import CheckApt
from icinga2confgen.Checks.NagiosPlugins.CheckDisk import CheckDisk
from icinga2confgen.Checks.NagiosPlugins.CheckLoad import CheckLoad
from icinga2confgen.Checks.NagiosPlugins.CheckNTPTime import CheckNTPTime
from icinga2confgen.Checks.NagiosPlugins.CheckProcs import CheckProcs
from icinga2confgen.Checks.NagiosPlugins.CheckSWAP import CheckSWAP
from icinga2confgen.Checks.NagiosPlugins.CheckSensors import CheckSensors
from icinga2confgen.Checks.NagiosPlugins.CheckUsers import CheckUsers
from icinga2confgen.Groups.ServiceGroup import ServiceGroup
from icinga2confgen.Helpers.LocalCheckManager import LocalCheckManager
from icinga2confgen.ValueChecker import ValueChecker


class DefaultLocalChecks(LocalCheckManager):

    def __init__(self, servers=[], notifications=[], sudoers=[], additional_users=[]):
        LocalCheckManager.__init__(self, servers=servers, notifications=notifications)
        self.__additional_users = additional_users
        self.__check_load = True
        self.__check_procs = True
        self.__check_sensors = False
        self.__check_apt = True
        self.__check_yum = False
        self.__check_users = True
        self.__check_swap = True
        self.__check_ntp_time = True
        self.__check_disk = True
        self.__check_reboot_required = True
        self.__check_sshd_security = True
        self.__check_sshd_running = True
        self.__check_mysqld_running = False
        self.__check_postgres_running = False
        self.__check_cron_running = True
        self.__check_crond_running = False
        self.__check_rsyslogd_running = True
        self.__check_nginx_running = False
        self.__check_apache_running = False
        self.__check_httpd_running = False
        self.__check_tomcat_running = False
        self.__check_php_fpm_running = False
        self.__check_freshclam_running = False
        self.__check_clamd_running = False
        self.__check_postfix_running = False
        self.__check_sudoers = True
        self.__check_normal_users = True
        self.__check_wheel = False
        self.__check_ufw = True
        self.__sudoers = sudoers
        self.__check_partitions = []
        self.__ufw_rules = []
        self.__ufw_defaults = ('deny', 'allow', 'deny')

    def check_load(self, enabled):
        ValueChecker.is_bool(enabled)
        self.__check_load = enabled

        return self

    def is_checking_load(self):
        return self.__check_load

    def check_reboot_required(self, enabled):
        ValueChecker.is_bool(enabled)
        self.__check_reboot_required = enabled

        return self

    def is_checking_reboot_required(self):
        return self.__check_reboot_required

    def check_procs(self, enabled):
        ValueChecker.is_bool(enabled)
        self.__check_procs = enabled

        return self

    def is_checking_procs(self):
        return self.__check_procs

    def check_sensors(self, enabled):
        ValueChecker.is_bool(enabled)
        self.__check_sensors = enabled

        return self

    def is_checking_sensors(self):
        return self.__check_sensors

    def check_apt(self, enabled):
        ValueChecker.is_bool(enabled)
        self.__check_apt = enabled

        return self

    def is_checking_apt(self):
        return self.__check_apt

    def check_yum(self, enabled):
        ValueChecker.is_bool(enabled)
        self.__check_yum = enabled

        return self

    def is_checking_yum(self):
        return self.__check_yum

    def check_users(self, enabled):
        ValueChecker.is_bool(enabled)
        self.__check_users = enabled

        return self

    def is_checking_users(self):
        return self.__check_users

    def check_swap(self, enabled):
        ValueChecker.is_bool(enabled)
        self.__check_swap = enabled

        return self

    def is_checking_swap(self):
        return self.__check_swap

    def check_ntp_time(self, enabled):
        ValueChecker.is_bool(enabled)
        self.__check_ntp_time = enabled

        return self

    def is_checking_ntp_time(self):
        return self.__check_ntp_time

    def check_disk(self, enabled):
        ValueChecker.is_bool(enabled)
        self.__check_disk = enabled

        return self

    def is_checking_disk(self):
        return self.__check_disk

    def check_sshd_security(self, enabled):
        ValueChecker.is_bool(enabled)
        self.__check_sshd_security = enabled

        return self

    def is_checking_sshd_security(self):
        return self.__check_sshd_security

    def check_sshd_running(self, enabled):
        ValueChecker.is_bool(enabled)
        self.__check_sshd_running = enabled

        return self

    def is_checking_sshd_running(self):
        return self.__check_sshd_running

    def check_freshclam_running(self, enabled):
        ValueChecker.is_bool(enabled)
        self.__check_freshclam_running = enabled

        return self

    def is_checking_freshclam_running(self):
        return self.__check_freshclam_running

    def check_clamd_running(self, enabled):
        ValueChecker.is_bool(enabled)
        self.__check_clamd_running = enabled

        return self

    def is_checking_clamd_running(self):
        return self.__check_clamd_running

    def check_postfix_running(self, enabled):
        ValueChecker.is_bool(enabled)
        self.__check_postfix_running = enabled

        return self

    def is_checking_postfix_running(self):
        return self.__check_postfix_running

    def check_mysqld_running(self, enabled):
        ValueChecker.is_bool(enabled)
        self.__check_mysqld_running = enabled

        return self

    def is_checking_mysqld_running(self):
        return self.__check_mysqld_running

    def check_postgres_running(self, enabled):
        ValueChecker.is_bool(enabled)
        self.__check_postgres_running = enabled

        return self

    def is_checking_postgres_running(self):
        return self.__check_postgres_running

    def check_cron_running(self, enabled):
        ValueChecker.is_bool(enabled)
        self.__check_cron_running = enabled

        return self

    def is_checking_cron_running(self):
        return self.__check_cron_running

    def check_crond_running(self, enabled):
        ValueChecker.is_bool(enabled)
        self.__check_crond_running = enabled

        return self

    def is_checking_crond_running(self):
        return self.__check_crond_running

    def check_rsyslogd_running(self, enabled):
        ValueChecker.is_bool(enabled)
        self.__check_rsyslogd_running = enabled

        return self

    def is_checking_rsyslogd_running(self):
        return self.__check_rsyslogd_running

    def check_nginx_running(self, enabled):
        ValueChecker.is_bool(enabled)
        self.__check_nginx_running = enabled

        return self

    def is_checking_nginx_running(self):
        return self.__check_nginx_running

    def check_apache_running(self, enabled):
        ValueChecker.is_bool(enabled)
        self.__check_apache_running = enabled

        return self

    def is_checking_apache_running(self):
        return self.__check_apache_running

    def check_httpd_running(self, enabled):
        ValueChecker.is_bool(enabled)
        self.__check_httpd_running = enabled

        return self

    def is_checking_httpd_running(self):
        return self.__check_httpd_running

    def check_tomcat_running(self, enabled):
        ValueChecker.is_bool(enabled)
        self.__check_tomcat_running = enabled

        return self

    def is_checking_tomcat_running(self):
        return self.__check_tomcat_running

    def check_php_fpm_running(self, enabled):
        ValueChecker.is_bool(enabled)
        self.__check_php_fpm_running = enabled

        return self

    def is_checking_php_fpm_running(self):
        return self.__check_php_fpm_running

    def check_ufw(self, enabled):
        ValueChecker.is_bool(enabled)
        self.__check_ufw = enabled

        return self

    def is_checking_ufw(self):
        return self.__check_ufw

    def add_ufw_rule(self, policy_from, policy_to, policy_action):
        ValueChecker.is_string(policy_from)
        ValueChecker.is_string(policy_to)
        ValueChecker.is_string(policy_action)
        self.__ufw_rules.append(
            (policy_from.replace(' ', '-'), policy_to.replace(' ', '-'), policy_action.replace(' ', '-')))
        return self

    def set_ufw_defaults(self, incoming, outgoing, routing):
        self.__ufw_defaults = tuple((incoming, outgoing, routing))
        return self

    def add_partition(self, id, path, warning_percent, critical_percent):
        ValueChecker.is_string(id)
        ValueChecker.is_string(path)
        ValueChecker.is_number(warning_percent)
        ValueChecker.is_number(critical_percent)
        self.__check_partitions.append((id, path, warning_percent, critical_percent))

        return self

    def check_sudoers(self, enabled):
        ValueChecker.is_bool(enabled)
        self.__check_sudoers = enabled

        return self

    def is_checking_sudoers(self):
        return self.__check_sudoers

    def check_normal_users(self, enabled):
        ValueChecker.is_bool(enabled)
        self.__check_normal_users = enabled

        return self

    def is_checking_normal_users(self):
        return self.__check_normal_users

    def check_wheel(self, enabled):
        ValueChecker.is_bool(enabled)
        self.__check_wheel = enabled

        return self

    def is_checking_wheel(self):
        return self.__check_wheel

    def add_sudoers(self, username):
        ValueChecker.is_string(username)
        self.__sudoers.append(username)

        return self

    def add_normal_user(self, username):
        ValueChecker.is_string(username)
        self.__additional_users.append(username)

        return self

    def add_notification(self, notification):
        # todo type check
        self.__notifications.append(notification)
        return self

    def get_notification(self):
        return self.__notifications

    def apply(self):
        for server in self.get_servers():
            if True is self.__check_apt:
                check = CheckApt.create('apt_' + server.get_id())
                self.apply_check(check, server)

            if True is self.__check_yum:
                check = CheckYum.create('yum_' + server.get_id())
                self.apply_check(check, server)

            if True is self.__check_load:
                check = CheckLoad.create('load_' + server.get_id())
                self.apply_check(check, server)

            if True is self.__check_reboot_required:
                check = CheckRebootRequired.create('reboot_required_' + server.get_id())
                self.apply_check(check, server)

            if True is self.__check_procs:
                check = CheckProcs.create('procs_' + server.get_id())
                self.apply_check(check, server)

            if True is self.__check_sensors:
                check = CheckSensors.create('sensors_' + server.get_id())
                self.apply_check(check, server)

            if True is self.__check_ntp_time:
                check = CheckNTPTime.create('ntp_time_' + server.get_id())
                self.apply_check(check, server)

            if True is self.__check_swap:
                check = CheckSWAP.create('swap_' + server.get_id())

                self.apply_check(check, server)

            if True is self.__check_users:
                check = CheckUsers.create('users_' + server.get_id())
                self.apply_check(check, server)

            sshd_running_check = None
            if True is self.__check_sshd_running:
                self.create_running_check('sshd', 'sshd', server)

            if True is self.__check_sshd_security:
                check = CheckSSHDSecurity.create('sshd_security_' + server.get_id())
                self.apply_check(check, server, sshd_running_check)

            if True is self.__check_mysqld_running:
                self.create_running_check('mysql', 'mysqld', server, ['database'])

            if True is self.__check_postgres_running:
                self.create_running_check('postgres', 'postgres', server, ['database'])

            if True is self.__check_cron_running:
                self.create_running_check('cron', 'cron', server)

            if True is self.__check_crond_running:
                self.create_running_check('cron', 'crond', server)

            if True is self.__check_rsyslogd_running:
                self.create_running_check('rsyslogd', 'rsyslogd', server)

            if True is self.__check_nginx_running:
                self.create_running_check('nginx', 'nginx', server, ['webserver'])

            if True is self.__check_apache_running:
                self.create_running_check('apache', 'apache2', server, ['webserver'])

            if True is self.__check_httpd_running:
                self.create_running_check('httpd', 'httpd', server, ['webserver'])

            if True is self.__check_tomcat_running:
                self.create_running_check_arguments('tomcat', 'tomcat', server, ['webserver'])

            if True is self.__check_php_fpm_running:
                self.create_running_check('php_fpm', 'php-fpm', server, ['webserver'])

            if True is self.__check_freshclam_running:
                self.create_running_check('freshclam', 'freshclam', server, ['security', 'antivirus'])

            if True is self.__check_clamd_running:
                self.create_running_check('clamd', 'clamd', server, ['security', 'antivirus'])

            if True is DefaultLocalChecks.is_checking_postfix_running(self):
                self.create_running_check_arguments('postfix', 'postfix', server, ['mail'])

            if True is self.__check_sudoers:
                check = CheckGroupMembers.create('sudoers_group_members_' + server.get_id()) \
                    .add_service_group(ServiceGroup.create('sudoers'))
                for user in self.__sudoers:
                    check.append_user(user)

                self.apply_check(check, server)

            if True is self.__check_wheel:
                check = CheckGroupMembers.create('wheel_group_members_' + server.get_id()) \
                    .set_group('wheel') \
                    .add_service_group(ServiceGroup.create('sudoers'))
                for user in self.__sudoers:
                    check.append_user(user)

                self.apply_check(check, server)

            if True is self.__check_normal_users:
                check = CheckExistingUsers.create('existing_users_' + server.get_id())
                for user in self.__sudoers:
                    check.append_existing_users(user)
                for user in self.__additional_users:
                    check.append_existing_users(user)

                self.apply_check(check, server)

            if True is self.__check_ufw:
                check = CheckUFWStatus.create('ufw_status_' + server.get_id()) \
                    .set_incoming(self.__ufw_defaults[0]) \
                    .set_outgoing(self.__ufw_defaults[1]) \
                    .set_routing(self.__ufw_defaults[2])

                check.set_display_name(check.get_display_name() + ' ' + server.get_display_name())
                for policy in self.__ufw_rules:
                    check.add_rule(policy[0], policy[1], policy[2])

                self.apply_check(check, server)

            if True is self.__check_disk:
                if len(self.__check_partitions) == 0:
                    check = CheckDisk.create('disk_' + server.get_id())
                    self.apply_check(check, server)
                else:
                    for config in self.__check_partitions:
                        check = CheckDisk.create('disk_' + config[0] + '_' + server.get_id())
                        check.set_display_name(check.get_display_name() + ' ' + config[0]) \
                            .set_partition(config[1]) \
                            .set_warning_percent(config[2]) \
                            .set_critical_percent(config[3])
                        self.apply_check(check, server)
