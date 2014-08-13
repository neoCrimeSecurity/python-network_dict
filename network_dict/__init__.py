#!/usr/bin/env python
#
# (C) Copyright 2014 Michael Henry aka neoCrimeLabs ( http://neocri.me/ )
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the GNU Lesser General Public License
# (LGPL) version 2.1 which accompanies this distribution, and is available at
# http://www.gnu.org/licenses/lgpl-2.1.html
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# Contributors:
#     Michael Henry aka neoCrimeLabs ( http://neocri.me/ )

from netaddr import *

class NetworkDict:


    def __init__(self, networks = {}, debug = False, format = 'value', firstHit = True, ignoreHosts = True ):
        self.networks    = {}
        self.bits        = []
        self.debug       = debug
        self.format      = str(format).lower()
        self.firstHit    = firstHit
        self.ignoreHosts = ignoreHosts

        for cidr, value in networks.iteritems():
            self._addNetwork(cidr, value)

    def _format(self,key,value):
        if self.format == 'both':
            return (str(key), value)
        elif self.format == 'value':
            return value
        elif self.format == 'key':
            return str(key)
        else:
            raise TypeError('Invalid return format, must be: "key", "value", or "both".')


    def _addNetwork(self, key, value):
        ip = IPNetwork(key)

        if self.ignoreHosts == True:
            IPv4 = (ip.prefixlen == 32)  & (ip.version == 4)
            IPv6 = (ip.prefixlen == 128) & (ip.version == 6)
            if (IPv4 | IPv6):
                return

        if ip.prefixlen not in self.networks:
            self.networks[ip.prefixlen] = {}
            self._cache_bits()

        self.networks[ip.prefixlen][ip.cidr] = value


    def _cache_bits(self):
        # So we don't need to do this with every query
        self.bits = sorted(self.networks.keys(), reverse=True)


    def __len__(self):
        ret = 0
        for mask in self.bits:
            ret += len(self.networks[mask])

        return ret


    def _getNetworks(self, key):
        ip   = IPNetwork(key)
        bits = ip.prefixlen
        ret  = []

        for mask in self.bits:
            if bits >= mask:
                ip.prefixlen = mask
                if ip.cidr in self.networks[mask]:
                    if self.firstHit is True:
                        ret = self._format(ip.cidr, self.networks[mask][ip.cidr])
                        break
                    else:
                        ret.append(self._format(ip.cidr, self.networks[mask][ip.cidr]))
        return ret


    def __getitem__(self, key, default=None):
        ret = self._getNetworks(key)

        if len(ret) == 0:
            if default is None:
                raise KeyError('No matching networks found, and no default network set')
            else:
                ret = [self._format(IPNetwork(key).cidr, default)]

        return ret


    def __contains__(self, key):
        ret = self._getNetworks(key)

        if len(ret) == 0:
            return False
        else:
            return True


    def pop(self, key, default=None):
        ip  = IPNetwork(key)
        ret = None

        if ip.prefixlen in networks:
            if ip.cidr in networks[ip.prefixlen]:
                ret = networks[ip.prefixlen][ip.cidr]
                del networks[ip.prefixlen][ip.cidr]
                if len(networks[ip.prefixlen]) == 0:
                    del(networks[ip.prefixlen])
                    self._cache_bits()

        if ret is None:
            if default is None:
                raise KeyError('No matching network found. Deletion requires exact network/netmask to work.')
            else:
                return self._format(ip.cidr,default)
        else:
            return self._format(ip.cidr, ret)


    def keys(self):
        ret = []
        for mask in sorted(self.bits):  # larger networks first
            for network in self.networks[mask].keys():
                ret.append(str(network))
        return ret


    def values(self):
        ret = []
        for mask in sorted(self.bits):  # larger networks first
            ret += self.networks[mask].values()
        return ret


    def items(self):
        ret = []
        for mask in sorted(self.bits):  # larger networks first
            for network,value in self.networks[mask].iteritems():
                ret.append((str(network), value))
        return ret

    def clear(self):
        self.networks = {}
        self.bits     = []


    def setdefault(self, key, default=None):
        value = self._getNetworks(key)

        if len(value) == 0:
            if default is None:
                raise KeyError('No matching network found, and no default value supplied')
            else:
                self.__setitem__(key, default)
                return [self._format(IPNetwork(key).cidr, default)]
        else:
            return value

    def __dict__(self):
        return dict(self.items())

    def __str__(self):
        return str(dict(self.items()))

    def __repr__(self):
        return "NetworkDict(%s)" % str(dict(self.items()))

    # Aliased Methods
    has_key    = __contains__
    get        = __getitem__
    iterkeys   = keys
    itervalues = values
    iteritems  = items
    viewkeys   = keys
    viewvalues = values
    viewitems  = items
    __delitem__= pop
    __int__    = __len__
    __setitem__= _addNetwork
