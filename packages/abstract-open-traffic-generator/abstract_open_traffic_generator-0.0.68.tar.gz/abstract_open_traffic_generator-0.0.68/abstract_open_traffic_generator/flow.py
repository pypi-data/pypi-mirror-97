

class Flow(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow

    A high level data plane traffic flow  
    Acts as a container for endpoints, frame size, frame rate, duration and packet headers  

    Args
    ----
    - name (str): Unique system wide name of an object that is also the primary key for objects found in arrays
    - tx_rx (TxRx): A container for different types of transmit and receive endpoint containers
    - packet (list[Header]): The packet is a list of traffic protocol headers
     The order of traffic protocol headers assigned to the list is the order they will appear on the wire
    - size (Size): The frame size which overrides the total length of the packet
    - rate (Rate): The rate of packet transmission
    - duration (Duration): A container for different transmit durations
    """
    def __init__(self, name=None, tx_rx=None, packet=[], size=None, rate=None, duration=None):
        from abstract_open_traffic_generator.flow import TxRx
        from abstract_open_traffic_generator.flow import Size
        from abstract_open_traffic_generator.flow import Rate
        from abstract_open_traffic_generator.flow import Duration
        if isinstance(name, (str)) is True:
            import re
            assert(bool(re.match(r'^[\sa-zA-Z0-9-_()><\[\]]+$', name)) is True)
            self.name = name
        else:
            raise TypeError('name must be an instance of (str)')
        if isinstance(tx_rx, (TxRx)) is True:
            self.tx_rx = tx_rx
        else:
            raise TypeError('tx_rx must be an instance of (TxRx)')
        if isinstance(packet, (list, type(None))) is True:
            self.packet = [] if packet is None else list(packet)
        else:
            raise TypeError('packet must be an instance of (list, type(None))')
        if isinstance(size, (Size, type(None))) is True:
            self.size = size
        else:
            raise TypeError('size must be an instance of (Size, type(None))')
        if isinstance(rate, (Rate, type(None))) is True:
            self.rate = rate
        else:
            raise TypeError('rate must be an instance of (Rate, type(None))')
        if isinstance(duration, (Duration, type(None))) is True:
            self.duration = duration
        else:
            raise TypeError('duration must be an instance of (Duration, type(None))')


class TxRx(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.TxRx

    A container for different types of transmit and receive endpoint containers  

    Args
    ----
    - choice (Union[PortTxRx, DeviceTxRx]): The type of transmit and receive container used by the flow
    """
    _CHOICE_MAP = {
        'PortTxRx': 'port',
        'DeviceTxRx': 'device',
    }
    def __init__(self, choice=None):
        from abstract_open_traffic_generator.flow import PortTxRx
        from abstract_open_traffic_generator.flow import DeviceTxRx
        if isinstance(choice, (PortTxRx, DeviceTxRx)) is False:
            raise TypeError('choice must be of type: PortTxRx, DeviceTxRx')
        self.__setattr__('choice', TxRx._CHOICE_MAP[type(choice).__name__])
        self.__setattr__(TxRx._CHOICE_MAP[type(choice).__name__], choice)


class PortTxRx(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.PortTxRx

    A container for a transmit port and 0..n intended receive ports  
    When assigning this container to a flow the flows's packet headers will not be populated with any address resolution information such as source and/or destination addresses  
    For example Flow.Ethernet dst mac address values will be defaulted to 0  
    For full control over the Flow.properties.packet header contents use this container  

    Args
    ----
    - tx_port_name (str): The unique name of a port that is the transmit port
    - rx_port_name (str): The unique name of a port that is the intended receive port
    """
    def __init__(self, tx_port_name=None, rx_port_name=None):
        if isinstance(tx_port_name, (str)) is True:
            self.tx_port_name = tx_port_name
        else:
            raise TypeError('tx_port_name must be an instance of (str)')
        if isinstance(rx_port_name, (str, type(None))) is True:
            self.rx_port_name = rx_port_name
        else:
            raise TypeError('rx_port_name must be an instance of (str, type(None))')


class DeviceTxRx(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.DeviceTxRx

    A container for 1..n transmit devices and 1..n receive devices  
    Implemementations may use learned information from the devices to pre-populate Flow.properties.packet[Flow.Header fields]  
    For example an implementation may automatically start devices, get arp table information and pre-populate the Flow.Ethernet dst mac address values  
    To discover what the implementation supports use the /results/capabilities API  

    Args
    ----
    - tx_device_names (list[str]): The unique names of devices that will be transmitting
    - rx_device_names (list[str]): The unique names of emulated devices that will be receiving
    """
    def __init__(self, tx_device_names=[], rx_device_names=[]):
        if isinstance(tx_device_names, (list)) is True:
            self.tx_device_names = tx_device_names
        else:
            raise TypeError('tx_device_names must be an instance of (list)')
        if isinstance(rx_device_names, (list)) is True:
            self.rx_device_names = rx_device_names
        else:
            raise TypeError('rx_device_names must be an instance of (list)')


class Header(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.Header

    Container for all traffic packet headers  

    Args
    ----
    - choice (Union[Custom, Ethernet, Vlan, Vxlan, Ipv4, Ipv6, PfcPause, EthernetPause, Tcp, Udp, Gre, Gtpv1, Gtpv2]): TBD
    """
    _CHOICE_MAP = {
        'Custom': 'custom',
        'Ethernet': 'ethernet',
        'Vlan': 'vlan',
        'Vxlan': 'vxlan',
        'Ipv4': 'ipv4',
        'Ipv6': 'ipv6',
        'PfcPause': 'pfcpause',
        'EthernetPause': 'ethernetpause',
        'Tcp': 'tcp',
        'Udp': 'udp',
        'Gre': 'gre',
        'Gtpv1': 'gtpv1',
        'Gtpv2': 'gtpv2',
    }
    def __init__(self, choice=None):
        from abstract_open_traffic_generator.flow import Custom
        from abstract_open_traffic_generator.flow import Ethernet
        from abstract_open_traffic_generator.flow import Vlan
        from abstract_open_traffic_generator.flow import Vxlan
        from abstract_open_traffic_generator.flow import Ipv4
        from abstract_open_traffic_generator.flow import Ipv6
        from abstract_open_traffic_generator.flow import PfcPause
        from abstract_open_traffic_generator.flow import EthernetPause
        from abstract_open_traffic_generator.flow import Tcp
        from abstract_open_traffic_generator.flow import Udp
        from abstract_open_traffic_generator.flow import Gre
        from abstract_open_traffic_generator.flow import Gtpv1
        from abstract_open_traffic_generator.flow import Gtpv2
        if isinstance(choice, (Custom, Ethernet, Vlan, Vxlan, Ipv4, Ipv6, PfcPause, EthernetPause, Tcp, Udp, Gre, Gtpv1, Gtpv2)) is False:
            raise TypeError('choice must be of type: Custom, Ethernet, Vlan, Vxlan, Ipv4, Ipv6, PfcPause, EthernetPause, Tcp, Udp, Gre, Gtpv1, Gtpv2')
        self.__setattr__('choice', Header._CHOICE_MAP[type(choice).__name__])
        self.__setattr__(Header._CHOICE_MAP[type(choice).__name__], choice)


class Custom(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.Custom

    Custom packet header  

    Args
    ----
    - bytes (str): A custom packet header defined as a string of hex bytes
     The string MUST contain valid hex characters
     Spaces or colons can be part of the bytes but will be discarded This can be used to create a custom protocol from other inputs such as scapy, wireshark, pcap etc
     An example of ethernet/ipv4: '00000000000200000000000108004500001400010000400066e70a0000010a000002'
    - patterns (list[BitPattern]): Modify the bytes with bit based patterns
    """
    def __init__(self, bytes=None, patterns=[]):
        if isinstance(bytes, (str)) is True:
            import re
            assert(bool(re.match(r'^[A-Fa-f0-9: ]+$', bytes)) is True)
            self.bytes = bytes
        else:
            raise TypeError('bytes must be an instance of (str)')
        if isinstance(patterns, (list, type(None))) is True:
            self.patterns = [] if patterns is None else list(patterns)
        else:
            raise TypeError('patterns must be an instance of (list, type(None))')


class BitPattern(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.BitPattern

    Container for a bit pattern  

    Args
    ----
    - choice (Union[BitList, BitCounter]): TBD
    """
    _CHOICE_MAP = {
        'BitList': 'bitlist',
        'BitCounter': 'bitcounter',
    }
    def __init__(self, choice=None):
        from abstract_open_traffic_generator.flow import BitList
        from abstract_open_traffic_generator.flow import BitCounter
        if isinstance(choice, (BitList, BitCounter)) is False:
            raise TypeError('choice must be of type: BitList, BitCounter')
        self.__setattr__('choice', BitPattern._CHOICE_MAP[type(choice).__name__])
        self.__setattr__(BitPattern._CHOICE_MAP[type(choice).__name__], choice)


class BitList(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.BitList

    A pattern which is a list of values  

    Args
    ----
    - offset (int): Bit offset in the packet at which the pattern will be applied
    - length (int): The number of bits in the packet that the pattern will span
    - count (int): The number of values to generate before repeating
    - values (list[str]): TBD
    """
    def __init__(self, offset=1, length=1, count=1, values=[]):
        if isinstance(offset, (float, int, type(None))) is True:
            self.offset = offset
        else:
            raise TypeError('offset must be an instance of (float, int, type(None))')
        if isinstance(length, (float, int, type(None))) is True:
            self.length = length
        else:
            raise TypeError('length must be an instance of (float, int, type(None))')
        if isinstance(count, (float, int, type(None))) is True:
            self.count = count
        else:
            raise TypeError('count must be an instance of (float, int, type(None))')
        if isinstance(values, (list, type(None))) is True:
            self.values = [] if values is None else list(values)
        else:
            raise TypeError('values must be an instance of (list, type(None))')


class BitCounter(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.BitCounter

    An incrementing pattern  

    Args
    ----
    - offset (int): Bit offset in the packet at which the pattern will be applied
    - length (int): The number of bits in the packet that the pattern will span
    - count (int): The number of values to generate before repeating A value of 0 means the pattern will count continuously
    - start (str): The starting value of the pattern
     If the value is greater than the length it will be truncated
    - step (str): The amount the start value will be incremented by If the value is greater than the length it will be truncated
    """
    def __init__(self, offset=0, length=32, count=1, start='0', step='0'):
        if isinstance(offset, (float, int, type(None))) is True:
            self.offset = offset
        else:
            raise TypeError('offset must be an instance of (float, int, type(None))')
        if isinstance(length, (float, int, type(None))) is True:
            self.length = length
        else:
            raise TypeError('length must be an instance of (float, int, type(None))')
        if isinstance(count, (float, int, type(None))) is True:
            self.count = count
        else:
            raise TypeError('count must be an instance of (float, int, type(None))')
        if isinstance(start, (str, type(None))) is True:
            import re
            assert(bool(re.match(r'^[A-Fa-f0-9: ]+$', start)) is True)
            self.start = start
        else:
            raise TypeError('start must be an instance of (str, type(None))')
        if isinstance(step, (str, type(None))) is True:
            import re
            assert(bool(re.match(r'^[A-Fa-f0-9: ]+$', step)) is True)
            self.step = step
        else:
            raise TypeError('step must be an instance of (str, type(None))')


class Ethernet(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.Ethernet

    Ethernet packet header  

    Args
    ----
    - dst (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - src (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - ether_type (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - pfc_queue (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Optional field of 3 bits
    """
    def __init__(self, dst=None, src=None, ether_type=None, pfc_queue=None):
        from abstract_open_traffic_generator.flow import Pattern
        if isinstance(dst, (Pattern, type(None))) is True:
            self.dst = dst
        else:
            raise TypeError('dst must be an instance of (Pattern, type(None))')
        if isinstance(src, (Pattern, type(None))) is True:
            self.src = src
        else:
            raise TypeError('src must be an instance of (Pattern, type(None))')
        if isinstance(ether_type, (Pattern, type(None))) is True:
            self.ether_type = ether_type
        else:
            raise TypeError('ether_type must be an instance of (Pattern, type(None))')
        if isinstance(pfc_queue, (Pattern, type(None))) is True:
            self.pfc_queue = pfc_queue
        else:
            raise TypeError('pfc_queue must be an instance of (Pattern, type(None))')


class Pattern(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.Pattern

    A container for packet header field patterns  
    Possible patterns are fixed, list, counter, random  

    Args
    ----
    - choice (Union[str, list, Counter, Random]): TBD
    - ingress_result_name (str): A unique name is used to indicate to the system that the field may extend the result row key and create an aggregate result row for every unique ingress value
     To have ingress columns appear in flow result rows the flow result request allows for the ingress_result_name value to be specified as part of the request
    """
    _CHOICE_MAP = {
        'str': 'fixed',
        'list': 'list',
        'Counter': 'counter',
        'Random': 'random',
    }
    def __init__(self, choice=None, ingress_result_name=None):
        from abstract_open_traffic_generator.flow import Counter
        from abstract_open_traffic_generator.flow import Random
        if isinstance(choice, (str, list, Counter, Random)) is False:
            raise TypeError('choice must be of type: str, list, Counter, Random')
        self.__setattr__('choice', Pattern._CHOICE_MAP[type(choice).__name__])
        self.__setattr__(Pattern._CHOICE_MAP[type(choice).__name__], choice)
        if isinstance(ingress_result_name, (str, type(None))) is True:
            self.ingress_result_name = ingress_result_name
        else:
            raise TypeError('ingress_result_name must be an instance of (str, type(None))')


class Counter(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.Counter

    A counter pattern that can increment or decrement  

    Args
    ----
    - start (str): The value at which the pattern will start
    - step (str): The value at which the pattern will increment or decrement by
    - count (Union[float, int]): The number of values in the pattern
    - up (Union[True, False]): Determines whether the pattern will increment (true) or decrement (false)
    """
    def __init__(self, start=None, step=None, count=None, up=True):
        if isinstance(start, (str, type(None))) is True:
            self.start = start
        else:
            raise TypeError('start must be an instance of (str, type(None))')
        if isinstance(step, (str, type(None))) is True:
            self.step = step
        else:
            raise TypeError('step must be an instance of (str, type(None))')
        if isinstance(count, (float, int, type(None))) is True:
            self.count = count
        else:
            raise TypeError('count must be an instance of (float, int, type(None))')
        if isinstance(up, (bool, type(None))) is True:
            self.up = up
        else:
            raise TypeError('up must be an instance of (bool, type(None))')


class Random(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.Random

    A repeatable random range pattern  

    Args
    ----
    - min (str): TBD
    - max (str): TBD
    - step (Union[float, int]): TBD
    - seed (str): TBD
    - count (Union[float, int]): TBD
    """
    def __init__(self, min=None, max=None, step=None, seed=None, count=None):
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
        if isinstance(count, (float, int, type(None))) is True:
            self.count = count
        else:
            raise TypeError('count must be an instance of (float, int, type(None))')


class Vlan(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.Vlan

    Vlan packet header  

    Args
    ----
    - priority (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - cfi (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - id (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - protocol (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    """
    def __init__(self, priority=None, cfi=None, id=None, protocol=None):
        from abstract_open_traffic_generator.flow import Pattern
        if isinstance(priority, (Pattern, type(None))) is True:
            self.priority = priority
        else:
            raise TypeError('priority must be an instance of (Pattern, type(None))')
        if isinstance(cfi, (Pattern, type(None))) is True:
            self.cfi = cfi
        else:
            raise TypeError('cfi must be an instance of (Pattern, type(None))')
        if isinstance(id, (Pattern, type(None))) is True:
            self.id = id
        else:
            raise TypeError('id must be an instance of (Pattern, type(None))')
        if isinstance(protocol, (Pattern, type(None))) is True:
            self.protocol = protocol
        else:
            raise TypeError('protocol must be an instance of (Pattern, type(None))')


class Vxlan(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.Vxlan

    Vxlan packet header  

    Args
    ----
    - flags (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     RRRRIRRR Where the I flag MUST be set to 1 for a valid vxlan network id (VNI)
     The other 7 bits (designated "R") are reserved fields and MUST be set to zero on transmission and ignored on receipt
     8 bits
    - reserved0 (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Set to 0
     24 bits
    - vni (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Vxlan network id
     24 bits
    - reserved1 (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Set to 0
     8 bits
    """
    def __init__(self, flags=None, reserved0=None, vni=None, reserved1=None):
        from abstract_open_traffic_generator.flow import Pattern
        if isinstance(flags, (Pattern, type(None))) is True:
            self.flags = flags
        else:
            raise TypeError('flags must be an instance of (Pattern, type(None))')
        if isinstance(reserved0, (Pattern, type(None))) is True:
            self.reserved0 = reserved0
        else:
            raise TypeError('reserved0 must be an instance of (Pattern, type(None))')
        if isinstance(vni, (Pattern, type(None))) is True:
            self.vni = vni
        else:
            raise TypeError('vni must be an instance of (Pattern, type(None))')
        if isinstance(reserved1, (Pattern, type(None))) is True:
            self.reserved1 = reserved1
        else:
            raise TypeError('reserved1 must be an instance of (Pattern, type(None))')


class Ipv4(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.Ipv4

    Ipv4 packet header  

    Args
    ----
    - version (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - header_length (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - priority (Priority): A container for ipv4 raw, tos, dscp ip priorities
    - total_length (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - identification (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - reserved (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - dont_fragment (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - more_fragments (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - fragment_offset (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - time_to_live (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - protocol (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - header_checksum (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - src (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - dst (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    """
    def __init__(self, version=None, header_length=None, priority=None, total_length=None, identification=None, reserved=None, dont_fragment=None, more_fragments=None, fragment_offset=None, time_to_live=None, protocol=None, header_checksum=None, src=None, dst=None):
        from abstract_open_traffic_generator.flow import Pattern
        from abstract_open_traffic_generator.flow_ipv4 import Priority
        if isinstance(version, (Pattern, type(None))) is True:
            self.version = version
        else:
            raise TypeError('version must be an instance of (Pattern, type(None))')
        if isinstance(header_length, (Pattern, type(None))) is True:
            self.header_length = header_length
        else:
            raise TypeError('header_length must be an instance of (Pattern, type(None))')
        if isinstance(priority, (Priority, type(None))) is True:
            self.priority = priority
        else:
            raise TypeError('priority must be an instance of (Priority, type(None))')
        if isinstance(total_length, (Pattern, type(None))) is True:
            self.total_length = total_length
        else:
            raise TypeError('total_length must be an instance of (Pattern, type(None))')
        if isinstance(identification, (Pattern, type(None))) is True:
            self.identification = identification
        else:
            raise TypeError('identification must be an instance of (Pattern, type(None))')
        if isinstance(reserved, (Pattern, type(None))) is True:
            self.reserved = reserved
        else:
            raise TypeError('reserved must be an instance of (Pattern, type(None))')
        if isinstance(dont_fragment, (Pattern, type(None))) is True:
            self.dont_fragment = dont_fragment
        else:
            raise TypeError('dont_fragment must be an instance of (Pattern, type(None))')
        if isinstance(more_fragments, (Pattern, type(None))) is True:
            self.more_fragments = more_fragments
        else:
            raise TypeError('more_fragments must be an instance of (Pattern, type(None))')
        if isinstance(fragment_offset, (Pattern, type(None))) is True:
            self.fragment_offset = fragment_offset
        else:
            raise TypeError('fragment_offset must be an instance of (Pattern, type(None))')
        if isinstance(time_to_live, (Pattern, type(None))) is True:
            self.time_to_live = time_to_live
        else:
            raise TypeError('time_to_live must be an instance of (Pattern, type(None))')
        if isinstance(protocol, (Pattern, type(None))) is True:
            self.protocol = protocol
        else:
            raise TypeError('protocol must be an instance of (Pattern, type(None))')
        if isinstance(header_checksum, (Pattern, type(None))) is True:
            self.header_checksum = header_checksum
        else:
            raise TypeError('header_checksum must be an instance of (Pattern, type(None))')
        if isinstance(src, (Pattern, type(None))) is True:
            self.src = src
        else:
            raise TypeError('src must be an instance of (Pattern, type(None))')
        if isinstance(dst, (Pattern, type(None))) is True:
            self.dst = dst
        else:
            raise TypeError('dst must be an instance of (Pattern, type(None))')


class Ipv6(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.Ipv6

    Ipv6 packet header  

    Args
    ----
    - version (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Default version number is 6 (bit sequence 0110) 4 bits
    - traffic_class (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     8 bits
    - flow_label (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     20 bits
    - payload_length (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     16 bits
    - next_header (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     8 bits
    - hop_limit (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     8 bits
    - src (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     128 bits
    - dst (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     128 bits
    """
    def __init__(self, version=None, traffic_class=None, flow_label=None, payload_length=None, next_header=None, hop_limit=None, src=None, dst=None):
        from abstract_open_traffic_generator.flow import Pattern
        if isinstance(version, (Pattern, type(None))) is True:
            self.version = version
        else:
            raise TypeError('version must be an instance of (Pattern, type(None))')
        if isinstance(traffic_class, (Pattern, type(None))) is True:
            self.traffic_class = traffic_class
        else:
            raise TypeError('traffic_class must be an instance of (Pattern, type(None))')
        if isinstance(flow_label, (Pattern, type(None))) is True:
            self.flow_label = flow_label
        else:
            raise TypeError('flow_label must be an instance of (Pattern, type(None))')
        if isinstance(payload_length, (Pattern, type(None))) is True:
            self.payload_length = payload_length
        else:
            raise TypeError('payload_length must be an instance of (Pattern, type(None))')
        if isinstance(next_header, (Pattern, type(None))) is True:
            self.next_header = next_header
        else:
            raise TypeError('next_header must be an instance of (Pattern, type(None))')
        if isinstance(hop_limit, (Pattern, type(None))) is True:
            self.hop_limit = hop_limit
        else:
            raise TypeError('hop_limit must be an instance of (Pattern, type(None))')
        if isinstance(src, (Pattern, type(None))) is True:
            self.src = src
        else:
            raise TypeError('src must be an instance of (Pattern, type(None))')
        if isinstance(dst, (Pattern, type(None))) is True:
            self.dst = dst
        else:
            raise TypeError('dst must be an instance of (Pattern, type(None))')


class PfcPause(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.PfcPause

    IEEE 802.1Qbb PFC Pause packet header  
    - dst: 01:80:C2:00:00:01 48bits - src: 48bits - ether_type: 0x8808 16bits - control_op_code: 0x0101 16bits - class_enable_vector: 16bits - pause_class_0: 0x0000 16bits - pause_class_1: 0x0000 16bits - pause_class_2: 0x0000 16bits - pause_class_3: 0x0000 16bits - pause_class_4: 0x0000 16bits - pause_class_5: 0x0000 16bits - pause_class_6: 0x0000 16bits - pause_class_7: 0x0000 16bits  

    Args
    ----
    - dst (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - src (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - ether_type (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - control_op_code (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - class_enable_vector (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - pause_class_0 (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - pause_class_1 (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - pause_class_2 (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - pause_class_3 (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - pause_class_4 (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - pause_class_5 (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - pause_class_6 (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - pause_class_7 (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    """
    def __init__(self, dst=None, src=None, ether_type=None, control_op_code=None, class_enable_vector=None, pause_class_0=None, pause_class_1=None, pause_class_2=None, pause_class_3=None, pause_class_4=None, pause_class_5=None, pause_class_6=None, pause_class_7=None):
        from abstract_open_traffic_generator.flow import Pattern
        if isinstance(dst, (Pattern, type(None))) is True:
            self.dst = dst
        else:
            raise TypeError('dst must be an instance of (Pattern, type(None))')
        if isinstance(src, (Pattern, type(None))) is True:
            self.src = src
        else:
            raise TypeError('src must be an instance of (Pattern, type(None))')
        if isinstance(ether_type, (Pattern, type(None))) is True:
            self.ether_type = ether_type
        else:
            raise TypeError('ether_type must be an instance of (Pattern, type(None))')
        if isinstance(control_op_code, (Pattern, type(None))) is True:
            self.control_op_code = control_op_code
        else:
            raise TypeError('control_op_code must be an instance of (Pattern, type(None))')
        if isinstance(class_enable_vector, (Pattern, type(None))) is True:
            self.class_enable_vector = class_enable_vector
        else:
            raise TypeError('class_enable_vector must be an instance of (Pattern, type(None))')
        if isinstance(pause_class_0, (Pattern, type(None))) is True:
            self.pause_class_0 = pause_class_0
        else:
            raise TypeError('pause_class_0 must be an instance of (Pattern, type(None))')
        if isinstance(pause_class_1, (Pattern, type(None))) is True:
            self.pause_class_1 = pause_class_1
        else:
            raise TypeError('pause_class_1 must be an instance of (Pattern, type(None))')
        if isinstance(pause_class_2, (Pattern, type(None))) is True:
            self.pause_class_2 = pause_class_2
        else:
            raise TypeError('pause_class_2 must be an instance of (Pattern, type(None))')
        if isinstance(pause_class_3, (Pattern, type(None))) is True:
            self.pause_class_3 = pause_class_3
        else:
            raise TypeError('pause_class_3 must be an instance of (Pattern, type(None))')
        if isinstance(pause_class_4, (Pattern, type(None))) is True:
            self.pause_class_4 = pause_class_4
        else:
            raise TypeError('pause_class_4 must be an instance of (Pattern, type(None))')
        if isinstance(pause_class_5, (Pattern, type(None))) is True:
            self.pause_class_5 = pause_class_5
        else:
            raise TypeError('pause_class_5 must be an instance of (Pattern, type(None))')
        if isinstance(pause_class_6, (Pattern, type(None))) is True:
            self.pause_class_6 = pause_class_6
        else:
            raise TypeError('pause_class_6 must be an instance of (Pattern, type(None))')
        if isinstance(pause_class_7, (Pattern, type(None))) is True:
            self.pause_class_7 = pause_class_7
        else:
            raise TypeError('pause_class_7 must be an instance of (Pattern, type(None))')


class EthernetPause(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.EthernetPause

    IEEE 802.3x Ethernet Pause packet header  
    - dst: 01:80:C2:00:00:01 48bits - src: 48bits - ether_type: 0x8808 16bits - control_op_code: 0x0001 16bits - time: 0x0000 16bits  

    Args
    ----
    - dst (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - src (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - ether_type (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - control_op_code (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    - time (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
    """
    def __init__(self, dst=None, src=None, ether_type=None, control_op_code=None, time=None):
        from abstract_open_traffic_generator.flow import Pattern
        if isinstance(dst, (Pattern, type(None))) is True:
            self.dst = dst
        else:
            raise TypeError('dst must be an instance of (Pattern, type(None))')
        if isinstance(src, (Pattern, type(None))) is True:
            self.src = src
        else:
            raise TypeError('src must be an instance of (Pattern, type(None))')
        if isinstance(ether_type, (Pattern, type(None))) is True:
            self.ether_type = ether_type
        else:
            raise TypeError('ether_type must be an instance of (Pattern, type(None))')
        if isinstance(control_op_code, (Pattern, type(None))) is True:
            self.control_op_code = control_op_code
        else:
            raise TypeError('control_op_code must be an instance of (Pattern, type(None))')
        if isinstance(time, (Pattern, type(None))) is True:
            self.time = time
        else:
            raise TypeError('time must be an instance of (Pattern, type(None))')


class Tcp(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.Tcp

    Tcp packet header  

    Args
    ----
    - src_port (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Tcp source port
     Max length is 2 bytes
    - dst_port (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Tcp destination port
     Max length is 2 bytes
    - seq_num (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Tcp Sequence Number
     Max length is 4 bytes
    - ack_num (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Tcp Acknowledgement Number
     Max length is 4 bytes
    - data_offset (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     The number of 32 bit words in the TCP header
     This indicates where the data begins
     Max length is 4 bits
    - ecn_ns (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Explicit congestion notification, concealment protection
     Max length is 1 bit
    - ecn_cwr (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Explicit congestion notification, congestion window reduced
     Max length is 1 bit
    - ecn_echo (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Explicit congestion notification, echo
     1 indicates the peer is ecn capable
     0 indicates that a packet with ipv4
     ecn = 11 in the ip header was received during normal transmission
     Max length is 1 bit
    - ctl_urg (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     A value of 1 indicates that the urgent pointer field is significant
     Max length is 1 bit
    - ctl_ack (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     A value of 1 indicates that the ackknowledgment field is significant
     Max length is 1 bit
    - ctl_psh (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Asks to push the buffered data to the receiving application
     Max length is 1 bit
    - ctl_rst (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Reset the connection
     Max length is 1 bit
    - ctl_syn (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Synchronize sequenece numbers
     Max length is 1 bit
    - ctl_fin (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Last packet from the sender
     Max length is 1 bit
    - window (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Tcp connection window
     Max length is 2 bytes
    """
    def __init__(self, src_port=None, dst_port=None, seq_num=None, ack_num=None, data_offset=None, ecn_ns=None, ecn_cwr=None, ecn_echo=None, ctl_urg=None, ctl_ack=None, ctl_psh=None, ctl_rst=None, ctl_syn=None, ctl_fin=None, window=None):
        from abstract_open_traffic_generator.flow import Pattern
        if isinstance(src_port, (Pattern, type(None))) is True:
            self.src_port = src_port
        else:
            raise TypeError('src_port must be an instance of (Pattern, type(None))')
        if isinstance(dst_port, (Pattern, type(None))) is True:
            self.dst_port = dst_port
        else:
            raise TypeError('dst_port must be an instance of (Pattern, type(None))')
        if isinstance(seq_num, (Pattern, type(None))) is True:
            self.seq_num = seq_num
        else:
            raise TypeError('seq_num must be an instance of (Pattern, type(None))')
        if isinstance(ack_num, (Pattern, type(None))) is True:
            self.ack_num = ack_num
        else:
            raise TypeError('ack_num must be an instance of (Pattern, type(None))')
        if isinstance(data_offset, (Pattern, type(None))) is True:
            self.data_offset = data_offset
        else:
            raise TypeError('data_offset must be an instance of (Pattern, type(None))')
        if isinstance(ecn_ns, (Pattern, type(None))) is True:
            self.ecn_ns = ecn_ns
        else:
            raise TypeError('ecn_ns must be an instance of (Pattern, type(None))')
        if isinstance(ecn_cwr, (Pattern, type(None))) is True:
            self.ecn_cwr = ecn_cwr
        else:
            raise TypeError('ecn_cwr must be an instance of (Pattern, type(None))')
        if isinstance(ecn_echo, (Pattern, type(None))) is True:
            self.ecn_echo = ecn_echo
        else:
            raise TypeError('ecn_echo must be an instance of (Pattern, type(None))')
        if isinstance(ctl_urg, (Pattern, type(None))) is True:
            self.ctl_urg = ctl_urg
        else:
            raise TypeError('ctl_urg must be an instance of (Pattern, type(None))')
        if isinstance(ctl_ack, (Pattern, type(None))) is True:
            self.ctl_ack = ctl_ack
        else:
            raise TypeError('ctl_ack must be an instance of (Pattern, type(None))')
        if isinstance(ctl_psh, (Pattern, type(None))) is True:
            self.ctl_psh = ctl_psh
        else:
            raise TypeError('ctl_psh must be an instance of (Pattern, type(None))')
        if isinstance(ctl_rst, (Pattern, type(None))) is True:
            self.ctl_rst = ctl_rst
        else:
            raise TypeError('ctl_rst must be an instance of (Pattern, type(None))')
        if isinstance(ctl_syn, (Pattern, type(None))) is True:
            self.ctl_syn = ctl_syn
        else:
            raise TypeError('ctl_syn must be an instance of (Pattern, type(None))')
        if isinstance(ctl_fin, (Pattern, type(None))) is True:
            self.ctl_fin = ctl_fin
        else:
            raise TypeError('ctl_fin must be an instance of (Pattern, type(None))')
        if isinstance(window, (Pattern, type(None))) is True:
            self.window = window
        else:
            raise TypeError('window must be an instance of (Pattern, type(None))')


class Udp(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.Udp

    Udp packet header  

    Args
    ----
    - src_port (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Udp source port
     Max length is 2 bytes
    - dst_port (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Tcp destination port
     Max length is 2 bytes
    - length (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Length in bytes of the udp header and yudp data
     Max length is 2 bytes
    - checksum (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Checksum field used for error checking of header and data
     Max length is 2 bytes
    """
    def __init__(self, src_port=None, dst_port=None, length=None, checksum=None):
        from abstract_open_traffic_generator.flow import Pattern
        if isinstance(src_port, (Pattern, type(None))) is True:
            self.src_port = src_port
        else:
            raise TypeError('src_port must be an instance of (Pattern, type(None))')
        if isinstance(dst_port, (Pattern, type(None))) is True:
            self.dst_port = dst_port
        else:
            raise TypeError('dst_port must be an instance of (Pattern, type(None))')
        if isinstance(length, (Pattern, type(None))) is True:
            self.length = length
        else:
            raise TypeError('length must be an instance of (Pattern, type(None))')
        if isinstance(checksum, (Pattern, type(None))) is True:
            self.checksum = checksum
        else:
            raise TypeError('checksum must be an instance of (Pattern, type(None))')


class Gre(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.Gre

    Gre packet header  

    Args
    ----
    - checksum_present (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Checksum bit
     Set to 1 if a checksum is present
    - key_present (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Key bit
     Set to 1 if a key is present
    - seq_number_present (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Sequence number bit
     Set to 1 if a sequence number is present
    - reserved0 (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Reserved bits
     Set to 0
     9 bits
    - version (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Gre version number
     Set to 0
     3 bits
    - protocol (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Indicates the ether protocol type of the encapsulated payload
     - 0x0800 ipv4 - 0x86DD ipv6
    - checksum (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Present if the checksum_present bit is set
     Contains the checksum for the gre header and payload
     16 bits
    - reserved1 (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Reserved bits
     Set to 0
     16 bits
    - key (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Present if the key_present bit is set
     Contains an application specific key value
     32 bits
    - sequence_number (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Present if the seq_number_present bit is set
     Contains a sequence number for the gre packet
     32 bits
    """
    def __init__(self, checksum_present=None, key_present=None, seq_number_present=None, reserved0=None, version=None, protocol=None, checksum=None, reserved1=None, key=None, sequence_number=None):
        from abstract_open_traffic_generator.flow import Pattern
        if isinstance(checksum_present, (Pattern, type(None))) is True:
            self.checksum_present = checksum_present
        else:
            raise TypeError('checksum_present must be an instance of (Pattern, type(None))')
        if isinstance(key_present, (Pattern, type(None))) is True:
            self.key_present = key_present
        else:
            raise TypeError('key_present must be an instance of (Pattern, type(None))')
        if isinstance(seq_number_present, (Pattern, type(None))) is True:
            self.seq_number_present = seq_number_present
        else:
            raise TypeError('seq_number_present must be an instance of (Pattern, type(None))')
        if isinstance(reserved0, (Pattern, type(None))) is True:
            self.reserved0 = reserved0
        else:
            raise TypeError('reserved0 must be an instance of (Pattern, type(None))')
        if isinstance(version, (Pattern, type(None))) is True:
            self.version = version
        else:
            raise TypeError('version must be an instance of (Pattern, type(None))')
        if isinstance(protocol, (Pattern, type(None))) is True:
            self.protocol = protocol
        else:
            raise TypeError('protocol must be an instance of (Pattern, type(None))')
        if isinstance(checksum, (Pattern, type(None))) is True:
            self.checksum = checksum
        else:
            raise TypeError('checksum must be an instance of (Pattern, type(None))')
        if isinstance(reserved1, (Pattern, type(None))) is True:
            self.reserved1 = reserved1
        else:
            raise TypeError('reserved1 must be an instance of (Pattern, type(None))')
        if isinstance(key, (Pattern, type(None))) is True:
            self.key = key
        else:
            raise TypeError('key must be an instance of (Pattern, type(None))')
        if isinstance(sequence_number, (Pattern, type(None))) is True:
            self.sequence_number = sequence_number
        else:
            raise TypeError('sequence_number must be an instance of (Pattern, type(None))')


class Gtpv1(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.Gtpv1

    GTPv1 packet header  

    Args
    ----
    - version (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     It is a 3-bit field
     For GTPv1, this has a value of 1
    - protocol_type (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     A 1-bit value that differentiates GTP (value 1) from GTP' (value 0)
    - reserved (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     A 1-bit reserved field (must be 0)
    - e_flag (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     A 1-bit value that states whether there is an extension header optional field
    - s_flag (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     A 1-bit value that states whether there is a Sequence Number optional field
    - pn_flag (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     A 1-bit value that states whether there is a N-PDU number optional field
    - message_type (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     An 8-bit field that indicates the type of GTP message
     Different types of messages are defined in 3GPP TS 29
     060 section 7
     1
    - message_length (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     A 16-bit field that indicates the length of the payload in bytes (rest of the packet following the mandatory 8-byte GTP header)
     Includes the optional fields
    - teid (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Tunnel endpoint identifier
     A 32-bit(4-octet) field used to multiplex different connections in the same GTP tunnel
    - squence_number (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     An (optional) 16-bit field
     This field exists if any of the e_flag, s_flag, or pn_flag bits are on
     The field must be interpreted only if the s_flag bit is on
    - n_pdu_number (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     An (optional) 8-bit field
     This field exists if any of the e_flag, s_flag, or pn_flag bits are on
     The field must be interpreted only if the pn_flag bit is on
    - next_extension_header_type (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     An (optional) 8-bit field
     This field exists if any of the e_flag, s_flag, or pn_flag bits are on
     The field must be interpreted only if the e_flag bit is on
    - extension_headers (list[GtpExtension]): A list of optional extension headers
    """
    def __init__(self, version=None, protocol_type=None, reserved=None, e_flag=None, s_flag=None, pn_flag=None, message_type=None, message_length=None, teid=None, squence_number=None, n_pdu_number=None, next_extension_header_type=None, extension_headers=[]):
        from abstract_open_traffic_generator.flow import Pattern
        if isinstance(version, (Pattern, type(None))) is True:
            self.version = version
        else:
            raise TypeError('version must be an instance of (Pattern, type(None))')
        if isinstance(protocol_type, (Pattern, type(None))) is True:
            self.protocol_type = protocol_type
        else:
            raise TypeError('protocol_type must be an instance of (Pattern, type(None))')
        if isinstance(reserved, (Pattern, type(None))) is True:
            self.reserved = reserved
        else:
            raise TypeError('reserved must be an instance of (Pattern, type(None))')
        if isinstance(e_flag, (Pattern, type(None))) is True:
            self.e_flag = e_flag
        else:
            raise TypeError('e_flag must be an instance of (Pattern, type(None))')
        if isinstance(s_flag, (Pattern, type(None))) is True:
            self.s_flag = s_flag
        else:
            raise TypeError('s_flag must be an instance of (Pattern, type(None))')
        if isinstance(pn_flag, (Pattern, type(None))) is True:
            self.pn_flag = pn_flag
        else:
            raise TypeError('pn_flag must be an instance of (Pattern, type(None))')
        if isinstance(message_type, (Pattern, type(None))) is True:
            self.message_type = message_type
        else:
            raise TypeError('message_type must be an instance of (Pattern, type(None))')
        if isinstance(message_length, (Pattern, type(None))) is True:
            self.message_length = message_length
        else:
            raise TypeError('message_length must be an instance of (Pattern, type(None))')
        if isinstance(teid, (Pattern, type(None))) is True:
            self.teid = teid
        else:
            raise TypeError('teid must be an instance of (Pattern, type(None))')
        if isinstance(squence_number, (Pattern, type(None))) is True:
            self.squence_number = squence_number
        else:
            raise TypeError('squence_number must be an instance of (Pattern, type(None))')
        if isinstance(n_pdu_number, (Pattern, type(None))) is True:
            self.n_pdu_number = n_pdu_number
        else:
            raise TypeError('n_pdu_number must be an instance of (Pattern, type(None))')
        if isinstance(next_extension_header_type, (Pattern, type(None))) is True:
            self.next_extension_header_type = next_extension_header_type
        else:
            raise TypeError('next_extension_header_type must be an instance of (Pattern, type(None))')
        if isinstance(extension_headers, (list, type(None))) is True:
            self.extension_headers = [] if extension_headers is None else list(extension_headers)
        else:
            raise TypeError('extension_headers must be an instance of (list, type(None))')


class GtpExtension(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.GtpExtension

    TBD  

    Args
    ----
    - extension_length (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     An 8-bit field
     This field states the length of this extension header, including the length, the contents, and the next extension header field, in 4-octet units, so the length of the extension must always be a multiple of 4
    - contents (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     The extension header contents
    - next_extension_header (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     An 8-bit field
     It states the type of the next extension, or 0 if no next extension exists
     This permits chaining several next extension headers
    """
    def __init__(self, extension_length=None, contents=None, next_extension_header=None):
        from abstract_open_traffic_generator.flow import Pattern
        if isinstance(extension_length, (Pattern, type(None))) is True:
            self.extension_length = extension_length
        else:
            raise TypeError('extension_length must be an instance of (Pattern, type(None))')
        if isinstance(contents, (Pattern, type(None))) is True:
            self.contents = contents
        else:
            raise TypeError('contents must be an instance of (Pattern, type(None))')
        if isinstance(next_extension_header, (Pattern, type(None))) is True:
            self.next_extension_header = next_extension_header
        else:
            raise TypeError('next_extension_header must be an instance of (Pattern, type(None))')


class Gtpv2(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.Gtpv2

    GTPv2 packet header  

    Args
    ----
    - version (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     It is a 3-bit field
     For GTPv2, this has a value of 2
    - piggybacking_flag (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     If this bit is set to 1 then another GTP-C message with its own header shall be present at the end of the current message
    - teid_flag (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     If this bit is set to 1 then the TEID field will be present between the message length and the sequence number
     All messages except Echo and Echo reply require TEID to be present
    - spare1 (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     A 3-bit reserved field (must be 0)
    - message_type (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     An 8-bit field that indicates the type of GTP message
     Different types of messages are defined in 3GPP TS 29
     060 section 7
     1
    - message_length (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     A 16-bit field that indicates the length of the payload in bytes (excluding the mandatory GTP-c header (first 4 bytes)
     Includes the TEID and sequence_number if they are present
    - teid (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Tunnel endpoint identifier
     A 32-bit (4-octet) field used to multiplex different connections in the same GTP tunnel
     Is present only if the teid_flag is set
    - sequence_number (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     A 24-bit field
    - spare2 (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     An 8-bit reserved field (must be 0)
    """
    def __init__(self, version=None, piggybacking_flag=None, teid_flag=None, spare1=None, message_type=None, message_length=None, teid=None, sequence_number=None, spare2=None):
        from abstract_open_traffic_generator.flow import Pattern
        if isinstance(version, (Pattern, type(None))) is True:
            self.version = version
        else:
            raise TypeError('version must be an instance of (Pattern, type(None))')
        if isinstance(piggybacking_flag, (Pattern, type(None))) is True:
            self.piggybacking_flag = piggybacking_flag
        else:
            raise TypeError('piggybacking_flag must be an instance of (Pattern, type(None))')
        if isinstance(teid_flag, (Pattern, type(None))) is True:
            self.teid_flag = teid_flag
        else:
            raise TypeError('teid_flag must be an instance of (Pattern, type(None))')
        if isinstance(spare1, (Pattern, type(None))) is True:
            self.spare1 = spare1
        else:
            raise TypeError('spare1 must be an instance of (Pattern, type(None))')
        if isinstance(message_type, (Pattern, type(None))) is True:
            self.message_type = message_type
        else:
            raise TypeError('message_type must be an instance of (Pattern, type(None))')
        if isinstance(message_length, (Pattern, type(None))) is True:
            self.message_length = message_length
        else:
            raise TypeError('message_length must be an instance of (Pattern, type(None))')
        if isinstance(teid, (Pattern, type(None))) is True:
            self.teid = teid
        else:
            raise TypeError('teid must be an instance of (Pattern, type(None))')
        if isinstance(sequence_number, (Pattern, type(None))) is True:
            self.sequence_number = sequence_number
        else:
            raise TypeError('sequence_number must be an instance of (Pattern, type(None))')
        if isinstance(spare2, (Pattern, type(None))) is True:
            self.spare2 = spare2
        else:
            raise TypeError('spare2 must be an instance of (Pattern, type(None))')


class Size(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.Size

    The frame size which overrides the total length of the packet  

    Args
    ----
    - choice (Union[float, int, SizeIncrement, SizeRandom]): TBD
    """
    _CHOICE_MAP = {
        'float': 'fixed',
        'int': 'fixed',
        'SizeIncrement': 'increment',
        'SizeRandom': 'random',
    }
    def __init__(self, choice=None):
        from abstract_open_traffic_generator.flow import SizeIncrement
        from abstract_open_traffic_generator.flow import SizeRandom
        if isinstance(choice, (float, int, SizeIncrement, SizeRandom)) is False:
            raise TypeError('choice must be of type: float, int, SizeIncrement, SizeRandom')
        self.__setattr__('choice', Size._CHOICE_MAP[type(choice).__name__])
        self.__setattr__(Size._CHOICE_MAP[type(choice).__name__], choice)


class SizeIncrement(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.SizeIncrement

    Frame size that increments from a starting size to an ending size incrementing by a step size  

    Args
    ----
    - start (int): Starting frame size in bytes
    - end (int): Ending frame size in bytes
    - step (int): Step frame size in bytes
    """
    def __init__(self, start=64, end=1518, step=1):
        if isinstance(start, (float, int)) is True:
            self.start = start
        else:
            raise TypeError('start must be an instance of (float, int)')
        if isinstance(end, (float, int)) is True:
            self.end = end
        else:
            raise TypeError('end must be an instance of (float, int)')
        if isinstance(step, (float, int)) is True:
            self.step = step
        else:
            raise TypeError('step must be an instance of (float, int)')


class SizeRandom(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.SizeRandom

    Random frame size from a min value to a max value  

    Args
    ----
    - min (int): TBD
    - max (int): TBD
    """
    def __init__(self, min=64, max=1518):
        if isinstance(min, (float, int)) is True:
            self.min = min
        else:
            raise TypeError('min must be an instance of (float, int)')
        if isinstance(max, (float, int)) is True:
            self.max = max
        else:
            raise TypeError('max must be an instance of (float, int)')


class Rate(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.Rate

    The rate of packet transmission  

    Args
    ----
    - unit (Union[pps, bps, kbps, mbps, gbps, line]): The value is a unit of this
    - value (int): The actual rate
    """
    def __init__(self, unit=None, value=None):
        if isinstance(unit, (str)) is True:
            self.unit = unit
        else:
            raise TypeError('unit must be an instance of (str)')
        if isinstance(value, (float, int)) is True:
            self.value = value
        else:
            raise TypeError('value must be an instance of (float, int)')


class Duration(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.Duration

    A container for different transmit durations  

    Args
    ----
    - choice (Union[FixedPackets, FixedSeconds, Burst, Continuous]): TBD
    """
    _CHOICE_MAP = {
        'FixedPackets': 'packets',
        'FixedSeconds': 'seconds',
        'Burst': 'burst',
        'Continuous': 'continuous',
    }
    def __init__(self, choice=None):
        from abstract_open_traffic_generator.flow import FixedPackets
        from abstract_open_traffic_generator.flow import FixedSeconds
        from abstract_open_traffic_generator.flow import Burst
        from abstract_open_traffic_generator.flow import Continuous
        if isinstance(choice, (FixedPackets, FixedSeconds, Burst, Continuous)) is False:
            raise TypeError('choice must be of type: FixedPackets, FixedSeconds, Burst, Continuous')
        self.__setattr__('choice', Duration._CHOICE_MAP[type(choice).__name__])
        self.__setattr__(Duration._CHOICE_MAP[type(choice).__name__], choice)


class Continuous(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.Continuous

    Transmit will be continuous and will not stop automatically  

    Args
    ----
    - gap (int): The minimum gap between packets expressed as bytes
    - delay (int): The delay before starting transmission of packets
    - delay_unit (Union[bytes, nanoseconds]): The delay expressed as a number of this value
    """
    def __init__(self, gap=12, delay=0, delay_unit='bytes'):
        if isinstance(gap, (float, int, type(None))) is True:
            self.gap = gap
        else:
            raise TypeError('gap must be an instance of (float, int, type(None))')
        if isinstance(delay, (float, int, type(None))) is True:
            self.delay = delay
        else:
            raise TypeError('delay must be an instance of (float, int, type(None))')
        if isinstance(delay_unit, (str, type(None))) is True:
            self.delay_unit = delay_unit
        else:
            raise TypeError('delay_unit must be an instance of (str, type(None))')


class FixedPackets(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.FixedPackets

    Transmit a fixed number of packets after which the flow will stop  

    Args
    ----
    - packets (int): Stop transmit of the flow after this number of packets
    - gap (int): The minimum gap between packets expressed as bytes
    - delay (int): The delay before starting transmission of packets
    - delay_unit (Union[bytes, nanoseconds]): The delay expressed as a number of this value
    """
    def __init__(self, packets=1, gap=12, delay=0, delay_unit='bytes'):
        if isinstance(packets, (float, int, type(None))) is True:
            self.packets = packets
        else:
            raise TypeError('packets must be an instance of (float, int, type(None))')
        if isinstance(gap, (float, int, type(None))) is True:
            self.gap = gap
        else:
            raise TypeError('gap must be an instance of (float, int, type(None))')
        if isinstance(delay, (float, int, type(None))) is True:
            self.delay = delay
        else:
            raise TypeError('delay must be an instance of (float, int, type(None))')
        if isinstance(delay_unit, (str, type(None))) is True:
            self.delay_unit = delay_unit
        else:
            raise TypeError('delay_unit must be an instance of (str, type(None))')


class FixedSeconds(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.FixedSeconds

    Transmit for a fixed number of seconds after which the flow will stop  

    Args
    ----
    - seconds (Union[float, int]): Stop transmit of the flow after this number of seconds
    - gap (int): The minimum gap between packets expressed as bytes
    - delay (int): The delay before starting transmission of packets
    - delay_unit (Union[bytes, nanoseconds]): The delay expressed as a number of this value
    """
    def __init__(self, seconds=1, gap=12, delay=0, delay_unit='bytes'):
        if isinstance(seconds, (float, int, type(None))) is True:
            self.seconds = seconds
        else:
            raise TypeError('seconds must be an instance of (float, int, type(None))')
        if isinstance(gap, (float, int, type(None))) is True:
            self.gap = gap
        else:
            raise TypeError('gap must be an instance of (float, int, type(None))')
        if isinstance(delay, (float, int, type(None))) is True:
            self.delay = delay
        else:
            raise TypeError('delay must be an instance of (float, int, type(None))')
        if isinstance(delay_unit, (str, type(None))) is True:
            self.delay_unit = delay_unit
        else:
            raise TypeError('delay_unit must be an instance of (str, type(None))')


class Burst(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.Burst

    A continuous burst of packets that will not automatically stop  

    Args
    ----
    - packets (int): The number of packets transmitted per burst
    - gap (int): The minimum gap between packets expressed as bytes
    - inter_burst_gap (int): The gap between the transmission of each burst
     A value of 0 means there is no gap between bursts
    - inter_burst_gap_unit (Union[bytes, nanoseconds]): The inter burst gap expressed as a number of this value
    """
    def __init__(self, packets=None, gap=12, inter_burst_gap=0, inter_burst_gap_unit='bytes'):
        if isinstance(packets, (float, int, type(None))) is True:
            self.packets = packets
        else:
            raise TypeError('packets must be an instance of (float, int, type(None))')
        if isinstance(gap, (float, int, type(None))) is True:
            self.gap = gap
        else:
            raise TypeError('gap must be an instance of (float, int, type(None))')
        if isinstance(inter_burst_gap, (float, int, type(None))) is True:
            self.inter_burst_gap = inter_burst_gap
        else:
            raise TypeError('inter_burst_gap must be an instance of (float, int, type(None))')
        if isinstance(inter_burst_gap_unit, (str, type(None))) is True:
            self.inter_burst_gap_unit = inter_burst_gap_unit
        else:
            raise TypeError('inter_burst_gap_unit must be an instance of (str, type(None))')
