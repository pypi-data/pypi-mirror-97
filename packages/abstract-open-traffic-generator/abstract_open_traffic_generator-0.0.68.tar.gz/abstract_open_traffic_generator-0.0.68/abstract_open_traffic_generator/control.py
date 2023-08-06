

class State(object):
    """Generated from OpenAPI schema object #/components/schemas/Control.State

    A container for the different types of states  

    Args
    ----
    - choice (Union[ConfigState, PortLinkState, PortCaptureState, FlowTransmitState, Bgpv4RouteAction, Bgpv6RouteAction]): TBD
    """
    _CHOICE_MAP = {
        'ConfigState': 'config_state',
        'PortLinkState': 'port_link_state',
        'PortCaptureState': 'port_capture_state',
        'FlowTransmitState': 'flow_transmit_state',
        'Bgpv4RouteAction': 'bgpv4_route_action',
        'Bgpv6RouteAction': 'bgpv6_route_action',
    }
    def __init__(self, choice=None):
        from abstract_open_traffic_generator.control import ConfigState
        from abstract_open_traffic_generator.control import PortLinkState
        from abstract_open_traffic_generator.control import PortCaptureState
        from abstract_open_traffic_generator.control import FlowTransmitState
        from abstract_open_traffic_generator.control import Bgpv4RouteAction
        from abstract_open_traffic_generator.control import Bgpv6RouteAction
        if isinstance(choice, (ConfigState, PortLinkState, PortCaptureState, FlowTransmitState, Bgpv4RouteAction, Bgpv6RouteAction)) is False:
            raise TypeError('choice must be of type: ConfigState, PortLinkState, PortCaptureState, FlowTransmitState, Bgpv4RouteAction, Bgpv6RouteAction')
        self.__setattr__('choice', State._CHOICE_MAP[type(choice).__name__])
        self.__setattr__(State._CHOICE_MAP[type(choice).__name__], choice)


class ConfigState(object):
    """Generated from OpenAPI schema object #/components/schemas/Control.ConfigState

    Control the configuration state on the traffic generator  

    Args
    ----
    - config (Config): A container for all models that are part of the configuration
    - state (Union[set, update]): Set the configuration state on the traffic generator
     - set is used to submit a complete running configuration on the traffic generator
     - update is used to submit a partial configuration which will be merged with the current running configuration on the traffic generator
    """
    def __init__(self, config=None, state=None):
        from abstract_open_traffic_generator.config import Config
        if isinstance(config, (Config)) is True:
            self.config = config
        else:
            raise TypeError('config must be an instance of (Config)')
        if isinstance(state, (str)) is True:
            self.state = state
        else:
            raise TypeError('state must be an instance of (str)')


class PortLinkState(object):
    """Generated from OpenAPI schema object #/components/schemas/Control.PortLinkState

    Control port link state  

    Args
    ----
    - port_names (list[str]): The names of port objects to
     An empty or null list will control all port objects
    - state (Union[up, down]): The link state
    """
    def __init__(self, port_names=[], state=None):
        if isinstance(port_names, (list, type(None))) is True:
            self.port_names = [] if port_names is None else list(port_names)
        else:
            raise TypeError('port_names must be an instance of (list, type(None))')
        if isinstance(state, (str)) is True:
            self.state = state
        else:
            raise TypeError('state must be an instance of (str)')


class FlowTransmitState(object):
    """Generated from OpenAPI schema object #/components/schemas/Control.FlowTransmitState

    Control flow transmit state  

    Args
    ----
    - flow_names (list[str]): The names of flow objects to control
     An empty or null list will control all flow objects
    - state (Union[start, stop, pause]): The transmit state
    """
    def __init__(self, flow_names=[], state=None):
        if isinstance(flow_names, (list, type(None))) is True:
            self.flow_names = [] if flow_names is None else list(flow_names)
        else:
            raise TypeError('flow_names must be an instance of (list, type(None))')
        if isinstance(state, (str)) is True:
            self.state = state
        else:
            raise TypeError('state must be an instance of (str)')


class PortCaptureState(object):
    """Generated from OpenAPI schema object #/components/schemas/Control.PortCaptureState

    Control port capture state  

    Args
    ----
    - port_names (list[str]): The name of ports to start capturing packets on
     An empty or null list will control all port objects
    - state (Union[start, stop]): The capture state
    """
    def __init__(self, port_names=[], state=None):
        if isinstance(port_names, (list, type(None))) is True:
            self.port_names = [] if port_names is None else list(port_names)
        else:
            raise TypeError('port_names must be an instance of (list, type(None))')
        if isinstance(state, (str)) is True:
            self.state = state
        else:
            raise TypeError('state must be an instance of (str)')


class Bgpv4RouteAction(object):
    """Generated from OpenAPI schema object #/components/schemas/Control.Bgpv4RouteAction

    BGPv4 route specific action  

    Args
    ----
    - names (list[str]): The names of Bgpv4RouteRange object to control
    - action (Union[withdraw_routes, advertise_routes]): BGPv4 route specific action
    """
    def __init__(self, names=[], action=None):
        if isinstance(names, (list, type(None))) is True:
            self.names = [] if names is None else list(names)
        else:
            raise TypeError('names must be an instance of (list, type(None))')
        if isinstance(action, (str)) is True:
            self.action = action
        else:
            raise TypeError('action must be an instance of (str)')


class Bgpv6RouteAction(object):
    """Generated from OpenAPI schema object #/components/schemas/Control.Bgpv6RouteAction

    BGPv6 route specific action  

    Args
    ----
    - names (list[str]): The names of Bgpv6RouteRange object to control
    - action (Union[withdraw_routes, advertise_routes]): BGPv6 route specific action
    """
    def __init__(self, names=[], action=None):
        if isinstance(names, (list, type(None))) is True:
            self.names = [] if names is None else list(names)
        else:
            raise TypeError('names must be an instance of (list, type(None))')
        if isinstance(action, (str)) is True:
            self.action = action
        else:
            raise TypeError('action must be an instance of (str)')
