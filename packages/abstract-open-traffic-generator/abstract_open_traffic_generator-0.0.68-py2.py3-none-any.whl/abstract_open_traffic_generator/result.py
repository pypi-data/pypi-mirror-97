

class RequestConflict(object):
    """Generated from OpenAPI schema object #/components/schemas/Result.RequestConflict

    Container for a request conflict  

    Args
    ----
    - current (str): Informational message describing the currently executing request
    """
    def __init__(self, current=None):
        if isinstance(current, (str, type(None))) is True:
            self.current = current
        else:
            raise TypeError('current must be an instance of (str, type(None))')


class RequestPending(object):
    """Generated from OpenAPI schema object #/components/schemas/Result.RequestPending

    The standard response to any request  
    This allows an implementation to be either async or sync  

    Args
    ----
    - state (Union[pending, success]): TBD
    - url (str): The url to poll while the state is pending
    """
    def __init__(self, state=None, url=None):
        if isinstance(state, (str, type(None))) is True:
            self.state = state
        else:
            raise TypeError('state must be an instance of (str, type(None))')
        if isinstance(url, (str, type(None))) is True:
            self.url = url
        else:
            raise TypeError('url must be an instance of (str, type(None))')


class RequestDetail(object):
    """Generated from OpenAPI schema object #/components/schemas/Result.RequestDetail

    TBD  

    Args
    ----
    - errors (list[str]): A list of any errors that may have occurred while executing the request
    - warnings (list[str]): A list of any warnings generated while executing the request
    """
    def __init__(self, errors=[], warnings=[]):
        if isinstance(errors, (list, type(None))) is True:
            self.errors = [] if errors is None else list(errors)
        else:
            raise TypeError('errors must be an instance of (list, type(None))')
        if isinstance(warnings, (list, type(None))) is True:
            self.warnings = [] if warnings is None else list(warnings)
        else:
            raise TypeError('warnings must be an instance of (list, type(None))')


class State(object):
    """Generated from OpenAPI schema object #/components/schemas/Result.State

    A container for the different types of states  

    Args
    ----
    - port_state (list[PortState]): TBD
    - flow_state (list[FlowState]): TBD
    """
    def __init__(self, port_state=[], flow_state=[]):
        if isinstance(port_state, (list, type(None))) is True:
            self.port_state = [] if port_state is None else list(port_state)
        else:
            raise TypeError('port_state must be an instance of (list, type(None))')
        if isinstance(flow_state, (list, type(None))) is True:
            self.flow_state = [] if flow_state is None else list(flow_state)
        else:
            raise TypeError('flow_state must be an instance of (list, type(None))')


class PortState(object):
    """Generated from OpenAPI schema object #/components/schemas/Result.PortState

    TBD  

    Args
    ----
    - name (str): TBD
    - link (Union[up, down]): TBD
    - capture (Union[started, stopped]): TBD
    """
    def __init__(self, name=None, link=None, capture=None):
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(link, (str, type(None))) is True:
            self.link = link
        else:
            raise TypeError('link must be an instance of (str, type(None))')
        if isinstance(capture, (str, type(None))) is True:
            self.capture = capture
        else:
            raise TypeError('capture must be an instance of (str, type(None))')


class FlowState(object):
    """Generated from OpenAPI schema object #/components/schemas/Result.FlowState

    TBD  

    Args
    ----
    - name (str): TBD
    - transmit (Union[started, stopped, paused]): TBD
    """
    def __init__(self, name=None, transmit=None):
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(transmit, (str, type(None))) is True:
            self.transmit = transmit
        else:
            raise TypeError('transmit must be an instance of (str, type(None))')


class Table(object):
    """Generated from OpenAPI schema object #/components/schemas/Result.Table

    A table of result values  
    Each row in the table is an object  
    """
    def __init__(self):
        pass


