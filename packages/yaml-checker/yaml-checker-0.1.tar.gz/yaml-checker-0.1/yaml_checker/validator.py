import yaml
from cerberus import Validator
import sys
import json
import os


LIMITS = {
    "instance_count": {"min": 1, "max":3},
    "domain": ["msgreen.dom", "msorange.dom", "msred.dom"],
    "folder": "TEST",
    "dns_servers": ["172.30.170.130", "172.30.170.131"],
    "network_name": ["VLAN192", "VLAN194", "VLAN20"],
    "template_name": "Templates/Template_CentOS_7.7_IAC",
    "details": [{"cpu": "2", "memory": "4096", "disk": "120", "label": "disk0"},
                {"cpu": "4", "memory": "4096", "disk": "120", "label": "disk0"},
                {"cpu": "4", "memory": "8192", "disk": "120", "label": "disk0"},
                {"cpu": "4", "memory": "12288", "disk": "120", "label": "disk0"},
                {"cpu": "10", "memory": "24576", "disk": "120", "label": "disk0"}]
}

PARSED_YAML = None

def load_yaml_file(path_to_yaml='sample.yml'):
    with open(path_to_yaml) as yaml_file:
        global PARSED_YAML
        PARSED_YAML = yaml.load(yaml_file, Loader=yaml.FullLoader)


def validate_yaml(path_to_schema='yaml_checker/schema.py'):
    validation_schema = eval(open(path_to_schema).read())
    v = Validator(validation_schema)
    validation_result = v.validate(PARSED_YAML, validation_schema)
    
    if not validation_result:
        raise ValueError(v.errors)


def validate_content():
    yaml_errors = []

    try:
        assert PARSED_YAML.get("instance_count") in range(LIMITS.get("instance_count").get("min"), \
                                                          LIMITS.get("instance_count").get("max") + 1), \
            "Instance Count is beyond threshold, actual: {}".format(PARSED_YAML.get("instance_count"))
    except AssertionError as e:
        yaml_errors.append(str(e))

    try:
        assert PARSED_YAML.get("virtual_machine_domain") in LIMITS.get("domain"), \
            "Domain is misconfigured, actual: {}".format(PARSED_YAML.get("virtual_machine_domain"))
    except AssertionError as e:
        yaml_errors.append(str(e))

    try:
        assert PARSED_YAML.get("vsphere_virtual_machine_folder") == LIMITS.get("folder"), \
            "Virtual machine folder is misconfigured, actual: {}".format(PARSED_YAML.get("vsphere_virtual_machine_folder"))
    except AssertionError as e:
        yaml_errors.append(str(e))

    try:
        assert PARSED_YAML.get("virtual_machine_dns_servers") == LIMITS.get("dns_servers"), \
            "Virtual machine DNS is misconfigured, actual: {}".format(PARSED_YAML.get("virtual_machine_dns_servers"))
    except AssertionError as e:
        yaml_errors.append(str(e))

    try:
        assert PARSED_YAML.get("vsphere_network_name") in LIMITS.get("network_name"), \
            "Network name is misconfigured, actual: {}".format(PARSED_YAML.get("vsphere_network_name"))
    except AssertionError as e:
        yaml_errors.append(str(e))

    try:
        assert PARSED_YAML.get("vsphere_template_name") == LIMITS.get("template_name"), \
            "Template name is misconfigured, actual: {}".format(PARSED_YAML.get("vsphere_template_name"))
    except AssertionError as e:
        yaml_errors.append(str(e))

    machine_details = {
        "cpu": PARSED_YAML.get("vsphere_virtual_machine_cpus"),
        "memory": PARSED_YAML.get("vsphere_virtual_machine_memory"),
        "disk": PARSED_YAML.get("vsphere_virtual_machine_disks")[0].get("size"),
        "label": PARSED_YAML.get("vsphere_virtual_machine_disks")[0].get("label")
    }

    try:
        assert machine_details in LIMITS.get("details"), \
            "Machine type is misconfigured, actual: {}".format(machine_details)
    except AssertionError as e:
        yaml_errors.append(str(e))
    
    if yaml_errors:
        raise ValueError(yaml_errors)


def validate(yaml):
    load_yaml_file(path_to_yaml=yaml)
    validate_yaml()
    validate_content()

if __name__ == "__main__":
    validate(yaml=sys.argv[1])
