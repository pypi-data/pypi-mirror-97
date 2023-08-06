import importlib
try:
    from typing import Union
except ImportError:
    pass
try:
    from typing import Literal
except ImportError:
    pass
from .snappicommon import SnappiObject
from .snappicommon import SnappiIter
from .snappicommon import SnappiHttpTransport


class Config(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'ports': 'PortIter',
        'lags': 'LagIter',
        'layer1': 'Layer1Iter',
        'captures': 'CaptureIter',
        'devices': 'DeviceIter',
        'flows': 'FlowIter',
        'options': 'ConfigOptions',
    }

    def __init__(self, parent=None, choice=None):
        super(Config, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def ports(self):
        # type: () -> PortIter
        """ports getter

        The ports that will be configured on the traffic generator.

        Returns: list[obj(snappi.Port)]
        """
        return self._get_property('ports', PortIter)

    @property
    def lags(self):
        # type: () -> LagIter
        """lags getter

        The lags that will be configured on the traffic generator.

        Returns: list[obj(snappi.Lag)]
        """
        return self._get_property('lags', LagIter)

    @property
    def layer1(self):
        # type: () -> Layer1Iter
        """layer1 getter

        The layer1 settings that will be configured on the traffic generator.

        Returns: list[obj(snappi.Layer1)]
        """
        return self._get_property('layer1', Layer1Iter)

    @property
    def captures(self):
        # type: () -> CaptureIter
        """captures getter

        The capture settings that will be configured on the traffic generator.

        Returns: list[obj(snappi.Capture)]
        """
        return self._get_property('captures', CaptureIter)

    @property
    def devices(self):
        # type: () -> DeviceIter
        """devices getter

        The emulated device settings that will be configured on the traffic generator.

        Returns: list[obj(snappi.Device)]
        """
        return self._get_property('devices', DeviceIter)

    @property
    def flows(self):
        # type: () -> FlowIter
        """flows getter

        The flows that will be configured on the traffic generator.

        Returns: list[obj(snappi.Flow)]
        """
        return self._get_property('flows', FlowIter)

    @property
    def options(self):
        # type: () -> ConfigOptions
        """options getter

        Global configuration options.

        Returns: obj(snappi.ConfigOptions)
        """
        return self._get_property('options', ConfigOptions)


class Port(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, location=None, name=None):
        super(Port, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('location', location)
        self._set_property('name', name)

    @property
    def location(self):
        # type: () -> str
        """location getter

        The location of a test port. It is the endpoint where packets will emit from.. Test port locations can be the following:. - physical appliance with multiple ports. - physical chassis with multiple cards and ports. - local interface. - virtual machine, docker container, kubernetes cluster. . The test port location format is implementation specific. Use the /results/capabilities API to determine what formats an implementation supports for the location property.. Get the configured location state by using the /results/port API.

        Returns: str
        """
        return self._get_property('location')

    @location.setter
    def location(self, value):
        """location setter

        The location of a test port. It is the endpoint where packets will emit from.. Test port locations can be the following:. - physical appliance with multiple ports. - physical chassis with multiple cards and ports. - local interface. - virtual machine, docker container, kubernetes cluster. . The test port location format is implementation specific. Use the /results/capabilities API to determine what formats an implementation supports for the location property.. Get the configured location state by using the /results/port API.

        value: str
        """
        self._set_property('location', value)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)


class PortIter(SnappiIter):
    __slots__ = ()

    def __init__(self):
        super(PortIter, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[Port]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> PortIter
        return self._iter()

    def __next__(self):
        # type: () -> Port
        return self._next()

    def next(self):
        # type: () -> Port
        return self._next()

    def port(self, location=None, name=None):
        # type: () -> PortIter
        """Factory method that creates an instance of Port class

        An abstract test port.
        """
        item = Port(location=location, name=name)
        self._add(item)
        return self


class Lag(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'ports': 'LagPortIter',
    }

    def __init__(self, parent=None, choice=None, name=None):
        super(Lag, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('name', name)

    @property
    def ports(self):
        # type: () -> LagPortIter
        """ports getter

        TBD

        Returns: list[obj(snappi.LagPort)]
        """
        return self._get_property('ports', LagPortIter)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)


class LagPort(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'protocol': 'LagProtocol',
        'ethernet': 'DeviceEthernetBase',
    }

    def __init__(self, parent=None, choice=None, port_name=None):
        super(LagPort, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('port_name', port_name)

    @property
    def port_name(self):
        # type: () -> str
        """port_name getter

        The name of a port object that will be part of the LAG. 

        Returns: str
        """
        return self._get_property('port_name')

    @port_name.setter
    def port_name(self, value):
        """port_name setter

        The name of a port object that will be part of the LAG. 

        value: str
        """
        self._set_property('port_name', value)

    @property
    def protocol(self):
        # type: () -> LagProtocol
        """protocol getter

        

        Returns: obj(snappi.LagProtocol)
        """
        return self._get_property('protocol', LagProtocol)

    @property
    def ethernet(self):
        # type: () -> DeviceEthernetBase
        """ethernet getter

        Base ethernet interface

        Returns: obj(snappi.DeviceEthernetBase)
        """
        return self._get_property('ethernet', DeviceEthernetBase)


class LagProtocol(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'lacp': 'LagLacp',
        'static': 'LagStatic',
    }

    LACP = 'lacp'
    STATIC = 'static'

    def __init__(self, parent=None, choice=None):
        super(LagProtocol, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def lacp(self):
        # type: () -> LagLacp
        """Factory property that returns an instance of the LagLacp class

        The container for link aggregation control protocol settings.
        """
        return self._get_property('lacp', LagLacp(self, 'lacp'))

    @property
    def static(self):
        # type: () -> LagStatic
        """Factory property that returns an instance of the LagStatic class

        The container for static link aggregation protocol settings.
        """
        return self._get_property('static', LagStatic(self, 'static'))

    @property
    def choice(self):
        # type: () -> Union[lacp, static, choice, choice, choice]
        """choice getter

        The type of LAG protocol.

        Returns: Union[lacp, static, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        The type of LAG protocol.

        value: Union[lacp, static, choice, choice, choice]
        """
        self._set_property('choice', value)


class LagLacp(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    FAST = '1'
    SLOW = '30'
    AUTO = '0'

    SHORT = '3'
    LONG = '90'
    AUTO = '0'

    PASSIVE = 'passive'
    ACTIVE = 'active'

    def __init__(self, parent=None, choice=None, actor_key=None, actor_port_number=None, actor_port_priority=None, actor_system_id=None, actor_system_priority=None, lacpdu_periodic_time_interval=None, lacpdu_timeout=None, actor_activity=None):
        super(LagLacp, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('actor_key', actor_key)
        self._set_property('actor_port_number', actor_port_number)
        self._set_property('actor_port_priority', actor_port_priority)
        self._set_property('actor_system_id', actor_system_id)
        self._set_property('actor_system_priority', actor_system_priority)
        self._set_property('lacpdu_periodic_time_interval', lacpdu_periodic_time_interval)
        self._set_property('lacpdu_timeout', lacpdu_timeout)
        self._set_property('actor_activity', actor_activity)

    @property
    def actor_key(self):
        # type: () -> int
        """actor_key getter

        The actor key

        Returns: int
        """
        return self._get_property('actor_key')

    @actor_key.setter
    def actor_key(self, value):
        """actor_key setter

        The actor key

        value: int
        """
        self._set_property('actor_key', value)

    @property
    def actor_port_number(self):
        # type: () -> int
        """actor_port_number getter

        The actor port number

        Returns: int
        """
        return self._get_property('actor_port_number')

    @actor_port_number.setter
    def actor_port_number(self, value):
        """actor_port_number setter

        The actor port number

        value: int
        """
        self._set_property('actor_port_number', value)

    @property
    def actor_port_priority(self):
        # type: () -> int
        """actor_port_priority getter

        The actor port priority

        Returns: int
        """
        return self._get_property('actor_port_priority')

    @actor_port_priority.setter
    def actor_port_priority(self, value):
        """actor_port_priority setter

        The actor port priority

        value: int
        """
        self._set_property('actor_port_priority', value)

    @property
    def actor_system_id(self):
        # type: () -> str
        """actor_system_id getter

        The actor system id

        Returns: str
        """
        return self._get_property('actor_system_id')

    @actor_system_id.setter
    def actor_system_id(self, value):
        """actor_system_id setter

        The actor system id

        value: str
        """
        self._set_property('actor_system_id', value)

    @property
    def actor_system_priority(self):
        # type: () -> int
        """actor_system_priority getter

        The actor system priority

        Returns: int
        """
        return self._get_property('actor_system_priority')

    @actor_system_priority.setter
    def actor_system_priority(self, value):
        """actor_system_priority setter

        The actor system priority

        value: int
        """
        self._set_property('actor_system_priority', value)

    @property
    def lacpdu_periodic_time_interval(self):
        # type: () -> int
        """lacpdu_periodic_time_interval getter

        This field defines how frequently LACPDUs are sent to the link partner

        Returns: int
        """
        return self._get_property('lacpdu_periodic_time_interval')

    @lacpdu_periodic_time_interval.setter
    def lacpdu_periodic_time_interval(self, value):
        """lacpdu_periodic_time_interval setter

        This field defines how frequently LACPDUs are sent to the link partner

        value: int
        """
        self._set_property('lacpdu_periodic_time_interval', value)

    @property
    def lacpdu_timeout(self):
        # type: () -> int
        """lacpdu_timeout getter

        This timer is used to detect whether received protocol information has expired

        Returns: int
        """
        return self._get_property('lacpdu_timeout')

    @lacpdu_timeout.setter
    def lacpdu_timeout(self, value):
        """lacpdu_timeout setter

        This timer is used to detect whether received protocol information has expired

        value: int
        """
        self._set_property('lacpdu_timeout', value)

    @property
    def actor_activity(self):
        # type: () -> Union[passive, active]
        """actor_activity getter

        Sets the value of LACP actor activity as either passive or active. Passive indicates the port's preference for not transmitting LACPDUs unless its partner's control is Active. Active indicates the port's preference to participate in the protocol regardless of the partner's control value

        Returns: Union[passive, active]
        """
        return self._get_property('actor_activity')

    @actor_activity.setter
    def actor_activity(self, value):
        """actor_activity setter

        Sets the value of LACP actor activity as either passive or active. Passive indicates the port's preference for not transmitting LACPDUs unless its partner's control is Active. Active indicates the port's preference to participate in the protocol regardless of the partner's control value

        value: Union[passive, active]
        """
        self._set_property('actor_activity', value)


class LagStatic(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, lag_id=None):
        super(LagStatic, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('lag_id', lag_id)

    @property
    def lag_id(self):
        # type: () -> int
        """lag_id getter

        The static lag id

        Returns: int
        """
        return self._get_property('lag_id')

    @lag_id.setter
    def lag_id(self, value):
        """lag_id setter

        The static lag id

        value: int
        """
        self._set_property('lag_id', value)


class DeviceEthernetBase(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'vlans': 'DeviceVlanIter',
    }

    def __init__(self, parent=None, choice=None, mac=None, mtu=None, name=None):
        super(DeviceEthernetBase, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('mac', mac)
        self._set_property('mtu', mtu)
        self._set_property('name', name)

    @property
    def mac(self):
        # type: () -> str
        """mac getter

        Media access control address

        Returns: str
        """
        return self._get_property('mac')

    @mac.setter
    def mac(self, value):
        """mac setter

        Media access control address

        value: str
        """
        self._set_property('mac', value)

    @property
    def mtu(self):
        # type: () -> int
        """mtu getter

        Maximum transmission unit

        Returns: int
        """
        return self._get_property('mtu')

    @mtu.setter
    def mtu(self, value):
        """mtu setter

        Maximum transmission unit

        value: int
        """
        self._set_property('mtu', value)

    @property
    def vlans(self):
        # type: () -> DeviceVlanIter
        """vlans getter

        List of VLANs

        Returns: list[obj(snappi.DeviceVlan)]
        """
        return self._get_property('vlans', DeviceVlanIter)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)


class DeviceVlan(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    X8100 = 'x8100'
    X88A8 = 'x88A8'
    X9100 = 'x9100'
    X9200 = 'x9200'
    X9300 = 'x9300'

    def __init__(self, parent=None, choice=None, tpid=None, priority=None, id=None, name=None):
        super(DeviceVlan, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('tpid', tpid)
        self._set_property('priority', priority)
        self._set_property('id', id)
        self._set_property('name', name)

    @property
    def tpid(self):
        # type: () -> Union[x8100, x88A8, x9100, x9200, x9300]
        """tpid getter

        Tag protocol identifier

        Returns: Union[x8100, x88A8, x9100, x9200, x9300]
        """
        return self._get_property('tpid')

    @tpid.setter
    def tpid(self, value):
        """tpid setter

        Tag protocol identifier

        value: Union[x8100, x88A8, x9100, x9200, x9300]
        """
        self._set_property('tpid', value)

    @property
    def priority(self):
        # type: () -> int
        """priority getter

        Priority code point

        Returns: int
        """
        return self._get_property('priority')

    @priority.setter
    def priority(self, value):
        """priority setter

        Priority code point

        value: int
        """
        self._set_property('priority', value)

    @property
    def id(self):
        # type: () -> int
        """id getter

        VLAN identifier

        Returns: int
        """
        return self._get_property('id')

    @id.setter
    def id(self, value):
        """id setter

        VLAN identifier

        value: int
        """
        self._set_property('id', value)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)


class DeviceVlanIter(SnappiIter):
    __slots__ = ()

    def __init__(self):
        super(DeviceVlanIter, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[DeviceVlan]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> DeviceVlanIter
        return self._iter()

    def __next__(self):
        # type: () -> DeviceVlan
        return self._next()

    def next(self):
        # type: () -> DeviceVlan
        return self._next()

    def vlan(self, tpid='x8100', priority=0, id=1, name=None):
        # type: () -> DeviceVlanIter
        """Factory method that creates an instance of DeviceVlan class

        Emulated VLAN protocol
        """
        item = DeviceVlan(tpid=tpid, priority=priority, id=id, name=name)
        self._add(item)
        return self


class LagPortIter(SnappiIter):
    __slots__ = ()

    def __init__(self):
        super(LagPortIter, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[LagPort]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> LagPortIter
        return self._iter()

    def __next__(self):
        # type: () -> LagPort
        return self._next()

    def next(self):
        # type: () -> LagPort
        return self._next()

    def port(self, port_name=None):
        # type: () -> LagPortIter
        """Factory method that creates an instance of LagPort class

        The container for a port's ethernet interface and LAG protocol settings
        """
        item = LagPort(port_name=port_name)
        self._add(item)
        return self


class LagIter(SnappiIter):
    __slots__ = ()

    def __init__(self):
        super(LagIter, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[Lag]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> LagIter
        return self._iter()

    def __next__(self):
        # type: () -> Lag
        return self._next()

    def next(self):
        # type: () -> Lag
        return self._next()

    def lag(self, name=None):
        # type: () -> LagIter
        """Factory method that creates an instance of Lag class

        The container for multiple LAG ports
        """
        item = Lag(name=name)
        self._add(item)
        return self


class Layer1(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'auto_negotiation': 'Layer1AutoNegotiation',
        'flow_control': 'Layer1FlowControl',
    }

    SPEED_10_FD_MBPS = 'speed_10_fd_mbps'
    SPEED_10_HD_MBPS = 'speed_10_hd_mbps'
    SPEED_100_FD_MBPS = 'speed_100_fd_mbps'
    SPEED_100_HD_MBPS = 'speed_100_hd_mbps'
    SPEED_1_GBPS = 'speed_1_gbps'
    SPEED_10_GBPS = 'speed_10_gbps'
    SPEED_25_GBPS = 'speed_25_gbps'
    SPEED_40_GBPS = 'speed_40_gbps'
    SPEED_100_GBPS = 'speed_100_gbps'
    SPEED_200_GBPS = 'speed_200_gbps'
    SPEED_400_GBPS = 'speed_400_gbps'

    COPPER = 'copper'
    FIBER = 'fiber'
    SGMII = 'sgmii'

    def __init__(self, parent=None, choice=None, port_names=None, speed=None, media=None, promiscuous=None, mtu=None, ieee_media_defaults=None, auto_negotiate=None, name=None):
        super(Layer1, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('port_names', port_names)
        self._set_property('speed', speed)
        self._set_property('media', media)
        self._set_property('promiscuous', promiscuous)
        self._set_property('mtu', mtu)
        self._set_property('ieee_media_defaults', ieee_media_defaults)
        self._set_property('auto_negotiate', auto_negotiate)
        self._set_property('name', name)

    @property
    def port_names(self):
        # type: () -> list[str]
        """port_names getter

        A list of unique names of port objects that will share the choice settings. 

        Returns: list[str]
        """
        return self._get_property('port_names')

    @port_names.setter
    def port_names(self, value):
        """port_names setter

        A list of unique names of port objects that will share the choice settings. 

        value: list[str]
        """
        self._set_property('port_names', value)

    @property
    def speed(self):
        # type: () -> Union[speed_10_fd_mbps, speed_10_hd_mbps, speed_100_fd_mbps, speed_100_hd_mbps, speed_1_gbps, speed_10_gbps, speed_25_gbps, speed_40_gbps, speed_100_gbps, speed_200_gbps, speed_400_gbps]
        """speed getter

        Set the speed if supported.

        Returns: Union[speed_10_fd_mbps, speed_10_hd_mbps, speed_100_fd_mbps, speed_100_hd_mbps, speed_1_gbps, speed_10_gbps, speed_25_gbps, speed_40_gbps, speed_100_gbps, speed_200_gbps, speed_400_gbps]
        """
        return self._get_property('speed')

    @speed.setter
    def speed(self, value):
        """speed setter

        Set the speed if supported.

        value: Union[speed_10_fd_mbps, speed_10_hd_mbps, speed_100_fd_mbps, speed_100_hd_mbps, speed_1_gbps, speed_10_gbps, speed_25_gbps, speed_40_gbps, speed_100_gbps, speed_200_gbps, speed_400_gbps]
        """
        self._set_property('speed', value)

    @property
    def media(self):
        # type: () -> Union[copper, fiber, sgmii]
        """media getter

        Set the type of media interface if supported.

        Returns: Union[copper, fiber, sgmii]
        """
        return self._get_property('media')

    @media.setter
    def media(self, value):
        """media setter

        Set the type of media interface if supported.

        value: Union[copper, fiber, sgmii]
        """
        self._set_property('media', value)

    @property
    def promiscuous(self):
        # type: () -> boolean
        """promiscuous getter

        Enable promiscuous mode if supported.

        Returns: boolean
        """
        return self._get_property('promiscuous')

    @promiscuous.setter
    def promiscuous(self, value):
        """promiscuous setter

        Enable promiscuous mode if supported.

        value: boolean
        """
        self._set_property('promiscuous', value)

    @property
    def mtu(self):
        # type: () -> int
        """mtu getter

        Set the maximum transmission unit size if supported.

        Returns: int
        """
        return self._get_property('mtu')

    @mtu.setter
    def mtu(self, value):
        """mtu setter

        Set the maximum transmission unit size if supported.

        value: int
        """
        self._set_property('mtu', value)

    @property
    def ieee_media_defaults(self):
        # type: () -> boolean
        """ieee_media_defaults getter

        Set to true to override the auto_negotiate, link_training and rs_fec settings for gigabit ethernet interfaces.

        Returns: boolean
        """
        return self._get_property('ieee_media_defaults')

    @ieee_media_defaults.setter
    def ieee_media_defaults(self, value):
        """ieee_media_defaults setter

        Set to true to override the auto_negotiate, link_training and rs_fec settings for gigabit ethernet interfaces.

        value: boolean
        """
        self._set_property('ieee_media_defaults', value)

    @property
    def auto_negotiate(self):
        # type: () -> boolean
        """auto_negotiate getter

        Enable/disable auto negotiation.

        Returns: boolean
        """
        return self._get_property('auto_negotiate')

    @auto_negotiate.setter
    def auto_negotiate(self, value):
        """auto_negotiate setter

        Enable/disable auto negotiation.

        value: boolean
        """
        self._set_property('auto_negotiate', value)

    @property
    def auto_negotiation(self):
        # type: () -> Layer1AutoNegotiation
        """auto_negotiation getter

        Container for auto negotiation settings

        Returns: obj(snappi.Layer1AutoNegotiation)
        """
        return self._get_property('auto_negotiation', Layer1AutoNegotiation)

    @property
    def flow_control(self):
        # type: () -> Layer1FlowControl
        """flow_control getter

        A container for layer1 receive flow control settings. To enable flow control settings on ports this object must be a valid object not a null value.

        Returns: obj(snappi.Layer1FlowControl)
        """
        return self._get_property('flow_control', Layer1FlowControl)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)


class Layer1AutoNegotiation(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, advertise_1000_mbps=None, advertise_100_fd_mbps=None, advertise_100_hd_mbps=None, advertise_10_fd_mbps=None, advertise_10_hd_mbps=None, link_training=None, rs_fec=None):
        super(Layer1AutoNegotiation, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('advertise_1000_mbps', advertise_1000_mbps)
        self._set_property('advertise_100_fd_mbps', advertise_100_fd_mbps)
        self._set_property('advertise_100_hd_mbps', advertise_100_hd_mbps)
        self._set_property('advertise_10_fd_mbps', advertise_10_fd_mbps)
        self._set_property('advertise_10_hd_mbps', advertise_10_hd_mbps)
        self._set_property('link_training', link_training)
        self._set_property('rs_fec', rs_fec)

    @property
    def advertise_1000_mbps(self):
        # type: () -> boolean
        """advertise_1000_mbps getter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        Returns: boolean
        """
        return self._get_property('advertise_1000_mbps')

    @advertise_1000_mbps.setter
    def advertise_1000_mbps(self, value):
        """advertise_1000_mbps setter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        value: boolean
        """
        self._set_property('advertise_1000_mbps', value)

    @property
    def advertise_100_fd_mbps(self):
        # type: () -> boolean
        """advertise_100_fd_mbps getter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        Returns: boolean
        """
        return self._get_property('advertise_100_fd_mbps')

    @advertise_100_fd_mbps.setter
    def advertise_100_fd_mbps(self, value):
        """advertise_100_fd_mbps setter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        value: boolean
        """
        self._set_property('advertise_100_fd_mbps', value)

    @property
    def advertise_100_hd_mbps(self):
        # type: () -> boolean
        """advertise_100_hd_mbps getter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        Returns: boolean
        """
        return self._get_property('advertise_100_hd_mbps')

    @advertise_100_hd_mbps.setter
    def advertise_100_hd_mbps(self, value):
        """advertise_100_hd_mbps setter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        value: boolean
        """
        self._set_property('advertise_100_hd_mbps', value)

    @property
    def advertise_10_fd_mbps(self):
        # type: () -> boolean
        """advertise_10_fd_mbps getter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        Returns: boolean
        """
        return self._get_property('advertise_10_fd_mbps')

    @advertise_10_fd_mbps.setter
    def advertise_10_fd_mbps(self, value):
        """advertise_10_fd_mbps setter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        value: boolean
        """
        self._set_property('advertise_10_fd_mbps', value)

    @property
    def advertise_10_hd_mbps(self):
        # type: () -> boolean
        """advertise_10_hd_mbps getter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        Returns: boolean
        """
        return self._get_property('advertise_10_hd_mbps')

    @advertise_10_hd_mbps.setter
    def advertise_10_hd_mbps(self, value):
        """advertise_10_hd_mbps setter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        value: boolean
        """
        self._set_property('advertise_10_hd_mbps', value)

    @property
    def link_training(self):
        # type: () -> boolean
        """link_training getter

        Enable/disable gigabit ethernet link training.

        Returns: boolean
        """
        return self._get_property('link_training')

    @link_training.setter
    def link_training(self, value):
        """link_training setter

        Enable/disable gigabit ethernet link training.

        value: boolean
        """
        self._set_property('link_training', value)

    @property
    def rs_fec(self):
        # type: () -> boolean
        """rs_fec getter

        Enable/disable gigabit ethernet reed solomon forward error correction (RS FEC).

        Returns: boolean
        """
        return self._get_property('rs_fec')

    @rs_fec.setter
    def rs_fec(self, value):
        """rs_fec setter

        Enable/disable gigabit ethernet reed solomon forward error correction (RS FEC).

        value: boolean
        """
        self._set_property('rs_fec', value)


class Layer1FlowControl(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'ieee_802_1qbb': 'Layer1Ieee8021qbb',
        'ieee_802_3x': 'Layer1Ieee8023x',
    }

    IEEE_802_1QBB = 'ieee_802_1qbb'
    IEEE_802_3X = 'ieee_802_3x'

    def __init__(self, parent=None, choice=None, directed_address=None):
        super(Layer1FlowControl, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('directed_address', directed_address)

    @property
    def ieee_802_1qbb(self):
        # type: () -> Layer1Ieee8021qbb
        """Factory property that returns an instance of the Layer1Ieee8021qbb class

        These settings enhance the existing 802.3x pause priority capabilities to enable flow control based on 802.1p priorities (classes of service). 
        """
        return self._get_property('ieee_802_1qbb', Layer1Ieee8021qbb(self, 'ieee_802_1qbb'))

    @property
    def ieee_802_3x(self):
        # type: () -> Layer1Ieee8023x
        """Factory property that returns an instance of the Layer1Ieee8023x class

        A container for ieee 802.3x rx pause settings
        """
        return self._get_property('ieee_802_3x', Layer1Ieee8023x(self, 'ieee_802_3x'))

    @property
    def directed_address(self):
        # type: () -> str
        """directed_address getter

        The 48bit mac address that the layer1 port names will listen on for a directed pause. 

        Returns: str
        """
        return self._get_property('directed_address')

    @directed_address.setter
    def directed_address(self, value):
        """directed_address setter

        The 48bit mac address that the layer1 port names will listen on for a directed pause. 

        value: str
        """
        self._set_property('directed_address', value)

    @property
    def choice(self):
        # type: () -> Union[ieee_802_1qbb, ieee_802_3x, choice, choice, choice]
        """choice getter

        The type of priority flow control.

        Returns: Union[ieee_802_1qbb, ieee_802_3x, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        The type of priority flow control.

        value: Union[ieee_802_1qbb, ieee_802_3x, choice, choice, choice]
        """
        self._set_property('choice', value)


class Layer1Ieee8021qbb(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, pfc_delay=None, pfc_class_0=None, pfc_class_1=None, pfc_class_2=None, pfc_class_3=None, pfc_class_4=None, pfc_class_5=None, pfc_class_6=None, pfc_class_7=None):
        super(Layer1Ieee8021qbb, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('pfc_delay', pfc_delay)
        self._set_property('pfc_class_0', pfc_class_0)
        self._set_property('pfc_class_1', pfc_class_1)
        self._set_property('pfc_class_2', pfc_class_2)
        self._set_property('pfc_class_3', pfc_class_3)
        self._set_property('pfc_class_4', pfc_class_4)
        self._set_property('pfc_class_5', pfc_class_5)
        self._set_property('pfc_class_6', pfc_class_6)
        self._set_property('pfc_class_7', pfc_class_7)

    @property
    def pfc_delay(self):
        # type: () -> int
        """pfc_delay getter

        The upper limit on the transmit time of a queue after receiving a message to pause a specified priority. A value of 0 or null indicates that pfc delay will not be enabled. 

        Returns: int
        """
        return self._get_property('pfc_delay')

    @pfc_delay.setter
    def pfc_delay(self, value):
        """pfc_delay setter

        The upper limit on the transmit time of a queue after receiving a message to pause a specified priority. A value of 0 or null indicates that pfc delay will not be enabled. 

        value: int
        """
        self._set_property('pfc_delay', value)

    @property
    def pfc_class_0(self):
        # type: () -> int
        """pfc_class_0 getter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        Returns: int
        """
        return self._get_property('pfc_class_0')

    @pfc_class_0.setter
    def pfc_class_0(self, value):
        """pfc_class_0 setter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        value: int
        """
        self._set_property('pfc_class_0', value)

    @property
    def pfc_class_1(self):
        # type: () -> int
        """pfc_class_1 getter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        Returns: int
        """
        return self._get_property('pfc_class_1')

    @pfc_class_1.setter
    def pfc_class_1(self, value):
        """pfc_class_1 setter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        value: int
        """
        self._set_property('pfc_class_1', value)

    @property
    def pfc_class_2(self):
        # type: () -> int
        """pfc_class_2 getter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        Returns: int
        """
        return self._get_property('pfc_class_2')

    @pfc_class_2.setter
    def pfc_class_2(self, value):
        """pfc_class_2 setter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        value: int
        """
        self._set_property('pfc_class_2', value)

    @property
    def pfc_class_3(self):
        # type: () -> int
        """pfc_class_3 getter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        Returns: int
        """
        return self._get_property('pfc_class_3')

    @pfc_class_3.setter
    def pfc_class_3(self, value):
        """pfc_class_3 setter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        value: int
        """
        self._set_property('pfc_class_3', value)

    @property
    def pfc_class_4(self):
        # type: () -> int
        """pfc_class_4 getter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        Returns: int
        """
        return self._get_property('pfc_class_4')

    @pfc_class_4.setter
    def pfc_class_4(self, value):
        """pfc_class_4 setter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        value: int
        """
        self._set_property('pfc_class_4', value)

    @property
    def pfc_class_5(self):
        # type: () -> int
        """pfc_class_5 getter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        Returns: int
        """
        return self._get_property('pfc_class_5')

    @pfc_class_5.setter
    def pfc_class_5(self, value):
        """pfc_class_5 setter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        value: int
        """
        self._set_property('pfc_class_5', value)

    @property
    def pfc_class_6(self):
        # type: () -> int
        """pfc_class_6 getter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        Returns: int
        """
        return self._get_property('pfc_class_6')

    @pfc_class_6.setter
    def pfc_class_6(self, value):
        """pfc_class_6 setter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        value: int
        """
        self._set_property('pfc_class_6', value)

    @property
    def pfc_class_7(self):
        # type: () -> int
        """pfc_class_7 getter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        Returns: int
        """
        return self._get_property('pfc_class_7')

    @pfc_class_7.setter
    def pfc_class_7(self, value):
        """pfc_class_7 setter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        value: int
        """
        self._set_property('pfc_class_7', value)


class Layer1Ieee8023x(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None):
        super(Layer1Ieee8023x, self).__init__()
        self._parent = parent
        self._choice = choice


class Layer1Iter(SnappiIter):
    __slots__ = ()

    def __init__(self):
        super(Layer1Iter, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[Layer1]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> Layer1Iter
        return self._iter()

    def __next__(self):
        # type: () -> Layer1
        return self._next()

    def next(self):
        # type: () -> Layer1
        return self._next()

    def layer1(self, port_names=None, speed='speed_10_gbps', media=None, promiscuous=False, mtu=1500, ieee_media_defaults=True, auto_negotiate=True, name=None):
        # type: () -> Layer1Iter
        """Factory method that creates an instance of Layer1 class

        A container for layer1 settings.
        """
        item = Layer1(port_names=port_names, speed=speed, media=media, promiscuous=promiscuous, mtu=mtu, ieee_media_defaults=ieee_media_defaults, auto_negotiate=auto_negotiate, name=name)
        self._add(item)
        return self


class Capture(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'filters': 'CaptureFilterIter',
    }

    PCAP = 'pcap'
    PCAPNG = 'pcapng'

    def __init__(self, parent=None, choice=None, port_names=None, overwrite=None, packet_size=None, format=None, name=None):
        super(Capture, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('port_names', port_names)
        self._set_property('overwrite', overwrite)
        self._set_property('packet_size', packet_size)
        self._set_property('format', format)
        self._set_property('name', name)

    @property
    def port_names(self):
        # type: () -> list[str]
        """port_names getter

        The unique names of ports that the capture settings will apply to. Port_names cannot be duplicated between capture objects.

        Returns: list[str]
        """
        return self._get_property('port_names')

    @port_names.setter
    def port_names(self, value):
        """port_names setter

        The unique names of ports that the capture settings will apply to. Port_names cannot be duplicated between capture objects.

        value: list[str]
        """
        self._set_property('port_names', value)

    @property
    def filters(self):
        # type: () -> CaptureFilterIter
        """filters getter

        A list of filters to apply to the capturing ports. If no filters are specified then all packets will be captured. A capture can have multiple filters. The number of filters supported is determined by the implementation which can be retrieved using the capabilities API.. When multiple filters are specified the capture implementation must && (and) all the filters.

        Returns: list[obj(snappi.CaptureFilter)]
        """
        return self._get_property('filters', CaptureFilterIter)

    @property
    def overwrite(self):
        # type: () -> boolean
        """overwrite getter

        Overwrite the capture buffer.

        Returns: boolean
        """
        return self._get_property('overwrite')

    @overwrite.setter
    def overwrite(self, value):
        """overwrite setter

        Overwrite the capture buffer.

        value: boolean
        """
        self._set_property('overwrite', value)

    @property
    def packet_size(self):
        # type: () -> int
        """packet_size getter

        The maximum size of each captured packet. If no value is specified or it is null then the entire packet will be captured.

        Returns: int
        """
        return self._get_property('packet_size')

    @packet_size.setter
    def packet_size(self, value):
        """packet_size setter

        The maximum size of each captured packet. If no value is specified or it is null then the entire packet will be captured.

        value: int
        """
        self._set_property('packet_size', value)

    @property
    def format(self):
        # type: () -> Union[pcap, pcapng]
        """format getter

        The format of the capture file.

        Returns: Union[pcap, pcapng]
        """
        return self._get_property('format')

    @format.setter
    def format(self, value):
        """format setter

        The format of the capture file.

        value: Union[pcap, pcapng]
        """
        self._set_property('format', value)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)


class CaptureFilter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'custom': 'CaptureCustom',
        'ethernet': 'CaptureEthernet',
        'vlan': 'CaptureVlan',
        'ipv4': 'CaptureIpv4',
    }

    CUSTOM = 'custom'
    ETHERNET = 'ethernet'
    VLAN = 'vlan'
    IPV4 = 'ipv4'

    def __init__(self, parent=None, choice=None):
        super(CaptureFilter, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def custom(self):
        # type: () -> CaptureCustom
        """Factory property that returns an instance of the CaptureCustom class

        TBD
        """
        return self._get_property('custom', CaptureCustom(self, 'custom'))

    @property
    def ethernet(self):
        # type: () -> CaptureEthernet
        """Factory property that returns an instance of the CaptureEthernet class

        TBD
        """
        return self._get_property('ethernet', CaptureEthernet(self, 'ethernet'))

    @property
    def vlan(self):
        # type: () -> CaptureVlan
        """Factory property that returns an instance of the CaptureVlan class

        TBD
        """
        return self._get_property('vlan', CaptureVlan(self, 'vlan'))

    @property
    def ipv4(self):
        # type: () -> CaptureIpv4
        """Factory property that returns an instance of the CaptureIpv4 class

        TBD
        """
        return self._get_property('ipv4', CaptureIpv4(self, 'ipv4'))

    @property
    def choice(self):
        # type: () -> Union[custom, ethernet, vlan, ipv4, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[custom, ethernet, vlan, ipv4, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[custom, ethernet, vlan, ipv4, choice, choice, choice]
        """
        self._set_property('choice', value)


class CaptureCustom(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, offset=None, value=None, mask=None, negate=None):
        super(CaptureCustom, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('offset', offset)
        self._set_property('value', value)
        self._set_property('mask', mask)
        self._set_property('negate', negate)

    @property
    def offset(self):
        # type: () -> int
        """offset getter

        The byte offset to filter on

        Returns: int
        """
        return self._get_property('offset')

    @offset.setter
    def offset(self, value):
        """offset setter

        The byte offset to filter on

        value: int
        """
        self._set_property('offset', value)

    @property
    def value(self):
        # type: () -> str
        """value getter

        TBD

        Returns: str
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: str
        """
        self._set_property('value', value)

    @property
    def mask(self):
        # type: () -> str
        """mask getter

        TBD

        Returns: str
        """
        return self._get_property('mask')

    @mask.setter
    def mask(self, value):
        """mask setter

        TBD

        value: str
        """
        self._set_property('mask', value)

    @property
    def negate(self):
        # type: () -> boolean
        """negate getter

        TBD

        Returns: boolean
        """
        return self._get_property('negate')

    @negate.setter
    def negate(self, value):
        """negate setter

        TBD

        value: boolean
        """
        self._set_property('negate', value)


class CaptureEthernet(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'src': 'CaptureField',
        'dst': 'CaptureField',
        'ether_type': 'CaptureField',
        'pfc_queue': 'CaptureField',
    }

    def __init__(self, parent=None, choice=None):
        super(CaptureEthernet, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def src(self):
        # type: () -> CaptureField
        """src getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('src', CaptureField)

    @property
    def dst(self):
        # type: () -> CaptureField
        """dst getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('dst', CaptureField)

    @property
    def ether_type(self):
        # type: () -> CaptureField
        """ether_type getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('ether_type', CaptureField)

    @property
    def pfc_queue(self):
        # type: () -> CaptureField
        """pfc_queue getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('pfc_queue', CaptureField)


class CaptureField(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, value=None, mask=None, negate=None):
        super(CaptureField, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('value', value)
        self._set_property('mask', mask)
        self._set_property('negate', negate)

    @property
    def value(self):
        # type: () -> str
        """value getter

        TBD

        Returns: str
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: str
        """
        self._set_property('value', value)

    @property
    def mask(self):
        # type: () -> str
        """mask getter

        TBD

        Returns: str
        """
        return self._get_property('mask')

    @mask.setter
    def mask(self, value):
        """mask setter

        TBD

        value: str
        """
        self._set_property('mask', value)

    @property
    def negate(self):
        # type: () -> boolean
        """negate getter

        TBD

        Returns: boolean
        """
        return self._get_property('negate')

    @negate.setter
    def negate(self, value):
        """negate setter

        TBD

        value: boolean
        """
        self._set_property('negate', value)


class CaptureVlan(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'priority': 'CaptureField',
        'cfi': 'CaptureField',
        'id': 'CaptureField',
        'protocol': 'CaptureField',
    }

    def __init__(self, parent=None, choice=None):
        super(CaptureVlan, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def priority(self):
        # type: () -> CaptureField
        """priority getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('priority', CaptureField)

    @property
    def cfi(self):
        # type: () -> CaptureField
        """cfi getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('cfi', CaptureField)

    @property
    def id(self):
        # type: () -> CaptureField
        """id getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('id', CaptureField)

    @property
    def protocol(self):
        # type: () -> CaptureField
        """protocol getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('protocol', CaptureField)


class CaptureIpv4(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'version': 'CaptureField',
        'headeer_length': 'CaptureField',
        'priority': 'CaptureField',
        'total_length': 'CaptureField',
        'identification': 'CaptureField',
        'reserved': 'CaptureField',
        'dont_fragment': 'CaptureField',
        'more_fragments': 'CaptureField',
        'fragment_offset': 'CaptureField',
        'time_to_live': 'CaptureField',
        'protocol': 'CaptureField',
        'header_checksum': 'CaptureField',
        'src': 'CaptureField',
        'dst': 'CaptureField',
    }

    def __init__(self, parent=None, choice=None):
        super(CaptureIpv4, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def version(self):
        # type: () -> CaptureField
        """version getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('version', CaptureField)

    @property
    def headeer_length(self):
        # type: () -> CaptureField
        """headeer_length getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('headeer_length', CaptureField)

    @property
    def priority(self):
        # type: () -> CaptureField
        """priority getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('priority', CaptureField)

    @property
    def total_length(self):
        # type: () -> CaptureField
        """total_length getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('total_length', CaptureField)

    @property
    def identification(self):
        # type: () -> CaptureField
        """identification getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('identification', CaptureField)

    @property
    def reserved(self):
        # type: () -> CaptureField
        """reserved getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('reserved', CaptureField)

    @property
    def dont_fragment(self):
        # type: () -> CaptureField
        """dont_fragment getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('dont_fragment', CaptureField)

    @property
    def more_fragments(self):
        # type: () -> CaptureField
        """more_fragments getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('more_fragments', CaptureField)

    @property
    def fragment_offset(self):
        # type: () -> CaptureField
        """fragment_offset getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('fragment_offset', CaptureField)

    @property
    def time_to_live(self):
        # type: () -> CaptureField
        """time_to_live getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('time_to_live', CaptureField)

    @property
    def protocol(self):
        # type: () -> CaptureField
        """protocol getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('protocol', CaptureField)

    @property
    def header_checksum(self):
        # type: () -> CaptureField
        """header_checksum getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('header_checksum', CaptureField)

    @property
    def src(self):
        # type: () -> CaptureField
        """src getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('src', CaptureField)

    @property
    def dst(self):
        # type: () -> CaptureField
        """dst getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('dst', CaptureField)


class CaptureFilterIter(SnappiIter):
    __slots__ = ()

    def __init__(self):
        super(CaptureFilterIter, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[CaptureEthernet, CaptureCustom, CaptureVlan, CaptureIpv4, CaptureFilter]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> CaptureFilterIter
        return self._iter()

    def __next__(self):
        # type: () -> CaptureFilter
        return self._next()

    def next(self):
        # type: () -> CaptureFilter
        return self._next()

    def filter(self):
        # type: () -> CaptureFilterIter
        """Factory method that creates an instance of CaptureFilter class

        Container for capture filters
        """
        item = CaptureFilter()
        self._add(item)
        return self

    def custom(self, offset=None, value=None, mask=None, negate=False):
        # type: () -> CaptureFilterIter
        """Factory method that creates an instance of CaptureCustom class

        TBD
        """
        item = CaptureFilter()
        item.custom
        item.choice = 'custom'
        self._add(item)
        return self

    def ethernet(self):
        # type: () -> CaptureFilterIter
        """Factory method that creates an instance of CaptureEthernet class

        TBD
        """
        item = CaptureFilter()
        item.ethernet
        item.choice = 'ethernet'
        self._add(item)
        return self

    def vlan(self):
        # type: () -> CaptureFilterIter
        """Factory method that creates an instance of CaptureVlan class

        TBD
        """
        item = CaptureFilter()
        item.vlan
        item.choice = 'vlan'
        self._add(item)
        return self

    def ipv4(self):
        # type: () -> CaptureFilterIter
        """Factory method that creates an instance of CaptureIpv4 class

        TBD
        """
        item = CaptureFilter()
        item.ipv4
        item.choice = 'ipv4'
        self._add(item)
        return self


class CaptureIter(SnappiIter):
    __slots__ = ()

    def __init__(self):
        super(CaptureIter, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[Capture]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> CaptureIter
        return self._iter()

    def __next__(self):
        # type: () -> Capture
        return self._next()

    def next(self):
        # type: () -> Capture
        return self._next()

    def capture(self, port_names=None, overwrite=False, packet_size=None, format='pcap', name=None):
        # type: () -> CaptureIter
        """Factory method that creates an instance of Capture class

        Container for capture settings.
        """
        item = Capture(port_names=port_names, overwrite=overwrite, packet_size=packet_size, format=format, name=name)
        self._add(item)
        return self


class Device(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'ethernet': 'DeviceEthernet',
    }

    def __init__(self, parent=None, choice=None, container_name=None, name=None):
        super(Device, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('container_name', container_name)
        self._set_property('name', name)

    @property
    def container_name(self):
        # type: () -> str
        """container_name getter

        The unique name of a Port or Lag object that will contain the emulated interfaces and/or protocol devices.

        Returns: str
        """
        return self._get_property('container_name')

    @container_name.setter
    def container_name(self, value):
        """container_name setter

        The unique name of a Port or Lag object that will contain the emulated interfaces and/or protocol devices.

        value: str
        """
        self._set_property('container_name', value)

    @property
    def ethernet(self):
        # type: () -> DeviceEthernet
        """ethernet getter

        An ethernet interface with an IPv4 and IPv6 interface stack. Base ethernet interfaceThe ethernet stack.

        Returns: obj(snappi.DeviceEthernet)
        """
        return self._get_property('ethernet', DeviceEthernet)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)


class DeviceEthernet(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'ipv4': 'DeviceIpv4',
        'ipv6': 'DeviceIpv6',
        'vlans': 'DeviceVlanIter',
    }

    def __init__(self, parent=None, choice=None, mac=None, mtu=None, name=None):
        super(DeviceEthernet, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('mac', mac)
        self._set_property('mtu', mtu)
        self._set_property('name', name)

    @property
    def ipv4(self):
        # type: () -> DeviceIpv4
        """ipv4 getter

        An IPv4 interface with gateway. A base IPv4 interface

        Returns: obj(snappi.DeviceIpv4)
        """
        return self._get_property('ipv4', DeviceIpv4)

    @property
    def ipv6(self):
        # type: () -> DeviceIpv6
        """ipv6 getter

        An IPv6 interface with gateway. A base IPv6 interface

        Returns: obj(snappi.DeviceIpv6)
        """
        return self._get_property('ipv6', DeviceIpv6)

    @property
    def mac(self):
        # type: () -> str
        """mac getter

        Media access control address

        Returns: str
        """
        return self._get_property('mac')

    @mac.setter
    def mac(self, value):
        """mac setter

        Media access control address

        value: str
        """
        self._set_property('mac', value)

    @property
    def mtu(self):
        # type: () -> int
        """mtu getter

        Maximum transmission unit

        Returns: int
        """
        return self._get_property('mtu')

    @mtu.setter
    def mtu(self, value):
        """mtu setter

        Maximum transmission unit

        value: int
        """
        self._set_property('mtu', value)

    @property
    def vlans(self):
        # type: () -> DeviceVlanIter
        """vlans getter

        List of VLANs

        Returns: list[obj(snappi.DeviceVlan)]
        """
        return self._get_property('vlans', DeviceVlanIter)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)


class DeviceIpv4(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'bgpv4': 'DeviceBgpv4',
    }

    def __init__(self, parent=None, choice=None, gateway=None, address=None, prefix=None, name=None):
        super(DeviceIpv4, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('gateway', gateway)
        self._set_property('address', address)
        self._set_property('prefix', prefix)
        self._set_property('name', name)

    @property
    def gateway(self):
        # type: () -> str
        """gateway getter

        The IPv4 address of the gateway

        Returns: str
        """
        return self._get_property('gateway')

    @gateway.setter
    def gateway(self, value):
        """gateway setter

        The IPv4 address of the gateway

        value: str
        """
        self._set_property('gateway', value)

    @property
    def address(self):
        # type: () -> str
        """address getter

        The IPv4 address

        Returns: str
        """
        return self._get_property('address')

    @address.setter
    def address(self, value):
        """address setter

        The IPv4 address

        value: str
        """
        self._set_property('address', value)

    @property
    def prefix(self):
        # type: () -> int
        """prefix getter

        The prefix of the IPv4 address

        Returns: int
        """
        return self._get_property('prefix')

    @prefix.setter
    def prefix(self, value):
        """prefix setter

        The prefix of the IPv4 address

        value: int
        """
        self._set_property('prefix', value)

    @property
    def bgpv4(self):
        # type: () -> DeviceBgpv4
        """bgpv4 getter

        Container for emulated BGPv4 peers and routes.. Container for basic emulated BGP peer settings.

        Returns: obj(snappi.DeviceBgpv4)
        """
        return self._get_property('bgpv4', DeviceBgpv4)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)


class DeviceBgpv4(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'advanced': 'DeviceBgpAdvanced',
        'capability': 'DeviceBgpCapability',
        'sr_te_policies': 'DeviceBgpSrTePolicyIter',
        'bgpv4_routes': 'DeviceBgpv4RouteIter',
        'bgpv6_routes': 'DeviceBgpv6RouteIter',
    }

    IBGP = 'ibgp'
    EBGP = 'ebgp'

    TWO = 'two'
    FOUR = 'four'

    DO_NOT_INCLUDE_AS = 'do_not_include_as'
    INCLUDE_AS_SEQ = 'include_as_seq'
    INCLUDE_AS_SET = 'include_as_set'
    INCLUDE_AS_SEQ_CONFED = 'include_as_seq_confed'
    INCLUDE_AS_SET_CONFED = 'include_as_set_confed'
    PREPEND_AS_TO_FIRST_SEGMENT = 'prepend_as_to_first_segment'

    def __init__(self, parent=None, choice=None, local_address=None, dut_address=None, router_id=None, as_type=None, as_number=None, as_number_width=None, as_number_set_mode=None, name=None, active=None):
        super(DeviceBgpv4, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('local_address', local_address)
        self._set_property('dut_address', dut_address)
        self._set_property('router_id', router_id)
        self._set_property('as_type', as_type)
        self._set_property('as_number', as_number)
        self._set_property('as_number_width', as_number_width)
        self._set_property('as_number_set_mode', as_number_set_mode)
        self._set_property('name', name)
        self._set_property('active', active)

    @property
    def local_address(self):
        # type: () -> str
        """local_address getter

        Local IPv4 address of the emulated router

        Returns: str
        """
        return self._get_property('local_address')

    @local_address.setter
    def local_address(self, value):
        """local_address setter

        Local IPv4 address of the emulated router

        value: str
        """
        self._set_property('local_address', value)

    @property
    def dut_address(self):
        # type: () -> str
        """dut_address getter

        IPv4 address of the BGP peer for the session

        Returns: str
        """
        return self._get_property('dut_address')

    @dut_address.setter
    def dut_address(self, value):
        """dut_address setter

        IPv4 address of the BGP peer for the session

        value: str
        """
        self._set_property('dut_address', value)

    @property
    def router_id(self):
        # type: () -> str
        """router_id getter

        The BGP router ID is a unique identifier used by routing protocols. It is a 32-bit value that is often represented by an IPv4 address.

        Returns: str
        """
        return self._get_property('router_id')

    @router_id.setter
    def router_id(self, value):
        """router_id setter

        The BGP router ID is a unique identifier used by routing protocols. It is a 32-bit value that is often represented by an IPv4 address.

        value: str
        """
        self._set_property('router_id', value)

    @property
    def as_type(self):
        # type: () -> Union[ibgp, ebgp]
        """as_type getter

        The type of BGP autonomous system. External BGP is used for BGP links between two or more autonomous systems (ebgp) Internal BGP is used within a single autonomous system (ibgp). BGP property defaults are aligned with this object defined as an internal BGP peer. If the as_type is specified as ebgp then other properties will need to be specified according an external BGP peer.

        Returns: Union[ibgp, ebgp]
        """
        return self._get_property('as_type')

    @as_type.setter
    def as_type(self, value):
        """as_type setter

        The type of BGP autonomous system. External BGP is used for BGP links between two or more autonomous systems (ebgp) Internal BGP is used within a single autonomous system (ibgp). BGP property defaults are aligned with this object defined as an internal BGP peer. If the as_type is specified as ebgp then other properties will need to be specified according an external BGP peer.

        value: Union[ibgp, ebgp]
        """
        self._set_property('as_type', value)

    @property
    def as_number(self):
        # type: () -> int
        """as_number getter

        Autonomous System Number (AS number or ASN)

        Returns: int
        """
        return self._get_property('as_number')

    @as_number.setter
    def as_number(self, value):
        """as_number setter

        Autonomous System Number (AS number or ASN)

        value: int
        """
        self._set_property('as_number', value)

    @property
    def as_number_width(self):
        # type: () -> Union[two, four]
        """as_number_width getter

        The width in bytes of the as_number values. Any as_number values that exceed the width MUST result in an error

        Returns: Union[two, four]
        """
        return self._get_property('as_number_width')

    @as_number_width.setter
    def as_number_width(self, value):
        """as_number_width setter

        The width in bytes of the as_number values. Any as_number values that exceed the width MUST result in an error

        value: Union[two, four]
        """
        self._set_property('as_number_width', value)

    @property
    def as_number_set_mode(self):
        # type: () -> Union[do_not_include_as, include_as_seq, include_as_set, include_as_seq_confed, include_as_set_confed, prepend_as_to_first_segment]
        """as_number_set_mode getter

        The AS number set mode

        Returns: Union[do_not_include_as, include_as_seq, include_as_set, include_as_seq_confed, include_as_set_confed, prepend_as_to_first_segment]
        """
        return self._get_property('as_number_set_mode')

    @as_number_set_mode.setter
    def as_number_set_mode(self, value):
        """as_number_set_mode setter

        The AS number set mode

        value: Union[do_not_include_as, include_as_seq, include_as_set, include_as_seq_confed, include_as_set_confed, prepend_as_to_first_segment]
        """
        self._set_property('as_number_set_mode', value)

    @property
    def advanced(self):
        # type: () -> DeviceBgpAdvanced
        """advanced getter

        Container for BGP advanced settings.

        Returns: obj(snappi.DeviceBgpAdvanced)
        """
        return self._get_property('advanced', DeviceBgpAdvanced)

    @property
    def capability(self):
        # type: () -> DeviceBgpCapability
        """capability getter

        Container for BGP capability settings.

        Returns: obj(snappi.DeviceBgpCapability)
        """
        return self._get_property('capability', DeviceBgpCapability)

    @property
    def sr_te_policies(self):
        # type: () -> DeviceBgpSrTePolicyIter
        """sr_te_policies getter

        Segment routing/traffic engineering policies

        Returns: list[obj(snappi.DeviceBgpSrTePolicy)]
        """
        return self._get_property('sr_te_policies', DeviceBgpSrTePolicyIter)

    @property
    def bgpv4_routes(self):
        # type: () -> DeviceBgpv4RouteIter
        """bgpv4_routes getter

        Emulated BGPv4 routes

        Returns: list[obj(snappi.DeviceBgpv4Route)]
        """
        return self._get_property('bgpv4_routes', DeviceBgpv4RouteIter)

    @property
    def bgpv6_routes(self):
        # type: () -> DeviceBgpv6RouteIter
        """bgpv6_routes getter

        Emulated BGPv6 routes

        Returns: list[obj(snappi.DeviceBgpv6Route)]
        """
        return self._get_property('bgpv6_routes', DeviceBgpv6RouteIter)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)

    @property
    def active(self):
        # type: () -> boolean
        """active getter

        If enabled means that this part of the configuration including any active 'children' nodes will be advertised to peer. If disabled, this means that though config is present, it is not taking any part of the test but can be activated at run-time to advertise just this part of the configuration to the peer.

        Returns: boolean
        """
        return self._get_property('active')

    @active.setter
    def active(self, value):
        """active setter

        If enabled means that this part of the configuration including any active 'children' nodes will be advertised to peer. If disabled, this means that though config is present, it is not taking any part of the test but can be activated at run-time to advertise just this part of the configuration to the peer.

        value: boolean
        """
        self._set_property('active', value)


class DeviceBgpAdvanced(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, hold_time_interval=None, keep_alive_interval=None, update_interval=None, time_to_live=None, md5_key=None):
        super(DeviceBgpAdvanced, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('hold_time_interval', hold_time_interval)
        self._set_property('keep_alive_interval', keep_alive_interval)
        self._set_property('update_interval', update_interval)
        self._set_property('time_to_live', time_to_live)
        self._set_property('md5_key', md5_key)

    @property
    def hold_time_interval(self):
        # type: () -> int
        """hold_time_interval getter

        Number of seconds the sender proposes for the value of the Hold Timer

        Returns: int
        """
        return self._get_property('hold_time_interval')

    @hold_time_interval.setter
    def hold_time_interval(self, value):
        """hold_time_interval setter

        Number of seconds the sender proposes for the value of the Hold Timer

        value: int
        """
        self._set_property('hold_time_interval', value)

    @property
    def keep_alive_interval(self):
        # type: () -> int
        """keep_alive_interval getter

        Number of seconds between transmissions of Keep Alive messages by router

        Returns: int
        """
        return self._get_property('keep_alive_interval')

    @keep_alive_interval.setter
    def keep_alive_interval(self, value):
        """keep_alive_interval setter

        Number of seconds between transmissions of Keep Alive messages by router

        value: int
        """
        self._set_property('keep_alive_interval', value)

    @property
    def update_interval(self):
        # type: () -> int
        """update_interval getter

        The time interval at which UPDATE messages are sent to the DUT, expressed as the number of milliseconds between UPDATE messages.

        Returns: int
        """
        return self._get_property('update_interval')

    @update_interval.setter
    def update_interval(self, value):
        """update_interval setter

        The time interval at which UPDATE messages are sent to the DUT, expressed as the number of milliseconds between UPDATE messages.

        value: int
        """
        self._set_property('update_interval', value)

    @property
    def time_to_live(self):
        # type: () -> int
        """time_to_live getter

        The limited number of iterations that a unit of data can experience before the data is discarded. This is placed in the TTL field in the IP header of the transmitted packets.

        Returns: int
        """
        return self._get_property('time_to_live')

    @time_to_live.setter
    def time_to_live(self, value):
        """time_to_live setter

        The limited number of iterations that a unit of data can experience before the data is discarded. This is placed in the TTL field in the IP header of the transmitted packets.

        value: int
        """
        self._set_property('time_to_live', value)

    @property
    def md5_key(self):
        # type: () -> str
        """md5_key getter

        The value to be used as a secret MD5 key for authentication. If null or an empty string then authentication will not be enabled.

        Returns: str
        """
        return self._get_property('md5_key')

    @md5_key.setter
    def md5_key(self, value):
        """md5_key setter

        The value to be used as a secret MD5 key for authentication. If null or an empty string then authentication will not be enabled.

        value: str
        """
        self._set_property('md5_key', value)


class DeviceBgpCapability(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, vpls=None, route_refresh=None, route_constraint=None, link_state_non_vpn=None, link_state_vpn=None, evpn=None, extended_next_hop_encoding=None, ipv4_unicast=None, ipv4_multicast=None, ipv4_multicast_vpn=None, ipv4_mpls_vpn=None, ipv4_mdt=None, ipv4_multicast_mpls_vpn=None, ipv4_unicast_flow_spec=None, ipv4_sr_te_policy=None, ipv4_unicast_add_path=None, ipv6_unicast=None, ipv6_multicast=None, ipv6_multicast_vpn=None, ipv6_mpls_vpn=None, ipv6_mdt=None, ipv6_multicast_mpls_vpn=None, ipv6_unicast_flow_spec=None, ipv6_sr_te_policy=None, ipv6_unicast_add_path=None):
        super(DeviceBgpCapability, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('vpls', vpls)
        self._set_property('route_refresh', route_refresh)
        self._set_property('route_constraint', route_constraint)
        self._set_property('link_state_non_vpn', link_state_non_vpn)
        self._set_property('link_state_vpn', link_state_vpn)
        self._set_property('evpn', evpn)
        self._set_property('extended_next_hop_encoding', extended_next_hop_encoding)
        self._set_property('ipv4_unicast', ipv4_unicast)
        self._set_property('ipv4_multicast', ipv4_multicast)
        self._set_property('ipv4_multicast_vpn', ipv4_multicast_vpn)
        self._set_property('ipv4_mpls_vpn', ipv4_mpls_vpn)
        self._set_property('ipv4_mdt', ipv4_mdt)
        self._set_property('ipv4_multicast_mpls_vpn', ipv4_multicast_mpls_vpn)
        self._set_property('ipv4_unicast_flow_spec', ipv4_unicast_flow_spec)
        self._set_property('ipv4_sr_te_policy', ipv4_sr_te_policy)
        self._set_property('ipv4_unicast_add_path', ipv4_unicast_add_path)
        self._set_property('ipv6_unicast', ipv6_unicast)
        self._set_property('ipv6_multicast', ipv6_multicast)
        self._set_property('ipv6_multicast_vpn', ipv6_multicast_vpn)
        self._set_property('ipv6_mpls_vpn', ipv6_mpls_vpn)
        self._set_property('ipv6_mdt', ipv6_mdt)
        self._set_property('ipv6_multicast_mpls_vpn', ipv6_multicast_mpls_vpn)
        self._set_property('ipv6_unicast_flow_spec', ipv6_unicast_flow_spec)
        self._set_property('ipv6_sr_te_policy', ipv6_sr_te_policy)
        self._set_property('ipv6_unicast_add_path', ipv6_unicast_add_path)

    @property
    def vpls(self):
        # type: () -> boolean
        """vpls getter

        TBD

        Returns: boolean
        """
        return self._get_property('vpls')

    @vpls.setter
    def vpls(self, value):
        """vpls setter

        TBD

        value: boolean
        """
        self._set_property('vpls', value)

    @property
    def route_refresh(self):
        # type: () -> boolean
        """route_refresh getter

        TBD

        Returns: boolean
        """
        return self._get_property('route_refresh')

    @route_refresh.setter
    def route_refresh(self, value):
        """route_refresh setter

        TBD

        value: boolean
        """
        self._set_property('route_refresh', value)

    @property
    def route_constraint(self):
        # type: () -> boolean
        """route_constraint getter

        TBD

        Returns: boolean
        """
        return self._get_property('route_constraint')

    @route_constraint.setter
    def route_constraint(self, value):
        """route_constraint setter

        TBD

        value: boolean
        """
        self._set_property('route_constraint', value)

    @property
    def link_state_non_vpn(self):
        # type: () -> boolean
        """link_state_non_vpn getter

        TBD

        Returns: boolean
        """
        return self._get_property('link_state_non_vpn')

    @link_state_non_vpn.setter
    def link_state_non_vpn(self, value):
        """link_state_non_vpn setter

        TBD

        value: boolean
        """
        self._set_property('link_state_non_vpn', value)

    @property
    def link_state_vpn(self):
        # type: () -> boolean
        """link_state_vpn getter

        TBD

        Returns: boolean
        """
        return self._get_property('link_state_vpn')

    @link_state_vpn.setter
    def link_state_vpn(self, value):
        """link_state_vpn setter

        TBD

        value: boolean
        """
        self._set_property('link_state_vpn', value)

    @property
    def evpn(self):
        # type: () -> boolean
        """evpn getter

        TBD

        Returns: boolean
        """
        return self._get_property('evpn')

    @evpn.setter
    def evpn(self, value):
        """evpn setter

        TBD

        value: boolean
        """
        self._set_property('evpn', value)

    @property
    def extended_next_hop_encoding(self):
        # type: () -> boolean
        """extended_next_hop_encoding getter

        TBD

        Returns: boolean
        """
        return self._get_property('extended_next_hop_encoding')

    @extended_next_hop_encoding.setter
    def extended_next_hop_encoding(self, value):
        """extended_next_hop_encoding setter

        TBD

        value: boolean
        """
        self._set_property('extended_next_hop_encoding', value)

    @property
    def ipv4_unicast(self):
        # type: () -> boolean
        """ipv4_unicast getter

        TBD

        Returns: boolean
        """
        return self._get_property('ipv4_unicast')

    @ipv4_unicast.setter
    def ipv4_unicast(self, value):
        """ipv4_unicast setter

        TBD

        value: boolean
        """
        self._set_property('ipv4_unicast', value)

    @property
    def ipv4_multicast(self):
        # type: () -> boolean
        """ipv4_multicast getter

        TBD

        Returns: boolean
        """
        return self._get_property('ipv4_multicast')

    @ipv4_multicast.setter
    def ipv4_multicast(self, value):
        """ipv4_multicast setter

        TBD

        value: boolean
        """
        self._set_property('ipv4_multicast', value)

    @property
    def ipv4_multicast_vpn(self):
        # type: () -> boolean
        """ipv4_multicast_vpn getter

        TBD

        Returns: boolean
        """
        return self._get_property('ipv4_multicast_vpn')

    @ipv4_multicast_vpn.setter
    def ipv4_multicast_vpn(self, value):
        """ipv4_multicast_vpn setter

        TBD

        value: boolean
        """
        self._set_property('ipv4_multicast_vpn', value)

    @property
    def ipv4_mpls_vpn(self):
        # type: () -> boolean
        """ipv4_mpls_vpn getter

        TBD

        Returns: boolean
        """
        return self._get_property('ipv4_mpls_vpn')

    @ipv4_mpls_vpn.setter
    def ipv4_mpls_vpn(self, value):
        """ipv4_mpls_vpn setter

        TBD

        value: boolean
        """
        self._set_property('ipv4_mpls_vpn', value)

    @property
    def ipv4_mdt(self):
        # type: () -> boolean
        """ipv4_mdt getter

        TBD

        Returns: boolean
        """
        return self._get_property('ipv4_mdt')

    @ipv4_mdt.setter
    def ipv4_mdt(self, value):
        """ipv4_mdt setter

        TBD

        value: boolean
        """
        self._set_property('ipv4_mdt', value)

    @property
    def ipv4_multicast_mpls_vpn(self):
        # type: () -> boolean
        """ipv4_multicast_mpls_vpn getter

        TBD

        Returns: boolean
        """
        return self._get_property('ipv4_multicast_mpls_vpn')

    @ipv4_multicast_mpls_vpn.setter
    def ipv4_multicast_mpls_vpn(self, value):
        """ipv4_multicast_mpls_vpn setter

        TBD

        value: boolean
        """
        self._set_property('ipv4_multicast_mpls_vpn', value)

    @property
    def ipv4_unicast_flow_spec(self):
        # type: () -> boolean
        """ipv4_unicast_flow_spec getter

        TBD

        Returns: boolean
        """
        return self._get_property('ipv4_unicast_flow_spec')

    @ipv4_unicast_flow_spec.setter
    def ipv4_unicast_flow_spec(self, value):
        """ipv4_unicast_flow_spec setter

        TBD

        value: boolean
        """
        self._set_property('ipv4_unicast_flow_spec', value)

    @property
    def ipv4_sr_te_policy(self):
        # type: () -> boolean
        """ipv4_sr_te_policy getter

        TBD

        Returns: boolean
        """
        return self._get_property('ipv4_sr_te_policy')

    @ipv4_sr_te_policy.setter
    def ipv4_sr_te_policy(self, value):
        """ipv4_sr_te_policy setter

        TBD

        value: boolean
        """
        self._set_property('ipv4_sr_te_policy', value)

    @property
    def ipv4_unicast_add_path(self):
        # type: () -> boolean
        """ipv4_unicast_add_path getter

        TBD

        Returns: boolean
        """
        return self._get_property('ipv4_unicast_add_path')

    @ipv4_unicast_add_path.setter
    def ipv4_unicast_add_path(self, value):
        """ipv4_unicast_add_path setter

        TBD

        value: boolean
        """
        self._set_property('ipv4_unicast_add_path', value)

    @property
    def ipv6_unicast(self):
        # type: () -> boolean
        """ipv6_unicast getter

        TBD

        Returns: boolean
        """
        return self._get_property('ipv6_unicast')

    @ipv6_unicast.setter
    def ipv6_unicast(self, value):
        """ipv6_unicast setter

        TBD

        value: boolean
        """
        self._set_property('ipv6_unicast', value)

    @property
    def ipv6_multicast(self):
        # type: () -> boolean
        """ipv6_multicast getter

        TBD

        Returns: boolean
        """
        return self._get_property('ipv6_multicast')

    @ipv6_multicast.setter
    def ipv6_multicast(self, value):
        """ipv6_multicast setter

        TBD

        value: boolean
        """
        self._set_property('ipv6_multicast', value)

    @property
    def ipv6_multicast_vpn(self):
        # type: () -> boolean
        """ipv6_multicast_vpn getter

        TBD

        Returns: boolean
        """
        return self._get_property('ipv6_multicast_vpn')

    @ipv6_multicast_vpn.setter
    def ipv6_multicast_vpn(self, value):
        """ipv6_multicast_vpn setter

        TBD

        value: boolean
        """
        self._set_property('ipv6_multicast_vpn', value)

    @property
    def ipv6_mpls_vpn(self):
        # type: () -> boolean
        """ipv6_mpls_vpn getter

        TBD

        Returns: boolean
        """
        return self._get_property('ipv6_mpls_vpn')

    @ipv6_mpls_vpn.setter
    def ipv6_mpls_vpn(self, value):
        """ipv6_mpls_vpn setter

        TBD

        value: boolean
        """
        self._set_property('ipv6_mpls_vpn', value)

    @property
    def ipv6_mdt(self):
        # type: () -> boolean
        """ipv6_mdt getter

        TBD

        Returns: boolean
        """
        return self._get_property('ipv6_mdt')

    @ipv6_mdt.setter
    def ipv6_mdt(self, value):
        """ipv6_mdt setter

        TBD

        value: boolean
        """
        self._set_property('ipv6_mdt', value)

    @property
    def ipv6_multicast_mpls_vpn(self):
        # type: () -> boolean
        """ipv6_multicast_mpls_vpn getter

        TBD

        Returns: boolean
        """
        return self._get_property('ipv6_multicast_mpls_vpn')

    @ipv6_multicast_mpls_vpn.setter
    def ipv6_multicast_mpls_vpn(self, value):
        """ipv6_multicast_mpls_vpn setter

        TBD

        value: boolean
        """
        self._set_property('ipv6_multicast_mpls_vpn', value)

    @property
    def ipv6_unicast_flow_spec(self):
        # type: () -> boolean
        """ipv6_unicast_flow_spec getter

        TBD

        Returns: boolean
        """
        return self._get_property('ipv6_unicast_flow_spec')

    @ipv6_unicast_flow_spec.setter
    def ipv6_unicast_flow_spec(self, value):
        """ipv6_unicast_flow_spec setter

        TBD

        value: boolean
        """
        self._set_property('ipv6_unicast_flow_spec', value)

    @property
    def ipv6_sr_te_policy(self):
        # type: () -> boolean
        """ipv6_sr_te_policy getter

        TBD

        Returns: boolean
        """
        return self._get_property('ipv6_sr_te_policy')

    @ipv6_sr_te_policy.setter
    def ipv6_sr_te_policy(self, value):
        """ipv6_sr_te_policy setter

        TBD

        value: boolean
        """
        self._set_property('ipv6_sr_te_policy', value)

    @property
    def ipv6_unicast_add_path(self):
        # type: () -> boolean
        """ipv6_unicast_add_path getter

        TBD

        Returns: boolean
        """
        return self._get_property('ipv6_unicast_add_path')

    @ipv6_unicast_add_path.setter
    def ipv6_unicast_add_path(self, value):
        """ipv6_unicast_add_path setter

        TBD

        value: boolean
        """
        self._set_property('ipv6_unicast_add_path', value)


class DeviceBgpSrTePolicy(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'next_hop': 'DeviceBgpSrTePolicyNextHop',
        'add_path': 'DeviceBgpAddPath',
        'as_path': 'DeviceBgpAsPath',
        'tunnel_tlvs': 'DeviceBgpTunnelTlvIter',
        'communities': 'DeviceBgpCommunityIter',
    }

    IPV4 = 'ipv4'
    IPV6 = 'ipv6'

    def __init__(self, parent=None, choice=None, policy_type=None, distinguisher=None, color=None, ipv4_endpoint=None, ipv6_endpoint=None):
        super(DeviceBgpSrTePolicy, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('policy_type', policy_type)
        self._set_property('distinguisher', distinguisher)
        self._set_property('color', color)
        self._set_property('ipv4_endpoint', ipv4_endpoint)
        self._set_property('ipv6_endpoint', ipv6_endpoint)

    @property
    def policy_type(self):
        # type: () -> Union[ipv4, ipv6]
        """policy_type getter

        Address family indicator (AFI).

        Returns: Union[ipv4, ipv6]
        """
        return self._get_property('policy_type')

    @policy_type.setter
    def policy_type(self, value):
        """policy_type setter

        Address family indicator (AFI).

        value: Union[ipv4, ipv6]
        """
        self._set_property('policy_type', value)

    @property
    def distinguisher(self):
        # type: () -> int
        """distinguisher getter

        Identifies the policy in the context of (color and endpoint) tuple. It is used by the SR Policy originator to make unique multiple occurrences of the same SR Policy.

        Returns: int
        """
        return self._get_property('distinguisher')

    @distinguisher.setter
    def distinguisher(self, value):
        """distinguisher setter

        Identifies the policy in the context of (color and endpoint) tuple. It is used by the SR Policy originator to make unique multiple occurrences of the same SR Policy.

        value: int
        """
        self._set_property('distinguisher', value)

    @property
    def color(self):
        # type: () -> int
        """color getter

        Identifies the policy. It is used to match the color of the destination prefixes to steer traffic into the SR Policy. 

        Returns: int
        """
        return self._get_property('color')

    @color.setter
    def color(self, value):
        """color setter

        Identifies the policy. It is used to match the color of the destination prefixes to steer traffic into the SR Policy. 

        value: int
        """
        self._set_property('color', value)

    @property
    def ipv4_endpoint(self):
        # type: () -> str
        """ipv4_endpoint getter

        Specifies a single node or a set of nodes. It is selected on the basis of the policy_type (AFI).

        Returns: str
        """
        return self._get_property('ipv4_endpoint')

    @ipv4_endpoint.setter
    def ipv4_endpoint(self, value):
        """ipv4_endpoint setter

        Specifies a single node or a set of nodes. It is selected on the basis of the policy_type (AFI).

        value: str
        """
        self._set_property('ipv4_endpoint', value)

    @property
    def ipv6_endpoint(self):
        # type: () -> str
        """ipv6_endpoint getter

        Specifies a single node or a set of nodes. It is selected on the basis of the policy_type (AFI).

        Returns: str
        """
        return self._get_property('ipv6_endpoint')

    @ipv6_endpoint.setter
    def ipv6_endpoint(self, value):
        """ipv6_endpoint setter

        Specifies a single node or a set of nodes. It is selected on the basis of the policy_type (AFI).

        value: str
        """
        self._set_property('ipv6_endpoint', value)

    @property
    def next_hop(self):
        # type: () -> DeviceBgpSrTePolicyNextHop
        """next_hop getter

        Optional container for BGP SR TE Policy next hop settings.

        Returns: obj(snappi.DeviceBgpSrTePolicyNextHop)
        """
        return self._get_property('next_hop', DeviceBgpSrTePolicyNextHop)

    @property
    def add_path(self):
        # type: () -> DeviceBgpAddPath
        """add_path getter

        The BGP Additional Paths feature is a BGP extension that allows the advertisement of multiple paths for the same prefix without the new paths implicitly replacing any previous paths.

        Returns: obj(snappi.DeviceBgpAddPath)
        """
        return self._get_property('add_path', DeviceBgpAddPath)

    @property
    def as_path(self):
        # type: () -> DeviceBgpAsPath
        """as_path getter

        Autonomous Systems (AS) numbers that a route passes through to reach the destination

        Returns: obj(snappi.DeviceBgpAsPath)
        """
        return self._get_property('as_path', DeviceBgpAsPath)

    @property
    def tunnel_tlvs(self):
        # type: () -> DeviceBgpTunnelTlvIter
        """tunnel_tlvs getter

        Optional tunnel TLV settings

        Returns: list[obj(snappi.DeviceBgpTunnelTlv)]
        """
        return self._get_property('tunnel_tlvs', DeviceBgpTunnelTlvIter)

    @property
    def communities(self):
        # type: () -> DeviceBgpCommunityIter
        """communities getter

        Optional community settings

        Returns: list[obj(snappi.DeviceBgpCommunity)]
        """
        return self._get_property('communities', DeviceBgpCommunityIter)


class DeviceBgpSrTePolicyNextHop(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    LOCAL_IP = 'local_ip'
    MANUAL = 'manual'

    IPV4 = 'ipv4'
    IPV6 = 'ipv6'

    def __init__(self, parent=None, choice=None, next_hop_mode=None, next_hop_address_type=None, ipv4_address=None, ipv6_address=None):
        super(DeviceBgpSrTePolicyNextHop, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('next_hop_mode', next_hop_mode)
        self._set_property('next_hop_address_type', next_hop_address_type)
        self._set_property('ipv4_address', ipv4_address)
        self._set_property('ipv6_address', ipv6_address)

    @property
    def next_hop_mode(self):
        # type: () -> Union[local_ip, manual]
        """next_hop_mode getter

        TBD

        Returns: Union[local_ip, manual]
        """
        return self._get_property('next_hop_mode')

    @next_hop_mode.setter
    def next_hop_mode(self, value):
        """next_hop_mode setter

        TBD

        value: Union[local_ip, manual]
        """
        self._set_property('next_hop_mode', value)

    @property
    def next_hop_address_type(self):
        # type: () -> Union[ipv4, ipv6]
        """next_hop_address_type getter

        TBD

        Returns: Union[ipv4, ipv6]
        """
        return self._get_property('next_hop_address_type')

    @next_hop_address_type.setter
    def next_hop_address_type(self, value):
        """next_hop_address_type setter

        TBD

        value: Union[ipv4, ipv6]
        """
        self._set_property('next_hop_address_type', value)

    @property
    def ipv4_address(self):
        # type: () -> str
        """ipv4_address getter

        The IPv4 address of the next hop if the next_hop_mode is manual and the next_hop_address_type is IPv4.

        Returns: str
        """
        return self._get_property('ipv4_address')

    @ipv4_address.setter
    def ipv4_address(self, value):
        """ipv4_address setter

        The IPv4 address of the next hop if the next_hop_mode is manual and the next_hop_address_type is IPv4.

        value: str
        """
        self._set_property('ipv4_address', value)

    @property
    def ipv6_address(self):
        # type: () -> str
        """ipv6_address getter

        The IPv6 address of the next hop if the next_hop_mode is manual and the next_hop_address_type is IPv6.

        Returns: str
        """
        return self._get_property('ipv6_address')

    @ipv6_address.setter
    def ipv6_address(self, value):
        """ipv6_address setter

        The IPv6 address of the next hop if the next_hop_mode is manual and the next_hop_address_type is IPv6.

        value: str
        """
        self._set_property('ipv6_address', value)


class DeviceBgpAddPath(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, path_id=None):
        super(DeviceBgpAddPath, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('path_id', path_id)

    @property
    def path_id(self):
        # type: () -> int
        """path_id getter

        The id of the additional path.

        Returns: int
        """
        return self._get_property('path_id')

    @path_id.setter
    def path_id(self, value):
        """path_id setter

        The id of the additional path.

        value: int
        """
        self._set_property('path_id', value)


class DeviceBgpAsPath(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'as_path_segments': 'DeviceBgpAsPathSegmentIter',
    }

    DO_NOT_INCLUDE_LOCAL_AS = 'do_not_include_local_as'
    INCLUDE_AS_SEQ = 'include_as_seq'
    INCLUDE_AS_SET = 'include_as_set'
    INCLUDE_AS_CONFED_SEQ = 'include_as_confed_seq'
    INCLUDE_AS_CONFED_SET = 'include_as_confed_set'
    PREPEND_TO_FIRST_SEGMENT = 'prepend_to_first_segment'

    def __init__(self, parent=None, choice=None, override_peer_as_set_mode=None, as_set_mode=None):
        super(DeviceBgpAsPath, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('override_peer_as_set_mode', override_peer_as_set_mode)
        self._set_property('as_set_mode', as_set_mode)

    @property
    def override_peer_as_set_mode(self):
        # type: () -> boolean
        """override_peer_as_set_mode getter

        TBD

        Returns: boolean
        """
        return self._get_property('override_peer_as_set_mode')

    @override_peer_as_set_mode.setter
    def override_peer_as_set_mode(self, value):
        """override_peer_as_set_mode setter

        TBD

        value: boolean
        """
        self._set_property('override_peer_as_set_mode', value)

    @property
    def as_set_mode(self):
        # type: () -> Union[do_not_include_local_as, include_as_seq, include_as_set, include_as_confed_seq, include_as_confed_set, prepend_to_first_segment]
        """as_set_mode getter

        TBD

        Returns: Union[do_not_include_local_as, include_as_seq, include_as_set, include_as_confed_seq, include_as_confed_set, prepend_to_first_segment]
        """
        return self._get_property('as_set_mode')

    @as_set_mode.setter
    def as_set_mode(self, value):
        """as_set_mode setter

        TBD

        value: Union[do_not_include_local_as, include_as_seq, include_as_set, include_as_confed_seq, include_as_confed_set, prepend_to_first_segment]
        """
        self._set_property('as_set_mode', value)

    @property
    def as_path_segments(self):
        # type: () -> DeviceBgpAsPathSegmentIter
        """as_path_segments getter

        The AS path segments (non random) per route range

        Returns: list[obj(snappi.DeviceBgpAsPathSegment)]
        """
        return self._get_property('as_path_segments', DeviceBgpAsPathSegmentIter)


class DeviceBgpAsPathSegment(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    AS_SEQ = 'as_seq'
    AS_SET = 'as_set'
    AS_CONFED_SEQ = 'as_confed_seq'
    AS_CONFED_SET = 'as_confed_set'

    def __init__(self, parent=None, choice=None, segment_type=None, as_numbers=None):
        super(DeviceBgpAsPathSegment, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('segment_type', segment_type)
        self._set_property('as_numbers', as_numbers)

    @property
    def segment_type(self):
        # type: () -> Union[as_seq, as_set, as_confed_seq, as_confed_set]
        """segment_type getter

        AS sequence is the most common type of AS_PATH, it contains the list of ASNs starting with the most recent ASN being added read from left to right.. The other three AS_PATH types are used for Confederations - AS_SET is the type of AS_PATH attribute that summarizes routes using using the aggregate-address command, allowing AS_PATHs to be summarized in the update as well. - AS_CONFED_SEQ gives the list of ASNs in the path starting with the most recent ASN to be added reading left to right - AS_CONFED_SET will allow summarization of multiple AS PATHs to be sent in BGP Updates.

        Returns: Union[as_seq, as_set, as_confed_seq, as_confed_set]
        """
        return self._get_property('segment_type')

    @segment_type.setter
    def segment_type(self, value):
        """segment_type setter

        AS sequence is the most common type of AS_PATH, it contains the list of ASNs starting with the most recent ASN being added read from left to right.. The other three AS_PATH types are used for Confederations - AS_SET is the type of AS_PATH attribute that summarizes routes using using the aggregate-address command, allowing AS_PATHs to be summarized in the update as well. - AS_CONFED_SEQ gives the list of ASNs in the path starting with the most recent ASN to be added reading left to right - AS_CONFED_SET will allow summarization of multiple AS PATHs to be sent in BGP Updates.

        value: Union[as_seq, as_set, as_confed_seq, as_confed_set]
        """
        self._set_property('segment_type', value)

    @property
    def as_numbers(self):
        # type: () -> list[int]
        """as_numbers getter

        The AS numbers in this AS path segment.

        Returns: list[int]
        """
        return self._get_property('as_numbers')

    @as_numbers.setter
    def as_numbers(self, value):
        """as_numbers setter

        The AS numbers in this AS path segment.

        value: list[int]
        """
        self._set_property('as_numbers', value)


class DeviceBgpAsPathSegmentIter(SnappiIter):
    __slots__ = ()

    def __init__(self):
        super(DeviceBgpAsPathSegmentIter, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[DeviceBgpAsPathSegment]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> DeviceBgpAsPathSegmentIter
        return self._iter()

    def __next__(self):
        # type: () -> DeviceBgpAsPathSegment
        return self._next()

    def next(self):
        # type: () -> DeviceBgpAsPathSegment
        return self._next()

    def bgpaspathsegment(self, segment_type='as_seq', as_numbers=None):
        # type: () -> DeviceBgpAsPathSegmentIter
        """Factory method that creates an instance of DeviceBgpAsPathSegment class

        Container for a single BGP AS path segment
        """
        item = DeviceBgpAsPathSegment(segment_type=segment_type, as_numbers=as_numbers)
        self._add(item)
        return self


class DeviceBgpTunnelTlv(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'segment_lists': 'DeviceBgpSegmentListIter',
        'remote_endpoint_sub_tlv': 'DeviceBgpRemoteEndpointSubTlv',
        'preference_sub_tlv': 'DeviceBgpPreferenceSubTlv',
        'binding_sub_tlv': 'DeviceBgpBindingSubTlv',
        'explicit_null_label_policy_sub_tlv': 'DeviceBgpExplicitNullLabelPolicySubTlv',
    }

    def __init__(self, parent=None, choice=None, active=None):
        super(DeviceBgpTunnelTlv, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('active', active)

    @property
    def segment_lists(self):
        # type: () -> DeviceBgpSegmentListIter
        """segment_lists getter

        TBD

        Returns: list[obj(snappi.DeviceBgpSegmentList)]
        """
        return self._get_property('segment_lists', DeviceBgpSegmentListIter)

    @property
    def remote_endpoint_sub_tlv(self):
        # type: () -> DeviceBgpRemoteEndpointSubTlv
        """remote_endpoint_sub_tlv getter

        Container for BGP remote endpoint sub TLV settings.

        Returns: obj(snappi.DeviceBgpRemoteEndpointSubTlv)
        """
        return self._get_property('remote_endpoint_sub_tlv', DeviceBgpRemoteEndpointSubTlv)

    @property
    def preference_sub_tlv(self):
        # type: () -> DeviceBgpPreferenceSubTlv
        """preference_sub_tlv getter

        Container for BGP preference sub TLV settings.

        Returns: obj(snappi.DeviceBgpPreferenceSubTlv)
        """
        return self._get_property('preference_sub_tlv', DeviceBgpPreferenceSubTlv)

    @property
    def binding_sub_tlv(self):
        # type: () -> DeviceBgpBindingSubTlv
        """binding_sub_tlv getter

        Container for BGP binding sub TLV settings.

        Returns: obj(snappi.DeviceBgpBindingSubTlv)
        """
        return self._get_property('binding_sub_tlv', DeviceBgpBindingSubTlv)

    @property
    def explicit_null_label_policy_sub_tlv(self):
        # type: () -> DeviceBgpExplicitNullLabelPolicySubTlv
        """explicit_null_label_policy_sub_tlv getter

        Container for BGP explicit null label policy sub TLV settings.

        Returns: obj(snappi.DeviceBgpExplicitNullLabelPolicySubTlv)
        """
        return self._get_property('explicit_null_label_policy_sub_tlv', DeviceBgpExplicitNullLabelPolicySubTlv)

    @property
    def active(self):
        # type: () -> boolean
        """active getter

        If enabled means that this part of the configuration including any active 'children' nodes will be advertised to peer. If disabled, this means that though config is present, it is not taking any part of the test but can be activated at run-time to advertise just this part of the configuration to the peer.

        Returns: boolean
        """
        return self._get_property('active')

    @active.setter
    def active(self, value):
        """active setter

        If enabled means that this part of the configuration including any active 'children' nodes will be advertised to peer. If disabled, this means that though config is present, it is not taking any part of the test but can be activated at run-time to advertise just this part of the configuration to the peer.

        value: boolean
        """
        self._set_property('active', value)


class DeviceBgpSegmentList(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'segments': 'DeviceBgpSegmentIter',
    }

    def __init__(self, parent=None, choice=None, segment_weight=None, active=None):
        super(DeviceBgpSegmentList, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('segment_weight', segment_weight)
        self._set_property('active', active)

    @property
    def segment_weight(self):
        # type: () -> int
        """segment_weight getter

        The weight associated with a given path.

        Returns: int
        """
        return self._get_property('segment_weight')

    @segment_weight.setter
    def segment_weight(self, value):
        """segment_weight setter

        The weight associated with a given path.

        value: int
        """
        self._set_property('segment_weight', value)

    @property
    def segments(self):
        # type: () -> DeviceBgpSegmentIter
        """segments getter

        TBD

        Returns: list[obj(snappi.DeviceBgpSegment)]
        """
        return self._get_property('segments', DeviceBgpSegmentIter)

    @property
    def active(self):
        # type: () -> boolean
        """active getter

        If enabled means that this part of the configuration including any active 'children' nodes will be advertised to peer. If disabled, this means that though config is present, it is not taking any part of the test but can be activated at run-time to advertise just this part of the configuration to the peer.

        Returns: boolean
        """
        return self._get_property('active')

    @active.setter
    def active(self, value):
        """active setter

        If enabled means that this part of the configuration including any active 'children' nodes will be advertised to peer. If disabled, this means that though config is present, it is not taking any part of the test but can be activated at run-time to advertise just this part of the configuration to the peer.

        value: boolean
        """
        self._set_property('active', value)


class DeviceBgpSegment(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    MPLS_SID = 'mpls_sid'
    IPV6_SID = 'ipv6_sid'

    def __init__(self, parent=None, choice=None, segment_type=None, mpls_label=None, mpls_tc=None, mpls_ttl=None, v_flag=None, ipv6_sid=None, remaining_flag_bits=None, active=None):
        super(DeviceBgpSegment, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('segment_type', segment_type)
        self._set_property('mpls_label', mpls_label)
        self._set_property('mpls_tc', mpls_tc)
        self._set_property('mpls_ttl', mpls_ttl)
        self._set_property('v_flag', v_flag)
        self._set_property('ipv6_sid', ipv6_sid)
        self._set_property('remaining_flag_bits', remaining_flag_bits)
        self._set_property('active', active)

    @property
    def segment_type(self):
        # type: () -> Union[mpls_sid, ipv6_sid]
        """segment_type getter

        TBD

        Returns: Union[mpls_sid, ipv6_sid]
        """
        return self._get_property('segment_type')

    @segment_type.setter
    def segment_type(self, value):
        """segment_type setter

        TBD

        value: Union[mpls_sid, ipv6_sid]
        """
        self._set_property('segment_type', value)

    @property
    def mpls_label(self):
        # type: () -> int
        """mpls_label getter

        MPLS label

        Returns: int
        """
        return self._get_property('mpls_label')

    @mpls_label.setter
    def mpls_label(self, value):
        """mpls_label setter

        MPLS label

        value: int
        """
        self._set_property('mpls_label', value)

    @property
    def mpls_tc(self):
        # type: () -> int
        """mpls_tc getter

        TBD

        Returns: int
        """
        return self._get_property('mpls_tc')

    @mpls_tc.setter
    def mpls_tc(self, value):
        """mpls_tc setter

        TBD

        value: int
        """
        self._set_property('mpls_tc', value)

    @property
    def mpls_ttl(self):
        # type: () -> int
        """mpls_ttl getter

        TBD

        Returns: int
        """
        return self._get_property('mpls_ttl')

    @mpls_ttl.setter
    def mpls_ttl(self, value):
        """mpls_ttl setter

        TBD

        value: int
        """
        self._set_property('mpls_ttl', value)

    @property
    def v_flag(self):
        # type: () -> boolean
        """v_flag getter

        TBD

        Returns: boolean
        """
        return self._get_property('v_flag')

    @v_flag.setter
    def v_flag(self, value):
        """v_flag setter

        TBD

        value: boolean
        """
        self._set_property('v_flag', value)

    @property
    def ipv6_sid(self):
        # type: () -> str
        """ipv6_sid getter

        TBD

        Returns: str
        """
        return self._get_property('ipv6_sid')

    @ipv6_sid.setter
    def ipv6_sid(self, value):
        """ipv6_sid setter

        TBD

        value: str
        """
        self._set_property('ipv6_sid', value)

    @property
    def remaining_flag_bits(self):
        # type: () -> int
        """remaining_flag_bits getter

        TBD

        Returns: int
        """
        return self._get_property('remaining_flag_bits')

    @remaining_flag_bits.setter
    def remaining_flag_bits(self, value):
        """remaining_flag_bits setter

        TBD

        value: int
        """
        self._set_property('remaining_flag_bits', value)

    @property
    def active(self):
        # type: () -> boolean
        """active getter

        If enabled means that this part of the configuration including any active 'children' nodes will be advertised to peer. If disabled, this means that though config is present, it is not taking any part of the test but can be activated at run-time to advertise just this part of the configuration to the peer.

        Returns: boolean
        """
        return self._get_property('active')

    @active.setter
    def active(self, value):
        """active setter

        If enabled means that this part of the configuration including any active 'children' nodes will be advertised to peer. If disabled, this means that though config is present, it is not taking any part of the test but can be activated at run-time to advertise just this part of the configuration to the peer.

        value: boolean
        """
        self._set_property('active', value)


class DeviceBgpSegmentIter(SnappiIter):
    __slots__ = ()

    def __init__(self):
        super(DeviceBgpSegmentIter, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[DeviceBgpSegment]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> DeviceBgpSegmentIter
        return self._iter()

    def __next__(self):
        # type: () -> DeviceBgpSegment
        return self._next()

    def next(self):
        # type: () -> DeviceBgpSegment
        return self._next()

    def bgpsegment(self, segment_type='mpls_sid', mpls_label=0, mpls_tc=0, mpls_ttl=0, v_flag=False, ipv6_sid='::0', remaining_flag_bits=0, active=True):
        # type: () -> DeviceBgpSegmentIter
        """Factory method that creates an instance of DeviceBgpSegment class

        Optional container for BGP SR TE Policy segment settings.
        """
        item = DeviceBgpSegment(segment_type=segment_type, mpls_label=mpls_label, mpls_tc=mpls_tc, mpls_ttl=mpls_ttl, v_flag=v_flag, ipv6_sid=ipv6_sid, remaining_flag_bits=remaining_flag_bits, active=active)
        self._add(item)
        return self


class DeviceBgpSegmentListIter(SnappiIter):
    __slots__ = ()

    def __init__(self):
        super(DeviceBgpSegmentListIter, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[DeviceBgpSegmentList]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> DeviceBgpSegmentListIter
        return self._iter()

    def __next__(self):
        # type: () -> DeviceBgpSegmentList
        return self._next()

    def next(self):
        # type: () -> DeviceBgpSegmentList
        return self._next()

    def bgpsegmentlist(self, segment_weight=0, active=True):
        # type: () -> DeviceBgpSegmentListIter
        """Factory method that creates an instance of DeviceBgpSegmentList class

        Optional container for BGP SR TE Policy segment list settings.
        """
        item = DeviceBgpSegmentList(segment_weight=segment_weight, active=active)
        self._add(item)
        return self


class DeviceBgpRemoteEndpointSubTlv(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    IPV4 = 'ipv4'
    IPV6 = 'ipv6'

    def __init__(self, parent=None, choice=None, as_number=None, address_family=None, ipv4_address=None, ipv6_address=None):
        super(DeviceBgpRemoteEndpointSubTlv, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('as_number', as_number)
        self._set_property('address_family', address_family)
        self._set_property('ipv4_address', ipv4_address)
        self._set_property('ipv6_address', ipv6_address)

    @property
    def as_number(self):
        # type: () -> int
        """as_number getter

        Autonomous system (AS) number

        Returns: int
        """
        return self._get_property('as_number')

    @as_number.setter
    def as_number(self, value):
        """as_number setter

        Autonomous system (AS) number

        value: int
        """
        self._set_property('as_number', value)

    @property
    def address_family(self):
        # type: () -> Union[ipv4, ipv6]
        """address_family getter

        Determines the address type

        Returns: Union[ipv4, ipv6]
        """
        return self._get_property('address_family')

    @address_family.setter
    def address_family(self, value):
        """address_family setter

        Determines the address type

        value: Union[ipv4, ipv6]
        """
        self._set_property('address_family', value)

    @property
    def ipv4_address(self):
        # type: () -> str
        """ipv4_address getter

        The IPv4 address

        Returns: str
        """
        return self._get_property('ipv4_address')

    @ipv4_address.setter
    def ipv4_address(self, value):
        """ipv4_address setter

        The IPv4 address

        value: str
        """
        self._set_property('ipv4_address', value)

    @property
    def ipv6_address(self):
        # type: () -> str
        """ipv6_address getter

        The IPv6 address

        Returns: str
        """
        return self._get_property('ipv6_address')

    @ipv6_address.setter
    def ipv6_address(self, value):
        """ipv6_address setter

        The IPv6 address

        value: str
        """
        self._set_property('ipv6_address', value)


class DeviceBgpPreferenceSubTlv(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, preference=None):
        super(DeviceBgpPreferenceSubTlv, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('preference', preference)

    @property
    def preference(self):
        # type: () -> int
        """preference getter

        TBD

        Returns: int
        """
        return self._get_property('preference')

    @preference.setter
    def preference(self, value):
        """preference setter

        TBD

        value: int
        """
        self._set_property('preference', value)


class DeviceBgpBindingSubTlv(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    NO_BINDING = 'no_binding'
    FOUR_OCTET_SID = 'four_octet_sid'
    IPV6_SID = 'ipv6_sid'

    def __init__(self, parent=None, choice=None, binding_sid_type=None, four_octet_sid=None, bsid_as_mpls_label=None, ipv6_sid=None, s_flag=None, i_flag=None, remaining_flag_bits=None):
        super(DeviceBgpBindingSubTlv, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('binding_sid_type', binding_sid_type)
        self._set_property('four_octet_sid', four_octet_sid)
        self._set_property('bsid_as_mpls_label', bsid_as_mpls_label)
        self._set_property('ipv6_sid', ipv6_sid)
        self._set_property('s_flag', s_flag)
        self._set_property('i_flag', i_flag)
        self._set_property('remaining_flag_bits', remaining_flag_bits)

    @property
    def binding_sid_type(self):
        # type: () -> Union[no_binding, four_octet_sid, ipv6_sid]
        """binding_sid_type getter

        TBD

        Returns: Union[no_binding, four_octet_sid, ipv6_sid]
        """
        return self._get_property('binding_sid_type')

    @binding_sid_type.setter
    def binding_sid_type(self, value):
        """binding_sid_type setter

        TBD

        value: Union[no_binding, four_octet_sid, ipv6_sid]
        """
        self._set_property('binding_sid_type', value)

    @property
    def four_octet_sid(self):
        # type: () -> int
        """four_octet_sid getter

        TBD

        Returns: int
        """
        return self._get_property('four_octet_sid')

    @four_octet_sid.setter
    def four_octet_sid(self, value):
        """four_octet_sid setter

        TBD

        value: int
        """
        self._set_property('four_octet_sid', value)

    @property
    def bsid_as_mpls_label(self):
        # type: () -> boolean
        """bsid_as_mpls_label getter

        Only valid if binding_sid_type is four_octet_sid

        Returns: boolean
        """
        return self._get_property('bsid_as_mpls_label')

    @bsid_as_mpls_label.setter
    def bsid_as_mpls_label(self, value):
        """bsid_as_mpls_label setter

        Only valid if binding_sid_type is four_octet_sid

        value: boolean
        """
        self._set_property('bsid_as_mpls_label', value)

    @property
    def ipv6_sid(self):
        # type: () -> str
        """ipv6_sid getter

        Only valid if binding_sid_type is ipv6_sid

        Returns: str
        """
        return self._get_property('ipv6_sid')

    @ipv6_sid.setter
    def ipv6_sid(self, value):
        """ipv6_sid setter

        Only valid if binding_sid_type is ipv6_sid

        value: str
        """
        self._set_property('ipv6_sid', value)

    @property
    def s_flag(self):
        # type: () -> boolean
        """s_flag getter

        TBD

        Returns: boolean
        """
        return self._get_property('s_flag')

    @s_flag.setter
    def s_flag(self, value):
        """s_flag setter

        TBD

        value: boolean
        """
        self._set_property('s_flag', value)

    @property
    def i_flag(self):
        # type: () -> boolean
        """i_flag getter

        TBD

        Returns: boolean
        """
        return self._get_property('i_flag')

    @i_flag.setter
    def i_flag(self, value):
        """i_flag setter

        TBD

        value: boolean
        """
        self._set_property('i_flag', value)

    @property
    def remaining_flag_bits(self):
        # type: () -> int
        """remaining_flag_bits getter

        TBD

        Returns: int
        """
        return self._get_property('remaining_flag_bits')

    @remaining_flag_bits.setter
    def remaining_flag_bits(self, value):
        """remaining_flag_bits setter

        TBD

        value: int
        """
        self._set_property('remaining_flag_bits', value)


class DeviceBgpExplicitNullLabelPolicySubTlv(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    RESERVED_ENLP = 'reserved_enlp'
    PUSH_IPV4_ENLP = 'push_ipv4_enlp'
    PUSH_IPV6_ENLP = 'push_ipv6_enlp'
    PUSH_IPV4_IPV6_ENLP = 'push_ipv4_ipv6_enlp'
    DO_NOT_PUSH_ENLP = 'do_not_push_enlp'

    def __init__(self, parent=None, choice=None, explicit_null_label_policy=None):
        super(DeviceBgpExplicitNullLabelPolicySubTlv, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('explicit_null_label_policy', explicit_null_label_policy)

    @property
    def explicit_null_label_policy(self):
        # type: () -> Union[reserved_enlp, push_ipv4_enlp, push_ipv6_enlp, push_ipv4_ipv6_enlp, do_not_push_enlp]
        """explicit_null_label_policy getter

        The value of the explicit null label policy 

        Returns: Union[reserved_enlp, push_ipv4_enlp, push_ipv6_enlp, push_ipv4_ipv6_enlp, do_not_push_enlp]
        """
        return self._get_property('explicit_null_label_policy')

    @explicit_null_label_policy.setter
    def explicit_null_label_policy(self, value):
        """explicit_null_label_policy setter

        The value of the explicit null label policy 

        value: Union[reserved_enlp, push_ipv4_enlp, push_ipv6_enlp, push_ipv4_ipv6_enlp, do_not_push_enlp]
        """
        self._set_property('explicit_null_label_policy', value)


class DeviceBgpTunnelTlvIter(SnappiIter):
    __slots__ = ()

    def __init__(self):
        super(DeviceBgpTunnelTlvIter, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[DeviceBgpTunnelTlv]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> DeviceBgpTunnelTlvIter
        return self._iter()

    def __next__(self):
        # type: () -> DeviceBgpTunnelTlv
        return self._next()

    def next(self):
        # type: () -> DeviceBgpTunnelTlv
        return self._next()

    def bgptunneltlv(self, active=True):
        # type: () -> DeviceBgpTunnelTlvIter
        """Factory method that creates an instance of DeviceBgpTunnelTlv class

        Container for BGP tunnel TLV settings.
        """
        item = DeviceBgpTunnelTlv(active=active)
        self._add(item)
        return self


class DeviceBgpCommunity(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    MANUAL_AS_NUMBER = 'manual_as_number'
    NO_EXPORT = 'no_export'
    NO_ADVERTISED = 'no_advertised'
    NO_EXPORT_SUBCONFED = 'no_export_subconfed'
    LLGR_STALE = 'llgr_stale'
    NO_LLGR = 'no_llgr'

    def __init__(self, parent=None, choice=None, community_type=None, as_number=None, as_custom=None):
        super(DeviceBgpCommunity, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('community_type', community_type)
        self._set_property('as_number', as_number)
        self._set_property('as_custom', as_custom)

    @property
    def community_type(self):
        # type: () -> Union[manual_as_number, no_export, no_advertised, no_export_subconfed, llgr_stale, no_llgr]
        """community_type getter

        The type of community AS number.

        Returns: Union[manual_as_number, no_export, no_advertised, no_export_subconfed, llgr_stale, no_llgr]
        """
        return self._get_property('community_type')

    @community_type.setter
    def community_type(self, value):
        """community_type setter

        The type of community AS number.

        value: Union[manual_as_number, no_export, no_advertised, no_export_subconfed, llgr_stale, no_llgr]
        """
        self._set_property('community_type', value)

    @property
    def as_number(self):
        # type: () -> int
        """as_number getter

        First two octets of 32 bit community AS number

        Returns: int
        """
        return self._get_property('as_number')

    @as_number.setter
    def as_number(self, value):
        """as_number setter

        First two octets of 32 bit community AS number

        value: int
        """
        self._set_property('as_number', value)

    @property
    def as_custom(self):
        # type: () -> int
        """as_custom getter

        Last two octets of the community AS number 

        Returns: int
        """
        return self._get_property('as_custom')

    @as_custom.setter
    def as_custom(self, value):
        """as_custom setter

        Last two octets of the community AS number 

        value: int
        """
        self._set_property('as_custom', value)


class DeviceBgpCommunityIter(SnappiIter):
    __slots__ = ()

    def __init__(self):
        super(DeviceBgpCommunityIter, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[DeviceBgpCommunity]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> DeviceBgpCommunityIter
        return self._iter()

    def __next__(self):
        # type: () -> DeviceBgpCommunity
        return self._next()

    def next(self):
        # type: () -> DeviceBgpCommunity
        return self._next()

    def bgpcommunity(self, community_type=None, as_number=0, as_custom=0):
        # type: () -> DeviceBgpCommunityIter
        """Factory method that creates an instance of DeviceBgpCommunity class

        BGP communities provide additional capability for tagging routes and for modifying BGP routing policy on upstream and downstream routers BGP community is a 32-bit number which broken into 16-bit AS number and a 16-bit custom value
        """
        item = DeviceBgpCommunity(community_type=community_type, as_number=as_number, as_custom=as_custom)
        self._add(item)
        return self


class DeviceBgpSrTePolicyIter(SnappiIter):
    __slots__ = ()

    def __init__(self):
        super(DeviceBgpSrTePolicyIter, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[DeviceBgpSrTePolicy]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> DeviceBgpSrTePolicyIter
        return self._iter()

    def __next__(self):
        # type: () -> DeviceBgpSrTePolicy
        return self._next()

    def next(self):
        # type: () -> DeviceBgpSrTePolicy
        return self._next()

    def bgpsrtepolicy(self, policy_type='ipv4', distinguisher=1, color=100, ipv4_endpoint='0.0.0.0', ipv6_endpoint='::0'):
        # type: () -> DeviceBgpSrTePolicyIter
        """Factory method that creates an instance of DeviceBgpSrTePolicy class

        Container for BGP basic segment routing traffic engineering policy . settings.. 
        """
        item = DeviceBgpSrTePolicy(policy_type=policy_type, distinguisher=distinguisher, color=color, ipv4_endpoint=ipv4_endpoint, ipv6_endpoint=ipv6_endpoint)
        self._add(item)
        return self


class DeviceBgpv4Route(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'addresses': 'DeviceBgpv4RouteAddressIter',
        'advanced': 'DeviceBgpRouteAdvanced',
        'communities': 'DeviceBgpCommunityIter',
        'as_path': 'DeviceBgpAsPath',
        'add_path': 'DeviceBgpAddPath',
    }

    def __init__(self, parent=None, choice=None, next_hop_address=None, name=None):
        super(DeviceBgpv4Route, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('next_hop_address', next_hop_address)
        self._set_property('name', name)

    @property
    def addresses(self):
        # type: () -> DeviceBgpv4RouteAddressIter
        """addresses getter

        A list of symmetrical or asymmetrical route addresses

        Returns: list[obj(snappi.DeviceBgpv4RouteAddress)]
        """
        return self._get_property('addresses', DeviceBgpv4RouteAddressIter)

    @property
    def next_hop_address(self):
        # type: () -> str
        """next_hop_address getter

        IP Address of next router to forward a packet to its final destination

        Returns: str
        """
        return self._get_property('next_hop_address')

    @next_hop_address.setter
    def next_hop_address(self, value):
        """next_hop_address setter

        IP Address of next router to forward a packet to its final destination

        value: str
        """
        self._set_property('next_hop_address', value)

    @property
    def advanced(self):
        # type: () -> DeviceBgpRouteAdvanced
        """advanced getter

        Container for advanced BGP route range settings

        Returns: obj(snappi.DeviceBgpRouteAdvanced)
        """
        return self._get_property('advanced', DeviceBgpRouteAdvanced)

    @property
    def communities(self):
        # type: () -> DeviceBgpCommunityIter
        """communities getter

        Optional community settings.

        Returns: list[obj(snappi.DeviceBgpCommunity)]
        """
        return self._get_property('communities', DeviceBgpCommunityIter)

    @property
    def as_path(self):
        # type: () -> DeviceBgpAsPath
        """as_path getter

        Autonomous Systems (AS) numbers that a route passes through to reach the destination

        Returns: obj(snappi.DeviceBgpAsPath)
        """
        return self._get_property('as_path', DeviceBgpAsPath)

    @property
    def add_path(self):
        # type: () -> DeviceBgpAddPath
        """add_path getter

        The BGP Additional Paths feature is a BGP extension that allows the advertisement of multiple paths for the same prefix without the new paths implicitly replacing any previous paths.

        Returns: obj(snappi.DeviceBgpAddPath)
        """
        return self._get_property('add_path', DeviceBgpAddPath)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)


class DeviceBgpv4RouteAddress(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, address=None, prefix=None, count=None, step=None):
        super(DeviceBgpv4RouteAddress, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('address', address)
        self._set_property('prefix', prefix)
        self._set_property('count', count)
        self._set_property('step', step)

    @property
    def address(self):
        # type: () -> str
        """address getter

        The starting address of the network

        Returns: str
        """
        return self._get_property('address')

    @address.setter
    def address(self, value):
        """address setter

        The starting address of the network

        value: str
        """
        self._set_property('address', value)

    @property
    def prefix(self):
        # type: () -> int
        """prefix getter

        The IPv4 network prefix to be applied to the address. 

        Returns: int
        """
        return self._get_property('prefix')

    @prefix.setter
    def prefix(self, value):
        """prefix setter

        The IPv4 network prefix to be applied to the address. 

        value: int
        """
        self._set_property('prefix', value)

    @property
    def count(self):
        # type: () -> str
        """count getter

        The total number of addresses in the range

        Returns: str
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        The total number of addresses in the range

        value: str
        """
        self._set_property('count', value)

    @property
    def step(self):
        # type: () -> str
        """step getter

        The amount to increase each address by

        Returns: str
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        The amount to increase each address by

        value: str
        """
        self._set_property('step', value)


class DeviceBgpv4RouteAddressIter(SnappiIter):
    __slots__ = ()

    def __init__(self):
        super(DeviceBgpv4RouteAddressIter, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[DeviceBgpv4RouteAddress]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> DeviceBgpv4RouteAddressIter
        return self._iter()

    def __next__(self):
        # type: () -> DeviceBgpv4RouteAddress
        return self._next()

    def next(self):
        # type: () -> DeviceBgpv4RouteAddress
        return self._next()

    def bgpv4routeaddress(self, address='0.0.0.0', prefix=24, count='1', step='1'):
        # type: () -> DeviceBgpv4RouteAddressIter
        """Factory method that creates an instance of DeviceBgpv4RouteAddress class

        A container for BGPv4 route addresses
        """
        item = DeviceBgpv4RouteAddress(address=address, prefix=prefix, count=count, step=step)
        self._add(item)
        return self


class DeviceBgpRouteAdvanced(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    IGP = 'igp'
    EGP = 'egp'

    def __init__(self, parent=None, choice=None, multi_exit_discriminator=None, origin=None):
        super(DeviceBgpRouteAdvanced, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('multi_exit_discriminator', multi_exit_discriminator)
        self._set_property('origin', origin)

    @property
    def multi_exit_discriminator(self):
        # type: () -> int
        """multi_exit_discriminator getter

        The multi exit discriminator (MED) value. A null value means the MED feature is not enabled.

        Returns: int
        """
        return self._get_property('multi_exit_discriminator')

    @multi_exit_discriminator.setter
    def multi_exit_discriminator(self, value):
        """multi_exit_discriminator setter

        The multi exit discriminator (MED) value. A null value means the MED feature is not enabled.

        value: int
        """
        self._set_property('multi_exit_discriminator', value)

    @property
    def origin(self):
        # type: () -> Union[igp, egp]
        """origin getter

        The origin value. A null value means the origin feature is not enabled.

        Returns: Union[igp, egp]
        """
        return self._get_property('origin')

    @origin.setter
    def origin(self, value):
        """origin setter

        The origin value. A null value means the origin feature is not enabled.

        value: Union[igp, egp]
        """
        self._set_property('origin', value)


class DeviceBgpv4RouteIter(SnappiIter):
    __slots__ = ()

    def __init__(self):
        super(DeviceBgpv4RouteIter, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[DeviceBgpv4Route]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> DeviceBgpv4RouteIter
        return self._iter()

    def __next__(self):
        # type: () -> DeviceBgpv4Route
        return self._next()

    def next(self):
        # type: () -> DeviceBgpv4Route
        return self._next()

    def bgpv4route(self, next_hop_address='0.0.0.0', name=None):
        # type: () -> DeviceBgpv4RouteIter
        """Factory method that creates an instance of DeviceBgpv4Route class

        Emulated BGPv4 route. Container for BGP route ranges.
        """
        item = DeviceBgpv4Route(next_hop_address=next_hop_address, name=name)
        self._add(item)
        return self


class DeviceBgpv6Route(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'addresses': 'DeviceBgpv6RouteAddressIter',
        'advanced': 'DeviceBgpRouteAdvanced',
        'communities': 'DeviceBgpCommunityIter',
        'as_path': 'DeviceBgpAsPath',
        'add_path': 'DeviceBgpAddPath',
    }

    def __init__(self, parent=None, choice=None, next_hop_address=None, name=None):
        super(DeviceBgpv6Route, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('next_hop_address', next_hop_address)
        self._set_property('name', name)

    @property
    def addresses(self):
        # type: () -> DeviceBgpv6RouteAddressIter
        """addresses getter

        A list of symmetrical or asymmetrical route addresses

        Returns: list[obj(snappi.DeviceBgpv6RouteAddress)]
        """
        return self._get_property('addresses', DeviceBgpv6RouteAddressIter)

    @property
    def next_hop_address(self):
        # type: () -> str
        """next_hop_address getter

        IP Address of next router to forward a packet to its final destination

        Returns: str
        """
        return self._get_property('next_hop_address')

    @next_hop_address.setter
    def next_hop_address(self, value):
        """next_hop_address setter

        IP Address of next router to forward a packet to its final destination

        value: str
        """
        self._set_property('next_hop_address', value)

    @property
    def advanced(self):
        # type: () -> DeviceBgpRouteAdvanced
        """advanced getter

        Container for advanced BGP route range settings

        Returns: obj(snappi.DeviceBgpRouteAdvanced)
        """
        return self._get_property('advanced', DeviceBgpRouteAdvanced)

    @property
    def communities(self):
        # type: () -> DeviceBgpCommunityIter
        """communities getter

        Optional community settings.

        Returns: list[obj(snappi.DeviceBgpCommunity)]
        """
        return self._get_property('communities', DeviceBgpCommunityIter)

    @property
    def as_path(self):
        # type: () -> DeviceBgpAsPath
        """as_path getter

        Autonomous Systems (AS) numbers that a route passes through to reach the destination

        Returns: obj(snappi.DeviceBgpAsPath)
        """
        return self._get_property('as_path', DeviceBgpAsPath)

    @property
    def add_path(self):
        # type: () -> DeviceBgpAddPath
        """add_path getter

        The BGP Additional Paths feature is a BGP extension that allows the advertisement of multiple paths for the same prefix without the new paths implicitly replacing any previous paths.

        Returns: obj(snappi.DeviceBgpAddPath)
        """
        return self._get_property('add_path', DeviceBgpAddPath)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)


class DeviceBgpv6RouteAddress(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, address=None, prefix=None, count=None, step=None):
        super(DeviceBgpv6RouteAddress, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('address', address)
        self._set_property('prefix', prefix)
        self._set_property('count', count)
        self._set_property('step', step)

    @property
    def address(self):
        # type: () -> str
        """address getter

        The starting address of the network

        Returns: str
        """
        return self._get_property('address')

    @address.setter
    def address(self, value):
        """address setter

        The starting address of the network

        value: str
        """
        self._set_property('address', value)

    @property
    def prefix(self):
        # type: () -> int
        """prefix getter

        The IPv6 network prefix to be applied to the address

        Returns: int
        """
        return self._get_property('prefix')

    @prefix.setter
    def prefix(self, value):
        """prefix setter

        The IPv6 network prefix to be applied to the address

        value: int
        """
        self._set_property('prefix', value)

    @property
    def count(self):
        # type: () -> str
        """count getter

        The total number of addresses in the range

        Returns: str
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        The total number of addresses in the range

        value: str
        """
        self._set_property('count', value)

    @property
    def step(self):
        # type: () -> str
        """step getter

        The amount to increase each address by

        Returns: str
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        The amount to increase each address by

        value: str
        """
        self._set_property('step', value)


class DeviceBgpv6RouteAddressIter(SnappiIter):
    __slots__ = ()

    def __init__(self):
        super(DeviceBgpv6RouteAddressIter, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[DeviceBgpv6RouteAddress]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> DeviceBgpv6RouteAddressIter
        return self._iter()

    def __next__(self):
        # type: () -> DeviceBgpv6RouteAddress
        return self._next()

    def next(self):
        # type: () -> DeviceBgpv6RouteAddress
        return self._next()

    def bgpv6routeaddress(self, address='::0', prefix=64, count='1', step='1'):
        # type: () -> DeviceBgpv6RouteAddressIter
        """Factory method that creates an instance of DeviceBgpv6RouteAddress class

        A container for BGPv6 route addressses
        """
        item = DeviceBgpv6RouteAddress(address=address, prefix=prefix, count=count, step=step)
        self._add(item)
        return self


class DeviceBgpv6RouteIter(SnappiIter):
    __slots__ = ()

    def __init__(self):
        super(DeviceBgpv6RouteIter, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[DeviceBgpv6Route]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> DeviceBgpv6RouteIter
        return self._iter()

    def __next__(self):
        # type: () -> DeviceBgpv6Route
        return self._next()

    def next(self):
        # type: () -> DeviceBgpv6Route
        return self._next()

    def bgpv6route(self, next_hop_address='::0', name=None):
        # type: () -> DeviceBgpv6RouteIter
        """Factory method that creates an instance of DeviceBgpv6Route class

        Emulated BGPv6 route. Container for BGP route ranges.
        """
        item = DeviceBgpv6Route(next_hop_address=next_hop_address, name=name)
        self._add(item)
        return self


class DeviceIpv6(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'bgpv6': 'DeviceBgpv6',
    }

    def __init__(self, parent=None, choice=None, gateway=None, address=None, prefix=None, name=None):
        super(DeviceIpv6, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('gateway', gateway)
        self._set_property('address', address)
        self._set_property('prefix', prefix)
        self._set_property('name', name)

    @property
    def gateway(self):
        # type: () -> str
        """gateway getter

        The IPv6 gateway address

        Returns: str
        """
        return self._get_property('gateway')

    @gateway.setter
    def gateway(self, value):
        """gateway setter

        The IPv6 gateway address

        value: str
        """
        self._set_property('gateway', value)

    @property
    def address(self):
        # type: () -> str
        """address getter

        The IPv6 address.

        Returns: str
        """
        return self._get_property('address')

    @address.setter
    def address(self, value):
        """address setter

        The IPv6 address.

        value: str
        """
        self._set_property('address', value)

    @property
    def prefix(self):
        # type: () -> int
        """prefix getter

        The network prefix.

        Returns: int
        """
        return self._get_property('prefix')

    @prefix.setter
    def prefix(self, value):
        """prefix setter

        The network prefix.

        value: int
        """
        self._set_property('prefix', value)

    @property
    def bgpv6(self):
        # type: () -> DeviceBgpv6
        """bgpv6 getter

        Container for BGPv6 peer settings and routes.. Container for basic emulated BGP peer settings.

        Returns: obj(snappi.DeviceBgpv6)
        """
        return self._get_property('bgpv6', DeviceBgpv6)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)


class DeviceBgpv6(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'segment_routing': 'DeviceBgpv6SegmentRouting',
        'advanced': 'DeviceBgpAdvanced',
        'capability': 'DeviceBgpCapability',
        'sr_te_policies': 'DeviceBgpSrTePolicyIter',
        'bgpv4_routes': 'DeviceBgpv4RouteIter',
        'bgpv6_routes': 'DeviceBgpv6RouteIter',
    }

    IBGP = 'ibgp'
    EBGP = 'ebgp'

    TWO = 'two'
    FOUR = 'four'

    DO_NOT_INCLUDE_AS = 'do_not_include_as'
    INCLUDE_AS_SEQ = 'include_as_seq'
    INCLUDE_AS_SET = 'include_as_set'
    INCLUDE_AS_SEQ_CONFED = 'include_as_seq_confed'
    INCLUDE_AS_SET_CONFED = 'include_as_set_confed'
    PREPEND_AS_TO_FIRST_SEGMENT = 'prepend_as_to_first_segment'

    def __init__(self, parent=None, choice=None, local_address=None, dut_address=None, router_id=None, as_type=None, as_number=None, as_number_width=None, as_number_set_mode=None, name=None, active=None):
        super(DeviceBgpv6, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('local_address', local_address)
        self._set_property('dut_address', dut_address)
        self._set_property('router_id', router_id)
        self._set_property('as_type', as_type)
        self._set_property('as_number', as_number)
        self._set_property('as_number_width', as_number_width)
        self._set_property('as_number_set_mode', as_number_set_mode)
        self._set_property('name', name)
        self._set_property('active', active)

    @property
    def local_address(self):
        # type: () -> str
        """local_address getter

        Local IPv6 address of the emulated router

        Returns: str
        """
        return self._get_property('local_address')

    @local_address.setter
    def local_address(self, value):
        """local_address setter

        Local IPv6 address of the emulated router

        value: str
        """
        self._set_property('local_address', value)

    @property
    def dut_address(self):
        # type: () -> str
        """dut_address getter

        IPv6 address of the BGP peer for the session

        Returns: str
        """
        return self._get_property('dut_address')

    @dut_address.setter
    def dut_address(self, value):
        """dut_address setter

        IPv6 address of the BGP peer for the session

        value: str
        """
        self._set_property('dut_address', value)

    @property
    def segment_routing(self):
        # type: () -> DeviceBgpv6SegmentRouting
        """segment_routing getter

        Container for BGPv6 segment routing settings.

        Returns: obj(snappi.DeviceBgpv6SegmentRouting)
        """
        return self._get_property('segment_routing', DeviceBgpv6SegmentRouting)

    @property
    def router_id(self):
        # type: () -> str
        """router_id getter

        The BGP router ID is a unique identifier used by routing protocols. It is a 32-bit value that is often represented by an IPv4 address.

        Returns: str
        """
        return self._get_property('router_id')

    @router_id.setter
    def router_id(self, value):
        """router_id setter

        The BGP router ID is a unique identifier used by routing protocols. It is a 32-bit value that is often represented by an IPv4 address.

        value: str
        """
        self._set_property('router_id', value)

    @property
    def as_type(self):
        # type: () -> Union[ibgp, ebgp]
        """as_type getter

        The type of BGP autonomous system. External BGP is used for BGP links between two or more autonomous systems (ebgp) Internal BGP is used within a single autonomous system (ibgp). BGP property defaults are aligned with this object defined as an internal BGP peer. If the as_type is specified as ebgp then other properties will need to be specified according an external BGP peer.

        Returns: Union[ibgp, ebgp]
        """
        return self._get_property('as_type')

    @as_type.setter
    def as_type(self, value):
        """as_type setter

        The type of BGP autonomous system. External BGP is used for BGP links between two or more autonomous systems (ebgp) Internal BGP is used within a single autonomous system (ibgp). BGP property defaults are aligned with this object defined as an internal BGP peer. If the as_type is specified as ebgp then other properties will need to be specified according an external BGP peer.

        value: Union[ibgp, ebgp]
        """
        self._set_property('as_type', value)

    @property
    def as_number(self):
        # type: () -> int
        """as_number getter

        Autonomous System Number (AS number or ASN)

        Returns: int
        """
        return self._get_property('as_number')

    @as_number.setter
    def as_number(self, value):
        """as_number setter

        Autonomous System Number (AS number or ASN)

        value: int
        """
        self._set_property('as_number', value)

    @property
    def as_number_width(self):
        # type: () -> Union[two, four]
        """as_number_width getter

        The width in bytes of the as_number values. Any as_number values that exceed the width MUST result in an error

        Returns: Union[two, four]
        """
        return self._get_property('as_number_width')

    @as_number_width.setter
    def as_number_width(self, value):
        """as_number_width setter

        The width in bytes of the as_number values. Any as_number values that exceed the width MUST result in an error

        value: Union[two, four]
        """
        self._set_property('as_number_width', value)

    @property
    def as_number_set_mode(self):
        # type: () -> Union[do_not_include_as, include_as_seq, include_as_set, include_as_seq_confed, include_as_set_confed, prepend_as_to_first_segment]
        """as_number_set_mode getter

        The AS number set mode

        Returns: Union[do_not_include_as, include_as_seq, include_as_set, include_as_seq_confed, include_as_set_confed, prepend_as_to_first_segment]
        """
        return self._get_property('as_number_set_mode')

    @as_number_set_mode.setter
    def as_number_set_mode(self, value):
        """as_number_set_mode setter

        The AS number set mode

        value: Union[do_not_include_as, include_as_seq, include_as_set, include_as_seq_confed, include_as_set_confed, prepend_as_to_first_segment]
        """
        self._set_property('as_number_set_mode', value)

    @property
    def advanced(self):
        # type: () -> DeviceBgpAdvanced
        """advanced getter

        Container for BGP advanced settings.

        Returns: obj(snappi.DeviceBgpAdvanced)
        """
        return self._get_property('advanced', DeviceBgpAdvanced)

    @property
    def capability(self):
        # type: () -> DeviceBgpCapability
        """capability getter

        Container for BGP capability settings.

        Returns: obj(snappi.DeviceBgpCapability)
        """
        return self._get_property('capability', DeviceBgpCapability)

    @property
    def sr_te_policies(self):
        # type: () -> DeviceBgpSrTePolicyIter
        """sr_te_policies getter

        Segment routing/traffic engineering policies

        Returns: list[obj(snappi.DeviceBgpSrTePolicy)]
        """
        return self._get_property('sr_te_policies', DeviceBgpSrTePolicyIter)

    @property
    def bgpv4_routes(self):
        # type: () -> DeviceBgpv4RouteIter
        """bgpv4_routes getter

        Emulated BGPv4 routes

        Returns: list[obj(snappi.DeviceBgpv4Route)]
        """
        return self._get_property('bgpv4_routes', DeviceBgpv4RouteIter)

    @property
    def bgpv6_routes(self):
        # type: () -> DeviceBgpv6RouteIter
        """bgpv6_routes getter

        Emulated BGPv6 routes

        Returns: list[obj(snappi.DeviceBgpv6Route)]
        """
        return self._get_property('bgpv6_routes', DeviceBgpv6RouteIter)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)

    @property
    def active(self):
        # type: () -> boolean
        """active getter

        If enabled means that this part of the configuration including any active 'children' nodes will be advertised to peer. If disabled, this means that though config is present, it is not taking any part of the test but can be activated at run-time to advertise just this part of the configuration to the peer.

        Returns: boolean
        """
        return self._get_property('active')

    @active.setter
    def active(self, value):
        """active setter

        If enabled means that this part of the configuration including any active 'children' nodes will be advertised to peer. If disabled, this means that though config is present, it is not taking any part of the test but can be activated at run-time to advertise just this part of the configuration to the peer.

        value: boolean
        """
        self._set_property('active', value)


class DeviceBgpv6SegmentRouting(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, ingress_supports_vpn=None, reduced_encapsulation=None, copy_time_to_live=None, time_to_live=None, max_sids_per_srh=None, auto_generate_segment_left_value=None, segment_left_value=None, advertise_sr_te_policy=None):
        super(DeviceBgpv6SegmentRouting, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('ingress_supports_vpn', ingress_supports_vpn)
        self._set_property('reduced_encapsulation', reduced_encapsulation)
        self._set_property('copy_time_to_live', copy_time_to_live)
        self._set_property('time_to_live', time_to_live)
        self._set_property('max_sids_per_srh', max_sids_per_srh)
        self._set_property('auto_generate_segment_left_value', auto_generate_segment_left_value)
        self._set_property('segment_left_value', segment_left_value)
        self._set_property('advertise_sr_te_policy', advertise_sr_te_policy)

    @property
    def ingress_supports_vpn(self):
        # type: () -> boolean
        """ingress_supports_vpn getter

        TBD

        Returns: boolean
        """
        return self._get_property('ingress_supports_vpn')

    @ingress_supports_vpn.setter
    def ingress_supports_vpn(self, value):
        """ingress_supports_vpn setter

        TBD

        value: boolean
        """
        self._set_property('ingress_supports_vpn', value)

    @property
    def reduced_encapsulation(self):
        # type: () -> boolean
        """reduced_encapsulation getter

        TBD

        Returns: boolean
        """
        return self._get_property('reduced_encapsulation')

    @reduced_encapsulation.setter
    def reduced_encapsulation(self, value):
        """reduced_encapsulation setter

        TBD

        value: boolean
        """
        self._set_property('reduced_encapsulation', value)

    @property
    def copy_time_to_live(self):
        # type: () -> boolean
        """copy_time_to_live getter

        TBD

        Returns: boolean
        """
        return self._get_property('copy_time_to_live')

    @copy_time_to_live.setter
    def copy_time_to_live(self, value):
        """copy_time_to_live setter

        TBD

        value: boolean
        """
        self._set_property('copy_time_to_live', value)

    @property
    def time_to_live(self):
        # type: () -> int
        """time_to_live getter

        TBD

        Returns: int
        """
        return self._get_property('time_to_live')

    @time_to_live.setter
    def time_to_live(self, value):
        """time_to_live setter

        TBD

        value: int
        """
        self._set_property('time_to_live', value)

    @property
    def max_sids_per_srh(self):
        # type: () -> int
        """max_sids_per_srh getter

        TBD

        Returns: int
        """
        return self._get_property('max_sids_per_srh')

    @max_sids_per_srh.setter
    def max_sids_per_srh(self, value):
        """max_sids_per_srh setter

        TBD

        value: int
        """
        self._set_property('max_sids_per_srh', value)

    @property
    def auto_generate_segment_left_value(self):
        # type: () -> boolean
        """auto_generate_segment_left_value getter

        TBD

        Returns: boolean
        """
        return self._get_property('auto_generate_segment_left_value')

    @auto_generate_segment_left_value.setter
    def auto_generate_segment_left_value(self, value):
        """auto_generate_segment_left_value setter

        TBD

        value: boolean
        """
        self._set_property('auto_generate_segment_left_value', value)

    @property
    def segment_left_value(self):
        # type: () -> int
        """segment_left_value getter

        TBD

        Returns: int
        """
        return self._get_property('segment_left_value')

    @segment_left_value.setter
    def segment_left_value(self, value):
        """segment_left_value setter

        TBD

        value: int
        """
        self._set_property('segment_left_value', value)

    @property
    def advertise_sr_te_policy(self):
        # type: () -> boolean
        """advertise_sr_te_policy getter

        TBD

        Returns: boolean
        """
        return self._get_property('advertise_sr_te_policy')

    @advertise_sr_te_policy.setter
    def advertise_sr_te_policy(self, value):
        """advertise_sr_te_policy setter

        TBD

        value: boolean
        """
        self._set_property('advertise_sr_te_policy', value)


class DeviceIter(SnappiIter):
    __slots__ = ()

    def __init__(self):
        super(DeviceIter, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[Device]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> DeviceIter
        return self._iter()

    def __next__(self):
        # type: () -> Device
        return self._next()

    def next(self):
        # type: () -> Device
        return self._next()

    def device(self, container_name=None, name=None):
        # type: () -> DeviceIter
        """Factory method that creates an instance of Device class

        A container for emulated interfaces and protocol devices.
        """
        item = Device(container_name=container_name, name=name)
        self._add(item)
        return self


class Flow(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'tx_rx': 'FlowTxRx',
        'packet': 'FlowHeaderIter',
        'size': 'FlowSize',
        'rate': 'FlowRate',
        'duration': 'FlowDuration',
    }

    def __init__(self, parent=None, choice=None, name=None):
        super(Flow, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('name', name)

    @property
    def tx_rx(self):
        # type: () -> FlowTxRx
        """tx_rx getter

        A container for different types of transmit and receive endpoint containers.The transmit and receive endpoints.

        Returns: obj(snappi.FlowTxRx)
        """
        return self._get_property('tx_rx', FlowTxRx)

    @property
    def packet(self):
        # type: () -> FlowHeaderIter
        """packet getter

        The header is a list of traffic protocol headers. The order of traffic protocol headers assigned to the list is the order they will appear on the wire.

        Returns: list[obj(snappi.FlowHeader)]
        """
        return self._get_property('packet', FlowHeaderIter)

    @property
    def size(self):
        # type: () -> FlowSize
        """size getter

        The frame size which overrides the total length of the packetThe size of the packets.

        Returns: obj(snappi.FlowSize)
        """
        return self._get_property('size', FlowSize)

    @property
    def rate(self):
        # type: () -> FlowRate
        """rate getter

        The rate of packet transmissionThe transmit rate of the packets.

        Returns: obj(snappi.FlowRate)
        """
        return self._get_property('rate', FlowRate)

    @property
    def duration(self):
        # type: () -> FlowDuration
        """duration getter

        A container for different transmit durations. The transmit duration of the packets.

        Returns: obj(snappi.FlowDuration)
        """
        return self._get_property('duration', FlowDuration)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)


class FlowTxRx(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'port': 'FlowPort',
        'device': 'FlowDevice',
    }

    PORT = 'port'
    DEVICE = 'device'

    def __init__(self, parent=None, choice=None):
        super(FlowTxRx, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def port(self):
        # type: () -> FlowPort
        """Factory property that returns an instance of the FlowPort class

        A container for a transmit port and 0..n intended receive ports. When assigning this container to a flow the flows's packet headers will not be populated with any address resolution information such as source and/or destination addresses. For example Flow.Ethernet dst mac address values will be defaulted to 0. For full control over the Flow.properties.packet header contents use this container. 
        """
        return self._get_property('port', FlowPort(self, 'port'))

    @property
    def device(self):
        # type: () -> FlowDevice
        """Factory property that returns an instance of the FlowDevice class

        A container for 1..n transmit devices and 1..n receive devices. Implemementations may use learned information from the devices to pre-populate Flow.properties.packet[Flow.Header fields].. For example an implementation may automatically start devices, get arp table information and pre-populate the Flow.Ethernet dst mac address values.. To discover what the implementation supports use the /results/capabilities API.
        """
        return self._get_property('device', FlowDevice(self, 'device'))

    @property
    def choice(self):
        # type: () -> Union[port, device, choice, choice, choice]
        """choice getter

        The type of transmit and receive container used by the flow.

        Returns: Union[port, device, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        The type of transmit and receive container used by the flow.

        value: Union[port, device, choice, choice, choice]
        """
        self._set_property('choice', value)


class FlowPort(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, tx_name=None, rx_name=None):
        super(FlowPort, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('tx_name', tx_name)
        self._set_property('rx_name', rx_name)

    @property
    def tx_name(self):
        # type: () -> str
        """tx_name getter

        The unique name of a port that is the transmit port.

        Returns: str
        """
        return self._get_property('tx_name')

    @tx_name.setter
    def tx_name(self, value):
        """tx_name setter

        The unique name of a port that is the transmit port.

        value: str
        """
        self._set_property('tx_name', value)

    @property
    def rx_name(self):
        # type: () -> str
        """rx_name getter

        The unique name of a port that is the intended receive port.

        Returns: str
        """
        return self._get_property('rx_name')

    @rx_name.setter
    def rx_name(self, value):
        """rx_name setter

        The unique name of a port that is the intended receive port.

        value: str
        """
        self._set_property('rx_name', value)


class FlowDevice(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, tx_names=None, rx_names=None):
        super(FlowDevice, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('tx_names', tx_names)
        self._set_property('rx_names', rx_names)

    @property
    def tx_names(self):
        # type: () -> list[str]
        """tx_names getter

        The unique names of devices that will be transmitting.

        Returns: list[str]
        """
        return self._get_property('tx_names')

    @tx_names.setter
    def tx_names(self, value):
        """tx_names setter

        The unique names of devices that will be transmitting.

        value: list[str]
        """
        self._set_property('tx_names', value)

    @property
    def rx_names(self):
        # type: () -> list[str]
        """rx_names getter

        The unique names of emulated devices that will be receiving.

        Returns: list[str]
        """
        return self._get_property('rx_names')

    @rx_names.setter
    def rx_names(self, value):
        """rx_names setter

        The unique names of emulated devices that will be receiving.

        value: list[str]
        """
        self._set_property('rx_names', value)


class FlowHeader(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'custom': 'FlowCustom',
        'ethernet': 'FlowEthernet',
        'vlan': 'FlowVlan',
        'vxlan': 'FlowVxlan',
        'ipv4': 'FlowIpv4',
        'ipv6': 'FlowIpv6',
        'pfcpause': 'FlowPfcPause',
        'ethernetpause': 'FlowEthernetPause',
        'tcp': 'FlowTcp',
        'udp': 'FlowUdp',
        'gre': 'FlowGre',
        'gtpv1': 'FlowGtpv1',
        'gtpv2': 'FlowGtpv2',
        'arp': 'FlowArp',
        'icmp': 'FlowIcmp',
        'icmpv6': 'FlowIcmpv6',
        'ppp': 'FlowPpp',
        'igmpv1': 'FlowIgmpv1',
    }

    CUSTOM = 'custom'
    ETHERNET = 'ethernet'
    VLAN = 'vlan'
    VXLAN = 'vxlan'
    IPV4 = 'ipv4'
    IPV6 = 'ipv6'
    PFCPAUSE = 'pfcpause'
    ETHERNETPAUSE = 'ethernetpause'
    TCP = 'tcp'
    UDP = 'udp'
    GRE = 'gre'
    GTPV1 = 'gtpv1'
    GTPV2 = 'gtpv2'
    ARP = 'arp'
    ICMP = 'icmp'
    ICMPV6 = 'icmpv6'
    PPP = 'ppp'
    IGMPV1 = 'igmpv1'

    def __init__(self, parent=None, choice=None):
        super(FlowHeader, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def custom(self):
        # type: () -> FlowCustom
        """Factory property that returns an instance of the FlowCustom class

        Custom packet header
        """
        return self._get_property('custom', FlowCustom(self, 'custom'))

    @property
    def ethernet(self):
        # type: () -> FlowEthernet
        """Factory property that returns an instance of the FlowEthernet class

        Ethernet packet header
        """
        return self._get_property('ethernet', FlowEthernet(self, 'ethernet'))

    @property
    def vlan(self):
        # type: () -> FlowVlan
        """Factory property that returns an instance of the FlowVlan class

        VLAN packet header
        """
        return self._get_property('vlan', FlowVlan(self, 'vlan'))

    @property
    def vxlan(self):
        # type: () -> FlowVxlan
        """Factory property that returns an instance of the FlowVxlan class

        VXLAN packet header
        """
        return self._get_property('vxlan', FlowVxlan(self, 'vxlan'))

    @property
    def ipv4(self):
        # type: () -> FlowIpv4
        """Factory property that returns an instance of the FlowIpv4 class

        IPv4 packet header
        """
        return self._get_property('ipv4', FlowIpv4(self, 'ipv4'))

    @property
    def ipv6(self):
        # type: () -> FlowIpv6
        """Factory property that returns an instance of the FlowIpv6 class

        IPv6 packet header
        """
        return self._get_property('ipv6', FlowIpv6(self, 'ipv6'))

    @property
    def pfcpause(self):
        # type: () -> FlowPfcPause
        """Factory property that returns an instance of the FlowPfcPause class

        IEEE 802.1Qbb PFC Pause packet header.
        """
        return self._get_property('pfcpause', FlowPfcPause(self, 'pfcpause'))

    @property
    def ethernetpause(self):
        # type: () -> FlowEthernetPause
        """Factory property that returns an instance of the FlowEthernetPause class

        IEEE 802.3x global ethernet pause packet header
        """
        return self._get_property('ethernetpause', FlowEthernetPause(self, 'ethernetpause'))

    @property
    def tcp(self):
        # type: () -> FlowTcp
        """Factory property that returns an instance of the FlowTcp class

        TCP packet header
        """
        return self._get_property('tcp', FlowTcp(self, 'tcp'))

    @property
    def udp(self):
        # type: () -> FlowUdp
        """Factory property that returns an instance of the FlowUdp class

        UDP packet header
        """
        return self._get_property('udp', FlowUdp(self, 'udp'))

    @property
    def gre(self):
        # type: () -> FlowGre
        """Factory property that returns an instance of the FlowGre class

        Standard GRE packet header (RFC2784)
        """
        return self._get_property('gre', FlowGre(self, 'gre'))

    @property
    def gtpv1(self):
        # type: () -> FlowGtpv1
        """Factory property that returns an instance of the FlowGtpv1 class

        GTPv1 packet header
        """
        return self._get_property('gtpv1', FlowGtpv1(self, 'gtpv1'))

    @property
    def gtpv2(self):
        # type: () -> FlowGtpv2
        """Factory property that returns an instance of the FlowGtpv2 class

        GTPv2 packet header
        """
        return self._get_property('gtpv2', FlowGtpv2(self, 'gtpv2'))

    @property
    def arp(self):
        # type: () -> FlowArp
        """Factory property that returns an instance of the FlowArp class

        ARP packet header
        """
        return self._get_property('arp', FlowArp(self, 'arp'))

    @property
    def icmp(self):
        # type: () -> FlowIcmp
        """Factory property that returns an instance of the FlowIcmp class

        ICMP packet header
        """
        return self._get_property('icmp', FlowIcmp(self, 'icmp'))

    @property
    def icmpv6(self):
        # type: () -> FlowIcmpv6
        """Factory property that returns an instance of the FlowIcmpv6 class

        ICMPv6 packet header
        """
        return self._get_property('icmpv6', FlowIcmpv6(self, 'icmpv6'))

    @property
    def ppp(self):
        # type: () -> FlowPpp
        """Factory property that returns an instance of the FlowPpp class

        PPP packet header
        """
        return self._get_property('ppp', FlowPpp(self, 'ppp'))

    @property
    def igmpv1(self):
        # type: () -> FlowIgmpv1
        """Factory property that returns an instance of the FlowIgmpv1 class

        IGMPv1 packet header
        """
        return self._get_property('igmpv1', FlowIgmpv1(self, 'igmpv1'))

    @property
    def choice(self):
        # type: () -> Union[custom, ethernet, vlan, vxlan, ipv4, ipv6, pfcpause, ethernetpause, tcp, udp, gre, gtpv1, gtpv2, arp, icmp, icmpv6, ppp, igmpv1, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[custom, ethernet, vlan, vxlan, ipv4, ipv6, pfcpause, ethernetpause, tcp, udp, gre, gtpv1, gtpv2, arp, icmp, icmpv6, ppp, igmpv1, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[custom, ethernet, vlan, vxlan, ipv4, ipv6, pfcpause, ethernetpause, tcp, udp, gre, gtpv1, gtpv2, arp, icmp, icmpv6, ppp, igmpv1, choice, choice, choice]
        """
        self._set_property('choice', value)


class FlowCustom(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, bytes=None):
        super(FlowCustom, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('bytes', bytes)

    @property
    def bytes(self):
        # type: () -> str
        """bytes getter

        A custom packet header defined as a string of hex bytes. The string MUST contain sequence of valid hex bytes. Spaces or colons can be part of the bytes but will be discarded. This packet header can be used in multiple places in the packet.

        Returns: str
        """
        return self._get_property('bytes')

    @bytes.setter
    def bytes(self, value):
        """bytes setter

        A custom packet header defined as a string of hex bytes. The string MUST contain sequence of valid hex bytes. Spaces or colons can be part of the bytes but will be discarded. This packet header can be used in multiple places in the packet.

        value: str
        """
        self._set_property('bytes', value)


class FlowEthernet(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'dst': 'PatternFlowEthernetDst',
        'src': 'PatternFlowEthernetSrc',
        'ether_type': 'PatternFlowEthernetEtherType',
        'pfc_queue': 'PatternFlowEthernetPfcQueue',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowEthernet, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def dst(self):
        # type: () -> PatternFlowEthernetDst
        """dst getter

        Destination MAC addressDestination MAC address

        Returns: obj(snappi.PatternFlowEthernetDst)
        """
        return self._get_property('dst', PatternFlowEthernetDst)

    @property
    def src(self):
        # type: () -> PatternFlowEthernetSrc
        """src getter

        Source MAC addressSource MAC address

        Returns: obj(snappi.PatternFlowEthernetSrc)
        """
        return self._get_property('src', PatternFlowEthernetSrc)

    @property
    def ether_type(self):
        # type: () -> PatternFlowEthernetEtherType
        """ether_type getter

        Ethernet typeEthernet type

        Returns: obj(snappi.PatternFlowEthernetEtherType)
        """
        return self._get_property('ether_type', PatternFlowEthernetEtherType)

    @property
    def pfc_queue(self):
        # type: () -> PatternFlowEthernetPfcQueue
        """pfc_queue getter

        Priority flow control queuePriority flow control queue

        Returns: obj(snappi.PatternFlowEthernetPfcQueue)
        """
        return self._get_property('pfc_queue', PatternFlowEthernetPfcQueue)


class PatternFlowEthernetDst(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowEthernetDstCounter',
        'decrement': 'PatternFlowEthernetDstCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowEthernetDst, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowEthernetDstCounter
        """Factory property that returns an instance of the PatternFlowEthernetDstCounter class

        mac counter pattern
        """
        return self._get_property('increment', PatternFlowEthernetDstCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowEthernetDstCounter
        """Factory property that returns an instance of the PatternFlowEthernetDstCounter class

        mac counter pattern
        """
        return self._get_property('decrement', PatternFlowEthernetDstCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> str
        """value getter

        TBD

        Returns: str
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: str
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[str]
        """values getter

        TBD

        Returns: list[str]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[str]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowEthernetDstCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowEthernetDstCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> str
        """start getter

        TBD

        Returns: str
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: str
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> str
        """step getter

        TBD

        Returns: str
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: str
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowEthernetSrc(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowEthernetSrcCounter',
        'decrement': 'PatternFlowEthernetSrcCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowEthernetSrc, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowEthernetSrcCounter
        """Factory property that returns an instance of the PatternFlowEthernetSrcCounter class

        mac counter pattern
        """
        return self._get_property('increment', PatternFlowEthernetSrcCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowEthernetSrcCounter
        """Factory property that returns an instance of the PatternFlowEthernetSrcCounter class

        mac counter pattern
        """
        return self._get_property('decrement', PatternFlowEthernetSrcCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> str
        """value getter

        TBD

        Returns: str
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: str
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[str]
        """values getter

        TBD

        Returns: list[str]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[str]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowEthernetSrcCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowEthernetSrcCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> str
        """start getter

        TBD

        Returns: str
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: str
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> str
        """step getter

        TBD

        Returns: str
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: str
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowEthernetEtherType(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowEthernetEtherTypeCounter',
        'decrement': 'PatternFlowEthernetEtherTypeCounter',
    }

    IPV4 = '2048'
    IPV6 = '34525'
    ARP = '2054'
    VLAN_802_1_Q = '33024'
    RESERVED = '65535'

    VALUE = 'value'
    VALUES = 'values'
    AUTO = 'auto'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    AUTO = 'auto'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowEthernetEtherType, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowEthernetEtherTypeCounter
        """Factory property that returns an instance of the PatternFlowEthernetEtherTypeCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowEthernetEtherTypeCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowEthernetEtherTypeCounter
        """Factory property that returns an instance of the PatternFlowEthernetEtherTypeCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowEthernetEtherTypeCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, auto, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, auto, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, auto, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def auto(self):
        # type: () -> Union[auto]
        """auto getter

        TBD

        Returns: Union[auto]
        """
        return self._get_property('auto')

    @auto.setter
    def auto(self, value):
        """auto setter

        TBD

        value: Union[auto]
        """
        self._set_property('auto', value, 'auto')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowEthernetEtherTypeCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    IPV4 = '2048'
    IPV6 = '34525'
    ARP = '2054'
    VLAN_802_1_Q = '33024'
    RESERVED = '65535'

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowEthernetEtherTypeCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowEthernetPfcQueue(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowEthernetPfcQueueCounter',
        'decrement': 'PatternFlowEthernetPfcQueueCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowEthernetPfcQueue, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowEthernetPfcQueueCounter
        """Factory property that returns an instance of the PatternFlowEthernetPfcQueueCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowEthernetPfcQueueCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowEthernetPfcQueueCounter
        """Factory property that returns an instance of the PatternFlowEthernetPfcQueueCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowEthernetPfcQueueCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowEthernetPfcQueueCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowEthernetPfcQueueCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class FlowVlan(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'priority': 'PatternFlowVlanPriority',
        'cfi': 'PatternFlowVlanCfi',
        'id': 'PatternFlowVlanId',
        'tpid': 'PatternFlowVlanTpid',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowVlan, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def priority(self):
        # type: () -> PatternFlowVlanPriority
        """priority getter

        Priority code pointPriority code point

        Returns: obj(snappi.PatternFlowVlanPriority)
        """
        return self._get_property('priority', PatternFlowVlanPriority)

    @property
    def cfi(self):
        # type: () -> PatternFlowVlanCfi
        """cfi getter

        Canonical format indicator or drop elegible indicatorCanonical format indicator or drop elegible indicator

        Returns: obj(snappi.PatternFlowVlanCfi)
        """
        return self._get_property('cfi', PatternFlowVlanCfi)

    @property
    def id(self):
        # type: () -> PatternFlowVlanId
        """id getter

        Vlan identifierVlan identifier

        Returns: obj(snappi.PatternFlowVlanId)
        """
        return self._get_property('id', PatternFlowVlanId)

    @property
    def tpid(self):
        # type: () -> PatternFlowVlanTpid
        """tpid getter

        Protocol identifierProtocol identifier

        Returns: obj(snappi.PatternFlowVlanTpid)
        """
        return self._get_property('tpid', PatternFlowVlanTpid)


class PatternFlowVlanPriority(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowVlanPriorityCounter',
        'decrement': 'PatternFlowVlanPriorityCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowVlanPriority, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowVlanPriorityCounter
        """Factory property that returns an instance of the PatternFlowVlanPriorityCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowVlanPriorityCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowVlanPriorityCounter
        """Factory property that returns an instance of the PatternFlowVlanPriorityCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowVlanPriorityCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowVlanPriorityCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowVlanPriorityCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowVlanCfi(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowVlanCfiCounter',
        'decrement': 'PatternFlowVlanCfiCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowVlanCfi, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowVlanCfiCounter
        """Factory property that returns an instance of the PatternFlowVlanCfiCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowVlanCfiCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowVlanCfiCounter
        """Factory property that returns an instance of the PatternFlowVlanCfiCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowVlanCfiCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowVlanCfiCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowVlanCfiCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowVlanId(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowVlanIdCounter',
        'decrement': 'PatternFlowVlanIdCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowVlanId, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowVlanIdCounter
        """Factory property that returns an instance of the PatternFlowVlanIdCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowVlanIdCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowVlanIdCounter
        """Factory property that returns an instance of the PatternFlowVlanIdCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowVlanIdCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowVlanIdCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowVlanIdCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowVlanTpid(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowVlanTpidCounter',
        'decrement': 'PatternFlowVlanTpidCounter',
    }

    X8100 = '33024'
    X88A8 = '34984'
    X9100 = '37120'
    X9200 = '37376'
    X9300 = '37632'

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowVlanTpid, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowVlanTpidCounter
        """Factory property that returns an instance of the PatternFlowVlanTpidCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowVlanTpidCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowVlanTpidCounter
        """Factory property that returns an instance of the PatternFlowVlanTpidCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowVlanTpidCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowVlanTpidCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    X8100 = '33024'
    X88A8 = '34984'
    X9100 = '37120'
    X9200 = '37376'
    X9300 = '37632'

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowVlanTpidCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class FlowVxlan(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'flags': 'PatternFlowVxlanFlags',
        'reserved0': 'PatternFlowVxlanReserved0',
        'vni': 'PatternFlowVxlanVni',
        'reserved1': 'PatternFlowVxlanReserved1',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowVxlan, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def flags(self):
        # type: () -> PatternFlowVxlanFlags
        """flags getter

        Flags field with a bit format of RRRRIRRR. The I flag MUST be set to 1 for a valid vxlan network id (VNI). The other 7 bits (designated "R") are reserved fields and MUST be set to zero on transmission and ignored on receipt.Flags field with a bit format of RRRRIRRR. The I flag MUST be set to 1 for a valid vxlan network id (VNI). The other 7 bits (designated "R") are reserved fields and MUST be set to zero on transmission and ignored on receipt.

        Returns: obj(snappi.PatternFlowVxlanFlags)
        """
        return self._get_property('flags', PatternFlowVxlanFlags)

    @property
    def reserved0(self):
        # type: () -> PatternFlowVxlanReserved0
        """reserved0 getter

        Reserved fieldReserved field

        Returns: obj(snappi.PatternFlowVxlanReserved0)
        """
        return self._get_property('reserved0', PatternFlowVxlanReserved0)

    @property
    def vni(self):
        # type: () -> PatternFlowVxlanVni
        """vni getter

        VXLAN network idVXLAN network id

        Returns: obj(snappi.PatternFlowVxlanVni)
        """
        return self._get_property('vni', PatternFlowVxlanVni)

    @property
    def reserved1(self):
        # type: () -> PatternFlowVxlanReserved1
        """reserved1 getter

        Reserved fieldReserved field

        Returns: obj(snappi.PatternFlowVxlanReserved1)
        """
        return self._get_property('reserved1', PatternFlowVxlanReserved1)


class PatternFlowVxlanFlags(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowVxlanFlagsCounter',
        'decrement': 'PatternFlowVxlanFlagsCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowVxlanFlags, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowVxlanFlagsCounter
        """Factory property that returns an instance of the PatternFlowVxlanFlagsCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowVxlanFlagsCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowVxlanFlagsCounter
        """Factory property that returns an instance of the PatternFlowVxlanFlagsCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowVxlanFlagsCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowVxlanFlagsCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowVxlanFlagsCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowVxlanReserved0(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowVxlanReserved0Counter',
        'decrement': 'PatternFlowVxlanReserved0Counter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowVxlanReserved0, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowVxlanReserved0Counter
        """Factory property that returns an instance of the PatternFlowVxlanReserved0Counter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowVxlanReserved0Counter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowVxlanReserved0Counter
        """Factory property that returns an instance of the PatternFlowVxlanReserved0Counter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowVxlanReserved0Counter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowVxlanReserved0Counter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowVxlanReserved0Counter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowVxlanVni(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowVxlanVniCounter',
        'decrement': 'PatternFlowVxlanVniCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowVxlanVni, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowVxlanVniCounter
        """Factory property that returns an instance of the PatternFlowVxlanVniCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowVxlanVniCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowVxlanVniCounter
        """Factory property that returns an instance of the PatternFlowVxlanVniCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowVxlanVniCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowVxlanVniCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowVxlanVniCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowVxlanReserved1(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowVxlanReserved1Counter',
        'decrement': 'PatternFlowVxlanReserved1Counter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowVxlanReserved1, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowVxlanReserved1Counter
        """Factory property that returns an instance of the PatternFlowVxlanReserved1Counter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowVxlanReserved1Counter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowVxlanReserved1Counter
        """Factory property that returns an instance of the PatternFlowVxlanReserved1Counter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowVxlanReserved1Counter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowVxlanReserved1Counter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowVxlanReserved1Counter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class FlowIpv4(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'version': 'PatternFlowIpv4Version',
        'header_length': 'PatternFlowIpv4HeaderLength',
        'priority': 'FlowIpv4Priority',
        'total_length': 'PatternFlowIpv4TotalLength',
        'identification': 'PatternFlowIpv4Identification',
        'reserved': 'PatternFlowIpv4Reserved',
        'dont_fragment': 'PatternFlowIpv4DontFragment',
        'more_fragments': 'PatternFlowIpv4MoreFragments',
        'fragment_offset': 'PatternFlowIpv4FragmentOffset',
        'time_to_live': 'PatternFlowIpv4TimeToLive',
        'protocol': 'PatternFlowIpv4Protocol',
        'header_checksum': 'PatternFlowIpv4HeaderChecksum',
        'src': 'PatternFlowIpv4Src',
        'dst': 'PatternFlowIpv4Dst',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowIpv4, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def version(self):
        # type: () -> PatternFlowIpv4Version
        """version getter

        VersionVersion

        Returns: obj(snappi.PatternFlowIpv4Version)
        """
        return self._get_property('version', PatternFlowIpv4Version)

    @property
    def header_length(self):
        # type: () -> PatternFlowIpv4HeaderLength
        """header_length getter

        Header lengthHeader length

        Returns: obj(snappi.PatternFlowIpv4HeaderLength)
        """
        return self._get_property('header_length', PatternFlowIpv4HeaderLength)

    @property
    def priority(self):
        # type: () -> FlowIpv4Priority
        """priority getter

        A container for ipv4 raw, tos, dscp ip priorities.A container for ipv4 raw, tos, dscp ip priorities.

        Returns: obj(snappi.FlowIpv4Priority)
        """
        return self._get_property('priority', FlowIpv4Priority)

    @property
    def total_length(self):
        # type: () -> PatternFlowIpv4TotalLength
        """total_length getter

        Total lengthTotal length

        Returns: obj(snappi.PatternFlowIpv4TotalLength)
        """
        return self._get_property('total_length', PatternFlowIpv4TotalLength)

    @property
    def identification(self):
        # type: () -> PatternFlowIpv4Identification
        """identification getter

        IdentificationIdentification

        Returns: obj(snappi.PatternFlowIpv4Identification)
        """
        return self._get_property('identification', PatternFlowIpv4Identification)

    @property
    def reserved(self):
        # type: () -> PatternFlowIpv4Reserved
        """reserved getter

        VersionVersion

        Returns: obj(snappi.PatternFlowIpv4Reserved)
        """
        return self._get_property('reserved', PatternFlowIpv4Reserved)

    @property
    def dont_fragment(self):
        # type: () -> PatternFlowIpv4DontFragment
        """dont_fragment getter

        Dont fragmentDont fragment

        Returns: obj(snappi.PatternFlowIpv4DontFragment)
        """
        return self._get_property('dont_fragment', PatternFlowIpv4DontFragment)

    @property
    def more_fragments(self):
        # type: () -> PatternFlowIpv4MoreFragments
        """more_fragments getter

        More fragmentsMore fragments

        Returns: obj(snappi.PatternFlowIpv4MoreFragments)
        """
        return self._get_property('more_fragments', PatternFlowIpv4MoreFragments)

    @property
    def fragment_offset(self):
        # type: () -> PatternFlowIpv4FragmentOffset
        """fragment_offset getter

        Fragment offsetFragment offset

        Returns: obj(snappi.PatternFlowIpv4FragmentOffset)
        """
        return self._get_property('fragment_offset', PatternFlowIpv4FragmentOffset)

    @property
    def time_to_live(self):
        # type: () -> PatternFlowIpv4TimeToLive
        """time_to_live getter

        Time to liveTime to live

        Returns: obj(snappi.PatternFlowIpv4TimeToLive)
        """
        return self._get_property('time_to_live', PatternFlowIpv4TimeToLive)

    @property
    def protocol(self):
        # type: () -> PatternFlowIpv4Protocol
        """protocol getter

        Protocol, default is 61 any host internal protocolProtocol, default is 61 any host internal protocol

        Returns: obj(snappi.PatternFlowIpv4Protocol)
        """
        return self._get_property('protocol', PatternFlowIpv4Protocol)

    @property
    def header_checksum(self):
        # type: () -> PatternFlowIpv4HeaderChecksum
        """header_checksum getter

        Header checksumHeader checksum

        Returns: obj(snappi.PatternFlowIpv4HeaderChecksum)
        """
        return self._get_property('header_checksum', PatternFlowIpv4HeaderChecksum)

    @property
    def src(self):
        # type: () -> PatternFlowIpv4Src
        """src getter

        Source addressSource address

        Returns: obj(snappi.PatternFlowIpv4Src)
        """
        return self._get_property('src', PatternFlowIpv4Src)

    @property
    def dst(self):
        # type: () -> PatternFlowIpv4Dst
        """dst getter

        Destination addressDestination address

        Returns: obj(snappi.PatternFlowIpv4Dst)
        """
        return self._get_property('dst', PatternFlowIpv4Dst)


class PatternFlowIpv4Version(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIpv4VersionCounter',
        'decrement': 'PatternFlowIpv4VersionCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIpv4Version, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIpv4VersionCounter
        """Factory property that returns an instance of the PatternFlowIpv4VersionCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIpv4VersionCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIpv4VersionCounter
        """Factory property that returns an instance of the PatternFlowIpv4VersionCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIpv4VersionCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIpv4VersionCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIpv4VersionCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIpv4HeaderLength(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIpv4HeaderLengthCounter',
        'decrement': 'PatternFlowIpv4HeaderLengthCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    AUTO = 'auto'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    AUTO = 'auto'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIpv4HeaderLength, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIpv4HeaderLengthCounter
        """Factory property that returns an instance of the PatternFlowIpv4HeaderLengthCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIpv4HeaderLengthCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIpv4HeaderLengthCounter
        """Factory property that returns an instance of the PatternFlowIpv4HeaderLengthCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIpv4HeaderLengthCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, auto, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, auto, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, auto, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def auto(self):
        # type: () -> Union[auto]
        """auto getter

        TBD

        Returns: Union[auto]
        """
        return self._get_property('auto')

    @auto.setter
    def auto(self, value):
        """auto setter

        TBD

        value: Union[auto]
        """
        self._set_property('auto', value, 'auto')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIpv4HeaderLengthCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIpv4HeaderLengthCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class FlowIpv4Priority(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'raw': 'PatternFlowIpv4PriorityRaw',
        'tos': 'FlowIpv4Tos',
        'dscp': 'FlowIpv4Dscp',
    }

    RAW = 'raw'
    TOS = 'tos'
    DSCP = 'dscp'

    def __init__(self, parent=None, choice=None):
        super(FlowIpv4Priority, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def raw(self):
        # type: () -> PatternFlowIpv4PriorityRaw
        """Factory property that returns an instance of the PatternFlowIpv4PriorityRaw class

        Raw priority
        """
        return self._get_property('raw', PatternFlowIpv4PriorityRaw(self, 'raw'))

    @property
    def tos(self):
        # type: () -> FlowIpv4Tos
        """Factory property that returns an instance of the FlowIpv4Tos class

        Type of service (TOS) packet field.
        """
        return self._get_property('tos', FlowIpv4Tos(self, 'tos'))

    @property
    def dscp(self):
        # type: () -> FlowIpv4Dscp
        """Factory property that returns an instance of the FlowIpv4Dscp class

        Differentiated services code point (DSCP) packet field.
        """
        return self._get_property('dscp', FlowIpv4Dscp(self, 'dscp'))

    @property
    def choice(self):
        # type: () -> Union[raw, tos, dscp, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[raw, tos, dscp, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[raw, tos, dscp, choice, choice, choice]
        """
        self._set_property('choice', value)


class PatternFlowIpv4PriorityRaw(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIpv4PriorityRawCounter',
        'decrement': 'PatternFlowIpv4PriorityRawCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIpv4PriorityRaw, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIpv4PriorityRawCounter
        """Factory property that returns an instance of the PatternFlowIpv4PriorityRawCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIpv4PriorityRawCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIpv4PriorityRawCounter
        """Factory property that returns an instance of the PatternFlowIpv4PriorityRawCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIpv4PriorityRawCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIpv4PriorityRawCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIpv4PriorityRawCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class FlowIpv4Tos(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'precedence': 'PatternFlowIpv4TosPrecedence',
        'delay': 'PatternFlowIpv4TosDelay',
        'throughput': 'PatternFlowIpv4TosThroughput',
        'reliability': 'PatternFlowIpv4TosReliability',
        'monetary': 'PatternFlowIpv4TosMonetary',
        'unused': 'PatternFlowIpv4TosUnused',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowIpv4Tos, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def precedence(self):
        # type: () -> PatternFlowIpv4TosPrecedence
        """precedence getter

        PrecedencePrecedence

        Returns: obj(snappi.PatternFlowIpv4TosPrecedence)
        """
        return self._get_property('precedence', PatternFlowIpv4TosPrecedence)

    @property
    def delay(self):
        # type: () -> PatternFlowIpv4TosDelay
        """delay getter

        DelayDelay

        Returns: obj(snappi.PatternFlowIpv4TosDelay)
        """
        return self._get_property('delay', PatternFlowIpv4TosDelay)

    @property
    def throughput(self):
        # type: () -> PatternFlowIpv4TosThroughput
        """throughput getter

        ThroughputThroughput

        Returns: obj(snappi.PatternFlowIpv4TosThroughput)
        """
        return self._get_property('throughput', PatternFlowIpv4TosThroughput)

    @property
    def reliability(self):
        # type: () -> PatternFlowIpv4TosReliability
        """reliability getter

        ReliabilityReliability

        Returns: obj(snappi.PatternFlowIpv4TosReliability)
        """
        return self._get_property('reliability', PatternFlowIpv4TosReliability)

    @property
    def monetary(self):
        # type: () -> PatternFlowIpv4TosMonetary
        """monetary getter

        MonetaryMonetary

        Returns: obj(snappi.PatternFlowIpv4TosMonetary)
        """
        return self._get_property('monetary', PatternFlowIpv4TosMonetary)

    @property
    def unused(self):
        # type: () -> PatternFlowIpv4TosUnused
        """unused getter

        UnusedUnused

        Returns: obj(snappi.PatternFlowIpv4TosUnused)
        """
        return self._get_property('unused', PatternFlowIpv4TosUnused)


class PatternFlowIpv4TosPrecedence(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIpv4TosPrecedenceCounter',
        'decrement': 'PatternFlowIpv4TosPrecedenceCounter',
    }

    ROUTINE = '0'
    PRIORITY = '1'
    IMMEDIATE = '2'
    FLASH = '3'
    FLASH_OVERRIDE = '4'
    CRITIC_ECP = '5'
    INTERNETWORK_CONTROL = '6'
    NETWORK_CONTROL = '7'

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIpv4TosPrecedence, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIpv4TosPrecedenceCounter
        """Factory property that returns an instance of the PatternFlowIpv4TosPrecedenceCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIpv4TosPrecedenceCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIpv4TosPrecedenceCounter
        """Factory property that returns an instance of the PatternFlowIpv4TosPrecedenceCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIpv4TosPrecedenceCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIpv4TosPrecedenceCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    ROUTINE = '0'
    PRIORITY = '1'
    IMMEDIATE = '2'
    FLASH = '3'
    FLASH_OVERRIDE = '4'
    CRITIC_ECP = '5'
    INTERNETWORK_CONTROL = '6'
    NETWORK_CONTROL = '7'

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIpv4TosPrecedenceCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIpv4TosDelay(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIpv4TosDelayCounter',
        'decrement': 'PatternFlowIpv4TosDelayCounter',
    }

    NORMAL = '0'
    LOW = '1'

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIpv4TosDelay, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIpv4TosDelayCounter
        """Factory property that returns an instance of the PatternFlowIpv4TosDelayCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIpv4TosDelayCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIpv4TosDelayCounter
        """Factory property that returns an instance of the PatternFlowIpv4TosDelayCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIpv4TosDelayCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIpv4TosDelayCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    NORMAL = '0'
    LOW = '1'

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIpv4TosDelayCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIpv4TosThroughput(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIpv4TosThroughputCounter',
        'decrement': 'PatternFlowIpv4TosThroughputCounter',
    }

    NORMAL = '0'
    LOW = '1'

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIpv4TosThroughput, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIpv4TosThroughputCounter
        """Factory property that returns an instance of the PatternFlowIpv4TosThroughputCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIpv4TosThroughputCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIpv4TosThroughputCounter
        """Factory property that returns an instance of the PatternFlowIpv4TosThroughputCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIpv4TosThroughputCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIpv4TosThroughputCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    NORMAL = '0'
    LOW = '1'

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIpv4TosThroughputCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIpv4TosReliability(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIpv4TosReliabilityCounter',
        'decrement': 'PatternFlowIpv4TosReliabilityCounter',
    }

    NORMAL = '0'
    LOW = '1'

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIpv4TosReliability, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIpv4TosReliabilityCounter
        """Factory property that returns an instance of the PatternFlowIpv4TosReliabilityCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIpv4TosReliabilityCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIpv4TosReliabilityCounter
        """Factory property that returns an instance of the PatternFlowIpv4TosReliabilityCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIpv4TosReliabilityCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIpv4TosReliabilityCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    NORMAL = '0'
    LOW = '1'

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIpv4TosReliabilityCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIpv4TosMonetary(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIpv4TosMonetaryCounter',
        'decrement': 'PatternFlowIpv4TosMonetaryCounter',
    }

    NORMAL = '0'
    LOW = '1'

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIpv4TosMonetary, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIpv4TosMonetaryCounter
        """Factory property that returns an instance of the PatternFlowIpv4TosMonetaryCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIpv4TosMonetaryCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIpv4TosMonetaryCounter
        """Factory property that returns an instance of the PatternFlowIpv4TosMonetaryCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIpv4TosMonetaryCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIpv4TosMonetaryCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    NORMAL = '0'
    LOW = '1'

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIpv4TosMonetaryCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIpv4TosUnused(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIpv4TosUnusedCounter',
        'decrement': 'PatternFlowIpv4TosUnusedCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIpv4TosUnused, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIpv4TosUnusedCounter
        """Factory property that returns an instance of the PatternFlowIpv4TosUnusedCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIpv4TosUnusedCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIpv4TosUnusedCounter
        """Factory property that returns an instance of the PatternFlowIpv4TosUnusedCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIpv4TosUnusedCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIpv4TosUnusedCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIpv4TosUnusedCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class FlowIpv4Dscp(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'phb': 'PatternFlowIpv4DscpPhb',
        'ecn': 'PatternFlowIpv4DscpEcn',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowIpv4Dscp, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def phb(self):
        # type: () -> PatternFlowIpv4DscpPhb
        """phb getter

        Per hop behaviorPer hop behavior

        Returns: obj(snappi.PatternFlowIpv4DscpPhb)
        """
        return self._get_property('phb', PatternFlowIpv4DscpPhb)

    @property
    def ecn(self):
        # type: () -> PatternFlowIpv4DscpEcn
        """ecn getter

        Explicit congestion notificationExplicit congestion notification

        Returns: obj(snappi.PatternFlowIpv4DscpEcn)
        """
        return self._get_property('ecn', PatternFlowIpv4DscpEcn)


class PatternFlowIpv4DscpPhb(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIpv4DscpPhbCounter',
        'decrement': 'PatternFlowIpv4DscpPhbCounter',
    }

    DEFAULT = '0'
    CS1 = '8'
    CS2 = '16'
    CS3 = '24'
    CS4 = '32'
    CS5 = '40'
    CS6 = '48'
    CS7 = '56'
    AF11 = '10'
    AF12 = '12'
    AF13 = '14'
    AF21 = '18'
    AF22 = '20'
    AF23 = '22'
    AF31 = '26'
    AF32 = '28'
    AF33 = '30'
    AF41 = '34'
    AF42 = '36'
    AF43 = '38'
    EF46 = '46'

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIpv4DscpPhb, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIpv4DscpPhbCounter
        """Factory property that returns an instance of the PatternFlowIpv4DscpPhbCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIpv4DscpPhbCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIpv4DscpPhbCounter
        """Factory property that returns an instance of the PatternFlowIpv4DscpPhbCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIpv4DscpPhbCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIpv4DscpPhbCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    DEFAULT = '0'
    CS1 = '8'
    CS2 = '16'
    CS3 = '24'
    CS4 = '32'
    CS5 = '40'
    CS6 = '48'
    CS7 = '56'
    AF11 = '10'
    AF12 = '12'
    AF13 = '14'
    AF21 = '18'
    AF22 = '20'
    AF23 = '22'
    AF31 = '26'
    AF32 = '28'
    AF33 = '30'
    AF41 = '34'
    AF42 = '36'
    AF43 = '38'
    EF46 = '46'

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIpv4DscpPhbCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIpv4DscpEcn(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIpv4DscpEcnCounter',
        'decrement': 'PatternFlowIpv4DscpEcnCounter',
    }

    NON_CAPABLE = '0'
    CAPABLE_TRANSPORT_0 = '1'
    CAPABLE_TRANSPORT_1 = '2'
    CONGESTION_ENCOUNTERED = '3'

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIpv4DscpEcn, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIpv4DscpEcnCounter
        """Factory property that returns an instance of the PatternFlowIpv4DscpEcnCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIpv4DscpEcnCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIpv4DscpEcnCounter
        """Factory property that returns an instance of the PatternFlowIpv4DscpEcnCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIpv4DscpEcnCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIpv4DscpEcnCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    NON_CAPABLE = '0'
    CAPABLE_TRANSPORT_0 = '1'
    CAPABLE_TRANSPORT_1 = '2'
    CONGESTION_ENCOUNTERED = '3'

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIpv4DscpEcnCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIpv4TotalLength(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIpv4TotalLengthCounter',
        'decrement': 'PatternFlowIpv4TotalLengthCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    AUTO = 'auto'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    AUTO = 'auto'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIpv4TotalLength, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIpv4TotalLengthCounter
        """Factory property that returns an instance of the PatternFlowIpv4TotalLengthCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIpv4TotalLengthCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIpv4TotalLengthCounter
        """Factory property that returns an instance of the PatternFlowIpv4TotalLengthCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIpv4TotalLengthCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, auto, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, auto, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, auto, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def auto(self):
        # type: () -> Union[auto]
        """auto getter

        TBD

        Returns: Union[auto]
        """
        return self._get_property('auto')

    @auto.setter
    def auto(self, value):
        """auto setter

        TBD

        value: Union[auto]
        """
        self._set_property('auto', value, 'auto')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIpv4TotalLengthCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIpv4TotalLengthCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIpv4Identification(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIpv4IdentificationCounter',
        'decrement': 'PatternFlowIpv4IdentificationCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIpv4Identification, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIpv4IdentificationCounter
        """Factory property that returns an instance of the PatternFlowIpv4IdentificationCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIpv4IdentificationCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIpv4IdentificationCounter
        """Factory property that returns an instance of the PatternFlowIpv4IdentificationCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIpv4IdentificationCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIpv4IdentificationCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIpv4IdentificationCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIpv4Reserved(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIpv4ReservedCounter',
        'decrement': 'PatternFlowIpv4ReservedCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIpv4Reserved, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIpv4ReservedCounter
        """Factory property that returns an instance of the PatternFlowIpv4ReservedCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIpv4ReservedCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIpv4ReservedCounter
        """Factory property that returns an instance of the PatternFlowIpv4ReservedCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIpv4ReservedCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIpv4ReservedCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIpv4ReservedCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIpv4DontFragment(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIpv4DontFragmentCounter',
        'decrement': 'PatternFlowIpv4DontFragmentCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIpv4DontFragment, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIpv4DontFragmentCounter
        """Factory property that returns an instance of the PatternFlowIpv4DontFragmentCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIpv4DontFragmentCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIpv4DontFragmentCounter
        """Factory property that returns an instance of the PatternFlowIpv4DontFragmentCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIpv4DontFragmentCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIpv4DontFragmentCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIpv4DontFragmentCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIpv4MoreFragments(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIpv4MoreFragmentsCounter',
        'decrement': 'PatternFlowIpv4MoreFragmentsCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIpv4MoreFragments, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIpv4MoreFragmentsCounter
        """Factory property that returns an instance of the PatternFlowIpv4MoreFragmentsCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIpv4MoreFragmentsCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIpv4MoreFragmentsCounter
        """Factory property that returns an instance of the PatternFlowIpv4MoreFragmentsCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIpv4MoreFragmentsCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIpv4MoreFragmentsCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIpv4MoreFragmentsCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIpv4FragmentOffset(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIpv4FragmentOffsetCounter',
        'decrement': 'PatternFlowIpv4FragmentOffsetCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIpv4FragmentOffset, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIpv4FragmentOffsetCounter
        """Factory property that returns an instance of the PatternFlowIpv4FragmentOffsetCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIpv4FragmentOffsetCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIpv4FragmentOffsetCounter
        """Factory property that returns an instance of the PatternFlowIpv4FragmentOffsetCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIpv4FragmentOffsetCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIpv4FragmentOffsetCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIpv4FragmentOffsetCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIpv4TimeToLive(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIpv4TimeToLiveCounter',
        'decrement': 'PatternFlowIpv4TimeToLiveCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIpv4TimeToLive, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIpv4TimeToLiveCounter
        """Factory property that returns an instance of the PatternFlowIpv4TimeToLiveCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIpv4TimeToLiveCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIpv4TimeToLiveCounter
        """Factory property that returns an instance of the PatternFlowIpv4TimeToLiveCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIpv4TimeToLiveCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIpv4TimeToLiveCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIpv4TimeToLiveCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIpv4Protocol(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIpv4ProtocolCounter',
        'decrement': 'PatternFlowIpv4ProtocolCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIpv4Protocol, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIpv4ProtocolCounter
        """Factory property that returns an instance of the PatternFlowIpv4ProtocolCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIpv4ProtocolCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIpv4ProtocolCounter
        """Factory property that returns an instance of the PatternFlowIpv4ProtocolCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIpv4ProtocolCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIpv4ProtocolCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIpv4ProtocolCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIpv4HeaderChecksum(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    GENERATED = 'generated'
    CUSTOM = 'custom'

    GOOD = 'good'
    BAD = 'bad'

    def __init__(self, parent=None, choice=None):
        super(PatternFlowIpv4HeaderChecksum, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def choice(self):
        # type: () -> Union[generated, custom, choice, choice, choice]
        """choice getter

        The type of checksum

        Returns: Union[generated, custom, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        The type of checksum

        value: Union[generated, custom, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def generated(self):
        # type: () -> Union[good, bad]
        """generated getter

        A system generated checksum value

        Returns: Union[good, bad]
        """
        return self._get_property('generated')

    @generated.setter
    def generated(self, value):
        """generated setter

        A system generated checksum value

        value: Union[good, bad]
        """
        self._set_property('generated', value, 'generated')

    @property
    def custom(self):
        # type: () -> int
        """custom getter

        A custom checksum value

        Returns: int
        """
        return self._get_property('custom')

    @custom.setter
    def custom(self, value):
        """custom setter

        A custom checksum value

        value: int
        """
        self._set_property('custom', value, 'custom')


class PatternFlowIpv4Src(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIpv4SrcCounter',
        'decrement': 'PatternFlowIpv4SrcCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIpv4Src, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIpv4SrcCounter
        """Factory property that returns an instance of the PatternFlowIpv4SrcCounter class

        ipv4 counter pattern
        """
        return self._get_property('increment', PatternFlowIpv4SrcCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIpv4SrcCounter
        """Factory property that returns an instance of the PatternFlowIpv4SrcCounter class

        ipv4 counter pattern
        """
        return self._get_property('decrement', PatternFlowIpv4SrcCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> str
        """value getter

        TBD

        Returns: str
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: str
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[str]
        """values getter

        TBD

        Returns: list[str]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[str]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIpv4SrcCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIpv4SrcCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> str
        """start getter

        TBD

        Returns: str
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: str
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> str
        """step getter

        TBD

        Returns: str
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: str
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIpv4Dst(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIpv4DstCounter',
        'decrement': 'PatternFlowIpv4DstCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIpv4Dst, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIpv4DstCounter
        """Factory property that returns an instance of the PatternFlowIpv4DstCounter class

        ipv4 counter pattern
        """
        return self._get_property('increment', PatternFlowIpv4DstCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIpv4DstCounter
        """Factory property that returns an instance of the PatternFlowIpv4DstCounter class

        ipv4 counter pattern
        """
        return self._get_property('decrement', PatternFlowIpv4DstCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> str
        """value getter

        TBD

        Returns: str
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: str
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[str]
        """values getter

        TBD

        Returns: list[str]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[str]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIpv4DstCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIpv4DstCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> str
        """start getter

        TBD

        Returns: str
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: str
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> str
        """step getter

        TBD

        Returns: str
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: str
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class FlowIpv6(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'version': 'PatternFlowIpv6Version',
        'traffic_class': 'PatternFlowIpv6TrafficClass',
        'flow_label': 'PatternFlowIpv6FlowLabel',
        'payload_length': 'PatternFlowIpv6PayloadLength',
        'next_header': 'PatternFlowIpv6NextHeader',
        'hop_limit': 'PatternFlowIpv6HopLimit',
        'src': 'PatternFlowIpv6Src',
        'dst': 'PatternFlowIpv6Dst',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowIpv6, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def version(self):
        # type: () -> PatternFlowIpv6Version
        """version getter

        Version numberVersion number

        Returns: obj(snappi.PatternFlowIpv6Version)
        """
        return self._get_property('version', PatternFlowIpv6Version)

    @property
    def traffic_class(self):
        # type: () -> PatternFlowIpv6TrafficClass
        """traffic_class getter

        Traffic classTraffic class

        Returns: obj(snappi.PatternFlowIpv6TrafficClass)
        """
        return self._get_property('traffic_class', PatternFlowIpv6TrafficClass)

    @property
    def flow_label(self):
        # type: () -> PatternFlowIpv6FlowLabel
        """flow_label getter

        Flow labelFlow label

        Returns: obj(snappi.PatternFlowIpv6FlowLabel)
        """
        return self._get_property('flow_label', PatternFlowIpv6FlowLabel)

    @property
    def payload_length(self):
        # type: () -> PatternFlowIpv6PayloadLength
        """payload_length getter

        Payload lengthPayload length

        Returns: obj(snappi.PatternFlowIpv6PayloadLength)
        """
        return self._get_property('payload_length', PatternFlowIpv6PayloadLength)

    @property
    def next_header(self):
        # type: () -> PatternFlowIpv6NextHeader
        """next_header getter

        Next headerNext header

        Returns: obj(snappi.PatternFlowIpv6NextHeader)
        """
        return self._get_property('next_header', PatternFlowIpv6NextHeader)

    @property
    def hop_limit(self):
        # type: () -> PatternFlowIpv6HopLimit
        """hop_limit getter

        Hop limitHop limit

        Returns: obj(snappi.PatternFlowIpv6HopLimit)
        """
        return self._get_property('hop_limit', PatternFlowIpv6HopLimit)

    @property
    def src(self):
        # type: () -> PatternFlowIpv6Src
        """src getter

        Source addressSource address

        Returns: obj(snappi.PatternFlowIpv6Src)
        """
        return self._get_property('src', PatternFlowIpv6Src)

    @property
    def dst(self):
        # type: () -> PatternFlowIpv6Dst
        """dst getter

        Destination addressDestination address

        Returns: obj(snappi.PatternFlowIpv6Dst)
        """
        return self._get_property('dst', PatternFlowIpv6Dst)


class PatternFlowIpv6Version(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIpv6VersionCounter',
        'decrement': 'PatternFlowIpv6VersionCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIpv6Version, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIpv6VersionCounter
        """Factory property that returns an instance of the PatternFlowIpv6VersionCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIpv6VersionCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIpv6VersionCounter
        """Factory property that returns an instance of the PatternFlowIpv6VersionCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIpv6VersionCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIpv6VersionCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIpv6VersionCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIpv6TrafficClass(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIpv6TrafficClassCounter',
        'decrement': 'PatternFlowIpv6TrafficClassCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIpv6TrafficClass, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIpv6TrafficClassCounter
        """Factory property that returns an instance of the PatternFlowIpv6TrafficClassCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIpv6TrafficClassCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIpv6TrafficClassCounter
        """Factory property that returns an instance of the PatternFlowIpv6TrafficClassCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIpv6TrafficClassCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIpv6TrafficClassCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIpv6TrafficClassCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIpv6FlowLabel(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIpv6FlowLabelCounter',
        'decrement': 'PatternFlowIpv6FlowLabelCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIpv6FlowLabel, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIpv6FlowLabelCounter
        """Factory property that returns an instance of the PatternFlowIpv6FlowLabelCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIpv6FlowLabelCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIpv6FlowLabelCounter
        """Factory property that returns an instance of the PatternFlowIpv6FlowLabelCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIpv6FlowLabelCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIpv6FlowLabelCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIpv6FlowLabelCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIpv6PayloadLength(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIpv6PayloadLengthCounter',
        'decrement': 'PatternFlowIpv6PayloadLengthCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    AUTO = 'auto'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    AUTO = 'auto'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIpv6PayloadLength, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIpv6PayloadLengthCounter
        """Factory property that returns an instance of the PatternFlowIpv6PayloadLengthCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIpv6PayloadLengthCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIpv6PayloadLengthCounter
        """Factory property that returns an instance of the PatternFlowIpv6PayloadLengthCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIpv6PayloadLengthCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, auto, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, auto, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, auto, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def auto(self):
        # type: () -> Union[auto]
        """auto getter

        TBD

        Returns: Union[auto]
        """
        return self._get_property('auto')

    @auto.setter
    def auto(self, value):
        """auto setter

        TBD

        value: Union[auto]
        """
        self._set_property('auto', value, 'auto')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIpv6PayloadLengthCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIpv6PayloadLengthCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIpv6NextHeader(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIpv6NextHeaderCounter',
        'decrement': 'PatternFlowIpv6NextHeaderCounter',
    }

    HOPOPT = '0'
    ICMP = '1'
    IGMP = '2'
    GGP = '3'
    IP_IN_IP = '4'
    ST = '5'
    TCP = '6'
    CPT = '7'
    EGP = '8'
    IGP = '9'
    NO_NEXT_HEADER = '59'

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIpv6NextHeader, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIpv6NextHeaderCounter
        """Factory property that returns an instance of the PatternFlowIpv6NextHeaderCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIpv6NextHeaderCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIpv6NextHeaderCounter
        """Factory property that returns an instance of the PatternFlowIpv6NextHeaderCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIpv6NextHeaderCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIpv6NextHeaderCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    HOPOPT = '0'
    ICMP = '1'
    IGMP = '2'
    GGP = '3'
    IP_IN_IP = '4'
    ST = '5'
    TCP = '6'
    CPT = '7'
    EGP = '8'
    IGP = '9'
    NO_NEXT_HEADER = '59'

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIpv6NextHeaderCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIpv6HopLimit(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIpv6HopLimitCounter',
        'decrement': 'PatternFlowIpv6HopLimitCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIpv6HopLimit, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIpv6HopLimitCounter
        """Factory property that returns an instance of the PatternFlowIpv6HopLimitCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIpv6HopLimitCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIpv6HopLimitCounter
        """Factory property that returns an instance of the PatternFlowIpv6HopLimitCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIpv6HopLimitCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIpv6HopLimitCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIpv6HopLimitCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIpv6Src(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIpv6SrcCounter',
        'decrement': 'PatternFlowIpv6SrcCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIpv6Src, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIpv6SrcCounter
        """Factory property that returns an instance of the PatternFlowIpv6SrcCounter class

        ipv6 counter pattern
        """
        return self._get_property('increment', PatternFlowIpv6SrcCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIpv6SrcCounter
        """Factory property that returns an instance of the PatternFlowIpv6SrcCounter class

        ipv6 counter pattern
        """
        return self._get_property('decrement', PatternFlowIpv6SrcCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> str
        """value getter

        TBD

        Returns: str
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: str
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[str]
        """values getter

        TBD

        Returns: list[str]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[str]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIpv6SrcCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIpv6SrcCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> str
        """start getter

        TBD

        Returns: str
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: str
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> str
        """step getter

        TBD

        Returns: str
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: str
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIpv6Dst(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIpv6DstCounter',
        'decrement': 'PatternFlowIpv6DstCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIpv6Dst, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIpv6DstCounter
        """Factory property that returns an instance of the PatternFlowIpv6DstCounter class

        ipv6 counter pattern
        """
        return self._get_property('increment', PatternFlowIpv6DstCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIpv6DstCounter
        """Factory property that returns an instance of the PatternFlowIpv6DstCounter class

        ipv6 counter pattern
        """
        return self._get_property('decrement', PatternFlowIpv6DstCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> str
        """value getter

        TBD

        Returns: str
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: str
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[str]
        """values getter

        TBD

        Returns: list[str]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[str]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIpv6DstCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIpv6DstCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> str
        """start getter

        TBD

        Returns: str
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: str
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> str
        """step getter

        TBD

        Returns: str
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: str
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class FlowPfcPause(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'dst': 'PatternFlowPfcPauseDst',
        'src': 'PatternFlowPfcPauseSrc',
        'ether_type': 'PatternFlowPfcPauseEtherType',
        'control_op_code': 'PatternFlowPfcPauseControlOpCode',
        'class_enable_vector': 'PatternFlowPfcPauseClassEnableVector',
        'pause_class_0': 'PatternFlowPfcPausePauseClass0',
        'pause_class_1': 'PatternFlowPfcPausePauseClass1',
        'pause_class_2': 'PatternFlowPfcPausePauseClass2',
        'pause_class_3': 'PatternFlowPfcPausePauseClass3',
        'pause_class_4': 'PatternFlowPfcPausePauseClass4',
        'pause_class_5': 'PatternFlowPfcPausePauseClass5',
        'pause_class_6': 'PatternFlowPfcPausePauseClass6',
        'pause_class_7': 'PatternFlowPfcPausePauseClass7',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowPfcPause, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def dst(self):
        # type: () -> PatternFlowPfcPauseDst
        """dst getter

        Destination MAC addressDestination MAC address

        Returns: obj(snappi.PatternFlowPfcPauseDst)
        """
        return self._get_property('dst', PatternFlowPfcPauseDst)

    @property
    def src(self):
        # type: () -> PatternFlowPfcPauseSrc
        """src getter

        Source MAC addressSource MAC address

        Returns: obj(snappi.PatternFlowPfcPauseSrc)
        """
        return self._get_property('src', PatternFlowPfcPauseSrc)

    @property
    def ether_type(self):
        # type: () -> PatternFlowPfcPauseEtherType
        """ether_type getter

        Ethernet typeEthernet type

        Returns: obj(snappi.PatternFlowPfcPauseEtherType)
        """
        return self._get_property('ether_type', PatternFlowPfcPauseEtherType)

    @property
    def control_op_code(self):
        # type: () -> PatternFlowPfcPauseControlOpCode
        """control_op_code getter

        Control operation codeControl operation code

        Returns: obj(snappi.PatternFlowPfcPauseControlOpCode)
        """
        return self._get_property('control_op_code', PatternFlowPfcPauseControlOpCode)

    @property
    def class_enable_vector(self):
        # type: () -> PatternFlowPfcPauseClassEnableVector
        """class_enable_vector getter

        DestinationDestination

        Returns: obj(snappi.PatternFlowPfcPauseClassEnableVector)
        """
        return self._get_property('class_enable_vector', PatternFlowPfcPauseClassEnableVector)

    @property
    def pause_class_0(self):
        # type: () -> PatternFlowPfcPausePauseClass0
        """pause_class_0 getter

        Pause class 0Pause class 0

        Returns: obj(snappi.PatternFlowPfcPausePauseClass0)
        """
        return self._get_property('pause_class_0', PatternFlowPfcPausePauseClass0)

    @property
    def pause_class_1(self):
        # type: () -> PatternFlowPfcPausePauseClass1
        """pause_class_1 getter

        Pause class 1Pause class 1

        Returns: obj(snappi.PatternFlowPfcPausePauseClass1)
        """
        return self._get_property('pause_class_1', PatternFlowPfcPausePauseClass1)

    @property
    def pause_class_2(self):
        # type: () -> PatternFlowPfcPausePauseClass2
        """pause_class_2 getter

        Pause class 2Pause class 2

        Returns: obj(snappi.PatternFlowPfcPausePauseClass2)
        """
        return self._get_property('pause_class_2', PatternFlowPfcPausePauseClass2)

    @property
    def pause_class_3(self):
        # type: () -> PatternFlowPfcPausePauseClass3
        """pause_class_3 getter

        Pause class 3Pause class 3

        Returns: obj(snappi.PatternFlowPfcPausePauseClass3)
        """
        return self._get_property('pause_class_3', PatternFlowPfcPausePauseClass3)

    @property
    def pause_class_4(self):
        # type: () -> PatternFlowPfcPausePauseClass4
        """pause_class_4 getter

        Pause class 4Pause class 4

        Returns: obj(snappi.PatternFlowPfcPausePauseClass4)
        """
        return self._get_property('pause_class_4', PatternFlowPfcPausePauseClass4)

    @property
    def pause_class_5(self):
        # type: () -> PatternFlowPfcPausePauseClass5
        """pause_class_5 getter

        Pause class 5Pause class 5

        Returns: obj(snappi.PatternFlowPfcPausePauseClass5)
        """
        return self._get_property('pause_class_5', PatternFlowPfcPausePauseClass5)

    @property
    def pause_class_6(self):
        # type: () -> PatternFlowPfcPausePauseClass6
        """pause_class_6 getter

        Pause class 6Pause class 6

        Returns: obj(snappi.PatternFlowPfcPausePauseClass6)
        """
        return self._get_property('pause_class_6', PatternFlowPfcPausePauseClass6)

    @property
    def pause_class_7(self):
        # type: () -> PatternFlowPfcPausePauseClass7
        """pause_class_7 getter

        Pause class 7Pause class 7

        Returns: obj(snappi.PatternFlowPfcPausePauseClass7)
        """
        return self._get_property('pause_class_7', PatternFlowPfcPausePauseClass7)


class PatternFlowPfcPauseDst(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowPfcPauseDstCounter',
        'decrement': 'PatternFlowPfcPauseDstCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowPfcPauseDst, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowPfcPauseDstCounter
        """Factory property that returns an instance of the PatternFlowPfcPauseDstCounter class

        mac counter pattern
        """
        return self._get_property('increment', PatternFlowPfcPauseDstCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowPfcPauseDstCounter
        """Factory property that returns an instance of the PatternFlowPfcPauseDstCounter class

        mac counter pattern
        """
        return self._get_property('decrement', PatternFlowPfcPauseDstCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> str
        """value getter

        TBD

        Returns: str
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: str
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[str]
        """values getter

        TBD

        Returns: list[str]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[str]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowPfcPauseDstCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowPfcPauseDstCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> str
        """start getter

        TBD

        Returns: str
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: str
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> str
        """step getter

        TBD

        Returns: str
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: str
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowPfcPauseSrc(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowPfcPauseSrcCounter',
        'decrement': 'PatternFlowPfcPauseSrcCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowPfcPauseSrc, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowPfcPauseSrcCounter
        """Factory property that returns an instance of the PatternFlowPfcPauseSrcCounter class

        mac counter pattern
        """
        return self._get_property('increment', PatternFlowPfcPauseSrcCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowPfcPauseSrcCounter
        """Factory property that returns an instance of the PatternFlowPfcPauseSrcCounter class

        mac counter pattern
        """
        return self._get_property('decrement', PatternFlowPfcPauseSrcCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> str
        """value getter

        TBD

        Returns: str
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: str
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[str]
        """values getter

        TBD

        Returns: list[str]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[str]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowPfcPauseSrcCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowPfcPauseSrcCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> str
        """start getter

        TBD

        Returns: str
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: str
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> str
        """step getter

        TBD

        Returns: str
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: str
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowPfcPauseEtherType(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowPfcPauseEtherTypeCounter',
        'decrement': 'PatternFlowPfcPauseEtherTypeCounter',
    }

    X8808 = '34824'

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowPfcPauseEtherType, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowPfcPauseEtherTypeCounter
        """Factory property that returns an instance of the PatternFlowPfcPauseEtherTypeCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowPfcPauseEtherTypeCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowPfcPauseEtherTypeCounter
        """Factory property that returns an instance of the PatternFlowPfcPauseEtherTypeCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowPfcPauseEtherTypeCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowPfcPauseEtherTypeCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    X8808 = '34824'

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowPfcPauseEtherTypeCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowPfcPauseControlOpCode(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowPfcPauseControlOpCodeCounter',
        'decrement': 'PatternFlowPfcPauseControlOpCodeCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowPfcPauseControlOpCode, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowPfcPauseControlOpCodeCounter
        """Factory property that returns an instance of the PatternFlowPfcPauseControlOpCodeCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowPfcPauseControlOpCodeCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowPfcPauseControlOpCodeCounter
        """Factory property that returns an instance of the PatternFlowPfcPauseControlOpCodeCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowPfcPauseControlOpCodeCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowPfcPauseControlOpCodeCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowPfcPauseControlOpCodeCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowPfcPauseClassEnableVector(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowPfcPauseClassEnableVectorCounter',
        'decrement': 'PatternFlowPfcPauseClassEnableVectorCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowPfcPauseClassEnableVector, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowPfcPauseClassEnableVectorCounter
        """Factory property that returns an instance of the PatternFlowPfcPauseClassEnableVectorCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowPfcPauseClassEnableVectorCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowPfcPauseClassEnableVectorCounter
        """Factory property that returns an instance of the PatternFlowPfcPauseClassEnableVectorCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowPfcPauseClassEnableVectorCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowPfcPauseClassEnableVectorCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowPfcPauseClassEnableVectorCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowPfcPausePauseClass0(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowPfcPausePauseClass0Counter',
        'decrement': 'PatternFlowPfcPausePauseClass0Counter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowPfcPausePauseClass0, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowPfcPausePauseClass0Counter
        """Factory property that returns an instance of the PatternFlowPfcPausePauseClass0Counter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowPfcPausePauseClass0Counter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowPfcPausePauseClass0Counter
        """Factory property that returns an instance of the PatternFlowPfcPausePauseClass0Counter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowPfcPausePauseClass0Counter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowPfcPausePauseClass0Counter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowPfcPausePauseClass0Counter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowPfcPausePauseClass1(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowPfcPausePauseClass1Counter',
        'decrement': 'PatternFlowPfcPausePauseClass1Counter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowPfcPausePauseClass1, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowPfcPausePauseClass1Counter
        """Factory property that returns an instance of the PatternFlowPfcPausePauseClass1Counter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowPfcPausePauseClass1Counter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowPfcPausePauseClass1Counter
        """Factory property that returns an instance of the PatternFlowPfcPausePauseClass1Counter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowPfcPausePauseClass1Counter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowPfcPausePauseClass1Counter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowPfcPausePauseClass1Counter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowPfcPausePauseClass2(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowPfcPausePauseClass2Counter',
        'decrement': 'PatternFlowPfcPausePauseClass2Counter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowPfcPausePauseClass2, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowPfcPausePauseClass2Counter
        """Factory property that returns an instance of the PatternFlowPfcPausePauseClass2Counter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowPfcPausePauseClass2Counter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowPfcPausePauseClass2Counter
        """Factory property that returns an instance of the PatternFlowPfcPausePauseClass2Counter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowPfcPausePauseClass2Counter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowPfcPausePauseClass2Counter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowPfcPausePauseClass2Counter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowPfcPausePauseClass3(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowPfcPausePauseClass3Counter',
        'decrement': 'PatternFlowPfcPausePauseClass3Counter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowPfcPausePauseClass3, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowPfcPausePauseClass3Counter
        """Factory property that returns an instance of the PatternFlowPfcPausePauseClass3Counter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowPfcPausePauseClass3Counter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowPfcPausePauseClass3Counter
        """Factory property that returns an instance of the PatternFlowPfcPausePauseClass3Counter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowPfcPausePauseClass3Counter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowPfcPausePauseClass3Counter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowPfcPausePauseClass3Counter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowPfcPausePauseClass4(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowPfcPausePauseClass4Counter',
        'decrement': 'PatternFlowPfcPausePauseClass4Counter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowPfcPausePauseClass4, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowPfcPausePauseClass4Counter
        """Factory property that returns an instance of the PatternFlowPfcPausePauseClass4Counter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowPfcPausePauseClass4Counter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowPfcPausePauseClass4Counter
        """Factory property that returns an instance of the PatternFlowPfcPausePauseClass4Counter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowPfcPausePauseClass4Counter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowPfcPausePauseClass4Counter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowPfcPausePauseClass4Counter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowPfcPausePauseClass5(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowPfcPausePauseClass5Counter',
        'decrement': 'PatternFlowPfcPausePauseClass5Counter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowPfcPausePauseClass5, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowPfcPausePauseClass5Counter
        """Factory property that returns an instance of the PatternFlowPfcPausePauseClass5Counter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowPfcPausePauseClass5Counter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowPfcPausePauseClass5Counter
        """Factory property that returns an instance of the PatternFlowPfcPausePauseClass5Counter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowPfcPausePauseClass5Counter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowPfcPausePauseClass5Counter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowPfcPausePauseClass5Counter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowPfcPausePauseClass6(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowPfcPausePauseClass6Counter',
        'decrement': 'PatternFlowPfcPausePauseClass6Counter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowPfcPausePauseClass6, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowPfcPausePauseClass6Counter
        """Factory property that returns an instance of the PatternFlowPfcPausePauseClass6Counter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowPfcPausePauseClass6Counter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowPfcPausePauseClass6Counter
        """Factory property that returns an instance of the PatternFlowPfcPausePauseClass6Counter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowPfcPausePauseClass6Counter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowPfcPausePauseClass6Counter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowPfcPausePauseClass6Counter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowPfcPausePauseClass7(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowPfcPausePauseClass7Counter',
        'decrement': 'PatternFlowPfcPausePauseClass7Counter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowPfcPausePauseClass7, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowPfcPausePauseClass7Counter
        """Factory property that returns an instance of the PatternFlowPfcPausePauseClass7Counter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowPfcPausePauseClass7Counter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowPfcPausePauseClass7Counter
        """Factory property that returns an instance of the PatternFlowPfcPausePauseClass7Counter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowPfcPausePauseClass7Counter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowPfcPausePauseClass7Counter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowPfcPausePauseClass7Counter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class FlowEthernetPause(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'dst': 'PatternFlowEthernetPauseDst',
        'src': 'PatternFlowEthernetPauseSrc',
        'ether_type': 'PatternFlowEthernetPauseEtherType',
        'control_op_code': 'PatternFlowEthernetPauseControlOpCode',
        'time': 'PatternFlowEthernetPauseTime',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowEthernetPause, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def dst(self):
        # type: () -> PatternFlowEthernetPauseDst
        """dst getter

        Destination MAC addressDestination MAC address

        Returns: obj(snappi.PatternFlowEthernetPauseDst)
        """
        return self._get_property('dst', PatternFlowEthernetPauseDst)

    @property
    def src(self):
        # type: () -> PatternFlowEthernetPauseSrc
        """src getter

        Source MAC addressSource MAC address

        Returns: obj(snappi.PatternFlowEthernetPauseSrc)
        """
        return self._get_property('src', PatternFlowEthernetPauseSrc)

    @property
    def ether_type(self):
        # type: () -> PatternFlowEthernetPauseEtherType
        """ether_type getter

        Ethernet typeEthernet type

        Returns: obj(snappi.PatternFlowEthernetPauseEtherType)
        """
        return self._get_property('ether_type', PatternFlowEthernetPauseEtherType)

    @property
    def control_op_code(self):
        # type: () -> PatternFlowEthernetPauseControlOpCode
        """control_op_code getter

        Control operation codeControl operation code

        Returns: obj(snappi.PatternFlowEthernetPauseControlOpCode)
        """
        return self._get_property('control_op_code', PatternFlowEthernetPauseControlOpCode)

    @property
    def time(self):
        # type: () -> PatternFlowEthernetPauseTime
        """time getter

        TimeTime

        Returns: obj(snappi.PatternFlowEthernetPauseTime)
        """
        return self._get_property('time', PatternFlowEthernetPauseTime)


class PatternFlowEthernetPauseDst(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowEthernetPauseDstCounter',
        'decrement': 'PatternFlowEthernetPauseDstCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowEthernetPauseDst, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowEthernetPauseDstCounter
        """Factory property that returns an instance of the PatternFlowEthernetPauseDstCounter class

        mac counter pattern
        """
        return self._get_property('increment', PatternFlowEthernetPauseDstCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowEthernetPauseDstCounter
        """Factory property that returns an instance of the PatternFlowEthernetPauseDstCounter class

        mac counter pattern
        """
        return self._get_property('decrement', PatternFlowEthernetPauseDstCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> str
        """value getter

        TBD

        Returns: str
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: str
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[str]
        """values getter

        TBD

        Returns: list[str]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[str]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowEthernetPauseDstCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowEthernetPauseDstCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> str
        """start getter

        TBD

        Returns: str
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: str
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> str
        """step getter

        TBD

        Returns: str
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: str
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowEthernetPauseSrc(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowEthernetPauseSrcCounter',
        'decrement': 'PatternFlowEthernetPauseSrcCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowEthernetPauseSrc, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowEthernetPauseSrcCounter
        """Factory property that returns an instance of the PatternFlowEthernetPauseSrcCounter class

        mac counter pattern
        """
        return self._get_property('increment', PatternFlowEthernetPauseSrcCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowEthernetPauseSrcCounter
        """Factory property that returns an instance of the PatternFlowEthernetPauseSrcCounter class

        mac counter pattern
        """
        return self._get_property('decrement', PatternFlowEthernetPauseSrcCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> str
        """value getter

        TBD

        Returns: str
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: str
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[str]
        """values getter

        TBD

        Returns: list[str]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[str]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowEthernetPauseSrcCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowEthernetPauseSrcCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> str
        """start getter

        TBD

        Returns: str
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: str
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> str
        """step getter

        TBD

        Returns: str
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: str
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowEthernetPauseEtherType(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowEthernetPauseEtherTypeCounter',
        'decrement': 'PatternFlowEthernetPauseEtherTypeCounter',
    }

    FLOW_CONTROL = '34824'

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowEthernetPauseEtherType, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowEthernetPauseEtherTypeCounter
        """Factory property that returns an instance of the PatternFlowEthernetPauseEtherTypeCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowEthernetPauseEtherTypeCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowEthernetPauseEtherTypeCounter
        """Factory property that returns an instance of the PatternFlowEthernetPauseEtherTypeCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowEthernetPauseEtherTypeCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowEthernetPauseEtherTypeCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    FLOW_CONTROL = '34824'

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowEthernetPauseEtherTypeCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowEthernetPauseControlOpCode(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowEthernetPauseControlOpCodeCounter',
        'decrement': 'PatternFlowEthernetPauseControlOpCodeCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowEthernetPauseControlOpCode, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowEthernetPauseControlOpCodeCounter
        """Factory property that returns an instance of the PatternFlowEthernetPauseControlOpCodeCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowEthernetPauseControlOpCodeCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowEthernetPauseControlOpCodeCounter
        """Factory property that returns an instance of the PatternFlowEthernetPauseControlOpCodeCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowEthernetPauseControlOpCodeCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowEthernetPauseControlOpCodeCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowEthernetPauseControlOpCodeCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowEthernetPauseTime(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowEthernetPauseTimeCounter',
        'decrement': 'PatternFlowEthernetPauseTimeCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowEthernetPauseTime, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowEthernetPauseTimeCounter
        """Factory property that returns an instance of the PatternFlowEthernetPauseTimeCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowEthernetPauseTimeCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowEthernetPauseTimeCounter
        """Factory property that returns an instance of the PatternFlowEthernetPauseTimeCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowEthernetPauseTimeCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowEthernetPauseTimeCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowEthernetPauseTimeCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class FlowTcp(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'src_port': 'PatternFlowTcpSrcPort',
        'dst_port': 'PatternFlowTcpDstPort',
        'seq_num': 'PatternFlowTcpSeqNum',
        'ack_num': 'PatternFlowTcpAckNum',
        'data_offset': 'PatternFlowTcpDataOffset',
        'ecn_ns': 'PatternFlowTcpEcnNs',
        'ecn_cwr': 'PatternFlowTcpEcnCwr',
        'ecn_echo': 'PatternFlowTcpEcnEcho',
        'ctl_urg': 'PatternFlowTcpCtlUrg',
        'ctl_ack': 'PatternFlowTcpCtlAck',
        'ctl_psh': 'PatternFlowTcpCtlPsh',
        'ctl_rst': 'PatternFlowTcpCtlRst',
        'ctl_syn': 'PatternFlowTcpCtlSyn',
        'ctl_fin': 'PatternFlowTcpCtlFin',
        'window': 'PatternFlowTcpWindow',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowTcp, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def src_port(self):
        # type: () -> PatternFlowTcpSrcPort
        """src_port getter

        Source portSource port

        Returns: obj(snappi.PatternFlowTcpSrcPort)
        """
        return self._get_property('src_port', PatternFlowTcpSrcPort)

    @property
    def dst_port(self):
        # type: () -> PatternFlowTcpDstPort
        """dst_port getter

        Destination portDestination port

        Returns: obj(snappi.PatternFlowTcpDstPort)
        """
        return self._get_property('dst_port', PatternFlowTcpDstPort)

    @property
    def seq_num(self):
        # type: () -> PatternFlowTcpSeqNum
        """seq_num getter

        Sequence numberSequence number

        Returns: obj(snappi.PatternFlowTcpSeqNum)
        """
        return self._get_property('seq_num', PatternFlowTcpSeqNum)

    @property
    def ack_num(self):
        # type: () -> PatternFlowTcpAckNum
        """ack_num getter

        Acknowledgement numberAcknowledgement number

        Returns: obj(snappi.PatternFlowTcpAckNum)
        """
        return self._get_property('ack_num', PatternFlowTcpAckNum)

    @property
    def data_offset(self):
        # type: () -> PatternFlowTcpDataOffset
        """data_offset getter

        The number of 32 bit words in the TCP header. This indicates where the data begins.The number of 32 bit words in the TCP header. This indicates where the data begins.

        Returns: obj(snappi.PatternFlowTcpDataOffset)
        """
        return self._get_property('data_offset', PatternFlowTcpDataOffset)

    @property
    def ecn_ns(self):
        # type: () -> PatternFlowTcpEcnNs
        """ecn_ns getter

        Explicit congestion notification, concealment protection.Explicit congestion notification, concealment protection.

        Returns: obj(snappi.PatternFlowTcpEcnNs)
        """
        return self._get_property('ecn_ns', PatternFlowTcpEcnNs)

    @property
    def ecn_cwr(self):
        # type: () -> PatternFlowTcpEcnCwr
        """ecn_cwr getter

        Explicit congestion notification, congestion window reduced.Explicit congestion notification, congestion window reduced.

        Returns: obj(snappi.PatternFlowTcpEcnCwr)
        """
        return self._get_property('ecn_cwr', PatternFlowTcpEcnCwr)

    @property
    def ecn_echo(self):
        # type: () -> PatternFlowTcpEcnEcho
        """ecn_echo getter

        Explicit congestion notification, echo. 1 indicates the peer is ecn capable. 0 indicates that a packet with ipv4.ecn = 11 in the ip header was received during normal transmission.Explicit congestion notification, echo. 1 indicates the peer is ecn capable. 0 indicates that a packet with ipv4.ecn = 11 in the ip header was received during normal transmission.

        Returns: obj(snappi.PatternFlowTcpEcnEcho)
        """
        return self._get_property('ecn_echo', PatternFlowTcpEcnEcho)

    @property
    def ctl_urg(self):
        # type: () -> PatternFlowTcpCtlUrg
        """ctl_urg getter

        A value of 1 indicates that the urgent pointer field is significant.A value of 1 indicates that the urgent pointer field is significant.

        Returns: obj(snappi.PatternFlowTcpCtlUrg)
        """
        return self._get_property('ctl_urg', PatternFlowTcpCtlUrg)

    @property
    def ctl_ack(self):
        # type: () -> PatternFlowTcpCtlAck
        """ctl_ack getter

        A value of 1 indicates that the ackknowledgment field is significant.A value of 1 indicates that the ackknowledgment field is significant.

        Returns: obj(snappi.PatternFlowTcpCtlAck)
        """
        return self._get_property('ctl_ack', PatternFlowTcpCtlAck)

    @property
    def ctl_psh(self):
        # type: () -> PatternFlowTcpCtlPsh
        """ctl_psh getter

        Asks to push the buffered data to the receiving application. Asks to push the buffered data to the receiving application. 

        Returns: obj(snappi.PatternFlowTcpCtlPsh)
        """
        return self._get_property('ctl_psh', PatternFlowTcpCtlPsh)

    @property
    def ctl_rst(self):
        # type: () -> PatternFlowTcpCtlRst
        """ctl_rst getter

        Reset the connection. Reset the connection. 

        Returns: obj(snappi.PatternFlowTcpCtlRst)
        """
        return self._get_property('ctl_rst', PatternFlowTcpCtlRst)

    @property
    def ctl_syn(self):
        # type: () -> PatternFlowTcpCtlSyn
        """ctl_syn getter

        Synchronize sequenece numbers. Synchronize sequenece numbers. 

        Returns: obj(snappi.PatternFlowTcpCtlSyn)
        """
        return self._get_property('ctl_syn', PatternFlowTcpCtlSyn)

    @property
    def ctl_fin(self):
        # type: () -> PatternFlowTcpCtlFin
        """ctl_fin getter

        Last packet from the sender. Last packet from the sender. 

        Returns: obj(snappi.PatternFlowTcpCtlFin)
        """
        return self._get_property('ctl_fin', PatternFlowTcpCtlFin)

    @property
    def window(self):
        # type: () -> PatternFlowTcpWindow
        """window getter

        Tcp connection window.Tcp connection window.

        Returns: obj(snappi.PatternFlowTcpWindow)
        """
        return self._get_property('window', PatternFlowTcpWindow)


class PatternFlowTcpSrcPort(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowTcpSrcPortCounter',
        'decrement': 'PatternFlowTcpSrcPortCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowTcpSrcPort, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowTcpSrcPortCounter
        """Factory property that returns an instance of the PatternFlowTcpSrcPortCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowTcpSrcPortCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowTcpSrcPortCounter
        """Factory property that returns an instance of the PatternFlowTcpSrcPortCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowTcpSrcPortCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowTcpSrcPortCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowTcpSrcPortCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowTcpDstPort(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowTcpDstPortCounter',
        'decrement': 'PatternFlowTcpDstPortCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowTcpDstPort, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowTcpDstPortCounter
        """Factory property that returns an instance of the PatternFlowTcpDstPortCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowTcpDstPortCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowTcpDstPortCounter
        """Factory property that returns an instance of the PatternFlowTcpDstPortCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowTcpDstPortCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowTcpDstPortCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowTcpDstPortCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowTcpSeqNum(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowTcpSeqNumCounter',
        'decrement': 'PatternFlowTcpSeqNumCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowTcpSeqNum, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowTcpSeqNumCounter
        """Factory property that returns an instance of the PatternFlowTcpSeqNumCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowTcpSeqNumCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowTcpSeqNumCounter
        """Factory property that returns an instance of the PatternFlowTcpSeqNumCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowTcpSeqNumCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowTcpSeqNumCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowTcpSeqNumCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowTcpAckNum(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowTcpAckNumCounter',
        'decrement': 'PatternFlowTcpAckNumCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowTcpAckNum, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowTcpAckNumCounter
        """Factory property that returns an instance of the PatternFlowTcpAckNumCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowTcpAckNumCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowTcpAckNumCounter
        """Factory property that returns an instance of the PatternFlowTcpAckNumCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowTcpAckNumCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowTcpAckNumCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowTcpAckNumCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowTcpDataOffset(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowTcpDataOffsetCounter',
        'decrement': 'PatternFlowTcpDataOffsetCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowTcpDataOffset, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowTcpDataOffsetCounter
        """Factory property that returns an instance of the PatternFlowTcpDataOffsetCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowTcpDataOffsetCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowTcpDataOffsetCounter
        """Factory property that returns an instance of the PatternFlowTcpDataOffsetCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowTcpDataOffsetCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowTcpDataOffsetCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowTcpDataOffsetCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowTcpEcnNs(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowTcpEcnNsCounter',
        'decrement': 'PatternFlowTcpEcnNsCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowTcpEcnNs, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowTcpEcnNsCounter
        """Factory property that returns an instance of the PatternFlowTcpEcnNsCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowTcpEcnNsCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowTcpEcnNsCounter
        """Factory property that returns an instance of the PatternFlowTcpEcnNsCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowTcpEcnNsCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowTcpEcnNsCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowTcpEcnNsCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowTcpEcnCwr(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowTcpEcnCwrCounter',
        'decrement': 'PatternFlowTcpEcnCwrCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowTcpEcnCwr, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowTcpEcnCwrCounter
        """Factory property that returns an instance of the PatternFlowTcpEcnCwrCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowTcpEcnCwrCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowTcpEcnCwrCounter
        """Factory property that returns an instance of the PatternFlowTcpEcnCwrCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowTcpEcnCwrCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowTcpEcnCwrCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowTcpEcnCwrCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowTcpEcnEcho(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowTcpEcnEchoCounter',
        'decrement': 'PatternFlowTcpEcnEchoCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowTcpEcnEcho, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowTcpEcnEchoCounter
        """Factory property that returns an instance of the PatternFlowTcpEcnEchoCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowTcpEcnEchoCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowTcpEcnEchoCounter
        """Factory property that returns an instance of the PatternFlowTcpEcnEchoCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowTcpEcnEchoCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowTcpEcnEchoCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowTcpEcnEchoCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowTcpCtlUrg(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowTcpCtlUrgCounter',
        'decrement': 'PatternFlowTcpCtlUrgCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowTcpCtlUrg, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowTcpCtlUrgCounter
        """Factory property that returns an instance of the PatternFlowTcpCtlUrgCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowTcpCtlUrgCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowTcpCtlUrgCounter
        """Factory property that returns an instance of the PatternFlowTcpCtlUrgCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowTcpCtlUrgCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowTcpCtlUrgCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowTcpCtlUrgCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowTcpCtlAck(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowTcpCtlAckCounter',
        'decrement': 'PatternFlowTcpCtlAckCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowTcpCtlAck, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowTcpCtlAckCounter
        """Factory property that returns an instance of the PatternFlowTcpCtlAckCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowTcpCtlAckCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowTcpCtlAckCounter
        """Factory property that returns an instance of the PatternFlowTcpCtlAckCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowTcpCtlAckCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowTcpCtlAckCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowTcpCtlAckCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowTcpCtlPsh(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowTcpCtlPshCounter',
        'decrement': 'PatternFlowTcpCtlPshCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowTcpCtlPsh, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowTcpCtlPshCounter
        """Factory property that returns an instance of the PatternFlowTcpCtlPshCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowTcpCtlPshCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowTcpCtlPshCounter
        """Factory property that returns an instance of the PatternFlowTcpCtlPshCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowTcpCtlPshCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowTcpCtlPshCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowTcpCtlPshCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowTcpCtlRst(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowTcpCtlRstCounter',
        'decrement': 'PatternFlowTcpCtlRstCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowTcpCtlRst, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowTcpCtlRstCounter
        """Factory property that returns an instance of the PatternFlowTcpCtlRstCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowTcpCtlRstCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowTcpCtlRstCounter
        """Factory property that returns an instance of the PatternFlowTcpCtlRstCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowTcpCtlRstCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowTcpCtlRstCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowTcpCtlRstCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowTcpCtlSyn(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowTcpCtlSynCounter',
        'decrement': 'PatternFlowTcpCtlSynCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowTcpCtlSyn, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowTcpCtlSynCounter
        """Factory property that returns an instance of the PatternFlowTcpCtlSynCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowTcpCtlSynCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowTcpCtlSynCounter
        """Factory property that returns an instance of the PatternFlowTcpCtlSynCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowTcpCtlSynCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowTcpCtlSynCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowTcpCtlSynCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowTcpCtlFin(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowTcpCtlFinCounter',
        'decrement': 'PatternFlowTcpCtlFinCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowTcpCtlFin, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowTcpCtlFinCounter
        """Factory property that returns an instance of the PatternFlowTcpCtlFinCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowTcpCtlFinCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowTcpCtlFinCounter
        """Factory property that returns an instance of the PatternFlowTcpCtlFinCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowTcpCtlFinCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowTcpCtlFinCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowTcpCtlFinCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowTcpWindow(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowTcpWindowCounter',
        'decrement': 'PatternFlowTcpWindowCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowTcpWindow, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowTcpWindowCounter
        """Factory property that returns an instance of the PatternFlowTcpWindowCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowTcpWindowCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowTcpWindowCounter
        """Factory property that returns an instance of the PatternFlowTcpWindowCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowTcpWindowCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowTcpWindowCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowTcpWindowCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class FlowUdp(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'src_port': 'PatternFlowUdpSrcPort',
        'dst_port': 'PatternFlowUdpDstPort',
        'length': 'PatternFlowUdpLength',
        'checksum': 'PatternFlowUdpChecksum',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowUdp, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def src_port(self):
        # type: () -> PatternFlowUdpSrcPort
        """src_port getter

        Source portSource port

        Returns: obj(snappi.PatternFlowUdpSrcPort)
        """
        return self._get_property('src_port', PatternFlowUdpSrcPort)

    @property
    def dst_port(self):
        # type: () -> PatternFlowUdpDstPort
        """dst_port getter

        Destination portDestination port

        Returns: obj(snappi.PatternFlowUdpDstPort)
        """
        return self._get_property('dst_port', PatternFlowUdpDstPort)

    @property
    def length(self):
        # type: () -> PatternFlowUdpLength
        """length getter

        LengthLength

        Returns: obj(snappi.PatternFlowUdpLength)
        """
        return self._get_property('length', PatternFlowUdpLength)

    @property
    def checksum(self):
        # type: () -> PatternFlowUdpChecksum
        """checksum getter

        UDP checksumUDP checksum

        Returns: obj(snappi.PatternFlowUdpChecksum)
        """
        return self._get_property('checksum', PatternFlowUdpChecksum)


class PatternFlowUdpSrcPort(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowUdpSrcPortCounter',
        'decrement': 'PatternFlowUdpSrcPortCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowUdpSrcPort, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowUdpSrcPortCounter
        """Factory property that returns an instance of the PatternFlowUdpSrcPortCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowUdpSrcPortCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowUdpSrcPortCounter
        """Factory property that returns an instance of the PatternFlowUdpSrcPortCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowUdpSrcPortCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowUdpSrcPortCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowUdpSrcPortCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowUdpDstPort(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowUdpDstPortCounter',
        'decrement': 'PatternFlowUdpDstPortCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowUdpDstPort, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowUdpDstPortCounter
        """Factory property that returns an instance of the PatternFlowUdpDstPortCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowUdpDstPortCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowUdpDstPortCounter
        """Factory property that returns an instance of the PatternFlowUdpDstPortCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowUdpDstPortCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowUdpDstPortCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowUdpDstPortCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowUdpLength(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowUdpLengthCounter',
        'decrement': 'PatternFlowUdpLengthCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowUdpLength, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowUdpLengthCounter
        """Factory property that returns an instance of the PatternFlowUdpLengthCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowUdpLengthCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowUdpLengthCounter
        """Factory property that returns an instance of the PatternFlowUdpLengthCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowUdpLengthCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowUdpLengthCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowUdpLengthCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowUdpChecksum(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    GENERATED = 'generated'
    CUSTOM = 'custom'

    GOOD = 'good'
    BAD = 'bad'

    def __init__(self, parent=None, choice=None):
        super(PatternFlowUdpChecksum, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def choice(self):
        # type: () -> Union[generated, custom, choice, choice, choice]
        """choice getter

        The type of checksum

        Returns: Union[generated, custom, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        The type of checksum

        value: Union[generated, custom, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def generated(self):
        # type: () -> Union[good, bad]
        """generated getter

        A system generated checksum value

        Returns: Union[good, bad]
        """
        return self._get_property('generated')

    @generated.setter
    def generated(self, value):
        """generated setter

        A system generated checksum value

        value: Union[good, bad]
        """
        self._set_property('generated', value, 'generated')

    @property
    def custom(self):
        # type: () -> int
        """custom getter

        A custom checksum value

        Returns: int
        """
        return self._get_property('custom')

    @custom.setter
    def custom(self, value):
        """custom setter

        A custom checksum value

        value: int
        """
        self._set_property('custom', value, 'custom')


class FlowGre(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'checksum_present': 'PatternFlowGreChecksumPresent',
        'reserved0': 'PatternFlowGreReserved0',
        'version': 'PatternFlowGreVersion',
        'protocol': 'PatternFlowGreProtocol',
        'checksum': 'PatternFlowGreChecksum',
        'reserved1': 'PatternFlowGreReserved1',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowGre, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def checksum_present(self):
        # type: () -> PatternFlowGreChecksumPresent
        """checksum_present getter

        Checksum present bitChecksum present bit

        Returns: obj(snappi.PatternFlowGreChecksumPresent)
        """
        return self._get_property('checksum_present', PatternFlowGreChecksumPresent)

    @property
    def reserved0(self):
        # type: () -> PatternFlowGreReserved0
        """reserved0 getter

        Reserved bitsReserved bits

        Returns: obj(snappi.PatternFlowGreReserved0)
        """
        return self._get_property('reserved0', PatternFlowGreReserved0)

    @property
    def version(self):
        # type: () -> PatternFlowGreVersion
        """version getter

        GRE version numberGRE version number

        Returns: obj(snappi.PatternFlowGreVersion)
        """
        return self._get_property('version', PatternFlowGreVersion)

    @property
    def protocol(self):
        # type: () -> PatternFlowGreProtocol
        """protocol getter

        Protocol type of encapsulated payloadProtocol type of encapsulated payload

        Returns: obj(snappi.PatternFlowGreProtocol)
        """
        return self._get_property('protocol', PatternFlowGreProtocol)

    @property
    def checksum(self):
        # type: () -> PatternFlowGreChecksum
        """checksum getter

        Optional checksum of GRE header and payload. Only present if the checksum_present bit is set.Optional checksum of GRE header and payload. Only present if the checksum_present bit is set.

        Returns: obj(snappi.PatternFlowGreChecksum)
        """
        return self._get_property('checksum', PatternFlowGreChecksum)

    @property
    def reserved1(self):
        # type: () -> PatternFlowGreReserved1
        """reserved1 getter

        Optional reserved field. Only present if the checksum_present bit is set.Optional reserved field. Only present if the checksum_present bit is set.

        Returns: obj(snappi.PatternFlowGreReserved1)
        """
        return self._get_property('reserved1', PatternFlowGreReserved1)


class PatternFlowGreChecksumPresent(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowGreChecksumPresentCounter',
        'decrement': 'PatternFlowGreChecksumPresentCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowGreChecksumPresent, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowGreChecksumPresentCounter
        """Factory property that returns an instance of the PatternFlowGreChecksumPresentCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowGreChecksumPresentCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowGreChecksumPresentCounter
        """Factory property that returns an instance of the PatternFlowGreChecksumPresentCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowGreChecksumPresentCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowGreChecksumPresentCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowGreChecksumPresentCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowGreReserved0(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowGreReserved0Counter',
        'decrement': 'PatternFlowGreReserved0Counter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowGreReserved0, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowGreReserved0Counter
        """Factory property that returns an instance of the PatternFlowGreReserved0Counter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowGreReserved0Counter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowGreReserved0Counter
        """Factory property that returns an instance of the PatternFlowGreReserved0Counter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowGreReserved0Counter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowGreReserved0Counter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowGreReserved0Counter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowGreVersion(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowGreVersionCounter',
        'decrement': 'PatternFlowGreVersionCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowGreVersion, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowGreVersionCounter
        """Factory property that returns an instance of the PatternFlowGreVersionCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowGreVersionCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowGreVersionCounter
        """Factory property that returns an instance of the PatternFlowGreVersionCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowGreVersionCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowGreVersionCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowGreVersionCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowGreProtocol(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowGreProtocolCounter',
        'decrement': 'PatternFlowGreProtocolCounter',
    }

    IPV4 = '2048'
    IPV6 = '34525'

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowGreProtocol, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowGreProtocolCounter
        """Factory property that returns an instance of the PatternFlowGreProtocolCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowGreProtocolCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowGreProtocolCounter
        """Factory property that returns an instance of the PatternFlowGreProtocolCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowGreProtocolCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowGreProtocolCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    IPV4 = '2048'
    IPV6 = '34525'

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowGreProtocolCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowGreChecksum(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    GENERATED = 'generated'
    CUSTOM = 'custom'

    GOOD = 'good'
    BAD = 'bad'

    def __init__(self, parent=None, choice=None):
        super(PatternFlowGreChecksum, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def choice(self):
        # type: () -> Union[generated, custom, choice, choice, choice]
        """choice getter

        The type of checksum

        Returns: Union[generated, custom, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        The type of checksum

        value: Union[generated, custom, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def generated(self):
        # type: () -> Union[good, bad]
        """generated getter

        A system generated checksum value

        Returns: Union[good, bad]
        """
        return self._get_property('generated')

    @generated.setter
    def generated(self, value):
        """generated setter

        A system generated checksum value

        value: Union[good, bad]
        """
        self._set_property('generated', value, 'generated')

    @property
    def custom(self):
        # type: () -> int
        """custom getter

        A custom checksum value

        Returns: int
        """
        return self._get_property('custom')

    @custom.setter
    def custom(self, value):
        """custom setter

        A custom checksum value

        value: int
        """
        self._set_property('custom', value, 'custom')


class PatternFlowGreReserved1(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowGreReserved1Counter',
        'decrement': 'PatternFlowGreReserved1Counter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowGreReserved1, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowGreReserved1Counter
        """Factory property that returns an instance of the PatternFlowGreReserved1Counter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowGreReserved1Counter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowGreReserved1Counter
        """Factory property that returns an instance of the PatternFlowGreReserved1Counter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowGreReserved1Counter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowGreReserved1Counter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowGreReserved1Counter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class FlowGtpv1(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'version': 'PatternFlowGtpv1Version',
        'protocol_type': 'PatternFlowGtpv1ProtocolType',
        'reserved': 'PatternFlowGtpv1Reserved',
        'e_flag': 'PatternFlowGtpv1EFlag',
        's_flag': 'PatternFlowGtpv1SFlag',
        'pn_flag': 'PatternFlowGtpv1PnFlag',
        'message_type': 'PatternFlowGtpv1MessageType',
        'message_length': 'PatternFlowGtpv1MessageLength',
        'teid': 'PatternFlowGtpv1Teid',
        'squence_number': 'PatternFlowGtpv1SquenceNumber',
        'n_pdu_number': 'PatternFlowGtpv1NPduNumber',
        'next_extension_header_type': 'PatternFlowGtpv1NextExtensionHeaderType',
        'extension_headers': 'FlowGtpExtensionIter',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowGtpv1, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def version(self):
        # type: () -> PatternFlowGtpv1Version
        """version getter

        GTPv1 versionGTPv1 version

        Returns: obj(snappi.PatternFlowGtpv1Version)
        """
        return self._get_property('version', PatternFlowGtpv1Version)

    @property
    def protocol_type(self):
        # type: () -> PatternFlowGtpv1ProtocolType
        """protocol_type getter

        Protocol type, GTP is 1, GTP' is 0Protocol type, GTP is 1, GTP' is 0

        Returns: obj(snappi.PatternFlowGtpv1ProtocolType)
        """
        return self._get_property('protocol_type', PatternFlowGtpv1ProtocolType)

    @property
    def reserved(self):
        # type: () -> PatternFlowGtpv1Reserved
        """reserved getter

        Reserved fieldReserved field

        Returns: obj(snappi.PatternFlowGtpv1Reserved)
        """
        return self._get_property('reserved', PatternFlowGtpv1Reserved)

    @property
    def e_flag(self):
        # type: () -> PatternFlowGtpv1EFlag
        """e_flag getter

        Extension header field presentExtension header field present

        Returns: obj(snappi.PatternFlowGtpv1EFlag)
        """
        return self._get_property('e_flag', PatternFlowGtpv1EFlag)

    @property
    def s_flag(self):
        # type: () -> PatternFlowGtpv1SFlag
        """s_flag getter

        Sequence number field presentSequence number field present

        Returns: obj(snappi.PatternFlowGtpv1SFlag)
        """
        return self._get_property('s_flag', PatternFlowGtpv1SFlag)

    @property
    def pn_flag(self):
        # type: () -> PatternFlowGtpv1PnFlag
        """pn_flag getter

        N-PDU field presentN-PDU field present

        Returns: obj(snappi.PatternFlowGtpv1PnFlag)
        """
        return self._get_property('pn_flag', PatternFlowGtpv1PnFlag)

    @property
    def message_type(self):
        # type: () -> PatternFlowGtpv1MessageType
        """message_type getter

        The type of GTP message Different types of messages are defined in 3GPP TS 29.060 section 7.1The type of GTP message Different types of messages are defined in 3GPP TS 29.060 section 7.1

        Returns: obj(snappi.PatternFlowGtpv1MessageType)
        """
        return self._get_property('message_type', PatternFlowGtpv1MessageType)

    @property
    def message_length(self):
        # type: () -> PatternFlowGtpv1MessageLength
        """message_length getter

        The length of the payload (the bytes following the mandatory 8-byte GTP header) in bytes that includes any optional fieldsThe length of the payload (the bytes following the mandatory 8-byte GTP header) in bytes that includes any optional fields

        Returns: obj(snappi.PatternFlowGtpv1MessageLength)
        """
        return self._get_property('message_length', PatternFlowGtpv1MessageLength)

    @property
    def teid(self):
        # type: () -> PatternFlowGtpv1Teid
        """teid getter

        Tunnel endpoint identifier (TEID) used to multiplex connections in the same GTP tunnelTunnel endpoint identifier (TEID) used to multiplex connections in the same GTP tunnel

        Returns: obj(snappi.PatternFlowGtpv1Teid)
        """
        return self._get_property('teid', PatternFlowGtpv1Teid)

    @property
    def squence_number(self):
        # type: () -> PatternFlowGtpv1SquenceNumber
        """squence_number getter

        Sequence number. Exists if any of the e_flag, s_flag, or pn_flag bits are on. Must be interpreted only if the s_flag bit is on.Sequence number. Exists if any of the e_flag, s_flag, or pn_flag bits are on. Must be interpreted only if the s_flag bit is on.

        Returns: obj(snappi.PatternFlowGtpv1SquenceNumber)
        """
        return self._get_property('squence_number', PatternFlowGtpv1SquenceNumber)

    @property
    def n_pdu_number(self):
        # type: () -> PatternFlowGtpv1NPduNumber
        """n_pdu_number getter

        N-PDU number. Exists if any of the e_flag, s_flag, or pn_flag bits are on. Must be interpreted only if the pn_flag bit is on.N-PDU number. Exists if any of the e_flag, s_flag, or pn_flag bits are on. Must be interpreted only if the pn_flag bit is on.

        Returns: obj(snappi.PatternFlowGtpv1NPduNumber)
        """
        return self._get_property('n_pdu_number', PatternFlowGtpv1NPduNumber)

    @property
    def next_extension_header_type(self):
        # type: () -> PatternFlowGtpv1NextExtensionHeaderType
        """next_extension_header_type getter

        Next extension header. Exists if any of the e_flag, s_flag, or pn_flag bits are on. Must be interpreted only if the e_flag bit is on.Next extension header. Exists if any of the e_flag, s_flag, or pn_flag bits are on. Must be interpreted only if the e_flag bit is on.

        Returns: obj(snappi.PatternFlowGtpv1NextExtensionHeaderType)
        """
        return self._get_property('next_extension_header_type', PatternFlowGtpv1NextExtensionHeaderType)

    @property
    def extension_headers(self):
        # type: () -> FlowGtpExtensionIter
        """extension_headers getter

        A list of optional extension headers.

        Returns: list[obj(snappi.FlowGtpExtension)]
        """
        return self._get_property('extension_headers', FlowGtpExtensionIter)


class PatternFlowGtpv1Version(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowGtpv1VersionCounter',
        'decrement': 'PatternFlowGtpv1VersionCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowGtpv1Version, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowGtpv1VersionCounter
        """Factory property that returns an instance of the PatternFlowGtpv1VersionCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowGtpv1VersionCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowGtpv1VersionCounter
        """Factory property that returns an instance of the PatternFlowGtpv1VersionCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowGtpv1VersionCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowGtpv1VersionCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowGtpv1VersionCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowGtpv1ProtocolType(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowGtpv1ProtocolTypeCounter',
        'decrement': 'PatternFlowGtpv1ProtocolTypeCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowGtpv1ProtocolType, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowGtpv1ProtocolTypeCounter
        """Factory property that returns an instance of the PatternFlowGtpv1ProtocolTypeCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowGtpv1ProtocolTypeCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowGtpv1ProtocolTypeCounter
        """Factory property that returns an instance of the PatternFlowGtpv1ProtocolTypeCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowGtpv1ProtocolTypeCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowGtpv1ProtocolTypeCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowGtpv1ProtocolTypeCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowGtpv1Reserved(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowGtpv1ReservedCounter',
        'decrement': 'PatternFlowGtpv1ReservedCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowGtpv1Reserved, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowGtpv1ReservedCounter
        """Factory property that returns an instance of the PatternFlowGtpv1ReservedCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowGtpv1ReservedCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowGtpv1ReservedCounter
        """Factory property that returns an instance of the PatternFlowGtpv1ReservedCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowGtpv1ReservedCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowGtpv1ReservedCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowGtpv1ReservedCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowGtpv1EFlag(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowGtpv1EFlagCounter',
        'decrement': 'PatternFlowGtpv1EFlagCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowGtpv1EFlag, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowGtpv1EFlagCounter
        """Factory property that returns an instance of the PatternFlowGtpv1EFlagCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowGtpv1EFlagCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowGtpv1EFlagCounter
        """Factory property that returns an instance of the PatternFlowGtpv1EFlagCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowGtpv1EFlagCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowGtpv1EFlagCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowGtpv1EFlagCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowGtpv1SFlag(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowGtpv1SFlagCounter',
        'decrement': 'PatternFlowGtpv1SFlagCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowGtpv1SFlag, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowGtpv1SFlagCounter
        """Factory property that returns an instance of the PatternFlowGtpv1SFlagCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowGtpv1SFlagCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowGtpv1SFlagCounter
        """Factory property that returns an instance of the PatternFlowGtpv1SFlagCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowGtpv1SFlagCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowGtpv1SFlagCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowGtpv1SFlagCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowGtpv1PnFlag(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowGtpv1PnFlagCounter',
        'decrement': 'PatternFlowGtpv1PnFlagCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowGtpv1PnFlag, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowGtpv1PnFlagCounter
        """Factory property that returns an instance of the PatternFlowGtpv1PnFlagCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowGtpv1PnFlagCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowGtpv1PnFlagCounter
        """Factory property that returns an instance of the PatternFlowGtpv1PnFlagCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowGtpv1PnFlagCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowGtpv1PnFlagCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowGtpv1PnFlagCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowGtpv1MessageType(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowGtpv1MessageTypeCounter',
        'decrement': 'PatternFlowGtpv1MessageTypeCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowGtpv1MessageType, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowGtpv1MessageTypeCounter
        """Factory property that returns an instance of the PatternFlowGtpv1MessageTypeCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowGtpv1MessageTypeCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowGtpv1MessageTypeCounter
        """Factory property that returns an instance of the PatternFlowGtpv1MessageTypeCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowGtpv1MessageTypeCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowGtpv1MessageTypeCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowGtpv1MessageTypeCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowGtpv1MessageLength(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowGtpv1MessageLengthCounter',
        'decrement': 'PatternFlowGtpv1MessageLengthCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowGtpv1MessageLength, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowGtpv1MessageLengthCounter
        """Factory property that returns an instance of the PatternFlowGtpv1MessageLengthCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowGtpv1MessageLengthCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowGtpv1MessageLengthCounter
        """Factory property that returns an instance of the PatternFlowGtpv1MessageLengthCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowGtpv1MessageLengthCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowGtpv1MessageLengthCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowGtpv1MessageLengthCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowGtpv1Teid(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowGtpv1TeidCounter',
        'decrement': 'PatternFlowGtpv1TeidCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowGtpv1Teid, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowGtpv1TeidCounter
        """Factory property that returns an instance of the PatternFlowGtpv1TeidCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowGtpv1TeidCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowGtpv1TeidCounter
        """Factory property that returns an instance of the PatternFlowGtpv1TeidCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowGtpv1TeidCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowGtpv1TeidCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowGtpv1TeidCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowGtpv1SquenceNumber(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowGtpv1SquenceNumberCounter',
        'decrement': 'PatternFlowGtpv1SquenceNumberCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowGtpv1SquenceNumber, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowGtpv1SquenceNumberCounter
        """Factory property that returns an instance of the PatternFlowGtpv1SquenceNumberCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowGtpv1SquenceNumberCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowGtpv1SquenceNumberCounter
        """Factory property that returns an instance of the PatternFlowGtpv1SquenceNumberCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowGtpv1SquenceNumberCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowGtpv1SquenceNumberCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowGtpv1SquenceNumberCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowGtpv1NPduNumber(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowGtpv1NPduNumberCounter',
        'decrement': 'PatternFlowGtpv1NPduNumberCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowGtpv1NPduNumber, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowGtpv1NPduNumberCounter
        """Factory property that returns an instance of the PatternFlowGtpv1NPduNumberCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowGtpv1NPduNumberCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowGtpv1NPduNumberCounter
        """Factory property that returns an instance of the PatternFlowGtpv1NPduNumberCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowGtpv1NPduNumberCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowGtpv1NPduNumberCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowGtpv1NPduNumberCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowGtpv1NextExtensionHeaderType(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowGtpv1NextExtensionHeaderTypeCounter',
        'decrement': 'PatternFlowGtpv1NextExtensionHeaderTypeCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowGtpv1NextExtensionHeaderType, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowGtpv1NextExtensionHeaderTypeCounter
        """Factory property that returns an instance of the PatternFlowGtpv1NextExtensionHeaderTypeCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowGtpv1NextExtensionHeaderTypeCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowGtpv1NextExtensionHeaderTypeCounter
        """Factory property that returns an instance of the PatternFlowGtpv1NextExtensionHeaderTypeCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowGtpv1NextExtensionHeaderTypeCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowGtpv1NextExtensionHeaderTypeCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowGtpv1NextExtensionHeaderTypeCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class FlowGtpExtension(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'extension_length': 'PatternFlowGtpExtensionExtensionLength',
        'contents': 'PatternFlowGtpExtensionContents',
        'next_extension_header': 'PatternFlowGtpExtensionNextExtensionHeader',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowGtpExtension, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def extension_length(self):
        # type: () -> PatternFlowGtpExtensionExtensionLength
        """extension_length getter

        This field states the length of this extension header, including the length, the contents, and the next extension header field, in 4-octet units, so the length of the extension must always be a multiple of 4.

        Returns: obj(snappi.PatternFlowGtpExtensionExtensionLength)
        """
        return self._get_property('extension_length', PatternFlowGtpExtensionExtensionLength)

    @property
    def contents(self):
        # type: () -> PatternFlowGtpExtensionContents
        """contents getter

        The extension header contents

        Returns: obj(snappi.PatternFlowGtpExtensionContents)
        """
        return self._get_property('contents', PatternFlowGtpExtensionContents)

    @property
    def next_extension_header(self):
        # type: () -> PatternFlowGtpExtensionNextExtensionHeader
        """next_extension_header getter

        It states the type of the next extension, or 0 if no next extension exists. This permits chaining several next extension headers.

        Returns: obj(snappi.PatternFlowGtpExtensionNextExtensionHeader)
        """
        return self._get_property('next_extension_header', PatternFlowGtpExtensionNextExtensionHeader)


class PatternFlowGtpExtensionExtensionLength(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowGtpExtensionExtensionLengthCounter',
        'decrement': 'PatternFlowGtpExtensionExtensionLengthCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowGtpExtensionExtensionLength, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowGtpExtensionExtensionLengthCounter
        """Factory property that returns an instance of the PatternFlowGtpExtensionExtensionLengthCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowGtpExtensionExtensionLengthCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowGtpExtensionExtensionLengthCounter
        """Factory property that returns an instance of the PatternFlowGtpExtensionExtensionLengthCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowGtpExtensionExtensionLengthCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowGtpExtensionExtensionLengthCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowGtpExtensionExtensionLengthCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowGtpExtensionContents(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowGtpExtensionContentsCounter',
        'decrement': 'PatternFlowGtpExtensionContentsCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowGtpExtensionContents, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowGtpExtensionContentsCounter
        """Factory property that returns an instance of the PatternFlowGtpExtensionContentsCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowGtpExtensionContentsCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowGtpExtensionContentsCounter
        """Factory property that returns an instance of the PatternFlowGtpExtensionContentsCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowGtpExtensionContentsCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowGtpExtensionContentsCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowGtpExtensionContentsCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowGtpExtensionNextExtensionHeader(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowGtpExtensionNextExtensionHeaderCounter',
        'decrement': 'PatternFlowGtpExtensionNextExtensionHeaderCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowGtpExtensionNextExtensionHeader, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowGtpExtensionNextExtensionHeaderCounter
        """Factory property that returns an instance of the PatternFlowGtpExtensionNextExtensionHeaderCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowGtpExtensionNextExtensionHeaderCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowGtpExtensionNextExtensionHeaderCounter
        """Factory property that returns an instance of the PatternFlowGtpExtensionNextExtensionHeaderCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowGtpExtensionNextExtensionHeaderCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowGtpExtensionNextExtensionHeaderCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowGtpExtensionNextExtensionHeaderCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class FlowGtpExtensionIter(SnappiIter):
    __slots__ = ()

    def __init__(self):
        super(FlowGtpExtensionIter, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[FlowGtpExtension]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> FlowGtpExtensionIter
        return self._iter()

    def __next__(self):
        # type: () -> FlowGtpExtension
        return self._next()

    def next(self):
        # type: () -> FlowGtpExtension
        return self._next()

    def gtpextension(self):
        # type: () -> FlowGtpExtensionIter
        """Factory method that creates an instance of FlowGtpExtension class

        TBD
        """
        item = FlowGtpExtension()
        self._add(item)
        return self


class FlowGtpv2(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'version': 'PatternFlowGtpv2Version',
        'piggybacking_flag': 'PatternFlowGtpv2PiggybackingFlag',
        'teid_flag': 'PatternFlowGtpv2TeidFlag',
        'spare1': 'PatternFlowGtpv2Spare1',
        'message_type': 'PatternFlowGtpv2MessageType',
        'message_length': 'PatternFlowGtpv2MessageLength',
        'teid': 'PatternFlowGtpv2Teid',
        'sequence_number': 'PatternFlowGtpv2SequenceNumber',
        'spare2': 'PatternFlowGtpv2Spare2',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowGtpv2, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def version(self):
        # type: () -> PatternFlowGtpv2Version
        """version getter

        Version numberVersion number

        Returns: obj(snappi.PatternFlowGtpv2Version)
        """
        return self._get_property('version', PatternFlowGtpv2Version)

    @property
    def piggybacking_flag(self):
        # type: () -> PatternFlowGtpv2PiggybackingFlag
        """piggybacking_flag getter

        If piggybacking_flag is set to 1 then another GTP-C message with its own header shall be present at the end of the current messageIf piggybacking_flag is set to 1 then another GTP-C message with its own header shall be present at the end of the current message

        Returns: obj(snappi.PatternFlowGtpv2PiggybackingFlag)
        """
        return self._get_property('piggybacking_flag', PatternFlowGtpv2PiggybackingFlag)

    @property
    def teid_flag(self):
        # type: () -> PatternFlowGtpv2TeidFlag
        """teid_flag getter

        If teid_flag is set to 1 then the TEID field will be present between the message length and the sequence number. All messages except Echo and Echo reply require TEID to be presentIf teid_flag is set to 1 then the TEID field will be present between the message length and the sequence number. All messages except Echo and Echo reply require TEID to be present

        Returns: obj(snappi.PatternFlowGtpv2TeidFlag)
        """
        return self._get_property('teid_flag', PatternFlowGtpv2TeidFlag)

    @property
    def spare1(self):
        # type: () -> PatternFlowGtpv2Spare1
        """spare1 getter

        A 3-bit reserved field (must be 0).A 3-bit reserved field (must be 0).

        Returns: obj(snappi.PatternFlowGtpv2Spare1)
        """
        return self._get_property('spare1', PatternFlowGtpv2Spare1)

    @property
    def message_type(self):
        # type: () -> PatternFlowGtpv2MessageType
        """message_type getter

        An 8-bit field that indicates the type of GTP message. Different types of messages are defined in 3GPP TS 29.060 section 7.1An 8-bit field that indicates the type of GTP message. Different types of messages are defined in 3GPP TS 29.060 section 7.1

        Returns: obj(snappi.PatternFlowGtpv2MessageType)
        """
        return self._get_property('message_type', PatternFlowGtpv2MessageType)

    @property
    def message_length(self):
        # type: () -> PatternFlowGtpv2MessageLength
        """message_length getter

        A 16-bit field that indicates the length of the payload in bytes, excluding the mandatory GTP-c header (first 4 bytes). Includes the TEID and sequence_number if they are present.A 16-bit field that indicates the length of the payload in bytes, excluding the mandatory GTP-c header (first 4 bytes). Includes the TEID and sequence_number if they are present.

        Returns: obj(snappi.PatternFlowGtpv2MessageLength)
        """
        return self._get_property('message_length', PatternFlowGtpv2MessageLength)

    @property
    def teid(self):
        # type: () -> PatternFlowGtpv2Teid
        """teid getter

        Tunnel endpoint identifier. A 32-bit (4-octet) field used to multiplex different connections in the same GTP tunnel. Is present only if the teid_flag is set.Tunnel endpoint identifier. A 32-bit (4-octet) field used to multiplex different connections in the same GTP tunnel. Is present only if the teid_flag is set.

        Returns: obj(snappi.PatternFlowGtpv2Teid)
        """
        return self._get_property('teid', PatternFlowGtpv2Teid)

    @property
    def sequence_number(self):
        # type: () -> PatternFlowGtpv2SequenceNumber
        """sequence_number getter

        The sequence numberThe sequence number

        Returns: obj(snappi.PatternFlowGtpv2SequenceNumber)
        """
        return self._get_property('sequence_number', PatternFlowGtpv2SequenceNumber)

    @property
    def spare2(self):
        # type: () -> PatternFlowGtpv2Spare2
        """spare2 getter

        Reserved fieldReserved field

        Returns: obj(snappi.PatternFlowGtpv2Spare2)
        """
        return self._get_property('spare2', PatternFlowGtpv2Spare2)


class PatternFlowGtpv2Version(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowGtpv2VersionCounter',
        'decrement': 'PatternFlowGtpv2VersionCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowGtpv2Version, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowGtpv2VersionCounter
        """Factory property that returns an instance of the PatternFlowGtpv2VersionCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowGtpv2VersionCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowGtpv2VersionCounter
        """Factory property that returns an instance of the PatternFlowGtpv2VersionCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowGtpv2VersionCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowGtpv2VersionCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowGtpv2VersionCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowGtpv2PiggybackingFlag(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowGtpv2PiggybackingFlagCounter',
        'decrement': 'PatternFlowGtpv2PiggybackingFlagCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowGtpv2PiggybackingFlag, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowGtpv2PiggybackingFlagCounter
        """Factory property that returns an instance of the PatternFlowGtpv2PiggybackingFlagCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowGtpv2PiggybackingFlagCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowGtpv2PiggybackingFlagCounter
        """Factory property that returns an instance of the PatternFlowGtpv2PiggybackingFlagCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowGtpv2PiggybackingFlagCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowGtpv2PiggybackingFlagCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowGtpv2PiggybackingFlagCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowGtpv2TeidFlag(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowGtpv2TeidFlagCounter',
        'decrement': 'PatternFlowGtpv2TeidFlagCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowGtpv2TeidFlag, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowGtpv2TeidFlagCounter
        """Factory property that returns an instance of the PatternFlowGtpv2TeidFlagCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowGtpv2TeidFlagCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowGtpv2TeidFlagCounter
        """Factory property that returns an instance of the PatternFlowGtpv2TeidFlagCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowGtpv2TeidFlagCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowGtpv2TeidFlagCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowGtpv2TeidFlagCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowGtpv2Spare1(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowGtpv2Spare1Counter',
        'decrement': 'PatternFlowGtpv2Spare1Counter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowGtpv2Spare1, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowGtpv2Spare1Counter
        """Factory property that returns an instance of the PatternFlowGtpv2Spare1Counter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowGtpv2Spare1Counter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowGtpv2Spare1Counter
        """Factory property that returns an instance of the PatternFlowGtpv2Spare1Counter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowGtpv2Spare1Counter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowGtpv2Spare1Counter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowGtpv2Spare1Counter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowGtpv2MessageType(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowGtpv2MessageTypeCounter',
        'decrement': 'PatternFlowGtpv2MessageTypeCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowGtpv2MessageType, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowGtpv2MessageTypeCounter
        """Factory property that returns an instance of the PatternFlowGtpv2MessageTypeCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowGtpv2MessageTypeCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowGtpv2MessageTypeCounter
        """Factory property that returns an instance of the PatternFlowGtpv2MessageTypeCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowGtpv2MessageTypeCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowGtpv2MessageTypeCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowGtpv2MessageTypeCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowGtpv2MessageLength(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowGtpv2MessageLengthCounter',
        'decrement': 'PatternFlowGtpv2MessageLengthCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowGtpv2MessageLength, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowGtpv2MessageLengthCounter
        """Factory property that returns an instance of the PatternFlowGtpv2MessageLengthCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowGtpv2MessageLengthCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowGtpv2MessageLengthCounter
        """Factory property that returns an instance of the PatternFlowGtpv2MessageLengthCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowGtpv2MessageLengthCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowGtpv2MessageLengthCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowGtpv2MessageLengthCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowGtpv2Teid(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowGtpv2TeidCounter',
        'decrement': 'PatternFlowGtpv2TeidCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowGtpv2Teid, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowGtpv2TeidCounter
        """Factory property that returns an instance of the PatternFlowGtpv2TeidCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowGtpv2TeidCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowGtpv2TeidCounter
        """Factory property that returns an instance of the PatternFlowGtpv2TeidCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowGtpv2TeidCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowGtpv2TeidCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowGtpv2TeidCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowGtpv2SequenceNumber(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowGtpv2SequenceNumberCounter',
        'decrement': 'PatternFlowGtpv2SequenceNumberCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowGtpv2SequenceNumber, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowGtpv2SequenceNumberCounter
        """Factory property that returns an instance of the PatternFlowGtpv2SequenceNumberCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowGtpv2SequenceNumberCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowGtpv2SequenceNumberCounter
        """Factory property that returns an instance of the PatternFlowGtpv2SequenceNumberCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowGtpv2SequenceNumberCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowGtpv2SequenceNumberCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowGtpv2SequenceNumberCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowGtpv2Spare2(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowGtpv2Spare2Counter',
        'decrement': 'PatternFlowGtpv2Spare2Counter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowGtpv2Spare2, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowGtpv2Spare2Counter
        """Factory property that returns an instance of the PatternFlowGtpv2Spare2Counter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowGtpv2Spare2Counter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowGtpv2Spare2Counter
        """Factory property that returns an instance of the PatternFlowGtpv2Spare2Counter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowGtpv2Spare2Counter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowGtpv2Spare2Counter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowGtpv2Spare2Counter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class FlowArp(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'hardware_type': 'PatternFlowArpHardwareType',
        'protocol_type': 'PatternFlowArpProtocolType',
        'hardware_length': 'PatternFlowArpHardwareLength',
        'protocol_length': 'PatternFlowArpProtocolLength',
        'operation': 'PatternFlowArpOperation',
        'sender_hardware_addr': 'PatternFlowArpSenderHardwareAddr',
        'sender_protocol_addr': 'PatternFlowArpSenderProtocolAddr',
        'target_hardware_addr': 'PatternFlowArpTargetHardwareAddr',
        'target_protocol_addr': 'PatternFlowArpTargetProtocolAddr',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowArp, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def hardware_type(self):
        # type: () -> PatternFlowArpHardwareType
        """hardware_type getter

        Network link protocol typeNetwork link protocol type

        Returns: obj(snappi.PatternFlowArpHardwareType)
        """
        return self._get_property('hardware_type', PatternFlowArpHardwareType)

    @property
    def protocol_type(self):
        # type: () -> PatternFlowArpProtocolType
        """protocol_type getter

        The internetwork protocol for which the ARP request is intendedThe internetwork protocol for which the ARP request is intended

        Returns: obj(snappi.PatternFlowArpProtocolType)
        """
        return self._get_property('protocol_type', PatternFlowArpProtocolType)

    @property
    def hardware_length(self):
        # type: () -> PatternFlowArpHardwareLength
        """hardware_length getter

        Length (in octets) of a hardware addressLength (in octets) of a hardware address

        Returns: obj(snappi.PatternFlowArpHardwareLength)
        """
        return self._get_property('hardware_length', PatternFlowArpHardwareLength)

    @property
    def protocol_length(self):
        # type: () -> PatternFlowArpProtocolLength
        """protocol_length getter

        Length (in octets) of internetwork addressesLength (in octets) of internetwork addresses

        Returns: obj(snappi.PatternFlowArpProtocolLength)
        """
        return self._get_property('protocol_length', PatternFlowArpProtocolLength)

    @property
    def operation(self):
        # type: () -> PatternFlowArpOperation
        """operation getter

        The operation that the sender is performingThe operation that the sender is performing

        Returns: obj(snappi.PatternFlowArpOperation)
        """
        return self._get_property('operation', PatternFlowArpOperation)

    @property
    def sender_hardware_addr(self):
        # type: () -> PatternFlowArpSenderHardwareAddr
        """sender_hardware_addr getter

        Media address of the senderMedia address of the sender

        Returns: obj(snappi.PatternFlowArpSenderHardwareAddr)
        """
        return self._get_property('sender_hardware_addr', PatternFlowArpSenderHardwareAddr)

    @property
    def sender_protocol_addr(self):
        # type: () -> PatternFlowArpSenderProtocolAddr
        """sender_protocol_addr getter

        Internetwork address of the senderInternetwork address of the sender

        Returns: obj(snappi.PatternFlowArpSenderProtocolAddr)
        """
        return self._get_property('sender_protocol_addr', PatternFlowArpSenderProtocolAddr)

    @property
    def target_hardware_addr(self):
        # type: () -> PatternFlowArpTargetHardwareAddr
        """target_hardware_addr getter

        Media address of the targetMedia address of the target

        Returns: obj(snappi.PatternFlowArpTargetHardwareAddr)
        """
        return self._get_property('target_hardware_addr', PatternFlowArpTargetHardwareAddr)

    @property
    def target_protocol_addr(self):
        # type: () -> PatternFlowArpTargetProtocolAddr
        """target_protocol_addr getter

        Internetwork address of the targetInternetwork address of the target

        Returns: obj(snappi.PatternFlowArpTargetProtocolAddr)
        """
        return self._get_property('target_protocol_addr', PatternFlowArpTargetProtocolAddr)


class PatternFlowArpHardwareType(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowArpHardwareTypeCounter',
        'decrement': 'PatternFlowArpHardwareTypeCounter',
    }

    ETHERNET = '1'

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowArpHardwareType, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowArpHardwareTypeCounter
        """Factory property that returns an instance of the PatternFlowArpHardwareTypeCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowArpHardwareTypeCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowArpHardwareTypeCounter
        """Factory property that returns an instance of the PatternFlowArpHardwareTypeCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowArpHardwareTypeCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowArpHardwareTypeCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    ETHERNET = '1'

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowArpHardwareTypeCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowArpProtocolType(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowArpProtocolTypeCounter',
        'decrement': 'PatternFlowArpProtocolTypeCounter',
    }

    IPV4 = '2048'
    IPV6 = '34525'

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowArpProtocolType, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowArpProtocolTypeCounter
        """Factory property that returns an instance of the PatternFlowArpProtocolTypeCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowArpProtocolTypeCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowArpProtocolTypeCounter
        """Factory property that returns an instance of the PatternFlowArpProtocolTypeCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowArpProtocolTypeCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowArpProtocolTypeCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    IPV4 = '2048'
    IPV6 = '34525'

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowArpProtocolTypeCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowArpHardwareLength(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowArpHardwareLengthCounter',
        'decrement': 'PatternFlowArpHardwareLengthCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowArpHardwareLength, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowArpHardwareLengthCounter
        """Factory property that returns an instance of the PatternFlowArpHardwareLengthCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowArpHardwareLengthCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowArpHardwareLengthCounter
        """Factory property that returns an instance of the PatternFlowArpHardwareLengthCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowArpHardwareLengthCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowArpHardwareLengthCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowArpHardwareLengthCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowArpProtocolLength(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowArpProtocolLengthCounter',
        'decrement': 'PatternFlowArpProtocolLengthCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowArpProtocolLength, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowArpProtocolLengthCounter
        """Factory property that returns an instance of the PatternFlowArpProtocolLengthCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowArpProtocolLengthCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowArpProtocolLengthCounter
        """Factory property that returns an instance of the PatternFlowArpProtocolLengthCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowArpProtocolLengthCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowArpProtocolLengthCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowArpProtocolLengthCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowArpOperation(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowArpOperationCounter',
        'decrement': 'PatternFlowArpOperationCounter',
    }

    REQUEST = '1'
    REPLY = '2'

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowArpOperation, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowArpOperationCounter
        """Factory property that returns an instance of the PatternFlowArpOperationCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowArpOperationCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowArpOperationCounter
        """Factory property that returns an instance of the PatternFlowArpOperationCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowArpOperationCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowArpOperationCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    REQUEST = '1'
    REPLY = '2'

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowArpOperationCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowArpSenderHardwareAddr(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowArpSenderHardwareAddrCounter',
        'decrement': 'PatternFlowArpSenderHardwareAddrCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowArpSenderHardwareAddr, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowArpSenderHardwareAddrCounter
        """Factory property that returns an instance of the PatternFlowArpSenderHardwareAddrCounter class

        mac counter pattern
        """
        return self._get_property('increment', PatternFlowArpSenderHardwareAddrCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowArpSenderHardwareAddrCounter
        """Factory property that returns an instance of the PatternFlowArpSenderHardwareAddrCounter class

        mac counter pattern
        """
        return self._get_property('decrement', PatternFlowArpSenderHardwareAddrCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> str
        """value getter

        TBD

        Returns: str
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: str
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[str]
        """values getter

        TBD

        Returns: list[str]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[str]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowArpSenderHardwareAddrCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowArpSenderHardwareAddrCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> str
        """start getter

        TBD

        Returns: str
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: str
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> str
        """step getter

        TBD

        Returns: str
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: str
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowArpSenderProtocolAddr(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowArpSenderProtocolAddrCounter',
        'decrement': 'PatternFlowArpSenderProtocolAddrCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowArpSenderProtocolAddr, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowArpSenderProtocolAddrCounter
        """Factory property that returns an instance of the PatternFlowArpSenderProtocolAddrCounter class

        ipv4 counter pattern
        """
        return self._get_property('increment', PatternFlowArpSenderProtocolAddrCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowArpSenderProtocolAddrCounter
        """Factory property that returns an instance of the PatternFlowArpSenderProtocolAddrCounter class

        ipv4 counter pattern
        """
        return self._get_property('decrement', PatternFlowArpSenderProtocolAddrCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> str
        """value getter

        TBD

        Returns: str
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: str
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[str]
        """values getter

        TBD

        Returns: list[str]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[str]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowArpSenderProtocolAddrCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowArpSenderProtocolAddrCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> str
        """start getter

        TBD

        Returns: str
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: str
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> str
        """step getter

        TBD

        Returns: str
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: str
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowArpTargetHardwareAddr(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowArpTargetHardwareAddrCounter',
        'decrement': 'PatternFlowArpTargetHardwareAddrCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowArpTargetHardwareAddr, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowArpTargetHardwareAddrCounter
        """Factory property that returns an instance of the PatternFlowArpTargetHardwareAddrCounter class

        mac counter pattern
        """
        return self._get_property('increment', PatternFlowArpTargetHardwareAddrCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowArpTargetHardwareAddrCounter
        """Factory property that returns an instance of the PatternFlowArpTargetHardwareAddrCounter class

        mac counter pattern
        """
        return self._get_property('decrement', PatternFlowArpTargetHardwareAddrCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> str
        """value getter

        TBD

        Returns: str
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: str
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[str]
        """values getter

        TBD

        Returns: list[str]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[str]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowArpTargetHardwareAddrCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowArpTargetHardwareAddrCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> str
        """start getter

        TBD

        Returns: str
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: str
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> str
        """step getter

        TBD

        Returns: str
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: str
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowArpTargetProtocolAddr(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowArpTargetProtocolAddrCounter',
        'decrement': 'PatternFlowArpTargetProtocolAddrCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowArpTargetProtocolAddr, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowArpTargetProtocolAddrCounter
        """Factory property that returns an instance of the PatternFlowArpTargetProtocolAddrCounter class

        ipv4 counter pattern
        """
        return self._get_property('increment', PatternFlowArpTargetProtocolAddrCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowArpTargetProtocolAddrCounter
        """Factory property that returns an instance of the PatternFlowArpTargetProtocolAddrCounter class

        ipv4 counter pattern
        """
        return self._get_property('decrement', PatternFlowArpTargetProtocolAddrCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> str
        """value getter

        TBD

        Returns: str
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: str
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[str]
        """values getter

        TBD

        Returns: list[str]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[str]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowArpTargetProtocolAddrCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowArpTargetProtocolAddrCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> str
        """start getter

        TBD

        Returns: str
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: str
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> str
        """step getter

        TBD

        Returns: str
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: str
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class FlowIcmp(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'type': 'PatternFlowIcmpType',
        'code': 'PatternFlowIcmpCode',
        'checksum': 'PatternFlowIcmpChecksum',
        'rest_of_headers': 'PatternFlowIcmpRestOfHeaders',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowIcmp, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def type(self):
        # type: () -> PatternFlowIcmpType
        """type getter

        ICMP TypeICMP Type

        Returns: obj(snappi.PatternFlowIcmpType)
        """
        return self._get_property('type', PatternFlowIcmpType)

    @property
    def code(self):
        # type: () -> PatternFlowIcmpCode
        """code getter

        ICMP subtypeICMP subtype

        Returns: obj(snappi.PatternFlowIcmpCode)
        """
        return self._get_property('code', PatternFlowIcmpCode)

    @property
    def checksum(self):
        # type: () -> PatternFlowIcmpChecksum
        """checksum getter

        ICMP checksumICMP checksum

        Returns: obj(snappi.PatternFlowIcmpChecksum)
        """
        return self._get_property('checksum', PatternFlowIcmpChecksum)

    @property
    def rest_of_headers(self):
        # type: () -> PatternFlowIcmpRestOfHeaders
        """rest_of_headers getter

        Contents vary based on the ICMP type and codeContents vary based on the ICMP type and code

        Returns: obj(snappi.PatternFlowIcmpRestOfHeaders)
        """
        return self._get_property('rest_of_headers', PatternFlowIcmpRestOfHeaders)


class PatternFlowIcmpType(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIcmpTypeCounter',
        'decrement': 'PatternFlowIcmpTypeCounter',
    }

    ECHO_REPLY = '0'
    ECHO_REQUEST = '8'
    DESTINATION_UNREACHABLE = '3'
    SOURCE_QUENCH = '4'
    REDIRECT_MESSAGE = '5'
    TIME_EXCEEDED = '11'
    PARAMETER_PROBLEM = '12'
    TIMESTAMP = '13'
    TIMESTAMP_REPLY = '14'
    INFORMATION_REQUEST = '15'
    INFORMATION_REPLY = '16'

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIcmpType, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIcmpTypeCounter
        """Factory property that returns an instance of the PatternFlowIcmpTypeCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIcmpTypeCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIcmpTypeCounter
        """Factory property that returns an instance of the PatternFlowIcmpTypeCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIcmpTypeCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIcmpTypeCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    ECHO_REPLY = '0'
    ECHO_REQUEST = '8'
    DESTINATION_UNREACHABLE = '3'
    SOURCE_QUENCH = '4'
    REDIRECT_MESSAGE = '5'
    TIME_EXCEEDED = '11'
    PARAMETER_PROBLEM = '12'
    TIMESTAMP = '13'
    TIMESTAMP_REPLY = '14'
    INFORMATION_REQUEST = '15'
    INFORMATION_REPLY = '16'

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIcmpTypeCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIcmpCode(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIcmpCodeCounter',
        'decrement': 'PatternFlowIcmpCodeCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIcmpCode, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIcmpCodeCounter
        """Factory property that returns an instance of the PatternFlowIcmpCodeCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIcmpCodeCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIcmpCodeCounter
        """Factory property that returns an instance of the PatternFlowIcmpCodeCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIcmpCodeCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIcmpCodeCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIcmpCodeCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIcmpChecksum(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    GENERATED = 'generated'
    CUSTOM = 'custom'

    GOOD = 'good'
    BAD = 'bad'

    def __init__(self, parent=None, choice=None):
        super(PatternFlowIcmpChecksum, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def choice(self):
        # type: () -> Union[generated, custom, choice, choice, choice]
        """choice getter

        The type of checksum

        Returns: Union[generated, custom, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        The type of checksum

        value: Union[generated, custom, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def generated(self):
        # type: () -> Union[good, bad]
        """generated getter

        A system generated checksum value

        Returns: Union[good, bad]
        """
        return self._get_property('generated')

    @generated.setter
    def generated(self, value):
        """generated setter

        A system generated checksum value

        value: Union[good, bad]
        """
        self._set_property('generated', value, 'generated')

    @property
    def custom(self):
        # type: () -> int
        """custom getter

        A custom checksum value

        Returns: int
        """
        return self._get_property('custom')

    @custom.setter
    def custom(self, value):
        """custom setter

        A custom checksum value

        value: int
        """
        self._set_property('custom', value, 'custom')


class PatternFlowIcmpRestOfHeaders(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIcmpRestOfHeadersCounter',
        'decrement': 'PatternFlowIcmpRestOfHeadersCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIcmpRestOfHeaders, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIcmpRestOfHeadersCounter
        """Factory property that returns an instance of the PatternFlowIcmpRestOfHeadersCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIcmpRestOfHeadersCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIcmpRestOfHeadersCounter
        """Factory property that returns an instance of the PatternFlowIcmpRestOfHeadersCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIcmpRestOfHeadersCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIcmpRestOfHeadersCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIcmpRestOfHeadersCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class FlowIcmpv6(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'type': 'PatternFlowIcmpv6Type',
        'code': 'PatternFlowIcmpv6Code',
        'checksum': 'PatternFlowIcmpv6Checksum',
        'message_body': 'PatternFlowIcmpv6MessageBody',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowIcmpv6, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def type(self):
        # type: () -> PatternFlowIcmpv6Type
        """type getter

        ICMPv6 TypeICMPv6 Type

        Returns: obj(snappi.PatternFlowIcmpv6Type)
        """
        return self._get_property('type', PatternFlowIcmpv6Type)

    @property
    def code(self):
        # type: () -> PatternFlowIcmpv6Code
        """code getter

        ICMPv6 subtypeICMPv6 subtype

        Returns: obj(snappi.PatternFlowIcmpv6Code)
        """
        return self._get_property('code', PatternFlowIcmpv6Code)

    @property
    def checksum(self):
        # type: () -> PatternFlowIcmpv6Checksum
        """checksum getter

        ICMPv6 checksumICMPv6 checksum

        Returns: obj(snappi.PatternFlowIcmpv6Checksum)
        """
        return self._get_property('checksum', PatternFlowIcmpv6Checksum)

    @property
    def message_body(self):
        # type: () -> PatternFlowIcmpv6MessageBody
        """message_body getter

        Contents vary based on the ICMPv6 type and codeContents vary based on the ICMPv6 type and code

        Returns: obj(snappi.PatternFlowIcmpv6MessageBody)
        """
        return self._get_property('message_body', PatternFlowIcmpv6MessageBody)


class PatternFlowIcmpv6Type(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIcmpv6TypeCounter',
        'decrement': 'PatternFlowIcmpv6TypeCounter',
    }

    DESTINATION_UNREACHABLE = '1'
    PACKET_TOO_BIG = '2'
    TIME_EXCEEDED = '3'
    PARAMETER_PROBLEM = '4'
    ECHO_REPLY = '129'
    ECHO_REQUEST = '128'
    MULTICAST_LISTENER_QUERY = '130'

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIcmpv6Type, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIcmpv6TypeCounter
        """Factory property that returns an instance of the PatternFlowIcmpv6TypeCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIcmpv6TypeCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIcmpv6TypeCounter
        """Factory property that returns an instance of the PatternFlowIcmpv6TypeCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIcmpv6TypeCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIcmpv6TypeCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    DESTINATION_UNREACHABLE = '1'
    PACKET_TOO_BIG = '2'
    TIME_EXCEEDED = '3'
    PARAMETER_PROBLEM = '4'
    ECHO_REPLY = '129'
    ECHO_REQUEST = '128'
    MULTICAST_LISTENER_QUERY = '130'

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIcmpv6TypeCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIcmpv6Code(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIcmpv6CodeCounter',
        'decrement': 'PatternFlowIcmpv6CodeCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIcmpv6Code, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIcmpv6CodeCounter
        """Factory property that returns an instance of the PatternFlowIcmpv6CodeCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIcmpv6CodeCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIcmpv6CodeCounter
        """Factory property that returns an instance of the PatternFlowIcmpv6CodeCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIcmpv6CodeCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIcmpv6CodeCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIcmpv6CodeCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIcmpv6Checksum(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    GENERATED = 'generated'
    CUSTOM = 'custom'

    GOOD = 'good'
    BAD = 'bad'

    def __init__(self, parent=None, choice=None):
        super(PatternFlowIcmpv6Checksum, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def choice(self):
        # type: () -> Union[generated, custom, choice, choice, choice]
        """choice getter

        The type of checksum

        Returns: Union[generated, custom, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        The type of checksum

        value: Union[generated, custom, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def generated(self):
        # type: () -> Union[good, bad]
        """generated getter

        A system generated checksum value

        Returns: Union[good, bad]
        """
        return self._get_property('generated')

    @generated.setter
    def generated(self, value):
        """generated setter

        A system generated checksum value

        value: Union[good, bad]
        """
        self._set_property('generated', value, 'generated')

    @property
    def custom(self):
        # type: () -> int
        """custom getter

        A custom checksum value

        Returns: int
        """
        return self._get_property('custom')

    @custom.setter
    def custom(self, value):
        """custom setter

        A custom checksum value

        value: int
        """
        self._set_property('custom', value, 'custom')


class PatternFlowIcmpv6MessageBody(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIcmpv6MessageBodyCounter',
        'decrement': 'PatternFlowIcmpv6MessageBodyCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIcmpv6MessageBody, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIcmpv6MessageBodyCounter
        """Factory property that returns an instance of the PatternFlowIcmpv6MessageBodyCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIcmpv6MessageBodyCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIcmpv6MessageBodyCounter
        """Factory property that returns an instance of the PatternFlowIcmpv6MessageBodyCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIcmpv6MessageBodyCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIcmpv6MessageBodyCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIcmpv6MessageBodyCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class FlowPpp(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'address': 'PatternFlowPppAddress',
        'control': 'PatternFlowPppControl',
        'protocol_type': 'PatternFlowPppProtocolType',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowPpp, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def address(self):
        # type: () -> PatternFlowPppAddress
        """address getter

        PPP addressPPP address

        Returns: obj(snappi.PatternFlowPppAddress)
        """
        return self._get_property('address', PatternFlowPppAddress)

    @property
    def control(self):
        # type: () -> PatternFlowPppControl
        """control getter

        PPP controlPPP control

        Returns: obj(snappi.PatternFlowPppControl)
        """
        return self._get_property('control', PatternFlowPppControl)

    @property
    def protocol_type(self):
        # type: () -> PatternFlowPppProtocolType
        """protocol_type getter

        PPP protocol typePPP protocol type

        Returns: obj(snappi.PatternFlowPppProtocolType)
        """
        return self._get_property('protocol_type', PatternFlowPppProtocolType)


class PatternFlowPppAddress(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowPppAddressCounter',
        'decrement': 'PatternFlowPppAddressCounter',
    }

    STANDARD_ADDRESS = '255'

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowPppAddress, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowPppAddressCounter
        """Factory property that returns an instance of the PatternFlowPppAddressCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowPppAddressCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowPppAddressCounter
        """Factory property that returns an instance of the PatternFlowPppAddressCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowPppAddressCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowPppAddressCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    STANDARD_ADDRESS = '255'

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowPppAddressCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowPppControl(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowPppControlCounter',
        'decrement': 'PatternFlowPppControlCounter',
    }

    UNNUMBERED_DATA = '3'

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowPppControl, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowPppControlCounter
        """Factory property that returns an instance of the PatternFlowPppControlCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowPppControlCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowPppControlCounter
        """Factory property that returns an instance of the PatternFlowPppControlCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowPppControlCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowPppControlCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    UNNUMBERED_DATA = '3'

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowPppControlCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowPppProtocolType(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowPppProtocolTypeCounter',
        'decrement': 'PatternFlowPppProtocolTypeCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    AUTO = 'auto'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    AUTO = 'auto'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowPppProtocolType, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowPppProtocolTypeCounter
        """Factory property that returns an instance of the PatternFlowPppProtocolTypeCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowPppProtocolTypeCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowPppProtocolTypeCounter
        """Factory property that returns an instance of the PatternFlowPppProtocolTypeCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowPppProtocolTypeCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, auto, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, auto, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, auto, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def auto(self):
        # type: () -> Union[auto]
        """auto getter

        TBD

        Returns: Union[auto]
        """
        return self._get_property('auto')

    @auto.setter
    def auto(self, value):
        """auto setter

        TBD

        value: Union[auto]
        """
        self._set_property('auto', value, 'auto')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowPppProtocolTypeCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowPppProtocolTypeCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class FlowIgmpv1(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'version': 'PatternFlowIgmpv1Version',
        'type': 'PatternFlowIgmpv1Type',
        'unused': 'PatternFlowIgmpv1Unused',
        'checksum': 'PatternFlowIgmpv1Checksum',
        'group_address': 'PatternFlowIgmpv1GroupAddress',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowIgmpv1, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def version(self):
        # type: () -> PatternFlowIgmpv1Version
        """version getter

        Version numberVersion number

        Returns: obj(snappi.PatternFlowIgmpv1Version)
        """
        return self._get_property('version', PatternFlowIgmpv1Version)

    @property
    def type(self):
        # type: () -> PatternFlowIgmpv1Type
        """type getter

        Type of messageType of message

        Returns: obj(snappi.PatternFlowIgmpv1Type)
        """
        return self._get_property('type', PatternFlowIgmpv1Type)

    @property
    def unused(self):
        # type: () -> PatternFlowIgmpv1Unused
        """unused getter

        UnusedUnused

        Returns: obj(snappi.PatternFlowIgmpv1Unused)
        """
        return self._get_property('unused', PatternFlowIgmpv1Unused)

    @property
    def checksum(self):
        # type: () -> PatternFlowIgmpv1Checksum
        """checksum getter

        ChecksumChecksum

        Returns: obj(snappi.PatternFlowIgmpv1Checksum)
        """
        return self._get_property('checksum', PatternFlowIgmpv1Checksum)

    @property
    def group_address(self):
        # type: () -> PatternFlowIgmpv1GroupAddress
        """group_address getter

        Group addressGroup address

        Returns: obj(snappi.PatternFlowIgmpv1GroupAddress)
        """
        return self._get_property('group_address', PatternFlowIgmpv1GroupAddress)


class PatternFlowIgmpv1Version(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIgmpv1VersionCounter',
        'decrement': 'PatternFlowIgmpv1VersionCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIgmpv1Version, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIgmpv1VersionCounter
        """Factory property that returns an instance of the PatternFlowIgmpv1VersionCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIgmpv1VersionCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIgmpv1VersionCounter
        """Factory property that returns an instance of the PatternFlowIgmpv1VersionCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIgmpv1VersionCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIgmpv1VersionCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIgmpv1VersionCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIgmpv1Type(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIgmpv1TypeCounter',
        'decrement': 'PatternFlowIgmpv1TypeCounter',
    }

    QUERY = '17'
    REPORT = '18'

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIgmpv1Type, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIgmpv1TypeCounter
        """Factory property that returns an instance of the PatternFlowIgmpv1TypeCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIgmpv1TypeCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIgmpv1TypeCounter
        """Factory property that returns an instance of the PatternFlowIgmpv1TypeCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIgmpv1TypeCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIgmpv1TypeCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    QUERY = '17'
    REPORT = '18'

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIgmpv1TypeCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIgmpv1Unused(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIgmpv1UnusedCounter',
        'decrement': 'PatternFlowIgmpv1UnusedCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIgmpv1Unused, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIgmpv1UnusedCounter
        """Factory property that returns an instance of the PatternFlowIgmpv1UnusedCounter class

        integer counter pattern
        """
        return self._get_property('increment', PatternFlowIgmpv1UnusedCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIgmpv1UnusedCounter
        """Factory property that returns an instance of the PatternFlowIgmpv1UnusedCounter class

        integer counter pattern
        """
        return self._get_property('decrement', PatternFlowIgmpv1UnusedCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> int
        """value getter

        TBD

        Returns: int
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: int
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[int]
        """values getter

        TBD

        Returns: list[int]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[int]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIgmpv1UnusedCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIgmpv1UnusedCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> int
        """start getter

        TBD

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: int
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        TBD

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: int
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class PatternFlowIgmpv1Checksum(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    GENERATED = 'generated'
    CUSTOM = 'custom'

    GOOD = 'good'
    BAD = 'bad'

    def __init__(self, parent=None, choice=None):
        super(PatternFlowIgmpv1Checksum, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def choice(self):
        # type: () -> Union[generated, custom, choice, choice, choice]
        """choice getter

        The type of checksum

        Returns: Union[generated, custom, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        The type of checksum

        value: Union[generated, custom, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def generated(self):
        # type: () -> Union[good, bad]
        """generated getter

        A system generated checksum value

        Returns: Union[good, bad]
        """
        return self._get_property('generated')

    @generated.setter
    def generated(self, value):
        """generated setter

        A system generated checksum value

        value: Union[good, bad]
        """
        self._set_property('generated', value, 'generated')

    @property
    def custom(self):
        # type: () -> int
        """custom getter

        A custom checksum value

        Returns: int
        """
        return self._get_property('custom')

    @custom.setter
    def custom(self, value):
        """custom setter

        A custom checksum value

        value: int
        """
        self._set_property('custom', value, 'custom')


class PatternFlowIgmpv1GroupAddress(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'PatternFlowIgmpv1GroupAddressCounter',
        'decrement': 'PatternFlowIgmpv1GroupAddressCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(PatternFlowIgmpv1GroupAddress, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> PatternFlowIgmpv1GroupAddressCounter
        """Factory property that returns an instance of the PatternFlowIgmpv1GroupAddressCounter class

        ipv4 counter pattern
        """
        return self._get_property('increment', PatternFlowIgmpv1GroupAddressCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> PatternFlowIgmpv1GroupAddressCounter
        """Factory property that returns an instance of the PatternFlowIgmpv1GroupAddressCounter class

        ipv4 counter pattern
        """
        return self._get_property('decrement', PatternFlowIgmpv1GroupAddressCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> str
        """value getter

        TBD

        Returns: str
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: str
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[str]
        """values getter

        TBD

        Returns: list[str]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[str]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class PatternFlowIgmpv1GroupAddressCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(PatternFlowIgmpv1GroupAddressCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> str
        """start getter

        TBD

        Returns: str
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: str
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> str
        """step getter

        TBD

        Returns: str
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: str
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)


class FlowHeaderIter(SnappiIter):
    __slots__ = ()

    def __init__(self):
        super(FlowHeaderIter, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[FlowPpp, FlowArp, FlowEthernet, FlowGtpv1, FlowEthernetPause, FlowTcp, FlowIcmp, FlowIpv6, FlowHeader, FlowIcmpv6, FlowPfcPause, FlowVxlan, FlowGre, FlowUdp, FlowIpv4, FlowIgmpv1, FlowGtpv2, FlowVlan, FlowCustom]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> FlowHeaderIter
        return self._iter()

    def __next__(self):
        # type: () -> FlowHeader
        return self._next()

    def next(self):
        # type: () -> FlowHeader
        return self._next()

    def header(self):
        # type: () -> FlowHeaderIter
        """Factory method that creates an instance of FlowHeader class

        Container for all traffic packet headers
        """
        item = FlowHeader()
        self._add(item)
        return self

    def custom(self, bytes=None):
        # type: () -> FlowHeaderIter
        """Factory method that creates an instance of FlowCustom class

        Custom packet header
        """
        item = FlowHeader()
        item.custom
        item.choice = 'custom'
        self._add(item)
        return self

    def ethernet(self):
        # type: () -> FlowHeaderIter
        """Factory method that creates an instance of FlowEthernet class

        Ethernet packet header
        """
        item = FlowHeader()
        item.ethernet
        item.choice = 'ethernet'
        self._add(item)
        return self

    def vlan(self):
        # type: () -> FlowHeaderIter
        """Factory method that creates an instance of FlowVlan class

        VLAN packet header
        """
        item = FlowHeader()
        item.vlan
        item.choice = 'vlan'
        self._add(item)
        return self

    def vxlan(self):
        # type: () -> FlowHeaderIter
        """Factory method that creates an instance of FlowVxlan class

        VXLAN packet header
        """
        item = FlowHeader()
        item.vxlan
        item.choice = 'vxlan'
        self._add(item)
        return self

    def ipv4(self):
        # type: () -> FlowHeaderIter
        """Factory method that creates an instance of FlowIpv4 class

        IPv4 packet header
        """
        item = FlowHeader()
        item.ipv4
        item.choice = 'ipv4'
        self._add(item)
        return self

    def ipv6(self):
        # type: () -> FlowHeaderIter
        """Factory method that creates an instance of FlowIpv6 class

        IPv6 packet header
        """
        item = FlowHeader()
        item.ipv6
        item.choice = 'ipv6'
        self._add(item)
        return self

    def pfcpause(self):
        # type: () -> FlowHeaderIter
        """Factory method that creates an instance of FlowPfcPause class

        IEEE 802.1Qbb PFC Pause packet header.
        """
        item = FlowHeader()
        item.pfcpause
        item.choice = 'pfcpause'
        self._add(item)
        return self

    def ethernetpause(self):
        # type: () -> FlowHeaderIter
        """Factory method that creates an instance of FlowEthernetPause class

        IEEE 802.3x global ethernet pause packet header
        """
        item = FlowHeader()
        item.ethernetpause
        item.choice = 'ethernetpause'
        self._add(item)
        return self

    def tcp(self):
        # type: () -> FlowHeaderIter
        """Factory method that creates an instance of FlowTcp class

        TCP packet header
        """
        item = FlowHeader()
        item.tcp
        item.choice = 'tcp'
        self._add(item)
        return self

    def udp(self):
        # type: () -> FlowHeaderIter
        """Factory method that creates an instance of FlowUdp class

        UDP packet header
        """
        item = FlowHeader()
        item.udp
        item.choice = 'udp'
        self._add(item)
        return self

    def gre(self):
        # type: () -> FlowHeaderIter
        """Factory method that creates an instance of FlowGre class

        Standard GRE packet header (RFC2784)
        """
        item = FlowHeader()
        item.gre
        item.choice = 'gre'
        self._add(item)
        return self

    def gtpv1(self):
        # type: () -> FlowHeaderIter
        """Factory method that creates an instance of FlowGtpv1 class

        GTPv1 packet header
        """
        item = FlowHeader()
        item.gtpv1
        item.choice = 'gtpv1'
        self._add(item)
        return self

    def gtpv2(self):
        # type: () -> FlowHeaderIter
        """Factory method that creates an instance of FlowGtpv2 class

        GTPv2 packet header
        """
        item = FlowHeader()
        item.gtpv2
        item.choice = 'gtpv2'
        self._add(item)
        return self

    def arp(self):
        # type: () -> FlowHeaderIter
        """Factory method that creates an instance of FlowArp class

        ARP packet header
        """
        item = FlowHeader()
        item.arp
        item.choice = 'arp'
        self._add(item)
        return self

    def icmp(self):
        # type: () -> FlowHeaderIter
        """Factory method that creates an instance of FlowIcmp class

        ICMP packet header
        """
        item = FlowHeader()
        item.icmp
        item.choice = 'icmp'
        self._add(item)
        return self

    def icmpv6(self):
        # type: () -> FlowHeaderIter
        """Factory method that creates an instance of FlowIcmpv6 class

        ICMPv6 packet header
        """
        item = FlowHeader()
        item.icmpv6
        item.choice = 'icmpv6'
        self._add(item)
        return self

    def ppp(self):
        # type: () -> FlowHeaderIter
        """Factory method that creates an instance of FlowPpp class

        PPP packet header
        """
        item = FlowHeader()
        item.ppp
        item.choice = 'ppp'
        self._add(item)
        return self

    def igmpv1(self):
        # type: () -> FlowHeaderIter
        """Factory method that creates an instance of FlowIgmpv1 class

        IGMPv1 packet header
        """
        item = FlowHeader()
        item.igmpv1
        item.choice = 'igmpv1'
        self._add(item)
        return self


class FlowSize(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'FlowSizeIncrement',
        'random': 'FlowSizeRandom',
    }

    FIXED = 'fixed'
    INCREMENT = 'increment'
    RANDOM = 'random'

    def __init__(self, parent=None, choice=None):
        super(FlowSize, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def increment(self):
        # type: () -> FlowSizeIncrement
        """Factory property that returns an instance of the FlowSizeIncrement class

        Frame size that increments from a starting size to an ending size incrementing by a step size.
        """
        return self._get_property('increment', FlowSizeIncrement(self, 'increment'))

    @property
    def random(self):
        # type: () -> FlowSizeRandom
        """Factory property that returns an instance of the FlowSizeRandom class

        Random frame size from a min value to a max value.
        """
        return self._get_property('random', FlowSizeRandom(self, 'random'))

    @property
    def choice(self):
        # type: () -> Union[fixed, increment, random, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[fixed, increment, random, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[fixed, increment, random, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def fixed(self):
        # type: () -> int
        """fixed getter

        TBD

        Returns: int
        """
        return self._get_property('fixed')

    @fixed.setter
    def fixed(self, value):
        """fixed setter

        TBD

        value: int
        """
        self._set_property('fixed', value, 'fixed')


class FlowSizeIncrement(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, end=None, step=None):
        super(FlowSizeIncrement, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('end', end)
        self._set_property('step', step)

    @property
    def start(self):
        # type: () -> int
        """start getter

        Starting frame size in bytes

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        Starting frame size in bytes

        value: int
        """
        self._set_property('start', value)

    @property
    def end(self):
        # type: () -> int
        """end getter

        Ending frame size in bytes

        Returns: int
        """
        return self._get_property('end')

    @end.setter
    def end(self, value):
        """end setter

        Ending frame size in bytes

        value: int
        """
        self._set_property('end', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        Step frame size in bytes

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        Step frame size in bytes

        value: int
        """
        self._set_property('step', value)


class FlowSizeRandom(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, min=None, max=None):
        super(FlowSizeRandom, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('min', min)
        self._set_property('max', max)

    @property
    def min(self):
        # type: () -> int
        """min getter

        TBD

        Returns: int
        """
        return self._get_property('min')

    @min.setter
    def min(self, value):
        """min setter

        TBD

        value: int
        """
        self._set_property('min', value)

    @property
    def max(self):
        # type: () -> int
        """max getter

        TBD

        Returns: int
        """
        return self._get_property('max')

    @max.setter
    def max(self, value):
        """max setter

        TBD

        value: int
        """
        self._set_property('max', value)


class FlowRate(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    PPS = 'pps'
    BPS = 'bps'
    KBPS = 'kbps'
    MBPS = 'mbps'
    GBPS = 'gbps'
    PERCENTAGE = 'percentage'

    def __init__(self, parent=None, choice=None):
        super(FlowRate, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def choice(self):
        # type: () -> Union[pps, bps, kbps, mbps, gbps, percentage, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[pps, bps, kbps, mbps, gbps, percentage, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[pps, bps, kbps, mbps, gbps, percentage, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def pps(self):
        # type: () -> int
        """pps getter

        Packets per second.

        Returns: int
        """
        return self._get_property('pps')

    @pps.setter
    def pps(self, value):
        """pps setter

        Packets per second.

        value: int
        """
        self._set_property('pps', value, 'pps')

    @property
    def bps(self):
        # type: () -> int
        """bps getter

        Bits per second.

        Returns: int
        """
        return self._get_property('bps')

    @bps.setter
    def bps(self, value):
        """bps setter

        Bits per second.

        value: int
        """
        self._set_property('bps', value, 'bps')

    @property
    def kbps(self):
        # type: () -> int
        """kbps getter

        Kilobits per second.

        Returns: int
        """
        return self._get_property('kbps')

    @kbps.setter
    def kbps(self, value):
        """kbps setter

        Kilobits per second.

        value: int
        """
        self._set_property('kbps', value, 'kbps')

    @property
    def mbps(self):
        # type: () -> int
        """mbps getter

        Megabits per second.

        Returns: int
        """
        return self._get_property('mbps')

    @mbps.setter
    def mbps(self, value):
        """mbps setter

        Megabits per second.

        value: int
        """
        self._set_property('mbps', value, 'mbps')

    @property
    def gbps(self):
        # type: () -> int
        """gbps getter

        Gigabits per second.

        Returns: int
        """
        return self._get_property('gbps')

    @gbps.setter
    def gbps(self, value):
        """gbps setter

        Gigabits per second.

        value: int
        """
        self._set_property('gbps', value, 'gbps')

    @property
    def percentage(self):
        # type: () -> float
        """percentage getter

        The percentage of a port location's available bandwidth.

        Returns: float
        """
        return self._get_property('percentage')

    @percentage.setter
    def percentage(self, value):
        """percentage setter

        The percentage of a port location's available bandwidth.

        value: float
        """
        self._set_property('percentage', value, 'percentage')


class FlowDuration(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'fixed_packets': 'FlowFixedPackets',
        'fixed_seconds': 'FlowFixedSeconds',
        'burst': 'FlowBurst',
        'continuous': 'FlowContinuous',
    }

    FIXED_PACKETS = 'fixed_packets'
    FIXED_SECONDS = 'fixed_seconds'
    BURST = 'burst'
    CONTINUOUS = 'continuous'

    def __init__(self, parent=None, choice=None):
        super(FlowDuration, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def fixed_packets(self):
        # type: () -> FlowFixedPackets
        """Factory property that returns an instance of the FlowFixedPackets class

        Transmit a fixed number of packets after which the flow will stop.
        """
        return self._get_property('fixed_packets', FlowFixedPackets(self, 'fixed_packets'))

    @property
    def fixed_seconds(self):
        # type: () -> FlowFixedSeconds
        """Factory property that returns an instance of the FlowFixedSeconds class

        Transmit for a fixed number of seconds after which the flow will stop.
        """
        return self._get_property('fixed_seconds', FlowFixedSeconds(self, 'fixed_seconds'))

    @property
    def burst(self):
        # type: () -> FlowBurst
        """Factory property that returns an instance of the FlowBurst class

        Transmits continuous or fixed burst of packets. For continuous burst of packets, it will not automatically stop. For fixed burst of packets, it will stop after transmitting fixed number of bursts. 
        """
        return self._get_property('burst', FlowBurst(self, 'burst'))

    @property
    def continuous(self):
        # type: () -> FlowContinuous
        """Factory property that returns an instance of the FlowContinuous class

        Transmit will be continuous and will not stop automatically. 
        """
        return self._get_property('continuous', FlowContinuous(self, 'continuous'))

    @property
    def choice(self):
        # type: () -> Union[fixed_packets, fixed_seconds, burst, continuous, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[fixed_packets, fixed_seconds, burst, continuous, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[fixed_packets, fixed_seconds, burst, continuous, choice, choice, choice]
        """
        self._set_property('choice', value)


class FlowFixedPackets(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    BYTES = 'bytes'
    NANOSECONDS = 'nanoseconds'

    def __init__(self, parent=None, choice=None, packets=None, gap=None, delay=None, delay_unit=None):
        super(FlowFixedPackets, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('packets', packets)
        self._set_property('gap', gap)
        self._set_property('delay', delay)
        self._set_property('delay_unit', delay_unit)

    @property
    def packets(self):
        # type: () -> int
        """packets getter

        Stop transmit of the flow after this number of packets.

        Returns: int
        """
        return self._get_property('packets')

    @packets.setter
    def packets(self, value):
        """packets setter

        Stop transmit of the flow after this number of packets.

        value: int
        """
        self._set_property('packets', value)

    @property
    def gap(self):
        # type: () -> int
        """gap getter

        The minimum gap between packets expressed as bytes.

        Returns: int
        """
        return self._get_property('gap')

    @gap.setter
    def gap(self, value):
        """gap setter

        The minimum gap between packets expressed as bytes.

        value: int
        """
        self._set_property('gap', value)

    @property
    def delay(self):
        # type: () -> int
        """delay getter

        The delay before starting transmission of packets.

        Returns: int
        """
        return self._get_property('delay')

    @delay.setter
    def delay(self, value):
        """delay setter

        The delay before starting transmission of packets.

        value: int
        """
        self._set_property('delay', value)

    @property
    def delay_unit(self):
        # type: () -> Union[bytes, nanoseconds]
        """delay_unit getter

        The delay expressed as a number of this value.

        Returns: Union[bytes, nanoseconds]
        """
        return self._get_property('delay_unit')

    @delay_unit.setter
    def delay_unit(self, value):
        """delay_unit setter

        The delay expressed as a number of this value.

        value: Union[bytes, nanoseconds]
        """
        self._set_property('delay_unit', value)


class FlowFixedSeconds(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    BYTES = 'bytes'
    NANOSECONDS = 'nanoseconds'

    def __init__(self, parent=None, choice=None, seconds=None, gap=None, delay=None, delay_unit=None):
        super(FlowFixedSeconds, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('seconds', seconds)
        self._set_property('gap', gap)
        self._set_property('delay', delay)
        self._set_property('delay_unit', delay_unit)

    @property
    def seconds(self):
        # type: () -> float
        """seconds getter

        Stop transmit of the flow after this number of seconds.

        Returns: float
        """
        return self._get_property('seconds')

    @seconds.setter
    def seconds(self, value):
        """seconds setter

        Stop transmit of the flow after this number of seconds.

        value: float
        """
        self._set_property('seconds', value)

    @property
    def gap(self):
        # type: () -> int
        """gap getter

        The minimum gap between packets expressed as bytes.

        Returns: int
        """
        return self._get_property('gap')

    @gap.setter
    def gap(self, value):
        """gap setter

        The minimum gap between packets expressed as bytes.

        value: int
        """
        self._set_property('gap', value)

    @property
    def delay(self):
        # type: () -> int
        """delay getter

        The delay before starting transmission of packets.

        Returns: int
        """
        return self._get_property('delay')

    @delay.setter
    def delay(self, value):
        """delay setter

        The delay before starting transmission of packets.

        value: int
        """
        self._set_property('delay', value)

    @property
    def delay_unit(self):
        # type: () -> Union[bytes, nanoseconds]
        """delay_unit getter

        The delay expressed as a number of this value.

        Returns: Union[bytes, nanoseconds]
        """
        return self._get_property('delay_unit')

    @delay_unit.setter
    def delay_unit(self, value):
        """delay_unit setter

        The delay expressed as a number of this value.

        value: Union[bytes, nanoseconds]
        """
        self._set_property('delay_unit', value)


class FlowBurst(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    BYTES = 'bytes'
    NANOSECONDS = 'nanoseconds'

    def __init__(self, parent=None, choice=None, bursts=None, packets=None, gap=None, inter_burst_gap=None, inter_burst_gap_unit=None):
        super(FlowBurst, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('bursts', bursts)
        self._set_property('packets', packets)
        self._set_property('gap', gap)
        self._set_property('inter_burst_gap', inter_burst_gap)
        self._set_property('inter_burst_gap_unit', inter_burst_gap_unit)

    @property
    def bursts(self):
        # type: () -> int
        """bursts getter

        The number of packet bursts transmitted per flow. A value of 0 implies continuous burst of packets.

        Returns: int
        """
        return self._get_property('bursts')

    @bursts.setter
    def bursts(self, value):
        """bursts setter

        The number of packet bursts transmitted per flow. A value of 0 implies continuous burst of packets.

        value: int
        """
        self._set_property('bursts', value)

    @property
    def packets(self):
        # type: () -> int
        """packets getter

        The number of packets transmitted per burst.

        Returns: int
        """
        return self._get_property('packets')

    @packets.setter
    def packets(self, value):
        """packets setter

        The number of packets transmitted per burst.

        value: int
        """
        self._set_property('packets', value)

    @property
    def gap(self):
        # type: () -> int
        """gap getter

        The minimum gap between packets expressed as bytes.

        Returns: int
        """
        return self._get_property('gap')

    @gap.setter
    def gap(self, value):
        """gap setter

        The minimum gap between packets expressed as bytes.

        value: int
        """
        self._set_property('gap', value)

    @property
    def inter_burst_gap(self):
        # type: () -> int
        """inter_burst_gap getter

        The gap between the transmission of each burst. A value of 0 means there is no gap between bursts.

        Returns: int
        """
        return self._get_property('inter_burst_gap')

    @inter_burst_gap.setter
    def inter_burst_gap(self, value):
        """inter_burst_gap setter

        The gap between the transmission of each burst. A value of 0 means there is no gap between bursts.

        value: int
        """
        self._set_property('inter_burst_gap', value)

    @property
    def inter_burst_gap_unit(self):
        # type: () -> Union[bytes, nanoseconds]
        """inter_burst_gap_unit getter

        The inter burst gap expressed as a number of this value.

        Returns: Union[bytes, nanoseconds]
        """
        return self._get_property('inter_burst_gap_unit')

    @inter_burst_gap_unit.setter
    def inter_burst_gap_unit(self, value):
        """inter_burst_gap_unit setter

        The inter burst gap expressed as a number of this value.

        value: Union[bytes, nanoseconds]
        """
        self._set_property('inter_burst_gap_unit', value)


class FlowContinuous(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    BYTES = 'bytes'
    NANOSECONDS = 'nanoseconds'

    def __init__(self, parent=None, choice=None, gap=None, delay=None, delay_unit=None):
        super(FlowContinuous, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('gap', gap)
        self._set_property('delay', delay)
        self._set_property('delay_unit', delay_unit)

    @property
    def gap(self):
        # type: () -> int
        """gap getter

        The minimum gap between packets expressed as bytes.

        Returns: int
        """
        return self._get_property('gap')

    @gap.setter
    def gap(self, value):
        """gap setter

        The minimum gap between packets expressed as bytes.

        value: int
        """
        self._set_property('gap', value)

    @property
    def delay(self):
        # type: () -> int
        """delay getter

        The delay before starting transmission of packets.

        Returns: int
        """
        return self._get_property('delay')

    @delay.setter
    def delay(self, value):
        """delay setter

        The delay before starting transmission of packets.

        value: int
        """
        self._set_property('delay', value)

    @property
    def delay_unit(self):
        # type: () -> Union[bytes, nanoseconds]
        """delay_unit getter

        The delay expressed as a number of this value.

        Returns: Union[bytes, nanoseconds]
        """
        return self._get_property('delay_unit')

    @delay_unit.setter
    def delay_unit(self, value):
        """delay_unit setter

        The delay expressed as a number of this value.

        value: Union[bytes, nanoseconds]
        """
        self._set_property('delay_unit', value)


class FlowIter(SnappiIter):
    __slots__ = ()

    def __init__(self):
        super(FlowIter, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[Flow]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> FlowIter
        return self._iter()

    def __next__(self):
        # type: () -> Flow
        return self._next()

    def next(self):
        # type: () -> Flow
        return self._next()

    def flow(self, name=None):
        # type: () -> FlowIter
        """Factory method that creates an instance of Flow class

        A high level data plane traffic flow. Acts as a container for endpoints, packet headers, packet size, transmit rate and transmit duration.
        """
        item = Flow(name=name)
        self._add(item)
        return self


class ConfigOptions(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'port_options': 'PortOptions',
    }

    def __init__(self, parent=None, choice=None):
        super(ConfigOptions, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def port_options(self):
        # type: () -> PortOptions
        """port_options getter

        Common port options that apply to all configured Port objects. 

        Returns: obj(snappi.PortOptions)
        """
        return self._get_property('port_options', PortOptions)


class PortOptions(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, location_preemption=None):
        super(PortOptions, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('location_preemption', location_preemption)

    @property
    def location_preemption(self):
        # type: () -> boolean
        """location_preemption getter

        Preempt all the test port locations as defined by the Port.Port.properties.location. If the test ports defined by their location values are in use and this value is true, the test ports will be preempted.

        Returns: boolean
        """
        return self._get_property('location_preemption')

    @location_preemption.setter
    def location_preemption(self, value):
        """location_preemption setter

        Preempt all the test port locations as defined by the Port.Port.properties.location. If the test ports defined by their location values are in use and this value is true, the test ports will be preempted.

        value: boolean
        """
        self._set_property('location_preemption', value)


class Details(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, errors=None, warnings=None):
        super(Details, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('errors', errors)
        self._set_property('warnings', warnings)

    @property
    def errors(self):
        # type: () -> list[str]
        """errors getter

        A list of any errors that may have occurred while executing the request.

        Returns: list[str]
        """
        return self._get_property('errors')

    @errors.setter
    def errors(self, value):
        """errors setter

        A list of any errors that may have occurred while executing the request.

        value: list[str]
        """
        self._set_property('errors', value)

    @property
    def warnings(self):
        # type: () -> list[str]
        """warnings getter

        A list of any warnings generated while executing the request.

        Returns: list[str]
        """
        return self._get_property('warnings')

    @warnings.setter
    def warnings(self, value):
        """warnings setter

        A list of any warnings generated while executing the request.

        value: list[str]
        """
        self._set_property('warnings', value)


class TransmitState(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    START = 'start'
    STOP = 'stop'
    PAUSE = 'pause'

    def __init__(self, parent=None, choice=None, flow_names=None, state=None):
        super(TransmitState, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('flow_names', flow_names)
        self._set_property('state', state)

    @property
    def flow_names(self):
        # type: () -> list[str]
        """flow_names getter

        The names of flows to which the transmit state will be applied to. If the list of flow_names is empty or null the state will be applied to all configured flows.

        Returns: list[str]
        """
        return self._get_property('flow_names')

    @flow_names.setter
    def flow_names(self, value):
        """flow_names setter

        The names of flows to which the transmit state will be applied to. If the list of flow_names is empty or null the state will be applied to all configured flows.

        value: list[str]
        """
        self._set_property('flow_names', value)

    @property
    def state(self):
        # type: () -> Union[start, stop, pause]
        """state getter

        The transmit state.

        Returns: Union[start, stop, pause]
        """
        return self._get_property('state')

    @state.setter
    def state(self, value):
        """state setter

        The transmit state.

        value: Union[start, stop, pause]
        """
        self._set_property('state', value)


class LinkState(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    UP = 'up'
    DOWN = 'down'

    def __init__(self, parent=None, choice=None, port_names=None, state=None):
        super(LinkState, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('port_names', port_names)
        self._set_property('state', state)

    @property
    def port_names(self):
        # type: () -> list[str]
        """port_names getter

        The names of port objects to. An empty or null list will control all port objects.

        Returns: list[str]
        """
        return self._get_property('port_names')

    @port_names.setter
    def port_names(self, value):
        """port_names setter

        The names of port objects to. An empty or null list will control all port objects.

        value: list[str]
        """
        self._set_property('port_names', value)

    @property
    def state(self):
        # type: () -> Union[up, down]
        """state getter

        The link state.

        Returns: Union[up, down]
        """
        return self._get_property('state')

    @state.setter
    def state(self, value):
        """state setter

        The link state.

        value: Union[up, down]
        """
        self._set_property('state', value)


class CaptureState(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    START = 'start'
    STOP = 'stop'

    def __init__(self, parent=None, choice=None, port_names=None, state=None):
        super(CaptureState, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('port_names', port_names)
        self._set_property('state', state)

    @property
    def port_names(self):
        # type: () -> list[str]
        """port_names getter

        The name of ports to start capturing packets on. An empty or null list will control all port objects.

        Returns: list[str]
        """
        return self._get_property('port_names')

    @port_names.setter
    def port_names(self, value):
        """port_names setter

        The name of ports to start capturing packets on. An empty or null list will control all port objects.

        value: list[str]
        """
        self._set_property('port_names', value)

    @property
    def state(self):
        # type: () -> Union[start, stop]
        """state getter

        The capture state.

        Returns: Union[start, stop]
        """
        return self._get_property('state')

    @state.setter
    def state(self, value):
        """state setter

        The capture state.

        value: Union[start, stop]
        """
        self._set_property('state', value)


class MetricsRequest(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'port': 'PortMetricsRequest',
        'flow': 'FlowMetricsRequest',
        'bgpv4': 'Bgpv4MetricsRequest',
        'bgpv6': 'Bgpv6MetricsRequest',
    }

    PORT = 'port'
    FLOW = 'flow'
    BGPV4 = 'bgpv4'
    BGPV6 = 'bgpv6'

    def __init__(self, parent=None, choice=None):
        super(MetricsRequest, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def port(self):
        # type: () -> PortMetricsRequest
        """Factory property that returns an instance of the PortMetricsRequest class

        The port result request to the traffic generator
        """
        return self._get_property('port', PortMetricsRequest(self, 'port'))

    @property
    def flow(self):
        # type: () -> FlowMetricsRequest
        """Factory property that returns an instance of the FlowMetricsRequest class

        The request to the traffic generator for flow results.
        """
        return self._get_property('flow', FlowMetricsRequest(self, 'flow'))

    @property
    def bgpv4(self):
        # type: () -> Bgpv4MetricsRequest
        """Factory property that returns an instance of the Bgpv4MetricsRequest class

        The request to retrieve BGPv4 Router statistics and learned routing information
        """
        return self._get_property('bgpv4', Bgpv4MetricsRequest(self, 'bgpv4'))

    @property
    def bgpv6(self):
        # type: () -> Bgpv6MetricsRequest
        """Factory property that returns an instance of the Bgpv6MetricsRequest class

        The request to retrieve BGPv6 Router statistics and learned routing information
        """
        return self._get_property('bgpv6', Bgpv6MetricsRequest(self, 'bgpv6'))

    @property
    def choice(self):
        # type: () -> Union[port, flow, bgpv4, bgpv6, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[port, flow, bgpv4, bgpv6, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[port, flow, bgpv4, bgpv6, choice, choice, choice]
        """
        self._set_property('choice', value)


class PortMetricsRequest(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    TRANSMIT = 'transmit'
    LOCATION = 'location'
    LINK = 'link'
    CAPTURE = 'capture'
    FRAMES_TX = 'frames_tx'
    FRAMES_RX = 'frames_rx'
    BYTES_TX = 'bytes_tx'
    BYTES_RX = 'bytes_rx'
    FRAMES_TX_RATE = 'frames_tx_rate'
    FRAMES_RX_RATE = 'frames_rx_rate'
    BYTES_TX_RATE = 'bytes_tx_rate'
    BYTES_RX_RATE = 'bytes_rx_rate'

    def __init__(self, parent=None, choice=None, port_names=None, column_names=None):
        super(PortMetricsRequest, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('port_names', port_names)
        self._set_property('column_names', column_names)

    @property
    def port_names(self):
        # type: () -> list[str]
        """port_names getter

        The names of objects to return results for. An empty list will return all port row results.

        Returns: list[str]
        """
        return self._get_property('port_names')

    @port_names.setter
    def port_names(self, value):
        """port_names setter

        The names of objects to return results for. An empty list will return all port row results.

        value: list[str]
        """
        self._set_property('port_names', value)

    @property
    def column_names(self):
        # type: () -> list[Union[transmit, location, link, capture, frames_tx, frames_rx, bytes_tx, bytes_rx, frames_tx_rate, frames_rx_rate, bytes_tx_rate, bytes_rx_rate]]
        """column_names getter

        The list of column names that the returned result set will contain. If the list is empty then all columns will be returned. The name of the port cannot be excluded.

        Returns: list[Union[transmit, location, link, capture, frames_tx, frames_rx, bytes_tx, bytes_rx, frames_tx_rate, frames_rx_rate, bytes_tx_rate, bytes_rx_rate]]
        """
        return self._get_property('column_names')

    @column_names.setter
    def column_names(self, value):
        """column_names setter

        The list of column names that the returned result set will contain. If the list is empty then all columns will be returned. The name of the port cannot be excluded.

        value: list[Union[transmit, location, link, capture, frames_tx, frames_rx, bytes_tx, bytes_rx, frames_tx_rate, frames_rx_rate, bytes_tx_rate, bytes_rx_rate]]
        """
        self._set_property('column_names', value)


class FlowMetricsRequest(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    TRANSMIT = 'transmit'
    PORT_TX = 'port_tx'
    PORT_RX = 'port_rx'
    FRAMES_TX = 'frames_tx'
    FRAMES_RX = 'frames_rx'
    BYTES_TX = 'bytes_tx'
    BYTES_RX = 'bytes_rx'
    FRAMES_TX_RATE = 'frames_tx_rate'
    FRAMES_RX_RATE = 'frames_rx_rate'
    MIN_LATENCY_NS = 'min_latency_ns'
    MAX_LATENCY_NS = 'max_latency_ns'
    AVG_LATENCY_NS = 'avg_latency_ns'
    LOSS = 'loss'

    def __init__(self, parent=None, choice=None, flow_names=None, column_names=None, metric_group_names=None):
        super(FlowMetricsRequest, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('flow_names', flow_names)
        self._set_property('column_names', column_names)
        self._set_property('metric_group_names', metric_group_names)

    @property
    def flow_names(self):
        # type: () -> list[str]
        """flow_names getter

        The names of flow objects to return results for. An empty list will return results for all flows.

        Returns: list[str]
        """
        return self._get_property('flow_names')

    @flow_names.setter
    def flow_names(self, value):
        """flow_names setter

        The names of flow objects to return results for. An empty list will return results for all flows.

        value: list[str]
        """
        self._set_property('flow_names', value)

    @property
    def column_names(self):
        # type: () -> list[Union[transmit, port_tx, port_rx, frames_tx, frames_rx, bytes_tx, bytes_rx, frames_tx_rate, frames_rx_rate, min_latency_ns, max_latency_ns, avg_latency_ns, loss]]
        """column_names getter

        The list of column names that the returned result set will contain. If the list is empty then all columns will be returned except for any result_groups. The name of the flow cannot be excluded.

        Returns: list[Union[transmit, port_tx, port_rx, frames_tx, frames_rx, bytes_tx, bytes_rx, frames_tx_rate, frames_rx_rate, min_latency_ns, max_latency_ns, avg_latency_ns, loss]]
        """
        return self._get_property('column_names')

    @column_names.setter
    def column_names(self, value):
        """column_names setter

        The list of column names that the returned result set will contain. If the list is empty then all columns will be returned except for any result_groups. The name of the flow cannot be excluded.

        value: list[Union[transmit, port_tx, port_rx, frames_tx, frames_rx, bytes_tx, bytes_rx, frames_tx_rate, frames_rx_rate, min_latency_ns, max_latency_ns, avg_latency_ns, loss]]
        """
        self._set_property('column_names', value)

    @property
    def metric_group_names(self):
        # type: () -> list[str]
        """metric_group_names getter

        Extend the details of flow metrics by specifying any configured flow packet header field metric_group names.

        Returns: list[str]
        """
        return self._get_property('metric_group_names')

    @metric_group_names.setter
    def metric_group_names(self, value):
        """metric_group_names setter

        Extend the details of flow metrics by specifying any configured flow packet header field metric_group names.

        value: list[str]
        """
        self._set_property('metric_group_names', value)


class Bgpv4MetricsRequest(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    SESSIONS_TOTAL = 'sessions_total'
    SESSIONS_UP = 'sessions_up'
    SESSIONS_DOWN = 'sessions_down'
    SESSIONS_NOT_STARTED = 'sessions_not_started'
    ROUTES_ADVERTISED = 'routes_advertised'
    ROUTES_WITHDRAWN = 'routes_withdrawn'

    def __init__(self, parent=None, choice=None, device_names=None, column_names=None):
        super(Bgpv4MetricsRequest, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('device_names', device_names)
        self._set_property('column_names', column_names)

    @property
    def device_names(self):
        # type: () -> list[str]
        """device_names getter

        The names of BGPv4 device to return results for. An empty list will return results for all BGPv4 devices.

        Returns: list[str]
        """
        return self._get_property('device_names')

    @device_names.setter
    def device_names(self, value):
        """device_names setter

        The names of BGPv4 device to return results for. An empty list will return results for all BGPv4 devices.

        value: list[str]
        """
        self._set_property('device_names', value)

    @property
    def column_names(self):
        # type: () -> list[Union[sessions_total, sessions_up, sessions_down, sessions_not_started, routes_advertised, routes_withdrawn]]
        """column_names getter

        The list of column names that the returned result set will contain. If the list is empty then all columns will be returned except for any result_groups. The name of the BGPv4 device cannot be excluded.

        Returns: list[Union[sessions_total, sessions_up, sessions_down, sessions_not_started, routes_advertised, routes_withdrawn]]
        """
        return self._get_property('column_names')

    @column_names.setter
    def column_names(self, value):
        """column_names setter

        The list of column names that the returned result set will contain. If the list is empty then all columns will be returned except for any result_groups. The name of the BGPv4 device cannot be excluded.

        value: list[Union[sessions_total, sessions_up, sessions_down, sessions_not_started, routes_advertised, routes_withdrawn]]
        """
        self._set_property('column_names', value)


class Bgpv6MetricsRequest(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    SESSIONS_TOTAL = 'sessions_total'
    SESSIONS_UP = 'sessions_up'
    SESSIONS_DOWN = 'sessions_down'
    SESSIONS_NOT_STARTED = 'sessions_not_started'
    ROUTES_ADVERTISED = 'routes_advertised'
    ROUTES_WITHDRAWN = 'routes_withdrawn'

    def __init__(self, parent=None, choice=None, device_names=None, column_names=None):
        super(Bgpv6MetricsRequest, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('device_names', device_names)
        self._set_property('column_names', column_names)

    @property
    def device_names(self):
        # type: () -> list[str]
        """device_names getter

        The names of BGPv6 device to return results for. An empty list will return results for all BGPv6 devices.

        Returns: list[str]
        """
        return self._get_property('device_names')

    @device_names.setter
    def device_names(self, value):
        """device_names setter

        The names of BGPv6 device to return results for. An empty list will return results for all BGPv6 devices.

        value: list[str]
        """
        self._set_property('device_names', value)

    @property
    def column_names(self):
        # type: () -> list[Union[sessions_total, sessions_up, sessions_down, sessions_not_started, routes_advertised, routes_withdrawn]]
        """column_names getter

        The list of column names that the returned result set will contain. If the list is empty then all columns will be returned except for any result_groups. The name of the BGPv6 device cannot be excluded.

        Returns: list[Union[sessions_total, sessions_up, sessions_down, sessions_not_started, routes_advertised, routes_withdrawn]]
        """
        return self._get_property('column_names')

    @column_names.setter
    def column_names(self, value):
        """column_names setter

        The list of column names that the returned result set will contain. If the list is empty then all columns will be returned except for any result_groups. The name of the BGPv6 device cannot be excluded.

        value: list[Union[sessions_total, sessions_up, sessions_down, sessions_not_started, routes_advertised, routes_withdrawn]]
        """
        self._set_property('column_names', value)


class MetricsResponse(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'port_metrics': 'PortMetricIter',
        'flow_metrics': 'FlowMetricIter',
        'bgpv4_metrics': 'Bgpv4MetricIter',
        'bgpv6_metrics': 'Bgpv6MetricIter',
    }

    PORT_METRICS = 'port_metrics'
    FLOW_METRICS = 'flow_metrics'
    BGPV4_METRICS = 'bgpv4_metrics'

    def __init__(self, parent=None, choice=None):
        super(MetricsResponse, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def choice(self):
        # type: () -> Union[port_metrics, flow_metrics, bgpv4_metrics, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[port_metrics, flow_metrics, bgpv4_metrics, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[port_metrics, flow_metrics, bgpv4_metrics, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def port_metrics(self):
        # type: () -> PortMetricIter
        """port_metrics getter

        TBD

        Returns: list[obj(snappi.PortMetric)]
        """
        return self._get_property('port_metrics', PortMetricIter)

    @property
    def flow_metrics(self):
        # type: () -> FlowMetricIter
        """flow_metrics getter

        TBD

        Returns: list[obj(snappi.FlowMetric)]
        """
        return self._get_property('flow_metrics', FlowMetricIter)

    @property
    def bgpv4_metrics(self):
        # type: () -> Bgpv4MetricIter
        """bgpv4_metrics getter

        TBD

        Returns: list[obj(snappi.Bgpv4Metric)]
        """
        return self._get_property('bgpv4_metrics', Bgpv4MetricIter)

    @property
    def bgpv6_metrics(self):
        # type: () -> Bgpv6MetricIter
        """bgpv6_metrics getter

        TBD

        Returns: list[obj(snappi.Bgpv6Metric)]
        """
        return self._get_property('bgpv6_metrics', Bgpv6MetricIter)


class PortMetric(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    UP = 'up'
    DOWN = 'down'

    STARTED = 'started'
    STOPPED = 'stopped'

    def __init__(self, parent=None, choice=None, name=None, location=None, link=None, capture=None, frames_tx=None, frames_rx=None, bytes_tx=None, bytes_rx=None, frames_tx_rate=None, frames_rx_rate=None, bytes_tx_rate=None, bytes_rx_rate=None):
        super(PortMetric, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('name', name)
        self._set_property('location', location)
        self._set_property('link', link)
        self._set_property('capture', capture)
        self._set_property('frames_tx', frames_tx)
        self._set_property('frames_rx', frames_rx)
        self._set_property('bytes_tx', bytes_tx)
        self._set_property('bytes_rx', bytes_rx)
        self._set_property('frames_tx_rate', frames_tx_rate)
        self._set_property('frames_rx_rate', frames_rx_rate)
        self._set_property('bytes_tx_rate', bytes_tx_rate)
        self._set_property('bytes_rx_rate', bytes_rx_rate)

    @property
    def name(self):
        # type: () -> str
        """name getter

        The name of a configured port

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        The name of a configured port

        value: str
        """
        self._set_property('name', value)

    @property
    def location(self):
        # type: () -> str
        """location getter

        The state of the connection to the test port location. The format should be the configured port location along with any custom connection state message.

        Returns: str
        """
        return self._get_property('location')

    @location.setter
    def location(self, value):
        """location setter

        The state of the connection to the test port location. The format should be the configured port location along with any custom connection state message.

        value: str
        """
        self._set_property('location', value)

    @property
    def link(self):
        # type: () -> Union[up, down]
        """link getter

        The state of the test port link The string can be up, down or a custom error message.

        Returns: Union[up, down]
        """
        return self._get_property('link')

    @link.setter
    def link(self, value):
        """link setter

        The state of the test port link The string can be up, down or a custom error message.

        value: Union[up, down]
        """
        self._set_property('link', value)

    @property
    def capture(self):
        # type: () -> Union[started, stopped]
        """capture getter

        The state of the test port capture infrastructure. The string can be started, stopped or a custom error message.

        Returns: Union[started, stopped]
        """
        return self._get_property('capture')

    @capture.setter
    def capture(self, value):
        """capture setter

        The state of the test port capture infrastructure. The string can be started, stopped or a custom error message.

        value: Union[started, stopped]
        """
        self._set_property('capture', value)

    @property
    def frames_tx(self):
        # type: () -> int
        """frames_tx getter

        The current total number of frames transmitted

        Returns: int
        """
        return self._get_property('frames_tx')

    @frames_tx.setter
    def frames_tx(self, value):
        """frames_tx setter

        The current total number of frames transmitted

        value: int
        """
        self._set_property('frames_tx', value)

    @property
    def frames_rx(self):
        # type: () -> int
        """frames_rx getter

        The current total number of valid frames received

        Returns: int
        """
        return self._get_property('frames_rx')

    @frames_rx.setter
    def frames_rx(self, value):
        """frames_rx setter

        The current total number of valid frames received

        value: int
        """
        self._set_property('frames_rx', value)

    @property
    def bytes_tx(self):
        # type: () -> int
        """bytes_tx getter

        The current total number of bytes transmitted

        Returns: int
        """
        return self._get_property('bytes_tx')

    @bytes_tx.setter
    def bytes_tx(self, value):
        """bytes_tx setter

        The current total number of bytes transmitted

        value: int
        """
        self._set_property('bytes_tx', value)

    @property
    def bytes_rx(self):
        # type: () -> int
        """bytes_rx getter

        The current total number of valid bytes received

        Returns: int
        """
        return self._get_property('bytes_rx')

    @bytes_rx.setter
    def bytes_rx(self, value):
        """bytes_rx setter

        The current total number of valid bytes received

        value: int
        """
        self._set_property('bytes_rx', value)

    @property
    def frames_tx_rate(self):
        # type: () -> float
        """frames_tx_rate getter

        The current rate of frames transmitted

        Returns: float
        """
        return self._get_property('frames_tx_rate')

    @frames_tx_rate.setter
    def frames_tx_rate(self, value):
        """frames_tx_rate setter

        The current rate of frames transmitted

        value: float
        """
        self._set_property('frames_tx_rate', value)

    @property
    def frames_rx_rate(self):
        # type: () -> float
        """frames_rx_rate getter

        The current rate of valid frames received

        Returns: float
        """
        return self._get_property('frames_rx_rate')

    @frames_rx_rate.setter
    def frames_rx_rate(self, value):
        """frames_rx_rate setter

        The current rate of valid frames received

        value: float
        """
        self._set_property('frames_rx_rate', value)

    @property
    def bytes_tx_rate(self):
        # type: () -> float
        """bytes_tx_rate getter

        The current rate of bytes transmitted

        Returns: float
        """
        return self._get_property('bytes_tx_rate')

    @bytes_tx_rate.setter
    def bytes_tx_rate(self, value):
        """bytes_tx_rate setter

        The current rate of bytes transmitted

        value: float
        """
        self._set_property('bytes_tx_rate', value)

    @property
    def bytes_rx_rate(self):
        # type: () -> float
        """bytes_rx_rate getter

        The current rate of bytes received

        Returns: float
        """
        return self._get_property('bytes_rx_rate')

    @bytes_rx_rate.setter
    def bytes_rx_rate(self, value):
        """bytes_rx_rate setter

        The current rate of bytes received

        value: float
        """
        self._set_property('bytes_rx_rate', value)


class PortMetricIter(SnappiIter):
    __slots__ = ()

    def __init__(self):
        super(PortMetricIter, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[PortMetric]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> PortMetricIter
        return self._iter()

    def __next__(self):
        # type: () -> PortMetric
        return self._next()

    def next(self):
        # type: () -> PortMetric
        return self._next()

    def metric(self, name=None, location=None, link=None, capture=None, frames_tx=None, frames_rx=None, bytes_tx=None, bytes_rx=None, frames_tx_rate=None, frames_rx_rate=None, bytes_tx_rate=None, bytes_rx_rate=None):
        # type: () -> PortMetricIter
        """Factory method that creates an instance of PortMetric class

        TBD
        """
        item = PortMetric(name=name, location=location, link=link, capture=capture, frames_tx=frames_tx, frames_rx=frames_rx, bytes_tx=bytes_tx, bytes_rx=bytes_rx, frames_tx_rate=frames_tx_rate, frames_rx_rate=frames_rx_rate, bytes_tx_rate=bytes_tx_rate, bytes_rx_rate=bytes_rx_rate)
        self._add(item)
        return self


class FlowMetric(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'metric_groups': 'FlowMetricGroupIter',
    }

    STARTED = 'started'
    STOPPED = 'stopped'
    PAUSED = 'paused'

    def __init__(self, parent=None, choice=None, name=None, transmit=None, port_tx=None, port_rx=None, frames_tx=None, frames_rx=None, bytes_tx=None, bytes_rx=None, frames_tx_rate=None, frames_rx_rate=None, min_latency_ns=None, max_latency_ns=None, avg_latency_ns=None, loss=None):
        super(FlowMetric, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('name', name)
        self._set_property('transmit', transmit)
        self._set_property('port_tx', port_tx)
        self._set_property('port_rx', port_rx)
        self._set_property('frames_tx', frames_tx)
        self._set_property('frames_rx', frames_rx)
        self._set_property('bytes_tx', bytes_tx)
        self._set_property('bytes_rx', bytes_rx)
        self._set_property('frames_tx_rate', frames_tx_rate)
        self._set_property('frames_rx_rate', frames_rx_rate)
        self._set_property('min_latency_ns', min_latency_ns)
        self._set_property('max_latency_ns', max_latency_ns)
        self._set_property('avg_latency_ns', avg_latency_ns)
        self._set_property('loss', loss)

    @property
    def name(self):
        # type: () -> str
        """name getter

        The name of a configured flow.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        The name of a configured flow.

        value: str
        """
        self._set_property('name', value)

    @property
    def transmit(self):
        # type: () -> Union[started, stopped, paused]
        """transmit getter

        The transmit state of the flow.

        Returns: Union[started, stopped, paused]
        """
        return self._get_property('transmit')

    @transmit.setter
    def transmit(self, value):
        """transmit setter

        The transmit state of the flow.

        value: Union[started, stopped, paused]
        """
        self._set_property('transmit', value)

    @property
    def port_tx(self):
        # type: () -> str
        """port_tx getter

        The name of a configured port

        Returns: str
        """
        return self._get_property('port_tx')

    @port_tx.setter
    def port_tx(self, value):
        """port_tx setter

        The name of a configured port

        value: str
        """
        self._set_property('port_tx', value)

    @property
    def port_rx(self):
        # type: () -> str
        """port_rx getter

        The name of a configured port

        Returns: str
        """
        return self._get_property('port_rx')

    @port_rx.setter
    def port_rx(self, value):
        """port_rx setter

        The name of a configured port

        value: str
        """
        self._set_property('port_rx', value)

    @property
    def frames_tx(self):
        # type: () -> int
        """frames_tx getter

        The current total number of frames transmitted

        Returns: int
        """
        return self._get_property('frames_tx')

    @frames_tx.setter
    def frames_tx(self, value):
        """frames_tx setter

        The current total number of frames transmitted

        value: int
        """
        self._set_property('frames_tx', value)

    @property
    def frames_rx(self):
        # type: () -> int
        """frames_rx getter

        The current total number of valid frames received

        Returns: int
        """
        return self._get_property('frames_rx')

    @frames_rx.setter
    def frames_rx(self, value):
        """frames_rx setter

        The current total number of valid frames received

        value: int
        """
        self._set_property('frames_rx', value)

    @property
    def bytes_tx(self):
        # type: () -> int
        """bytes_tx getter

        The current total number of bytes transmitted

        Returns: int
        """
        return self._get_property('bytes_tx')

    @bytes_tx.setter
    def bytes_tx(self, value):
        """bytes_tx setter

        The current total number of bytes transmitted

        value: int
        """
        self._set_property('bytes_tx', value)

    @property
    def bytes_rx(self):
        # type: () -> int
        """bytes_rx getter

        The current total number of bytes received

        Returns: int
        """
        return self._get_property('bytes_rx')

    @bytes_rx.setter
    def bytes_rx(self, value):
        """bytes_rx setter

        The current total number of bytes received

        value: int
        """
        self._set_property('bytes_rx', value)

    @property
    def frames_tx_rate(self):
        # type: () -> float
        """frames_tx_rate getter

        The current rate of frames transmitted

        Returns: float
        """
        return self._get_property('frames_tx_rate')

    @frames_tx_rate.setter
    def frames_tx_rate(self, value):
        """frames_tx_rate setter

        The current rate of frames transmitted

        value: float
        """
        self._set_property('frames_tx_rate', value)

    @property
    def frames_rx_rate(self):
        # type: () -> float
        """frames_rx_rate getter

        The current rate of valid frames received

        Returns: float
        """
        return self._get_property('frames_rx_rate')

    @frames_rx_rate.setter
    def frames_rx_rate(self, value):
        """frames_rx_rate setter

        The current rate of valid frames received

        value: float
        """
        self._set_property('frames_rx_rate', value)

    @property
    def min_latency_ns(self):
        # type: () -> float
        """min_latency_ns getter

        The minimum latency in nanoseconds for valid frames received

        Returns: float
        """
        return self._get_property('min_latency_ns')

    @min_latency_ns.setter
    def min_latency_ns(self, value):
        """min_latency_ns setter

        The minimum latency in nanoseconds for valid frames received

        value: float
        """
        self._set_property('min_latency_ns', value)

    @property
    def max_latency_ns(self):
        # type: () -> float
        """max_latency_ns getter

        The maximum latency in nanoseconds for valid frames received

        Returns: float
        """
        return self._get_property('max_latency_ns')

    @max_latency_ns.setter
    def max_latency_ns(self, value):
        """max_latency_ns setter

        The maximum latency in nanoseconds for valid frames received

        value: float
        """
        self._set_property('max_latency_ns', value)

    @property
    def avg_latency_ns(self):
        # type: () -> float
        """avg_latency_ns getter

        The avarage latency in nanoseconds for valid frames received

        Returns: float
        """
        return self._get_property('avg_latency_ns')

    @avg_latency_ns.setter
    def avg_latency_ns(self, value):
        """avg_latency_ns setter

        The avarage latency in nanoseconds for valid frames received

        value: float
        """
        self._set_property('avg_latency_ns', value)

    @property
    def loss(self):
        # type: () -> float
        """loss getter

        The percentage of lost frames

        Returns: float
        """
        return self._get_property('loss')

    @loss.setter
    def loss(self, value):
        """loss setter

        The percentage of lost frames

        value: float
        """
        self._set_property('loss', value)

    @property
    def metric_groups(self):
        # type: () -> FlowMetricGroupIter
        """metric_groups getter

        Any configured flow packet header field metric_group names will appear as additional name/value pairs.

        Returns: list[obj(snappi.FlowMetricGroup)]
        """
        return self._get_property('metric_groups', FlowMetricGroupIter)


class FlowMetricGroup(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, name=None, value=None):
        super(FlowMetricGroup, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('name', name)
        self._set_property('value', value)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Name provided as part of a flow packet header field metric group

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Name provided as part of a flow packet header field metric group

        value: str
        """
        self._set_property('name', value)

    @property
    def value(self):
        # type: () -> float
        """value getter

        The value of the flow packet header field

        Returns: float
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        The value of the flow packet header field

        value: float
        """
        self._set_property('value', value)


class FlowMetricGroupIter(SnappiIter):
    __slots__ = ()

    def __init__(self):
        super(FlowMetricGroupIter, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[FlowMetricGroup]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> FlowMetricGroupIter
        return self._iter()

    def __next__(self):
        # type: () -> FlowMetricGroup
        return self._next()

    def next(self):
        # type: () -> FlowMetricGroup
        return self._next()

    def metricgroup(self, name=None, value=None):
        # type: () -> FlowMetricGroupIter
        """Factory method that creates an instance of FlowMetricGroup class

        A metric group
        """
        item = FlowMetricGroup(name=name, value=value)
        self._add(item)
        return self


class FlowMetricIter(SnappiIter):
    __slots__ = ()

    def __init__(self):
        super(FlowMetricIter, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[FlowMetric]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> FlowMetricIter
        return self._iter()

    def __next__(self):
        # type: () -> FlowMetric
        return self._next()

    def next(self):
        # type: () -> FlowMetric
        return self._next()

    def metric(self, name=None, transmit=None, port_tx=None, port_rx=None, frames_tx=None, frames_rx=None, bytes_tx=None, bytes_rx=None, frames_tx_rate=None, frames_rx_rate=None, min_latency_ns=None, max_latency_ns=None, avg_latency_ns=None, loss=None):
        # type: () -> FlowMetricIter
        """Factory method that creates an instance of FlowMetric class

        TBD
        """
        item = FlowMetric(name=name, transmit=transmit, port_tx=port_tx, port_rx=port_rx, frames_tx=frames_tx, frames_rx=frames_rx, bytes_tx=bytes_tx, bytes_rx=bytes_rx, frames_tx_rate=frames_tx_rate, frames_rx_rate=frames_rx_rate, min_latency_ns=min_latency_ns, max_latency_ns=max_latency_ns, avg_latency_ns=avg_latency_ns, loss=loss)
        self._add(item)
        return self


class Bgpv4Metric(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, name=None, sessions_total=None, sessions_up=None, sessions_down=None, sessions_not_started=None, routes_advertised=None, routes_withdrawn=None):
        super(Bgpv4Metric, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('name', name)
        self._set_property('sessions_total', sessions_total)
        self._set_property('sessions_up', sessions_up)
        self._set_property('sessions_down', sessions_down)
        self._set_property('sessions_not_started', sessions_not_started)
        self._set_property('routes_advertised', routes_advertised)
        self._set_property('routes_withdrawn', routes_withdrawn)

    @property
    def name(self):
        # type: () -> str
        """name getter

        The name of a configured BGPv4 device.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        The name of a configured BGPv4 device.

        value: str
        """
        self._set_property('name', value)

    @property
    def sessions_total(self):
        # type: () -> int
        """sessions_total getter

        Total number of session

        Returns: int
        """
        return self._get_property('sessions_total')

    @sessions_total.setter
    def sessions_total(self, value):
        """sessions_total setter

        Total number of session

        value: int
        """
        self._set_property('sessions_total', value)

    @property
    def sessions_up(self):
        # type: () -> int
        """sessions_up getter

        Sessions are in active state

        Returns: int
        """
        return self._get_property('sessions_up')

    @sessions_up.setter
    def sessions_up(self, value):
        """sessions_up setter

        Sessions are in active state

        value: int
        """
        self._set_property('sessions_up', value)

    @property
    def sessions_down(self):
        # type: () -> int
        """sessions_down getter

        Sessions are not active state

        Returns: int
        """
        return self._get_property('sessions_down')

    @sessions_down.setter
    def sessions_down(self, value):
        """sessions_down setter

        Sessions are not active state

        value: int
        """
        self._set_property('sessions_down', value)

    @property
    def sessions_not_started(self):
        # type: () -> int
        """sessions_not_started getter

        Sessions not able to start due to some internal issue

        Returns: int
        """
        return self._get_property('sessions_not_started')

    @sessions_not_started.setter
    def sessions_not_started(self, value):
        """sessions_not_started setter

        Sessions not able to start due to some internal issue

        value: int
        """
        self._set_property('sessions_not_started', value)

    @property
    def routes_advertised(self):
        # type: () -> int
        """routes_advertised getter

        Number of advertised routes sent

        Returns: int
        """
        return self._get_property('routes_advertised')

    @routes_advertised.setter
    def routes_advertised(self, value):
        """routes_advertised setter

        Number of advertised routes sent

        value: int
        """
        self._set_property('routes_advertised', value)

    @property
    def routes_withdrawn(self):
        # type: () -> int
        """routes_withdrawn getter

        Number of routes withdrawn

        Returns: int
        """
        return self._get_property('routes_withdrawn')

    @routes_withdrawn.setter
    def routes_withdrawn(self, value):
        """routes_withdrawn setter

        Number of routes withdrawn

        value: int
        """
        self._set_property('routes_withdrawn', value)


class Bgpv4MetricIter(SnappiIter):
    __slots__ = ()

    def __init__(self):
        super(Bgpv4MetricIter, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[Bgpv4Metric]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> Bgpv4MetricIter
        return self._iter()

    def __next__(self):
        # type: () -> Bgpv4Metric
        return self._next()

    def next(self):
        # type: () -> Bgpv4Metric
        return self._next()

    def metric(self, name=None, sessions_total=None, sessions_up=None, sessions_down=None, sessions_not_started=None, routes_advertised=None, routes_withdrawn=None):
        # type: () -> Bgpv4MetricIter
        """Factory method that creates an instance of Bgpv4Metric class

        BGPv4 Router statistics and learned routing information
        """
        item = Bgpv4Metric(name=name, sessions_total=sessions_total, sessions_up=sessions_up, sessions_down=sessions_down, sessions_not_started=sessions_not_started, routes_advertised=routes_advertised, routes_withdrawn=routes_withdrawn)
        self._add(item)
        return self


class Bgpv6Metric(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, name=None, sessions_total=None, sessions_up=None, sessions_down=None, sessions_not_started=None, routes_advertised=None, routes_withdrawn=None):
        super(Bgpv6Metric, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('name', name)
        self._set_property('sessions_total', sessions_total)
        self._set_property('sessions_up', sessions_up)
        self._set_property('sessions_down', sessions_down)
        self._set_property('sessions_not_started', sessions_not_started)
        self._set_property('routes_advertised', routes_advertised)
        self._set_property('routes_withdrawn', routes_withdrawn)

    @property
    def name(self):
        # type: () -> str
        """name getter

        The name of a configured BGPv6 device.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        The name of a configured BGPv6 device.

        value: str
        """
        self._set_property('name', value)

    @property
    def sessions_total(self):
        # type: () -> int
        """sessions_total getter

        Total number of session

        Returns: int
        """
        return self._get_property('sessions_total')

    @sessions_total.setter
    def sessions_total(self, value):
        """sessions_total setter

        Total number of session

        value: int
        """
        self._set_property('sessions_total', value)

    @property
    def sessions_up(self):
        # type: () -> int
        """sessions_up getter

        Sessions are in active state

        Returns: int
        """
        return self._get_property('sessions_up')

    @sessions_up.setter
    def sessions_up(self, value):
        """sessions_up setter

        Sessions are in active state

        value: int
        """
        self._set_property('sessions_up', value)

    @property
    def sessions_down(self):
        # type: () -> int
        """sessions_down getter

        Sessions are not active state

        Returns: int
        """
        return self._get_property('sessions_down')

    @sessions_down.setter
    def sessions_down(self, value):
        """sessions_down setter

        Sessions are not active state

        value: int
        """
        self._set_property('sessions_down', value)

    @property
    def sessions_not_started(self):
        # type: () -> int
        """sessions_not_started getter

        Sessions not started yet or sessions not able to start due to some internal issue

        Returns: int
        """
        return self._get_property('sessions_not_started')

    @sessions_not_started.setter
    def sessions_not_started(self, value):
        """sessions_not_started setter

        Sessions not started yet or sessions not able to start due to some internal issue

        value: int
        """
        self._set_property('sessions_not_started', value)

    @property
    def routes_advertised(self):
        # type: () -> int
        """routes_advertised getter

        Number of advertised routes sent

        Returns: int
        """
        return self._get_property('routes_advertised')

    @routes_advertised.setter
    def routes_advertised(self, value):
        """routes_advertised setter

        Number of advertised routes sent

        value: int
        """
        self._set_property('routes_advertised', value)

    @property
    def routes_withdrawn(self):
        # type: () -> int
        """routes_withdrawn getter

        Number of routes withdrawn

        Returns: int
        """
        return self._get_property('routes_withdrawn')

    @routes_withdrawn.setter
    def routes_withdrawn(self, value):
        """routes_withdrawn setter

        Number of routes withdrawn

        value: int
        """
        self._set_property('routes_withdrawn', value)


class Bgpv6MetricIter(SnappiIter):
    __slots__ = ()

    def __init__(self):
        super(Bgpv6MetricIter, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[Bgpv6Metric]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> Bgpv6MetricIter
        return self._iter()

    def __next__(self):
        # type: () -> Bgpv6Metric
        return self._next()

    def next(self):
        # type: () -> Bgpv6Metric
        return self._next()

    def metric(self, name=None, sessions_total=None, sessions_up=None, sessions_down=None, sessions_not_started=None, routes_advertised=None, routes_withdrawn=None):
        # type: () -> Bgpv6MetricIter
        """Factory method that creates an instance of Bgpv6Metric class

        BGPv6 Router statistics and learned routing information
        """
        item = Bgpv6Metric(name=name, sessions_total=sessions_total, sessions_up=sessions_up, sessions_down=sessions_down, sessions_not_started=sessions_not_started, routes_advertised=routes_advertised, routes_withdrawn=routes_withdrawn)
        self._add(item)
        return self


class StateMetrics(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'port_state': 'PortStateIter',
        'flow_state': 'FlowStateIter',
    }

    def __init__(self, parent=None, choice=None):
        super(StateMetrics, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def port_state(self):
        # type: () -> PortStateIter
        """port_state getter

        TBD

        Returns: list[obj(snappi.PortState)]
        """
        return self._get_property('port_state', PortStateIter)

    @property
    def flow_state(self):
        # type: () -> FlowStateIter
        """flow_state getter

        TBD

        Returns: list[obj(snappi.FlowState)]
        """
        return self._get_property('flow_state', FlowStateIter)


class PortState(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    UP = 'up'
    DOWN = 'down'

    STARTED = 'started'
    STOPPED = 'stopped'

    def __init__(self, parent=None, choice=None, name=None, link=None, capture=None):
        super(PortState, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('name', name)
        self._set_property('link', link)
        self._set_property('capture', capture)

    @property
    def name(self):
        # type: () -> str
        """name getter

        TBD

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        TBD

        value: str
        """
        self._set_property('name', value)

    @property
    def link(self):
        # type: () -> Union[up, down]
        """link getter

        TBD

        Returns: Union[up, down]
        """
        return self._get_property('link')

    @link.setter
    def link(self, value):
        """link setter

        TBD

        value: Union[up, down]
        """
        self._set_property('link', value)

    @property
    def capture(self):
        # type: () -> Union[started, stopped]
        """capture getter

        TBD

        Returns: Union[started, stopped]
        """
        return self._get_property('capture')

    @capture.setter
    def capture(self, value):
        """capture setter

        TBD

        value: Union[started, stopped]
        """
        self._set_property('capture', value)


class PortStateIter(SnappiIter):
    __slots__ = ()

    def __init__(self):
        super(PortStateIter, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[PortState]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> PortStateIter
        return self._iter()

    def __next__(self):
        # type: () -> PortState
        return self._next()

    def next(self):
        # type: () -> PortState
        return self._next()

    def state(self, name=None, link=None, capture=None):
        # type: () -> PortStateIter
        """Factory method that creates an instance of PortState class

        TBD
        """
        item = PortState(name=name, link=link, capture=capture)
        self._add(item)
        return self


class FlowState(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    STARTED = 'started'
    STOPPED = 'stopped'
    PAUSED = 'paused'

    def __init__(self, parent=None, choice=None, name=None, transmit=None):
        super(FlowState, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('name', name)
        self._set_property('transmit', transmit)

    @property
    def name(self):
        # type: () -> str
        """name getter

        TBD

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        TBD

        value: str
        """
        self._set_property('name', value)

    @property
    def transmit(self):
        # type: () -> Union[started, stopped, paused]
        """transmit getter

        TBD

        Returns: Union[started, stopped, paused]
        """
        return self._get_property('transmit')

    @transmit.setter
    def transmit(self, value):
        """transmit setter

        TBD

        value: Union[started, stopped, paused]
        """
        self._set_property('transmit', value)


class FlowStateIter(SnappiIter):
    __slots__ = ()

    def __init__(self):
        super(FlowStateIter, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[FlowState]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> FlowStateIter
        return self._iter()

    def __next__(self):
        # type: () -> FlowState
        return self._next()

    def next(self):
        # type: () -> FlowState
        return self._next()

    def state(self, name=None, transmit=None):
        # type: () -> FlowStateIter
        """Factory method that creates an instance of FlowState class

        TBD
        """
        item = FlowState(name=name, transmit=transmit)
        self._add(item)
        return self


class Capabilities(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, unsupported=None, formats=None):
        super(Capabilities, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('unsupported', unsupported)
        self._set_property('formats', formats)

    @property
    def unsupported(self):
        # type: () -> list[str]
        """unsupported getter

        A list of /components/schemas/... paths that are not supported.

        Returns: list[str]
        """
        return self._get_property('unsupported')

    @unsupported.setter
    def unsupported(self, value):
        """unsupported setter

        A list of /components/schemas/... paths that are not supported.

        value: list[str]
        """
        self._set_property('unsupported', value)

    @property
    def formats(self):
        # type: () -> list[str]
        """formats getter

        A /components/schemas/... path and specific format details regarding the path. Specific model format details can be additional objects and properties represented as a hashmap. For example layer1 models are defined as a hashmap key to object with each object consisting of a specific name/value property pairs. This list of items will detail any specific formats, properties, enums.

        Returns: list[str]
        """
        return self._get_property('formats')

    @formats.setter
    def formats(self, value):
        """formats setter

        A /components/schemas/... path and specific format details regarding the path. Specific model format details can be additional objects and properties represented as a hashmap. For example layer1 models are defined as a hashmap key to object with each object consisting of a specific name/value property pairs. This list of items will detail any specific formats, properties, enums.

        value: list[str]
        """
        self._set_property('formats', value)


class CaptureRequest(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, port_name=None):
        super(CaptureRequest, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('port_name', port_name)

    @property
    def port_name(self):
        # type: () -> str
        """port_name getter

        The name of a port a capture is started on.

        Returns: str
        """
        return self._get_property('port_name')

    @port_name.setter
    def port_name(self, value):
        """port_name setter

        The name of a port a capture is started on.

        value: str
        """
        self._set_property('port_name', value)


class Api(object):
    """Snappi Abstract API
    """

    def __init__(self, host=None):
        self.host = host if host else "https://localhost"

    def set_config(self, payload):
        """POST /config

        Sets configuration resources on the traffic generator.

        Return: details
        """
        raise NotImplementedError("set_config")

    def update_config(self, payload):
        """PATCH /config

        Updates configuration resources on the traffic generator.

        Return: details
        """
        raise NotImplementedError("update_config")

    def get_config(self):
        """GET /config

        TBD

        Return: config
        """
        raise NotImplementedError("get_config")

    def set_transmit_state(self, payload):
        """POST /control/transmit

        Updates the state of configuration resources on the traffic generator.

        Return: details
        """
        raise NotImplementedError("set_transmit_state")

    def set_link_state(self, payload):
        """POST /control/link

        Updates the state of configuration resources on the traffic generator.

        Return: details
        """
        raise NotImplementedError("set_link_state")

    def set_capture_state(self, payload):
        """POST /control/capture

        Updates the state of configuration resources on the traffic generator.

        Return: details
        """
        raise NotImplementedError("set_capture_state")

    def get_metrics(self, payload):
        """POST /results/metrics

        TBD

        Return: metrics_response
        """
        raise NotImplementedError("get_metrics")

    def get_state_metrics(self):
        """POST /results/state

        TBD

        Return: state_metrics
        """
        raise NotImplementedError("get_state_metrics")

    def get_capabilities(self):
        """POST /results/capabilities

        TBD

        Return: capabilities
        """
        raise NotImplementedError("get_capabilities")

    def get_capture(self, payload):
        """POST /results/capture

        TBD

        Return: None
        """
        raise NotImplementedError("get_capture")

    def config(self):
        """Factory method that creates an instance of Config

        Return: Config
        """
        return Config()

    def details(self):
        """Factory method that creates an instance of Details

        Return: Details
        """
        return Details()

    def transmit_state(self):
        """Factory method that creates an instance of TransmitState

        Return: TransmitState
        """
        return TransmitState()

    def link_state(self):
        """Factory method that creates an instance of LinkState

        Return: LinkState
        """
        return LinkState()

    def capture_state(self):
        """Factory method that creates an instance of CaptureState

        Return: CaptureState
        """
        return CaptureState()

    def metrics_request(self):
        """Factory method that creates an instance of MetricsRequest

        Return: MetricsRequest
        """
        return MetricsRequest()

    def metrics_response(self):
        """Factory method that creates an instance of MetricsResponse

        Return: MetricsResponse
        """
        return MetricsResponse()

    def state_metrics(self):
        """Factory method that creates an instance of StateMetrics

        Return: StateMetrics
        """
        return StateMetrics()

    def capabilities(self):
        """Factory method that creates an instance of Capabilities

        Return: Capabilities
        """
        return Capabilities()

    def capture_request(self):
        """Factory method that creates an instance of CaptureRequest

        Return: CaptureRequest
        """
        return CaptureRequest()


class HttpApi(Api):
    """Snappi HTTP API
    """
    def __init__(self, host=None):
        super(HttpApi, self).__init__(host=host)
        self._transport = SnappiHttpTransport(host=self.host)

    def set_config(self, payload):
        """POST /config

        Sets configuration resources on the traffic generator.

        Return: details
        """
        return self._transport.send_recv(
            "post",
            "/config",
            payload=payload,
            return_object=self.details(),
        )

    def update_config(self, payload):
        """PATCH /config

        Updates configuration resources on the traffic generator.

        Return: details
        """
        return self._transport.send_recv(
            "patch",
            "/config",
            payload=payload,
            return_object=self.details(),
        )

    def get_config(self):
        """GET /config

        TBD

        Return: config
        """
        return self._transport.send_recv(
            "get",
            "/config",
            payload=None,
            return_object=self.config(),
        )

    def set_transmit_state(self, payload):
        """POST /control/transmit

        Updates the state of configuration resources on the traffic generator.

        Return: details
        """
        return self._transport.send_recv(
            "post",
            "/control/transmit",
            payload=payload,
            return_object=self.details(),
        )

    def set_link_state(self, payload):
        """POST /control/link

        Updates the state of configuration resources on the traffic generator.

        Return: details
        """
        return self._transport.send_recv(
            "post",
            "/control/link",
            payload=payload,
            return_object=self.details(),
        )

    def set_capture_state(self, payload):
        """POST /control/capture

        Updates the state of configuration resources on the traffic generator.

        Return: details
        """
        return self._transport.send_recv(
            "post",
            "/control/capture",
            payload=payload,
            return_object=self.details(),
        )

    def get_metrics(self, payload):
        """POST /results/metrics

        TBD

        Return: metrics_response
        """
        return self._transport.send_recv(
            "post",
            "/results/metrics",
            payload=payload,
            return_object=self.metrics_response(),
        )

    def get_state_metrics(self):
        """POST /results/state

        TBD

        Return: state_metrics
        """
        return self._transport.send_recv(
            "post",
            "/results/state",
            payload=None,
            return_object=self.state_metrics(),
        )

    def get_capabilities(self):
        """POST /results/capabilities

        TBD

        Return: capabilities
        """
        return self._transport.send_recv(
            "post",
            "/results/capabilities",
            payload=None,
            return_object=self.capabilities(),
        )

    def get_capture(self, payload):
        """POST /results/capture

        TBD

        Return: None
        """
        return self._transport.send_recv(
            "post",
            "/results/capture",
            payload=payload,
            return_object=None,
        )


def api(host=None, ext=None):
    if ext is None:
        return HttpApi(host=host)

    try:
        lib = importlib.import_module("snappi_%s" % ext)
        return lib.Api(host=host)
    except ImportError as err:
        msg = "Snappi extension %s is not installed or invalid: %s"
        raise Exception(msg % (ext, err))