class Capability(object):
    """Generated from OpenAPI schema object #/components/schemas/Result.Capability

    A list of capabilities of the implementation  

    Args
    ----
    - unsupported (list[str]): A list of /components/schemas/
     paths that are not supported
    - formats (list[str]): A /components/schemas/
     path and specific format details regarding the path
     Specific model format details can be additional objects and properties represented as a hashmap
     For example layer1 models are defined as a hashmap key to object with each object consisting of a specific name/value property pairs
     This list of items will detail any specific formats, properties, enums
    """
    def __init__(self, unsupported=[], formats=[]):
        if isinstance(unsupported, (list, type(None))) is True:
            self.unsupported = [] if unsupported is None else list(unsupported)
        else:
            raise TypeError('unsupported must be an instance of (list, type(None))')
        if isinstance(formats, (list, type(None))) is True:
            self.formats = [] if formats is None else list(formats)
        else:
            raise TypeError('formats must be an instance of (list, type(None))')


class PortRequest(object):
    """Generated from OpenAPI schema object #/components/schemas/Result.PortRequest

    The port result request to the traffic generator  

    Args
    ----
    - port_names (list[str]): The names of objects to return results for
     An empty list will return all port row results
    - column_names (list[str]): The names of Result
     Port properties to return
     If the list is empty then all properties will be returned
    """
    def __init__(self, port_names=[], column_names=[]):
        if isinstance(port_names, (list, type(None))) is True:
            self.port_names = [] if port_names is None else list(port_names)
        else:
            raise TypeError('port_names must be an instance of (list, type(None))')
        if isinstance(column_names, (list, type(None))) is True:
            self.column_names = [] if column_names is None else list(column_names)
        else:
            raise TypeError('column_names must be an instance of (list, type(None))')


