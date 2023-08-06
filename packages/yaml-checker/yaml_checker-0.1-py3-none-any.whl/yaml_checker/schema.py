{
    'virtual_machine_domain': {
        'required': True,
        'type': 'string'
    },
    'vsphere_virtual_machine_folder': {
        'required': True,
        'type': 'string'
    },
    'virtual_machine_dns_servers': {
        'required': True,
        'type': 'list',
        'schema': {
            'type': 'string'
        }
    },
    'vsphere_network_name': {
        'required': True,
        'type': 'string'
    },
    'vsphere_template_name': {
        'required': True,
        'type': 'string'
    },
    'instance_count': {
        'required': True,
        'type': 'number'
    },
    'virtual_machine_name': {
        'required': True,
        'type': 'string'
    },
    'vsphere_virtual_machine_cpus': {
        'required': True,
        'type': 'string'
    },
    'vsphere_virtual_machine_memory': {
        'required': True,
        'type': 'string'
    },
    'vsphere_virtual_machine_disks': {
        'required': True,
        'type': 'list',
        'items': [{
            'type': 'dict',
            'schema': {
                'label': {
                    'type': 'string',
                    'required': True
                    },
                'size': {
                    'type': 'string',
                    'required': True
                }
            }
            }]
    }
}
