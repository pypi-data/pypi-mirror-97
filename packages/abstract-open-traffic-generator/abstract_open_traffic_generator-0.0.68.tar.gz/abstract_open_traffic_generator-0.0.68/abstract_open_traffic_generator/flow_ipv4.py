

class Priority(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.Ipv4.Priority

    A container for ipv4 raw, tos, dscp ip priorities  

    Args
    ----
    - choice (Union[Pattern, Tos, Dscp]): TBD
    """
    
    PRIORITY_RAW = '0'
    
    _CHOICE_MAP = {
        'Pattern': 'raw',
        'Tos': 'tos',
        'Dscp': 'dscp',
    }
    def __init__(self, choice=None):
        from abstract_open_traffic_generator.flow import Pattern
        from abstract_open_traffic_generator.flow_ipv4 import Tos
        from abstract_open_traffic_generator.flow_ipv4 import Dscp
        if isinstance(choice, (Pattern, Tos, Dscp)) is False:
            raise TypeError('choice must be of type: Pattern, Tos, Dscp')
        self.__setattr__('choice', Priority._CHOICE_MAP[type(choice).__name__])
        self.__setattr__(Priority._CHOICE_MAP[type(choice).__name__], choice)


class Dscp(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.Ipv4.Dscp

    Differentiated services code point (DSCP) packet field  

    Args
    ----
    - phb (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     phb (per-hop-behavior) value is 6 bits: >=0 PHB <=63
    - ecn (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     ecn (explicit-congestion-notification) value is 2 bits: >=0 ecn <=3
    """
    
    PHB_DEFAULT = '0'
    PHB_CS1 = '8'
    PHB_CS2 = '16'
    PHB_CS3 = '24'
    PHB_CS4 = '32'
    PHB_CS5 = '40'
    PHB_CS6 = '48'
    PHB_CS7 = '56'
    PHB_AF11 = '10'
    PHB_AF12 = '12'
    PHB_AF13 = '14'
    PHB_AF21 = '18'
    PHB_AF22 = '20'
    PHB_AF23 = '22'
    PHB_AF31 = '26'
    PHB_AF32 = '28'
    PHB_AF33 = '30'
    PHB_AF41 = '34'
    PHB_AF42 = '36'
    PHB_AF43 = '38'
    PHB_EF46 = '46'
    ECN_NON_CAPABLE = '0'
    ECN_CAPABLE_TRANSPORT_0 = '1'
    ECN_CAPABLE_TRANSPORT_1 = '2'
    ECN_CONGESTION_ENCOUNTERED = '3'
    
    def __init__(self, phb=None, ecn=None):
        from abstract_open_traffic_generator.flow import Pattern
        if isinstance(phb, (Pattern, type(None))) is True:
            self.phb = phb
        else:
            raise TypeError('phb must be an instance of (Pattern, type(None))')
        if isinstance(ecn, (Pattern, type(None))) is True:
            self.ecn = ecn
        else:
            raise TypeError('ecn must be an instance of (Pattern, type(None))')


class Tos(object):
    """Generated from OpenAPI schema object #/components/schemas/Flow.Ipv4.Tos

    Type of service (TOS) packet field  

    Args
    ----
    - precedence (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Precedence value is 3 bits: >=0 precedence <=3
    - delay (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Delay value is 1 bit: >=0 delay <=1
    - throughput (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Throughput value is 1 bit: >=0 throughput <=3
    - reliability (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Reliability value is 1 bit: >=0 reliability <=1
    - monetary (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Monetary value is 1 bit: >=0 monetary <=1
    - unused (Pattern): A container for packet header field patterns
     Possible patterns are fixed, list, counter, random
     Unused value is 1 bit: >=0 unused <=1
    """
    
    PRE_ROUTINE = '0'
    PRE_PRIORITY = '1'
    PRE_IMMEDIATE = '2'
    PRE_FLASH = '3'
    PRE_FLASH_OVERRIDE = '4'
    PRE_CRITIC_ECP = '5'
    PRE_INTERNETWORK_CONTROL = '6'
    PRE_NETWORK_CONTROL = '7'
    NORMAL = '0'
    LOW = '1'
    
    def __init__(self, precedence=None, delay=None, throughput=None, reliability=None, monetary=None, unused=None):
        from abstract_open_traffic_generator.flow import Pattern
        if isinstance(precedence, (Pattern, type(None))) is True:
            self.precedence = precedence
        else:
            raise TypeError('precedence must be an instance of (Pattern, type(None))')
        if isinstance(delay, (Pattern, type(None))) is True:
            self.delay = delay
        else:
            raise TypeError('delay must be an instance of (Pattern, type(None))')
        if isinstance(throughput, (Pattern, type(None))) is True:
            self.throughput = throughput
        else:
            raise TypeError('throughput must be an instance of (Pattern, type(None))')
        if isinstance(reliability, (Pattern, type(None))) is True:
            self.reliability = reliability
        else:
            raise TypeError('reliability must be an instance of (Pattern, type(None))')
        if isinstance(monetary, (Pattern, type(None))) is True:
            self.monetary = monetary
        else:
            raise TypeError('monetary must be an instance of (Pattern, type(None))')
        if isinstance(unused, (Pattern, type(None))) is True:
            self.unused = unused
        else:
            raise TypeError('unused must be an instance of (Pattern, type(None))')