class Port(object):
    """Generated from OpenAPI schema object #/components/schemas/Result.Port

    TBD  

    Args
    ----
    - name (str): The name of a configured port
    - location (str): The state of the connection to the test port location
     The format should be the configured port location along with any custom connection state message
    - link (Union[up, down]): The state of the test port link The string can be up, down or a custom error message
    - capture (Union[started, stopped]): The state of the test port capture infrastructure
     The string can be started, stopped or a custom error message
    - frames_tx (int): The current total number of frames transmitted
    - frames_rx (int): The current total number of valid frames received
    - bytes_tx (int): The current total number of bytes transmitted
    - bytes_rx (int): The current total number of valid bytes received
    - frames_tx_rate (Union[float, int]): The current rate of frames transmitted
    - frames_rx_rate (Union[float, int]): The current rate of valid frames received
    - bytes_tx_rate (Union[float, int]): The current rate of bytes transmitted
    - bytes_rx_rate (Union[float, int]): The current rate of bytes received
    - pfc_class_0_frames_rx (int): The current total number of pfc class 0 frames received
    - pfc_class_1_frames_rx (int): The current total number of pfc class 1 frames received
    - pfc_class_2_frames_rx (int): The current total number of pfc class 2 frames received
    - pfc_class_3_frames_rx (int): The current total number of pfc class 3 frames received
    - pfc_class_4_frames_rx (int): The current total number of pfc class 4 frames received
    - pfc_class_5_frames_rx (Union[float, int]): The current total number of pfc class 5 frames received
    - pfc_class_6_frames_rx (int): The current total number of pfc class 6 frames received
    - pfc_class_7_frames_rx (int): The current total number of pfc class 7 frames received
    """
    def __init__(self, name=None, location=None, link=None, capture=None, frames_tx=None, frames_rx=None, bytes_tx=None, bytes_rx=None, frames_tx_rate=None, frames_rx_rate=None, bytes_tx_rate=None, bytes_rx_rate=None, pfc_class_0_frames_rx=None, pfc_class_1_frames_rx=None, pfc_class_2_frames_rx=None, pfc_class_3_frames_rx=None, pfc_class_4_frames_rx=None, pfc_class_5_frames_rx=None, pfc_class_6_frames_rx=None, pfc_class_7_frames_rx=None):
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(location, (str, type(None))) is True:
            self.location = location
        else:
            raise TypeError('location must be an instance of (str, type(None))')
        if isinstance(link, (str, type(None))) is True:
            self.link = link
        else:
            raise TypeError('link must be an instance of (str, type(None))')
        if isinstance(capture, (str, type(None))) is True:
            self.capture = capture
        else:
            raise TypeError('capture must be an instance of (str, type(None))')
        if isinstance(frames_tx, (float, int, type(None))) is True:
            self.frames_tx = frames_tx
        else:
            raise TypeError('frames_tx must be an instance of (float, int, type(None))')
        if isinstance(frames_rx, (float, int, type(None))) is True:
            self.frames_rx = frames_rx
        else:
            raise TypeError('frames_rx must be an instance of (float, int, type(None))')
        if isinstance(bytes_tx, (float, int, type(None))) is True:
            self.bytes_tx = bytes_tx
        else:
            raise TypeError('bytes_tx must be an instance of (float, int, type(None))')
        if isinstance(bytes_rx, (float, int, type(None))) is True:
            self.bytes_rx = bytes_rx
        else:
            raise TypeError('bytes_rx must be an instance of (float, int, type(None))')
        if isinstance(frames_tx_rate, (float, int, type(None))) is True:
            self.frames_tx_rate = frames_tx_rate
        else:
            raise TypeError('frames_tx_rate must be an instance of (float, int, type(None))')
        if isinstance(frames_rx_rate, (float, int, type(None))) is True:
            self.frames_rx_rate = frames_rx_rate
        else:
            raise TypeError('frames_rx_rate must be an instance of (float, int, type(None))')
        if isinstance(bytes_tx_rate, (float, int, type(None))) is True:
            self.bytes_tx_rate = bytes_tx_rate
        else:
            raise TypeError('bytes_tx_rate must be an instance of (float, int, type(None))')
        if isinstance(bytes_rx_rate, (float, int, type(None))) is True:
            self.bytes_rx_rate = bytes_rx_rate
        else:
            raise TypeError('bytes_rx_rate must be an instance of (float, int, type(None))')
        if isinstance(pfc_class_0_frames_rx, (float, int, type(None))) is True:
            self.pfc_class_0_frames_rx = pfc_class_0_frames_rx
        else:
            raise TypeError('pfc_class_0_frames_rx must be an instance of (float, int, type(None))')
        if isinstance(pfc_class_1_frames_rx, (float, int, type(None))) is True:
            self.pfc_class_1_frames_rx = pfc_class_1_frames_rx
        else:
            raise TypeError('pfc_class_1_frames_rx must be an instance of (float, int, type(None))')
        if isinstance(pfc_class_2_frames_rx, (float, int, type(None))) is True:
            self.pfc_class_2_frames_rx = pfc_class_2_frames_rx
        else:
            raise TypeError('pfc_class_2_frames_rx must be an instance of (float, int, type(None))')
        if isinstance(pfc_class_3_frames_rx, (float, int, type(None))) is True:
            self.pfc_class_3_frames_rx = pfc_class_3_frames_rx
        else:
            raise TypeError('pfc_class_3_frames_rx must be an instance of (float, int, type(None))')
        if isinstance(pfc_class_4_frames_rx, (float, int, type(None))) is True:
            self.pfc_class_4_frames_rx = pfc_class_4_frames_rx
        else:
            raise TypeError('pfc_class_4_frames_rx must be an instance of (float, int, type(None))')
        if isinstance(pfc_class_5_frames_rx, (float, int, type(None))) is True:
            self.pfc_class_5_frames_rx = pfc_class_5_frames_rx
        else:
            raise TypeError('pfc_class_5_frames_rx must be an instance of (float, int, type(None))')
        if isinstance(pfc_class_6_frames_rx, (float, int, type(None))) is True:
            self.pfc_class_6_frames_rx = pfc_class_6_frames_rx
        else:
            raise TypeError('pfc_class_6_frames_rx must be an instance of (float, int, type(None))')
        if isinstance(pfc_class_7_frames_rx, (float, int, type(None))) is True:
            self.pfc_class_7_frames_rx = pfc_class_7_frames_rx
        else:
            raise TypeError('pfc_class_7_frames_rx must be an instance of (float, int, type(None))')


