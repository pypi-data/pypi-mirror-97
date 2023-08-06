

class Device(object):
    """Generated from OpenAPI schema object #/components/schemas/Device

    A container for emulated protocol devices  

    Args
    ----
    - name (str): Unique system wide name of an object that is also the primary key for objects found in arrays
    - container_name (str): The unique name of a Port or Lag object that will contain the emulated interfaces and/or devices
    - device_count (int): The number of emulated protocol devices or interfaces per port
     Example: If the device_count is 10 and the choice property value is ethernet then an implementation MUST create 10 ethernet interfaces
     The ethernet property is a container for src, dst and eth_type properties with each on of those properties being a pattern container for 10 possible values
     If an implementation is unable to support the maximum device_count it MUST indicate what the maximum device_count is using the /results/capabilities API
     The device_count is also used by the individual child properties that are a container for a /components/schemas/Device
     Pattern
    - choice (Union[Ethernet, Ipv4, Ipv6, Bgpv4]): The type of emulated protocol interface or device
    """
    _CHOICE_MAP = {
        'Ethernet': 'ethernet',
        'Ipv4': 'ipv4',
        'Ipv6': 'ipv6',
        'Bgpv4': 'bgpv4',
    }
    def __init__(self, name=None, container_name=None, device_count=1, choice=None):
        from abstract_open_traffic_generator.device import Ethernet
        from abstract_open_traffic_generator.device import Ipv4
        from abstract_open_traffic_generator.device import Ipv6
        from abstract_open_traffic_generator.device import Bgpv4
        if isinstance(choice, (Ethernet, Ipv4, Ipv6, Bgpv4)) is False:
            raise TypeError('choice must be of type: Ethernet, Ipv4, Ipv6, Bgpv4')
        self.__setattr__('choice', Device._CHOICE_MAP[type(choice).__name__])
        self.__setattr__(Device._CHOICE_MAP[type(choice).__name__], choice)
        if isinstance(name, (str)) is True:
            import re
            assert(bool(re.match(r'^[\sa-zA-Z0-9-_()><\[\]]+$', name)) is True)
            self.name = name
        else:
            raise TypeError('name must be an instance of (str)')
        if isinstance(container_name, (str)) is True:
            self.container_name = container_name
        else:
            raise TypeError('container_name must be an instance of (str)')
        if isinstance(device_count, (float, int, type(None))) is True:
            self.device_count = device_count
        else:
            raise TypeError('device_count must be an instance of (float, int, type(None))')


class Ethernet(object):
    """Generated from OpenAPI schema object #/components/schemas/Device.Ethernet

    Emulated ethernet protocol  
    A top level in the emulated device stack  

    Args
    ----
    - name (str): Unique system wide name of an object that is also the primary key for objects found in arrays
    - mac (Pattern): A container for emulated device property patterns
     Media access control address (MAC) is a 48bit identifier for use as a network address
     The value can be an int or a hex string with or without spaces or colons separating each byte
     The min value is 0 or '00:00:00:00:00:00'
     The max value is 281474976710655 or 'FF:FF:FF:FF:FF:FF'
    - mtu (Pattern): A container for emulated device property patterns
    - vlans (list[Vlan]): List of vlans
    """
    def __init__(self, name=None, mac=None, mtu=None, vlans=[]):
        from abstract_open_traffic_generator.device import Pattern
        if isinstance(name, (str)) is True:
            import re
            assert(bool(re.match(r'^[\sa-zA-Z0-9-_()><\[\]]+$', name)) is True)
            self.name = name
        else:
            raise TypeError('name must be an instance of (str)')
        if isinstance(mac, (Pattern, type(None))) is True:
            self.mac = mac
        else:
            raise TypeError('mac must be an instance of (Pattern, type(None))')
        if isinstance(mtu, (Pattern, type(None))) is True:
            self.mtu = mtu
        else:
            raise TypeError('mtu must be an instance of (Pattern, type(None))')
        if isinstance(vlans, (list, type(None))) is True:
            self.vlans = [] if vlans is None else list(vlans)
        else:
            raise TypeError('vlans must be an instance of (list, type(None))')


