# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)

from ansible.utils.color import stringc
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
            'check_obsolete_config': self.check_obsolete_config,
            'migrate_config': self.migrate_config,
            'warning' : self.warning,
            'deprecated': self.deprecated,
            'template_syslog': self.template_syslog
        }

    def var_type(self, var):
        """
          Get the type of a variable
        """
        _type = type(var).__name__

        # display.v(f" {var}, type: {_type}")

        if isinstance(var, str) or _type == "AnsibleUnsafeText":
            _type = "str"

        # display.v(f" = result {_type}")

        return _type

    def get_service(self, data, search_for):
        name = None
        # count = len(data.keys())
        # display.vv("found: {} entries, use filter {}".format(count, search_for))
        regex_list_compiled = re.compile(f"^{search_for}.*.service$")

        for k, v in data.items():
            display.v(f"  - {k}  - {v}")
            if(re.match(regex_list_compiled, k)):
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

        display.v(f" = result {unique_dirs}")
        return unique_dirs

    def check_obsolete_config(self, data):
        """
        """
        result = [k for k, v in data.items() if v.get("file_name", None)]
        # okay = [k for k, v in data.items() if not v.get("file_name", None)]
#         if len(result) > 0:
#             """
#             """
#             m = ", ".join(result)
#             msg = f"""
# The following "syslog_logs" configurations have an old syntax and should be migrated:
#   - {m}
# """
#
#             result = msg

        return result

    def migrate_config(self, data, dest, sources={}):
        """
        """
        # display.v(f"data: {data}, {dest}, sources")

        result = {}

        if dest == "syslog_destinations":
            """
            """
            _data = self.__merge_two_dicts(data, sources)
        else:
            _data = data.copy()

        for k, v in _data.items():
            """
            """
            if dest == "syslog_logs" and v.get("file_name", None):
                _ = v.pop("file_name")

            if dest == "syslog_destinations":
                if v.get("filter", None):
                    _ = v.pop("filter")

        return _data


    def warning(self, data, columns, hostname, version):
        """
        """
        display.columns = int(columns)

        msg = f"""
{hostname}: {data}
This feature will be removed in version {version}"""

        return display.warning(msg, formatted = True)

    def deprecated(self, data, version):
        """
        """
        display.columns = 95
        return display.deprecated(data, version=version)


    def __merge_two_dicts(self, x, y):
        z = x.copy()   # start with x's keys and values
        z.update(y)    # modifies z with y's keys and values & returns None
        return z

    def template_syslog(self, data):
        """
        """
        display.v(f"template_syslog({data})")

        _transport = data.get("transport", None)
        _port = data.get("port", None)

        if not _transport or not _transport in ["udp", "tcp", "tls"]:
            _transport = "udp"

        if _transport == "udp" and not _port:
            _port = 514

        if _transport == "tcp" and not _port:
            _port = 601

        if _transport == "tls" and not _port:
            _port = 6514

        return _transport, _port


