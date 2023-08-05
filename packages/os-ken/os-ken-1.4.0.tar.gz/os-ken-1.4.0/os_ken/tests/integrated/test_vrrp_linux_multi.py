# Copyright (C) 2013 Nippon Telegraph and Telephone Corporation.
# Copyright (C) 2013 Isaku Yamahata <yamahata at valinux co jp>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

r"""
Usage:
osken-manager --verbose \
    os_ken.services.protocols.vrrp.dumper \
    os_ken.services.protocols.vrrp.sample_manager.py \
    os_ken.tests.integrated.test_vrrp_linux_multi \
    os_ken.app.rest

os_ken.services.protocols.vrrp.dumper is optional.
os_ken.app.rest is merely to prevent osken-manager from exiting.

                    ----------------
      /--<--veth0-->|              |
   OSKen            | linux bridge |<--veth2--> command to generate packets
      \--<--veth1-->|   (vrrpbr)   |
                    ----------------


# ip link add veth0 type veth peer name veth0-br
# ip link add veth1 type veth peer name veth1-br
# ip link add veth2 type veth peer name veth2-br

# ip link add vrrpbr type bridge
# ip link set dev veth0-br master vrrpbr
# ip link set dev veth1-br master vrrpbr
# ip link set dev veth2-br master vrrpbr

# ip link set veth0 up
# ip link set veth0-br up
# ip link set veth1 up
# ip link set veth1-br up
# ip link set veth2 up
# ip link set veth2-br up
# ip link set vrrpbr up

if you like, capture packets on each interfaces like
# tshark -i vrrpbr
# tshark -i veth0
# tshark -i veth1
# tshark -i veth2

virtual router mac address: 00:00:5E:00:01:{VRID} = 00:00:5E:00:01:07
during working, send packets destined to mac address 00:00:5E:00:01:07
from veth2 by packet generator like packeth

NOTE: vrid: 7 and ip address: 10.0.0.1... are hardcoded below
"""

from os_ken.base import app_manager
from os_ken.lib import hub
from os_ken.lib import mac as lib_mac
from os_ken.lib.packet import vrrp
from os_ken.services.protocols.vrrp import api as vrrp_api
from os_ken.services.protocols.vrrp import event as vrrp_event
from os_ken.services.protocols.vrrp import monitor_linux

from . import vrrp_common


class VRRPConfigApp(vrrp_common.VRRPCommon):
    _IFNAME0 = 'veth0'
    _IFNAME1 = 'veth1'

    def __init__(self, *args, **kwargs):
        super(VRRPConfigApp, self).__init__(*args, **kwargs)

    def start(self):
        hub.spawn(self._main)

    def _configure_vrrp_router(self, vrrp_version, priority,
                               primary_ip_address, ifname, vrid):
        interface = vrrp_event.VRRPInterfaceNetworkDevice(
            lib_mac.DONTCARE_STR, primary_ip_address, None, ifname)
        self.logger.debug('%s', interface)

        vip = '10.0.%d.1' % vrid
        ip_addresses = [vip]
        config = vrrp_event.VRRPConfig(
            version=vrrp_version, vrid=vrid, priority=priority,
            ip_addresses=ip_addresses)
        self.logger.debug('%s', config)

        rep = vrrp_api.vrrp_config(self, interface, config)
        self.logger.debug('%s', rep)

        return rep