class Pattern(object):
    """Generated from OpenAPI schema object #/components/schemas/Device.Pattern

    A container for emulated device property patterns  

    Args
    ----
    - choice (Union[str, list, Counter, Random]): TBD
    """
    _CHOICE_MAP = {
        'str': 'fixed',
        'list': 'list',
        'Counter': 'counter',
        'Random': 'random',
    }
    def __init__(self, choice=None):
        from abstract_open_traffic_generator.device import Counter
        from abstract_open_traffic_generator.device import Random
        if isinstance(choice, (str, list, Counter, Random)) is False:
            raise TypeError('choice must be of type: str, list, Counter, Random')
        self.__setattr__('choice', Pattern._CHOICE_MAP[type(choice).__name__])
        self.__setattr__(Pattern._CHOICE_MAP[type(choice).__name__], choice)


class Counter(object):
    """Generated from OpenAPI schema object #/components/schemas/Device.Counter

    An incrementing pattern  

    Args
    ----
    - start (str): TBD
    - step (str): TBD
    - up (Union[True, False]): TBD
    """
    def __init__(self, start=None, step=None, up=True):
        if isinstance(start, (str, type(None))) is True:
            self.start = start
        else:
            raise TypeError('start must be an instance of (str, type(None))')
        if isinstance(step, (str, type(None))) is True:
            self.step = step
        else:
            raise TypeError('step must be an instance of (str, type(None))')
        if isinstance(up, (bool, type(None))) is True:
            self.up = up
        else:
            raise TypeError('up must be an instance of (bool, type(None))')


class Random(object):
    """Generated from OpenAPI schema object #/components/schemas/Device.Random

    A repeatable random range pattern  

    Args
    ----
    - min (str): TBD
    - max (str): TBD
    - step (Union[float, int]): TBD
    - seed (str): TBD
    """
    def __init__(self, min=None, max=None, step=None, seed=None):
        if isinstance(min, (str, type(None))) is True:
            self.min = min
        else:
            raise TypeError('min must be an instance of (str, type(None))')
        if isinstance(max, (str, type(None))) is True:
            self.max = max
        else:
            raise TypeError('max must be an instance of (str, type(None))')
        if isinstance(step, (float, int, type(None))) is True:
            self.step = step
        else:
            raise TypeError('step must be an instance of (float, int, type(None))')
        if isinstance(seed, (str, type(None))) is True:
            self.seed = seed
        else:
            raise TypeError('seed must be an instance of (str, type(None))')


class Vlan(object):
    """Generated from OpenAPI schema object #/components/schemas/Device.Vlan

    Emulated vlan protocol  

    Args
    ----
    - name (str): Unique system wide name of an object that is also the primary key for objects found in arrays
    - tpid (Pattern): A container for emulated device property patterns
     Vlan tag protocol identifier
    - priority (Pattern): A container for emulated device property patterns
     Vlan priority
    - id (Pattern): A container for emulated device property patterns
     Vlan id
    """
    
    TPID_8100 = '8100'
    TPID_88A8 = '88a8'
    TPID_9100 = '9100'
    TPID_9200 = '9200'
    TPID_9300 = '9300'
    
    def __init__(self, name=None, tpid=None, priority=None, id=None):
        from abstract_open_traffic_generator.device import Pattern
        if isinstance(name, (str)) is True:
            import re
            assert(bool(re.match(r'^[\sa-zA-Z0-9-_()><\[\]]+$', name)) is True)
            self.name = name
        else:
            raise TypeError('name must be an instance of (str)')
        if isinstance(tpid, (Pattern, type(None))) is True:
            self.tpid = tpid
        else:
            raise TypeError('tpid must be an instance of (Pattern, type(None))')
        if isinstance(priority, (Pattern, type(None))) is True:
            self.priority = priority
        else:
            raise TypeError('priority must be an instance of (Pattern, type(None))')
        if isinstance(id, (Pattern, type(None))) is True:
            self.id = id
        else:
            raise TypeError('id must be an instance of (Pattern, type(None))')


