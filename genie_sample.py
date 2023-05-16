from genie.testbed import load
from genie.libs.sdk.apis.utils import compare_dict

# Load the testbed file
testbed = load('testbed.yaml')

# Define the golden template
golden_template = {
    'ip': {
        'domain': {
            'lookup-settings': {
                'lookup': {
                    'source-interface': {
                        'Vlan': '(mgmt_vlan_number)'
                    }
                }
            },
            'name': '(facility).chevrontexaco.net'
        },
        'name-server': {
            'APAC': {
                'no-vrf': [
                    '146.40.4.34',
                    '146.45.8.34',
                    '146.40.46.35',
                    '146.40.112.32',
                    '146.40.224.16'
                ]
            },
            'EMEA': {
                'no-vrf': [
                    '146.38.64.8',
                    '146.38.32.8',
                    '146.27.66.35'
                ]
            },
            'US': {
                'no-vrf': [
                    '146.36.82.34',
                    '146.36.80.34',
                    '146.27.66.35',
                    '146.27.66.36'
                ]
            }
        },
        'forward-protocol': {
            'udp': {
                'domain': False,
                'nameserver': False,
                'netbios-dgm': False,
                'netbios-ns': False,
                'tacacs': False,
                'tftp': False,
                'time': False
            }
        },
        'ftp': {
            'source-interface': {
                'Vlan': '(mgmt_vlan_number)'
            }
        },
        'source-route': False,
        'ssh': {
            'version': 2
        },
        'tcp': {
            'path-mtu-discovery': {}
        },
        'tftp': {
            'source-interface': {
                'Vlan': '(mgmt_vlan_number)'
            }
        },
        'access-list': {
            'standard': [
                {
                    'name': 'cvx-snmpv3-acl',
                    'access-list-seq-rule': [
                        {
                            'sequence': '10',
                            'permit': {
                                'std-ace': {
                                    'ipv4-prefix': '146.22.71.201'
                                }
                            }
                        }
                    ]
                }
            ]
        }
    }
}

# Define the compliance check function
def compliance_check(device, golden_template):
    device.connect(log_stdout=False)
    device.execute('terminal length 0')
    output = device.execute('show running-config')
    device.disconnect()

    # Parse the device's running configuration
    parsed_output = genie.parsergen.oper_fill_tabular(device_output=output, device_os='iosxe')

    # Compare the parsed output with the golden template
    result = compare_dict(parsed_output, golden_template)

    return result

# Perform compliance check for each device in the testbed
for device_name, device in testbed.devices.items():
    print(f"Performing compliance check for device: {device_name}")
    result = compliance_check(device, golden_template)
    if result:
        print("Device is compliant with the golden template")
    else:
        print("Device is not compliant with the golden template")
