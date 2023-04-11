#!/usr/bin/env python

#### Installation #################################
#
# apt-get install python-pip
# pip install requests
# pip install lxml
# # if lxml failes, try   "apt-get install python-lxml"
# pip install fritzconnection
#
###################################################

import sys


class FritzDevice(object):

    fc = None
    ip = None
    user = None
    password = None

    def __init__(self, ip, user, password):
        from fritzconnection import FritzConnection
        self.fc = FritzConnection(address=ip, user=user, password=password)
        self.ip = ip
        self.password = password
        self.user = user

    def get_data(self, service, action):
        return self.fc.call_action(service, action)

    @property
    def services(self):
        import fritzconnection as _fc
        return _fc.print_api(address=self.ip, user=self.user, password=self.password)


class Information(FritzDevice):

    def fetch(self, service, action, keys=[]):
        data = ""

        if not isinstance(action, (list, tuple)):
            action = [action]

        for a in action:
            ret = self.get_data(service, a)

            if keys:
                ks = keys
            else:
                ks = ret.keys()

            for key in ks:
                try:
                    data += "%s:%s " % (key, ret[key])
                except KeyError:
                    continue

        return data

    @property
    def ext_ip_address(self):
        # external IP Address
        service = 'WANIPConn1'
        action = 'GetExternalIPAddress'
        keys = [
        'NewExternalIPAddress',
        ]

        return self.fetch(service, action, keys)

    @property
    def dsl_information(self):
        # DSL Information
        service = 'WANDSLInterfaceConfig'
        action = 'GetInfo'
        keys = [
        'NewUpstreamAttenuation',
        'NewUpstreamPower',
        'NewDownstreamCurrRate',
        'NewDownstreamMaxRate',
        'NewUpstreamNoiseMargin',
        'NewDownstreamPower',
        'NewUpstreamMaxRate',
        'NewDownstreamNoiseMargin',
        'NewDownstreamAttenuation',
        'NewUpstreamCurrRate',
        ]

        return self.fetch(service, action, keys)

    @property
    def wan_information(self):
        # WAN Information
        service = 'WANCommonIFC1'
        action = 'GetAddonInfos'
        keys = [
          'NewX_AVM_DE_TotalBytesSent64',
          'NewX_AVM_DE_TotalBytesReceived64'
        ]

        return self.fetch(service, action, keys)


def run():

    arguments = sys.argv
    arguments.pop(0)
    ip, user, password, arg = arguments

    fc = Information(ip, user, password)

    if arg == "api_description":
        ret = fc.services
    elif arg == "dslinfo":
        ret = fc.dsl_information
    elif arg == "traffic":
        ret = fc.wan_information
    elif arg == 'ext_ip_address':
        ret = fc.ext_ip_address
    else:
        ret = "unknown Argument"

    return ret


if __name__ == '__main__':
    output = run()
    print(output)

