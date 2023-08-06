

class Capture(object):
    """Generated from OpenAPI schema object #/components/schemas/Capture

    Container for capture settings  

    Args
    ----
    - name (str): Unique system wide name of an object that is also the primary key for objects found in arrays
    - port_names (list[str]): The unique names of ports that the capture settings will apply to
    - choice (Union[list, str]): The type of filter
    - enable (Union[True, False]): Enable capture on the port
    - overwrite (Union[True, False]): Overwrite the capture buffer
    - format (Union[pcap, pcapng]): The format of the capture file
    """
    _CHOICE_MAP = {
        'list': 'basic',
        'str': 'pcap',
    }
    def __init__(self, name=None, port_names=[], choice=None, enable=True, overwrite=False, format='pcap'):
        if isinstance(choice, (list, str)) is False:
            raise TypeError('choice must be of type: list, str')
        self.__setattr__('choice', Capture._CHOICE_MAP[type(choice).__name__])
        self.__setattr__(Capture._CHOICE_MAP[type(choice).__name__], choice)
        if isinstance(name, (str)) is True:
            import re
            assert(bool(re.match(r'^[\sa-zA-Z0-9-_()><\[\]]+$', name)) is True)
            self.name = name
        else:
            raise TypeError('name must be an instance of (str)')
        if isinstance(port_names, (list, type(None))) is True:
            self.port_names = [] if port_names is None else list(port_names)
        else:
            raise TypeError('port_names must be an instance of (list, type(None))')
        if isinstance(enable, (bool, type(None))) is True:
            self.enable = enable
        else:
            raise TypeError('enable must be an instance of (bool, type(None))')
        if isinstance(overwrite, (bool, type(None))) is True:
            self.overwrite = overwrite
        else:
            raise TypeError('overwrite must be an instance of (bool, type(None))')
        if isinstance(format, (str, type(None))) is True:
            self.format = format
        else:
            raise TypeError('format must be an instance of (str, type(None))')


class BasicFilter(object):
    """Generated from OpenAPI schema object #/components/schemas/Capture.BasicFilter

    A container for different types of basic capture filters  

    Args
    ----
    - choice (Union[MacAddressFilter, CustomFilter]): TBD
    - and_operator (Union[True, False]): TBD
    - not_operator (Union[True, False]): TBD
    """
    _CHOICE_MAP = {
        'MacAddressFilter': 'mac_address',
        'CustomFilter': 'custom',
    }
    def __init__(self, choice=None, and_operator=True, not_operator=False):
        from abstract_open_traffic_generator.capture import MacAddressFilter
        from abstract_open_traffic_generator.capture import CustomFilter
        if isinstance(choice, (MacAddressFilter, CustomFilter)) is False:
            raise TypeError('choice must be of type: MacAddressFilter, CustomFilter')
        self.__setattr__('choice', BasicFilter._CHOICE_MAP[type(choice).__name__])
        self.__setattr__(BasicFilter._CHOICE_MAP[type(choice).__name__], choice)
        if isinstance(and_operator, (bool, type(None))) is True:
            self.and_operator = and_operator
        else:
            raise TypeError('and_operator must be an instance of (bool, type(None))')
        if isinstance(not_operator, (bool, type(None))) is True:
            self.not_operator = not_operator
        else:
            raise TypeError('not_operator must be an instance of (bool, type(None))')


class MacAddressFilter(object):
    """Generated from OpenAPI schema object #/components/schemas/Capture.MacAddressFilter

    A container for a mac address capture filter  

    Args
    ----
    - mac (Union[source, destination]): The type of mac address filters
     This can be either source or destination
    - filter (str): The value of the mac address
    - mask (str): The value of the mask to be applied to the mac address
    """
    def __init__(self, mac=None, filter=None, mask=None):
        if isinstance(mac, (str)) is True:
            self.mac = mac
        else:
            raise TypeError('mac must be an instance of (str)')
        if isinstance(filter, (str)) is True:
            self.filter = filter
        else:
            raise TypeError('filter must be an instance of (str)')
        if isinstance(mask, (str, type(None))) is True:
            self.mask = mask
        else:
            raise TypeError('mask must be an instance of (str, type(None))')


class CustomFilter(object):
    """Generated from OpenAPI schema object #/components/schemas/Capture.CustomFilter

    A container for a custom capture filter  

    Args
    ----
    - filter (str): The value to filter on
    - mask (str): The mask to be applied to the filter
    - offset (int): The offset in the packet to filter at
    """
    def __init__(self, filter=None, mask=None, offset=None):
        if isinstance(filter, (str)) is True:
            self.filter = filter
        else:
            raise TypeError('filter must be an instance of (str)')
        if isinstance(mask, (str, type(None))) is True:
            self.mask = mask
        else:
            raise TypeError('mask must be an instance of (str, type(None))')
        if isinstance(offset, (float, int)) is True:
            self.offset = offset
        else:
            raise TypeError('offset must be an instance of (float, int)')
