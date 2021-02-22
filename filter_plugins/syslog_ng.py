# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
from ansible.utils.display import Display

import re

__metaclass__ = type

display = Display()


class FilterModule(object):
    """
        Ansible file jinja2 tests
    """

    def filters(self):
        return {
            'get_service': self.get_service
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
