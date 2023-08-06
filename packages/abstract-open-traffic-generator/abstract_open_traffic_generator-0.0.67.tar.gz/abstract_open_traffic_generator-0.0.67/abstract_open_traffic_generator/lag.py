

class Lag(object):
    """Generated from OpenAPI schema object #/components/schemas/Lag

    The container for multiple LAG ports  

    Args
    ----
    - ports (list[Port]): TBD
    """
    def __init__(self, ports=[]):
        if isinstance(ports, (list, type(None))) is True:
            self.ports = [] if ports is None else list(ports)
        else:
            raise TypeError('ports must be an instance of (list, type(None))')


class Port(object):
    """Generated from OpenAPI schema object #/components/schemas/Lag.Port

    The container for a port's ethernet interface and LAG protocol settings  

    Args
    ----
    - port_name (str): The name of a port object that will be part of the LAG
    - protocol (Protocol): 
    - ethernet (Ethernet): Base ethernet interface
    """
    def __init__(self, port_name=None, protocol=None, ethernet=None):
        from abstract_open_traffic_generator.lag import Protocol
        from abstract_open_traffic_generator.lag import Ethernet
        if isinstance(port_name, (str)) is True:
            self.port_name = port_name
        else:
            raise TypeError('port_name must be an instance of (str)')
        if isinstance(protocol, (Protocol)) is True:
            self.protocol = protocol
        else:
            raise TypeError('protocol must be an instance of (Protocol)')
        if isinstance(ethernet, (Ethernet)) is True:
            self.ethernet = ethernet
        else:
            raise TypeError('ethernet must be an instance of (Ethernet)')


class Ethernet(object):
    """Generated from OpenAPI schema object #/components/schemas/Lag.Ethernet

    Base ethernet interface  

    Args
    ----
    - mac (str): Media access control address
    - mtu (int): Maximum transmission unit
    - vlans (list[Vlan]): List of VLANs
    """
    def __init__(self, mac='00:00:00:00:00:00', mtu=1500, vlans=[]):
        if isinstance(mac, (str, type(None))) is True:
            self.mac = mac
        else:
            raise TypeError('mac must be an instance of (str, type(None))')
        if isinstance(mtu, (float, int, type(None))) is True:
            self.mtu = mtu
        else:
            raise TypeError('mtu must be an instance of (float, int, type(None))')
        if isinstance(vlans, (list, type(None))) is True:
            self.vlans = [] if vlans is None else list(vlans)
        else:
            raise TypeError('vlans must be an instance of (list, type(None))')


class Vlan(object):
    """Generated from OpenAPI schema object #/components/schemas/Lag.Vlan

    Emulated VLAN protocol  

    Args
    ----
    - tpid (Union[x8100, x88A8, x9100, x9200, x9300]): Tag protocol identifier
    - priority (int): Priority code point
    - id (int): VLAN identifier
    """
    def __init__(self, tpid='x8100', priority=0, id=1):
        if isinstance(tpid, (str, type(None))) is True:
            self.tpid = tpid
        else:
            raise TypeError('tpid must be an instance of (str, type(None))')
        if isinstance(priority, (float, int, type(None))) is True:
            self.priority = priority
        else:
            raise TypeError('priority must be an instance of (float, int, type(None))')
        if isinstance(id, (float, int, type(None))) is True:
            self.id = id
        else:
            raise TypeError('id must be an instance of (float, int, type(None))')


class Protocol(object):
    """Generated from OpenAPI schema object #/components/schemas/Lag.Protocol

    TBD  

    Args
    ----
    - choice (Union[Lacp, Static]): The type of LAG protocol
    """
    _CHOICE_MAP = {
        'Lacp': 'lacp',
        'Static': 'static',
    }
    def __init__(self, choice='lacp'):
        from abstract_open_traffic_generator.lag import Lacp
        from abstract_open_traffic_generator.lag import Static
        if isinstance(choice, (Lacp, Static)) is False:
            raise TypeError('choice must be of type: Lacp, Static')
        self.__setattr__('choice', Protocol._CHOICE_MAP[type(choice).__name__])
        self.__setattr__(Protocol._CHOICE_MAP[type(choice).__name__], choice)


class Static(object):
    """Generated from OpenAPI schema object #/components/schemas/Lag.Static

    The container for static link aggregation protocol settings  

    Args
    ----
    - lag_id (int): The static lag id
    """
    def __init__(self, lag_id=0):
        if isinstance(lag_id, (float, int, type(None))) is True:
            self.lag_id = lag_id
        else:
            raise TypeError('lag_id must be an instance of (float, int, type(None))')


class Lacp(object):
    """Generated from OpenAPI schema object #/components/schemas/Lag.Lacp

    The container for link aggregation control protocol settings  

    Args
    ----
    - actor_key (int): The actor key
    - actor_port_number (int): The actor port number
    - actor_port_priority (int): The actor port priority
    - actor_system_id (str): The actor system id
    - actor_system_priority (int): The actor system priority
    - lacpdu_periodic_time_interval (int): This field defines how frequently LACPDUs are sent to the link partner
    - lacpdu_timeout (int): This timer is used to detect whether received protocol information has expired
    - actor_activity (Union[passive, active]): Sets the value of LACP actor activity as either passive or active Passive indicates the port's preference for not transmitting LACPDUs unless its partner's control is Active Active indicates the port's preference to participate in the protocol regardless of the partner's control value
    """
    def __init__(self, actor_key=0, actor_port_number=0, actor_port_priority=1, actor_system_id='00:00:00:00:00:00', actor_system_priority=0, lacpdu_periodic_time_interval=0, lacpdu_timeout=0, actor_activity='active'):
        if isinstance(actor_key, (float, int, type(None))) is True:
            self.actor_key = actor_key
        else:
            raise TypeError('actor_key must be an instance of (float, int, type(None))')
        if isinstance(actor_port_number, (float, int, type(None))) is True:
            self.actor_port_number = actor_port_number
        else:
            raise TypeError('actor_port_number must be an instance of (float, int, type(None))')
        if isinstance(actor_port_priority, (float, int, type(None))) is True:
            self.actor_port_priority = actor_port_priority
        else:
            raise TypeError('actor_port_priority must be an instance of (float, int, type(None))')
        if isinstance(actor_system_id, (str, type(None))) is True:
            self.actor_system_id = actor_system_id
        else:
            raise TypeError('actor_system_id must be an instance of (str, type(None))')
        if isinstance(actor_system_priority, (float, int, type(None))) is True:
            self.actor_system_priority = actor_system_priority
        else:
            raise TypeError('actor_system_priority must be an instance of (float, int, type(None))')
        if isinstance(lacpdu_periodic_time_interval, (float, int, type(None))) is True:
            self.lacpdu_periodic_time_interval = lacpdu_periodic_time_interval
        else:
            raise TypeError('lacpdu_periodic_time_interval must be an instance of (float, int, type(None))')
        if isinstance(lacpdu_timeout, (float, int, type(None))) is True:
            self.lacpdu_timeout = lacpdu_timeout
        else:
            raise TypeError('lacpdu_timeout must be an instance of (float, int, type(None))')
        if isinstance(actor_activity, (str, type(None))) is True:
            self.actor_activity = actor_activity
        else:
            raise TypeError('actor_activity must be an instance of (str, type(None))')
