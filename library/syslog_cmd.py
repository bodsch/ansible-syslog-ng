#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2020, Bodo Schulz <bodo@boone-schulz.de>
# BSD 2-clause (see LICENSE or https://opensource.org/licenses/BSD-2-Clause)

from __future__ import absolute_import, print_function

import re

from ansible.module_utils.basic import AnsibleModule


class SyslogNgCmd(object):
    module = None

    def __init__(self, module):
        """
          Initialize all needed Variables
        """
        self.module = module

        self._syslog_ng_bin = module.get_bin_path('syslog-ng', True)
        self.parameters = module.params.get("parameters")

    def run(self):
        ''' ... '''
        result = dict(
            failed=True,
            ansible_module_results='failed'
        )

        parameter_list = self._flatten_parameter()

        if(not self._syslog_ng_bin):
            return dict(
                rc = 1,
                failed = True,
                msg = "no installed syslog-ng found"
            )

        rc, out, err = self._exec(self.parameters)
        self.module.log(msg="  rc : '{}'".format(rc))
        self.module.log(msg="  out: '{}'".format(out))
        self.module.log(msg="  err: '{}'".format(err))

        if('--version' in parameter_list):
            """
              get version"
            """
            pattern = re.compile(r'.*Installer-Version: (?P<version>\d\.\d+)\.', re.MULTILINE)
            version = re.search(pattern, out)
            version = version.group(1)

            self.module.log(msg="version: '{}'".format(version))

            if(rc == 0):
                return dict(
                    rc = 0,
                    failed = False,
                    version = version
                )

        if('--syntax-only' in parameter_list):
            """
              check syntax
            """
            if(rc == 0):
                return dict(
                    rc = rc,
                    failed = False,
                    msg = "syntax okay"
                )
            else:
                return dict(
                    rc = rc,
                    failed = True,
                    msg = out
                )

        return result

    def _exec(self, args):
        '''   '''

        cmd = [self._syslog_ng_bin] + args
        # self.module.log(msg="cmd: {}".format(cmd))
        rc, out, err = self.module.run_command(cmd, check_rc=True)
        return rc, out, err

    def _flatten_parameter(self):
        """
          split and flatten parameter list

          input:  ['--validate', '--log-level debug']
          output: ['--validate', '--log-level', 'debug']
        """
        parameters = []

        for _parameter in self.parameters:
            if(' ' in _parameter):
                _list = _parameter.split(' ')
                for _element in _list:
                    parameters.append(_element)
            else:
                parameters.append(_parameter)

        return parameters

# ===========================================
# Module execution.
#


def main():

    module = AnsibleModule(
        argument_spec=dict(
            parameters=dict(required=True, type='list'),
        ),
        supports_check_mode=True,
    )

    icinga = SyslogNgCmd(module)
    result = icinga.run()

    module.exit_json(**result)


# import module snippets
if __name__ == '__main__':
    main()
