# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
from ansible.utils.display import Display

import re
import os

__metaclass__ = type

display = Display()


class FilterModule(object):
    """
        Ansible file jinja2 tests
    """

    def filters(self):
        return {
            'type': self.var_type,
            'get_service': self.get_service,
            'log_directories': self.log_directories,
        }

    def var_type(self, var):
        '''
        Get the type of a variable
        '''
        # display.v("var   : {} ({})".format(var, type(var)))
        # display.v("result: {}".format(type(var).__name__))

        _type = type(var).__name__

        display.v(f" {var}, type: {_type}")

        if (isinstance(var, str) or _type == "AnsibleUnsafeText"):
            _type = "str"

        display.v(f" = result {_type}")

        return _type

    def get_service(self, data, search_for):
        name = None
        # count = len(data.keys())
        # display.vv("found: {} entries, use filter {}".format(count, search_for))
        regex_list_compiled = re.compile("^{}.*.service$".format(search_for))

        for k, v in data.items():
            display.v("  - {}  - {}".format(k, v))
            if (re.match(regex_list_compiled, k)):
                # display.v("  = {}  - {}".format(k, v))
                name = v.get('name')
                break

        name = name.replace('.service', '')
        return name

    def log_directories(self, data, base_directory):
        """
          return a list of directories
        """
        log_dirs = []

        for k, v in data.items():
            file_name = v.get('file_name', f"{k}.log")
            # display.v(f" {file_name}")
            full_file_name = os.path.join(
                base_directory,
                file_name
            )

            log_dirs.append(
                os.path.dirname(full_file_name)
            )

        # display.v(f" {log_dirs}")
        unique_dirs = list(dict.fromkeys(log_dirs))

        # remove base_directory
        _ = unique_dirs.remove(base_directory)

        # display.v(f" unique_dirs: {unique_dirs} ({type(unique_dirs)})")

        log_dirs = []
        for d in unique_dirs:
            if "/$" in d:
                clean_dir_name = d.split("/$")[0]
                log_dirs.append(clean_dir_name)

        display.v(f"= result {log_dirs}")
        return log_dirs

