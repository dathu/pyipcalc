import logging
import unittest

import pyipcalc

log = logging.getLogger(__name__)


class IPCalc(unittest.TestCase):
    def test_ipv4_network(self):
        net = pyipcalc.IPNetwork('192.168.0.0/25')
        net2 = pyipcalc.IPNetwork('192.168.0.1/30')
        net3 = pyipcalc.IPNetwork('192.168.0.128/25')
        self.assertEqual('192.168.0.0/25', net.prefix())
        self.assertEqual('192.168.0.0', net.network())
        self.assertEqual('192.168.0.1', net.first())
        self.assertEqual('192.168.0.126', net.last())
        self.assertEqual('192.168.0.127', net.broadcast())
        self.assertEqual('255.255.255.128', net.mask())
        self.assertEqual(3232235520, pyipcalc.ip_to_int('192.168.0.0'))
        self.assertEqual('192.168.0.0', pyipcalc.int_to_ip(3232235520, 4))
        self.assertEqual('255.255.255.128', net.mask())
        def contains(net1, net2):
            if net1 in net2:
                return True
            else:
                return False
            
        self.assertEqual(True, contains(net2, net))
        self.assertEqual(False, contains(net3, net))
        self.assertEqual('192.168.0.0/24', pyipcalc.supernet(net,
                         net3).prefix())
        self.assertEqual(net[5].prefix(), '192.168.0.5/32')
        for i,ip in enumerate(net[0:1]):
            self.assertEqual(ip._ip, 3232235520 + i)
        for i,ip in enumerate(net[0:3:31]):
            self.assertEqual(ip._ip, 3232235520 + i*2)


    def test_ipv6_network(self):
        net = pyipcalc.IPNetwork('fff0::/64')
        self.assertEqual('fff0:0000:0000:0000:0000:0000:0000:0000/64', net.prefix())
        self.assertEqual('fff0:0000:0000:0000:0000:0000:0000:0000', net.network())
        self.assertEqual('fff0:0000:0000:0000:0000:0000:0000:0000', net.first())
        self.assertEqual('fff0:0000:0000:0000:ffff:ffff:ffff:ffff', net.last())
        self.assertEqual(340199290171201906239764863564210241535,
                         pyipcalc.ip_to_int('fff0:0000:0000:0000:ffff:ffff:ffff:ffff'))
        self.assertEqual('fff0:0000:0000:0000:ffff:ffff:ffff:ffff',
                         pyipcalc.int_to_ip(340199290171201906239764863564210241535,
                                        6))
        self.assertEqual(pyipcalc.int_128_to_32(340199290171201906239764863564210241535),
                         (4293918720, 0, 4294967295, 4294967295))
        self.assertEqual(pyipcalc.int_32_to_128(4293918720, 0, 4294967295, 4294967295),
                         340199290171201906239764863564210241535)