class Ipv4(object):
    """Generated from OpenAPI schema object #/components/schemas/Device.Ipv4

    Emulated ipv4 protocol  

    Args
    ----
    - name (str): Unique system wide name of an object that is also the primary key for objects found in arrays
    - address (Pattern): A container for emulated device property patterns
     The ipv4 address
    - gateway (Pattern): A container for emulated device property patterns
     The ipv4 address of the gateway
    - prefix (Pattern): A container for emulated device property patterns
     The prefix of the ipv4 address
    - ethernet (Ethernet): Emulated ethernet protocol
     A top level in the emulated device stack
    """
    def __init__(self, name=None, address=None, gateway=None, prefix=None, ethernet=None):
        from abstract_open_traffic_generator.device import Pattern
        from abstract_open_traffic_generator.device import Ethernet
        if isinstance(name, (str)) is True:
            import re
            assert(bool(re.match(r'^[\sa-zA-Z0-9-_()><\[\]]+$', name)) is True)
            self.name = name
        else:
            raise TypeError('name must be an instance of (str)')
        if isinstance(address, (Pattern, type(None))) is True:
            self.address = address
        else:
            raise TypeError('address must be an instance of (Pattern, type(None))')
        if isinstance(gateway, (Pattern, type(None))) is True:
            self.gateway = gateway
        else:
            raise TypeError('gateway must be an instance of (Pattern, type(None))')
        if isinstance(prefix, (Pattern, type(None))) is True:
            self.prefix = prefix
        else:
            raise TypeError('prefix must be an instance of (Pattern, type(None))')
        if isinstance(ethernet, (Ethernet, type(None))) is True:
            self.ethernet = ethernet
        else:
            raise TypeError('ethernet must be an instance of (Ethernet, type(None))')


class Ipv6(object):
    """Generated from OpenAPI schema object #/components/schemas/Device.Ipv6

    Emulated ipv6 protocol  

    Args
    ----
    - name (str): Unique system wide name of an object that is also the primary key for objects found in arrays
    - address (Pattern): A container for emulated device property patterns
    - gateway (Pattern): A container for emulated device property patterns
    - prefix (Pattern): A container for emulated device property patterns
    - ethernet (Ethernet): Emulated ethernet protocol
     A top level in the emulated device stack
    """
    def __init__(self, name=None, address=None, gateway=None, prefix=None, ethernet=None):
        from abstract_open_traffic_generator.device import Pattern
        from abstract_open_traffic_generator.device import Ethernet
        if isinstance(name, (str)) is True:
            import re
            assert(bool(re.match(r'^[\sa-zA-Z0-9-_()><\[\]]+$', name)) is True)
            self.name = name
        else:
            raise TypeError('name must be an instance of (str)')
        if isinstance(address, (Pattern, type(None))) is True:
            self.address = address
        else:
            raise TypeError('address must be an instance of (Pattern, type(None))')
        if isinstance(gateway, (Pattern, type(None))) is True:
            self.gateway = gateway
        else:
            raise TypeError('gateway must be an instance of (Pattern, type(None))')
        if isinstance(prefix, (Pattern, type(None))) is True:
            self.prefix = prefix
        else:
            raise TypeError('prefix must be an instance of (Pattern, type(None))')
        if isinstance(ethernet, (Ethernet, type(None))) is True:
            self.ethernet = ethernet
        else:
            raise TypeError('ethernet must be an instance of (Ethernet, type(None))')