class CaptureRequest(object):
    """Generated from OpenAPI schema object #/components/schemas/Result.CaptureRequest

    The capture result request to the traffic generator  
    Stops the port capture on the port_name and returns the capture  

    Args
    ----
    - port_name (str): The name of a port a capture is started on
    """
    def __init__(self, port_name=None):
        if isinstance(port_name, (str)) is True:
            self.port_name = port_name
        else:
            raise TypeError('port_name must be an instance of (str)')


class FlowRequest(object):
    """Generated from OpenAPI schema object #/components/schemas/Result.FlowRequest

    The request to the traffic generator for flow results  

    Args
    ----
    - flow_names (list[str]): The names of flow objects to return results for
     An empty list will return results for all flows
    - column_names (list[str]): The names of Result
     Flow properties to return
     If the list is empty then all properties will be returned
    - ingress_result_names (list[str]): Add any configured Flow
     Pattern
     ingress_result_name values that are to be included in the results
     If the name is not configured then it will be excluded from the Result
     Flow
     columns and Result
     Flow
     rows
     The name in the Result
     Flow
     columns will be a combination of the ingress_result_name and any system assigned name
    """
    def __init__(self, flow_names=[], column_names=[], ingress_result_names=[]):
        if isinstance(flow_names, (list, type(None))) is True:
            self.flow_names = [] if flow_names is None else list(flow_names)
        else:
            raise TypeError('flow_names must be an instance of (list, type(None))')
        if isinstance(column_names, (list, type(None))) is True:
            self.column_names = [] if column_names is None else list(column_names)
        else:
            raise TypeError('column_names must be an instance of (list, type(None))')
        if isinstance(ingress_result_names, (list, type(None))) is True:
            self.ingress_result_names = [] if ingress_result_names is None else list(ingress_result_names)
        else:
            raise TypeError('ingress_result_names must be an instance of (list, type(None))')


class Flow(object):
    """Generated from OpenAPI schema object #/components/schemas/Result.Flow

    TBD  

    Args
    ----
    - name (str): The name of a configured flow
    - transmit (Union[started, stopped, paused]): The transmit state of the flow
    - port_tx (str): The name of a configured port
    - port_rx (str): The name of a configured port
    - frames_tx (int): The current total number of frames transmitted
    - frames_rx (int): The current total number of valid frames received
    - bytes_tx (int): The current total number of bytes transmitted
    - bytes_rx (int): The current total number of bytes received
    - frames_tx_rate (Union[float, int]): The current rate of frames transmitted
    - frames_rx_rate (Union[float, int]): The current rate of valid frames received
    - loss (Union[float, int]): The percentage of lost frames
    - additional_properties (**additional_properties): Any requested ingress result names will appear as additional name/value pairs
     Ingress result names will be the keys in string format
     Ingress result values will be in number format
    """
    def __init__(self, name=None, transmit=None, port_tx=None, port_rx=None, frames_tx=None, frames_rx=None, bytes_tx=None, bytes_rx=None, frames_tx_rate=None, frames_rx_rate=None, loss=None, additionalProperties=None):
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(transmit, (str, type(None))) is True:
            self.transmit = transmit
        else:
            raise TypeError('transmit must be an instance of (str, type(None))')
        if isinstance(port_tx, (str, type(None))) is True:
            self.port_tx = port_tx
        else:
            raise TypeError('port_tx must be an instance of (str, type(None))')
        if isinstance(port_rx, (str, type(None))) is True:
            self.port_rx = port_rx
        else:
            raise TypeError('port_rx must be an instance of (str, type(None))')
        if isinstance(frames_tx, (float, int, type(None))) is True:
            self.frames_tx = frames_tx
        else:
            raise TypeError('frames_tx must be an instance of (float, int, type(None))')
        if isinstance(frames_rx, (float, int, type(None))) is True:
            self.frames_rx = frames_rx
        else:
            raise TypeError('frames_rx must be an instance of (float, int, type(None))')
        if isinstance(bytes_tx, (float, int, type(None))) is True:
            self.bytes_tx = bytes_tx
        else:
            raise TypeError('bytes_tx must be an instance of (float, int, type(None))')
        if isinstance(bytes_rx, (float, int, type(None))) is True:
            self.bytes_rx = bytes_rx
        else:
            raise TypeError('bytes_rx must be an instance of (float, int, type(None))')
        if isinstance(frames_tx_rate, (float, int, type(None))) is True:
            self.frames_tx_rate = frames_tx_rate
        else:
            raise TypeError('frames_tx_rate must be an instance of (float, int, type(None))')
        if isinstance(frames_rx_rate, (float, int, type(None))) is True:
            self.frames_rx_rate = frames_rx_rate
        else:
            raise TypeError('frames_rx_rate must be an instance of (float, int, type(None))')
        if isinstance(loss, (float, int, type(None))) is True:
            self.loss = loss
        else:
            raise TypeError('loss must be an instance of (float, int, type(None))')
        if isinstance(additionalProperties, **additional_properties) is True:
            self.additionalProperties = additionalProperties
        else:
            raise TypeError('additionalProperties must be an instance of **additional_properties')


