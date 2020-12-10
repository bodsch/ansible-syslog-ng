import pytest
import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.fixture()
def get_vars(host):
    defaults_files = "file=../../defaults/main.yml name=role_defaults"
    vars_files = "file=../../vars/main.yml name=role_vars"

    ansible_vars = host.ansible(
        "include_vars",
        defaults_files)["ansible_facts"]["role_defaults"]

    ansible_vars.update(host.ansible(
        "include_vars",
        vars_files)["ansible_facts"]["role_vars"])

    return ansible_vars


@pytest.mark.parametrize("dirs", [
    "/etc/syslog-ng/conf.d",
])
def test_directories(host, dirs):
    d = host.file(dirs)
    assert d.is_directory
    assert d.exists


@pytest.mark.parametrize("files", [
    "/etc/syslog-ng/syslog-ng.conf",
    "/etc/syslog-ng/conf.d/sources.conf",
    "/etc/syslog-ng/conf.d/destinations.conf",
    "/etc/syslog-ng/conf.d/filters.conf",
    "/etc/syslog-ng/conf.d/logs.conf",
])
def test_files(host, files):
    f = host.file(files)
    assert f.is_file
    assert f.exists