class Bgpv4(object):
    """Generated from OpenAPI schema object #/components/schemas/Device.Bgpv4

    Emulated BGPv4 router and routes  

    Args
    ----
    - name (str): Unique system wide name of an object that is also the primary key for objects found in arrays
    - router_id (Pattern): A container for emulated device property patterns
     specifies BGP router identifier
     It must be the string representation of an IPv4 address
    - as_number (Pattern): A container for emulated device property patterns
     Autonomous system (AS) number of 4 byte
    - as_type (Union[ibgp, ebgp]): The type of BGP autonomous system
     External BGP (EBGP) is used for BGP links between two or more autonomous systems
     Internal BGP (IBGP) is used within a single autonomous system
    - hold_time_interval (Pattern): A container for emulated device property patterns
     Number of seconds the sender proposes for the value of the Hold Timer
    - keep_alive_interval (Pattern): A container for emulated device property patterns
     Number of seconds between transmissions of Keep Alive messages by router
    - dut_ipv4_address (Pattern): A container for emulated device property patterns
     IPv4 address of the BGP peer for the session
    - dut_as_number (Pattern): A container for emulated device property patterns
     Autonomous system (AS) number of the BGP peer router (DUT)
    - ipv4 (Ipv4): Emulated ipv4 protocolThe ipv4 stack that the bgp4 protocol is implemented over
    - bgpv4_route_range (list[Bgpv4RouteRange]): Emulated BGPv4 route range
    - bgpv6_route_range (list[Bgpv6RouteRange]): Emulated bgpv6 route range
    """
    def __init__(self, name=None, router_id=None, as_number=None, as_type=None, hold_time_interval=None, keep_alive_interval=None, dut_ipv4_address=None, dut_as_number=None, ipv4=None, bgpv4_route_range=[], bgpv6_route_range=[]):
        from abstract_open_traffic_generator.device import Pattern
        from abstract_open_traffic_generator.device import Ipv4
        if isinstance(name, (str)) is True:
            import re
            assert(bool(re.match(r'^[\sa-zA-Z0-9-_()><\[\]]+$', name)) is True)
            self.name = name
        else:
            raise TypeError('name must be an instance of (str)')
        if isinstance(router_id, (Pattern, type(None))) is True:
            self.router_id = router_id
        else:
            raise TypeError('router_id must be an instance of (Pattern, type(None))')
        if isinstance(as_number, (Pattern, type(None))) is True:
            self.as_number = as_number
        else:
            raise TypeError('as_number must be an instance of (Pattern, type(None))')
        if isinstance(as_type, (str, type(None))) is True:
            self.as_type = as_type
        else:
            raise TypeError('as_type must be an instance of (str, type(None))')
        if isinstance(hold_time_interval, (Pattern, type(None))) is True:
            self.hold_time_interval = hold_time_interval
        else:
            raise TypeError('hold_time_interval must be an instance of (Pattern, type(None))')
        if isinstance(keep_alive_interval, (Pattern, type(None))) is True:
            self.keep_alive_interval = keep_alive_interval
        else:
            raise TypeError('keep_alive_interval must be an instance of (Pattern, type(None))')
        if isinstance(dut_ipv4_address, (Pattern, type(None))) is True:
            self.dut_ipv4_address = dut_ipv4_address
        else:
            raise TypeError('dut_ipv4_address must be an instance of (Pattern, type(None))')
        if isinstance(dut_as_number, (Pattern, type(None))) is True:
            self.dut_as_number = dut_as_number
        else:
            raise TypeError('dut_as_number must be an instance of (Pattern, type(None))')
        if isinstance(ipv4, (Ipv4, type(None))) is True:
            self.ipv4 = ipv4
        else:
            raise TypeError('ipv4 must be an instance of (Ipv4, type(None))')
        if isinstance(bgpv4_route_range, (list, type(None))) is True:
            self.bgpv4_route_range = [] if bgpv4_route_range is None else list(bgpv4_route_range)
        else:
            raise TypeError('bgpv4_route_range must be an instance of (list, type(None))')
        if isinstance(bgpv6_route_range, (list, type(None))) is True:
            self.bgpv6_route_range = [] if bgpv6_route_range is None else list(bgpv6_route_range)
        else:
            raise TypeError('bgpv6_route_range must be an instance of (list, type(None))')


