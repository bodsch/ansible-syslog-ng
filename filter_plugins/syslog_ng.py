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
            'get_service': self.get_service,
            'log_directories': self.log_directories,
        }

    def get_service(self, data, search_for):
        name = None
        # count = len(data.keys())
        # display.vv("found: {} entries, use filter {}".format(count, search_for))
        regex_list_compiled = re.compile("^{}.*.service$".format(search_for))

        for k, v in data.items():
            display.v("  - {}  - {}".format(k, v))
            if(re.match(regex_list_compiled, k)):
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
            full_file_name = os.path.join(
                base_directory,
                file_name
            )

            log_dirs.append(
                os.path.dirname(full_file_name)
            )

        unique_dirs = list(dict.fromkeys(log_dirs))

        # remove base_directory
        _ = unique_dirs.remove(base_directory)

        display.v(" = result {}".format(unique_dirs))
        return unique_dirs
