# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
from ansible.utils.display import Display

import re
import os

__metaclass__ = type

display = Display()


class FilterModule(object):
    """
    """
    def filters(self):
        return {
            'get_service': self.get_service,
            'log_directories': self.log_directories,
            'syslog_network_definition': self.syslog_network_definition,
        }

    def get_service(self, data, search_for):
        """
        """
        name = None
        regex_list_compiled = re.compile(f"^{search_for}.*")

        match = {k: v for k, v in data.items() if re.match(regex_list_compiled, k)}

        display.vv(f"found: {match}  {type(match)}")

        if isinstance(match, dict):
            values = list(match.values())[0]
            name = values.get('name', search_for).replace('.service', '')

        display.vv(f"= result {name}")
        return name

    def log_directories(self, data, base_directory):
        """
          return a list of directories
        """
        # display.v(f"log_directories(self, {data}, {base_directory})")
        log_dirs = []
        log_files = sorted([v.get('file_name') for k, v in data.items() if v.get('file_name')])
        unique = list(dict.fromkeys(log_files))
        for d in unique:
            if "/$" in d:
                clean_dir_name = d.split("/$")[0]
                log_dirs.append(clean_dir_name)

        unique_dirs = list(dict.fromkeys(log_dirs))

        log_dirs = []

        for file_name in unique_dirs:
            full_file_name = os.path.join(
                base_directory,
                file_name
            )
            log_dirs.append(full_file_name)

        display.vv(f"= result {log_dirs}")
        return log_dirs

    def validate_syslog_destination(self, data):
        """
        """
        pass

    def syslog_network_definition(self, data, conf_type="source"):
        """
        """
        result = None
        if isinstance(data, dict):
            _list = []
            network_ip = data.get("ip", None)
            network_port = data.get("port", None)
            network_spoof = data.get("spoof_source", None)
            network_fifo_size = data.get("log_fifo_size", None)
            if network_ip:
                if conf_type == "source":
                    _list.append(f"ip({network_ip})")
                else:
                    _list.append(f"\"{network_ip}\"")
            if network_port:
                _list.append(f"port({network_port})")
            if network_spoof:
                spoof = 'yes' if network_spoof else 'no'
                _list.append(f"spoof_source({spoof})")
            if network_fifo_size:
                _list.append(f"log_fifo_size({network_fifo_size})")

            result = " ".join(_list)

        if isinstance(data, str):
            result = data

        display.vv(f"= result {result}")
        return result