class Bgpv4RouteRange(object):
    """Generated from OpenAPI schema object #/components/schemas/Device.Bgpv4RouteRange

    Emulated BGPv4 route range  

    Args
    ----
    - name (str): Unique system wide name of an object that is also the primary key for objects found in arrays
    - route_count_per_device (int): The number of routes per device
    - address (Pattern): A container for emulated device property patterns
     The network address of the first network
    - prefix (Pattern): A container for emulated device property patterns
     Ipv4 prefix length with minimum value is 0 to maximum value is 32
    - as_path (Pattern): A container for emulated device property patterns
     Autonomous Systems (AS) numbers that a route passes through to reach the destination
    - next_hop_address (Pattern): A container for emulated device property patterns
     IP Address of next router to forward a packet to its final destination
    - community (Pattern): A container for emulated device property patterns
     BGP communities provide additional capability for tagging routes and for modifying BGP routing policy on upstream and downstream routers BGP community is a 32-bit number which broken into 16-bit As and 16-bit custom value Please specify those two values in this string format 65000:100
    """
    def __init__(self, name=None, route_count_per_device=1, address=None, prefix=None, as_path=None, next_hop_address=None, community=None):
        from abstract_open_traffic_generator.device import Pattern
        if isinstance(name, (str)) is True:
            import re
            assert(bool(re.match(r'^[\sa-zA-Z0-9-_()><\[\]]+$', name)) is True)
            self.name = name
        else:
            raise TypeError('name must be an instance of (str)')
        if isinstance(route_count_per_device, (float, int, type(None))) is True:
            self.route_count_per_device = route_count_per_device
        else:
            raise TypeError('route_count_per_device must be an instance of (float, int, type(None))')
        if isinstance(address, (Pattern, type(None))) is True:
            self.address = address
        else:
            raise TypeError('address must be an instance of (Pattern, type(None))')
        if isinstance(prefix, (Pattern, type(None))) is True:
            self.prefix = prefix
        else:
            raise TypeError('prefix must be an instance of (Pattern, type(None))')
        if isinstance(as_path, (Pattern, type(None))) is True:
            self.as_path = as_path
        else:
            raise TypeError('as_path must be an instance of (Pattern, type(None))')
        if isinstance(next_hop_address, (Pattern, type(None))) is True:
            self.next_hop_address = next_hop_address
        else:
            raise TypeError('next_hop_address must be an instance of (Pattern, type(None))')
        if isinstance(community, (Pattern, type(None))) is True:
            self.community = community
        else:
            raise TypeError('community must be an instance of (Pattern, type(None))')


class Bgpv6RouteRange(object):
    """Generated from OpenAPI schema object #/components/schemas/Device.Bgpv6RouteRange

    Emulated bgpv6 route range  

    Args
    ----
    - name (str): Unique system wide name of an object that is also the primary key for objects found in arrays
    - route_count_per_device (int): The number of routes per device
    - address (Pattern): A container for emulated device property patterns
     The network address of the first network
    - prefix (Pattern): A container for emulated device property patterns
     Ipv6 prefix length with minimum value is 0 to maximum value is 128
    - as_path (Pattern): A container for emulated device property patterns
     Autonomous Systems (AS) numbers that a route passes through to reach the destination
    - next_hop_address (Pattern): A container for emulated device property patterns
     IP Address of next router to forward a packet to its final destination
    - community (Pattern): A container for emulated device property patterns
     BGP communities provide additional capability for tagging routes and for modifying BGP routing policy on upstream and downstream routers BGP community is a 32-bit number which broken into 16-bit As and 16-bit custom value Please specify those two values in this string format 65000:100
    """
    def __init__(self, name=None, route_count_per_device=1, address=None, prefix=None, as_path=None, next_hop_address=None, community=None):
        from abstract_open_traffic_generator.device import Pattern
        if isinstance(name, (str)) is True:
            import re
            assert(bool(re.match(r'^[\sa-zA-Z0-9-_()><\[\]]+$', name)) is True)
            self.name = name
        else:
            raise TypeError('name must be an instance of (str)')
        if isinstance(route_count_per_device, (float, int, type(None))) is True:
            self.route_count_per_device = route_count_per_device
        else:
            raise TypeError('route_count_per_device must be an instance of (float, int, type(None))')
        if isinstance(address, (Pattern, type(None))) is True:
            self.address = address
        else:
            raise TypeError('address must be an instance of (Pattern, type(None))')
        if isinstance(prefix, (Pattern, type(None))) is True:
            self.prefix = prefix
        else:
            raise TypeError('prefix must be an instance of (Pattern, type(None))')
        if isinstance(as_path, (Pattern, type(None))) is True:
            self.as_path = as_path
        else:
            raise TypeError('as_path must be an instance of (Pattern, type(None))')
        if isinstance(next_hop_address, (Pattern, type(None))) is True:
            self.next_hop_address = next_hop_address
        else:
            raise TypeError('next_hop_address must be an instance of (Pattern, type(None))')
        if isinstance(community, (Pattern, type(None))) is True:
            self.community = community
        else:
            raise TypeError('community must be an instance of (Pattern, type(None))')