class Bgpv4Request(object):
    """Generated from OpenAPI schema object #/components/schemas/Result.Bgpv4Request

    The request to retrieve BGP Router statistics and learned routing information  

    Args
    ----
    - names (list[str]): The names of BGP objects to return results for
     An empty list will return results for all BGP
    """
    def __init__(self, names=[]):
        if isinstance(names, (list, type(None))) is True:
            self.names = [] if names is None else list(names)
        else:
            raise TypeError('names must be an instance of (list, type(None))')


class Bgpv4(object):
    """Generated from OpenAPI schema object #/components/schemas/Result.Bgpv4

    BGP Router statistics and learned routing information  

    Args
    ----
    - name (str): The name of a configured BGPv4 Object
    - sessions_total (int): Total number of session
    - sessions_up (int): Sessions are in active state
    - sessions_down (int): Sessions are not active state
    - sessions_not_started (int): Sessions not able to start due to some internal issue
    - routes_advertised (int): Number of advertised routes sent
    - routes_withdrawn (int): Number of routes withdrawn
    """
    def __init__(self, name=None, sessions_total=None, sessions_up=None, sessions_down=None, sessions_not_started=None, routes_advertised=None, routes_withdrawn=None):
        if isinstance(name, (str, type(None))) is True:
            self.name = name
        else:
            raise TypeError('name must be an instance of (str, type(None))')
        if isinstance(sessions_total, (float, int, type(None))) is True:
            self.sessions_total = sessions_total
        else:
            raise TypeError('sessions_total must be an instance of (float, int, type(None))')
        if isinstance(sessions_up, (float, int, type(None))) is True:
            self.sessions_up = sessions_up
        else:
            raise TypeError('sessions_up must be an instance of (float, int, type(None))')
        if isinstance(sessions_down, (float, int, type(None))) is True:
            self.sessions_down = sessions_down
        else:
            raise TypeError('sessions_down must be an instance of (float, int, type(None))')
        if isinstance(sessions_not_started, (float, int, type(None))) is True:
            self.sessions_not_started = sessions_not_started
        else:
            raise TypeError('sessions_not_started must be an instance of (float, int, type(None))')
        if isinstance(routes_advertised, (float, int, type(None))) is True:
            self.routes_advertised = routes_advertised
        else:
            raise TypeError('routes_advertised must be an instance of (float, int, type(None))')
        if isinstance(routes_withdrawn, (float, int, type(None))) is True:
            self.routes_withdrawn = routes_withdrawn
        else:
            raise TypeError('routes_withdrawn must be an instance of (float, int, type(None))')
