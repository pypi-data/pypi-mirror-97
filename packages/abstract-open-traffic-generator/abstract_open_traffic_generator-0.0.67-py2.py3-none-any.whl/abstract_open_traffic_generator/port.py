

class Port(object):
    """Generated from OpenAPI schema object #/components/schemas/Port

    An abstract test port  

    Args
    ----
    - name (str): Unique system wide name of an object that is also the primary key for objects found in arrays
    - location (str): The location of a test port
     It is the endpoint where packets will emit from
     Test port locations can be the following: - physical appliance with multiple ports - physical chassis with multiple cards and ports - local interface - virtual machine, docker container, kubernetes cluster The test port location format is implementation specific
     Use the /results/capabilities API to determine what formats an implementation supports for the location property
     Get the configured location state by using the /results/port API
    """
    def __init__(self, name=None, location=None):
        if isinstance(name, (str)) is True:
            import re
            assert(bool(re.match(r'^[\sa-zA-Z0-9-_()><\[\]]+$', name)) is True)
            self.name = name
        else:
            raise TypeError('name must be an instance of (str)')
        if isinstance(location, (str, type(None))) is True:
            self.location = location
        else:
            raise TypeError('location must be an instance of (str, type(None))')


class Options(object):
    """Generated from OpenAPI schema object #/components/schemas/Port.Options

    Common port options that apply to all configured Port.Port objects  

    Args
    ----
    - location_preemption (Union[True, False]): Preempt all the test port locations as defined by the Port
     Port
     properties
     location
     If the test ports as defined by their location values are in use and this value is true, the test ports will be preempted
    """
    def __init__(self, location_preemption=False):
        if isinstance(location_preemption, (bool, type(None))) is True:
            self.location_preemption = location_preemption
        else:
            raise TypeError('location_preemption must be an instance of (bool, type(None))')
