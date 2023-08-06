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

from icinga2confgen.Checks.Check import Check
from icinga2confgen.Commands.NagiosPlugins.NTCommand import NTCommand
from icinga2confgen.ConfigBuilder import ConfigBuilder
from icinga2confgen.Groups.ServiceGroup import ServiceGroup
from icinga2confgen.ValueChecker import ValueChecker


class CheckNT(Check):

    def __init__(self, id):
        Check.__init__(self, id, 'CheckNT', 'nt')
        self.__host = None
        self.__warning = None
        self.__critical = None
        self.__variable = None
        self.__timeout = None
        self.__params = None
        self.__display = None
        self.add_service_group(ServiceGroup.create('ns_client'))

    def set_host(self, host):
        ValueChecker.is_string(host)
        self.__host = host
        return self

    def get_host(self):
        return self.__host

    def set_variable(self, variable):
        ValueChecker.is_string(variable)
        self.__variable = variable
        return self

    def get_variable(self):
        return self.__variable

    def set_warning(self, warning):
        ValueChecker.is_number(warning)
        self.__warning = warning
        return self

    def get_warning(self):
        return self.__warning

    def set_critical(self, critical):
        ValueChecker.is_number(critical)
        self.__critical = critical
        return self

    def get_critical(self):
        return self.__critical

    def set_timeout(self, timeout):
        ValueChecker.is_number(timeout)
        self.__timeout = timeout
        return self

    def get_timeout(self):
        return self.__timeout

    def set_params(self, params):
        ValueChecker.is_string(params)
        self.__params = params
        return self

    def get_params(self):
        return self.__params

    def set_display(self, display):
        ValueChecker.is_string(display)
        self.__display = display
        return self

    def get_display(self):
        return self.__display

    @staticmethod
    def create(id, force_create=False):
        ValueChecker.validate_id(id)
        check = None if force_create else ConfigBuilder.get_check(id)
        if None is check:
            check = CheckNT(id)
            ConfigBuilder.add_check(id, check)
        elif not isinstance(check, CheckNT):
            raise Exception('Id must be for an instance of CheckNT but other instance is returned')

        if None is ConfigBuilder.get_command('nt'):
            NTCommand.create('nt')

        return check

    def validate(self):
        if None is self.__host:
            raise Exception('You have to specify a host for ' + self.get_id())
        if None is self.__variable:
            raise Exception('You have to specify a variable for ' + self.get_id())
