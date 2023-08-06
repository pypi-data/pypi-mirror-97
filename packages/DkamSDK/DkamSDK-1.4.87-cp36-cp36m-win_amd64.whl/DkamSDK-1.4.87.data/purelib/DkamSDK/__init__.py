"""
DkamSDK
=======

Provides
	1. Discover cameras in LAN
	2. Connect the camera
	3. Open the data stream (Point cloud/Gray/RGB)
	4. Set the trigger mode of point cloud/gray camera and RGB camera
	5. Set the number of trigger sheets
	6. Capture image
	7. Save point cloud/gray/RGB/depth image/point cloud filter
	8. Save Point cloud and Gray fusion, Point cloud and RGB fusion
	9. Set ROI Mapping
	10. Close the data stream (Point cloud/Gray/RGB)
	11. Disconnect the camera

How to use the DkamSDK
----------------------------
You can download DkamSDK from the "https://pypi.org/"
Note the difference between Windows and Linux when downloading

  '>>> import DkamSDK'
  '>>> DkamSDK.DiscoverCamera()'

Use the built-in ``help`` function to view a function's docstring

  '>>>help(DkamSDK.DiscoverCamera())'

Other documents
---------------
sample
	Major functional use cases
""" 
from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError("Python 2.7 or later required")

# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _DkamSDK
else:
    import _DkamSDK

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "thisown":
            self.this.own(value)
        elif name == "this":
            set(self, name, value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)
    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)
    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""
    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())
    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)


class SwigPyIterator(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _DkamSDK.delete_SwigPyIterator

    def value(self):
        return _DkamSDK.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _DkamSDK.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _DkamSDK.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _DkamSDK.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _DkamSDK.SwigPyIterator_equal(self, x)

    def copy(self):
        return _DkamSDK.SwigPyIterator_copy(self)

    def next(self):
        return _DkamSDK.SwigPyIterator_next(self)

    def __next__(self):
        return _DkamSDK.SwigPyIterator___next__(self)

    def previous(self):
        return _DkamSDK.SwigPyIterator_previous(self)

    def advance(self, n):
        return _DkamSDK.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _DkamSDK.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _DkamSDK.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _DkamSDK.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _DkamSDK.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _DkamSDK.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _DkamSDK.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _DkamSDK:
_DkamSDK.SwigPyIterator_swigregister(SwigPyIterator)

class StringVector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def iterator(self):
        return _DkamSDK.StringVector_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _DkamSDK.StringVector___nonzero__(self)

    def __bool__(self):
        return _DkamSDK.StringVector___bool__(self)

    def __len__(self):
        return _DkamSDK.StringVector___len__(self)

    def __getslice__(self, i, j):
        return _DkamSDK.StringVector___getslice__(self, i, j)

    def __setslice__(self, *args):
        return _DkamSDK.StringVector___setslice__(self, *args)

    def __delslice__(self, i, j):
        return _DkamSDK.StringVector___delslice__(self, i, j)

    def __delitem__(self, *args):
        return _DkamSDK.StringVector___delitem__(self, *args)

    def __getitem__(self, *args):
        return _DkamSDK.StringVector___getitem__(self, *args)

    def __setitem__(self, *args):
        return _DkamSDK.StringVector___setitem__(self, *args)

    def pop(self):
        return _DkamSDK.StringVector_pop(self)

    def append(self, x):
        return _DkamSDK.StringVector_append(self, x)

    def empty(self):
        return _DkamSDK.StringVector_empty(self)

    def size(self):
        return _DkamSDK.StringVector_size(self)

    def swap(self, v):
        return _DkamSDK.StringVector_swap(self, v)

    def begin(self):
        return _DkamSDK.StringVector_begin(self)

    def end(self):
        return _DkamSDK.StringVector_end(self)

    def rbegin(self):
        return _DkamSDK.StringVector_rbegin(self)

    def rend(self):
        return _DkamSDK.StringVector_rend(self)

    def clear(self):
        return _DkamSDK.StringVector_clear(self)

    def get_allocator(self):
        return _DkamSDK.StringVector_get_allocator(self)

    def pop_back(self):
        return _DkamSDK.StringVector_pop_back(self)

    def erase(self, *args):
        return _DkamSDK.StringVector_erase(self, *args)

    def __init__(self, *args):
        _DkamSDK.StringVector_swiginit(self, _DkamSDK.new_StringVector(*args))

    def push_back(self, x):
        return _DkamSDK.StringVector_push_back(self, x)

    def front(self):
        return _DkamSDK.StringVector_front(self)

    def back(self):
        return _DkamSDK.StringVector_back(self)

    def assign(self, n, x):
        return _DkamSDK.StringVector_assign(self, n, x)

    def resize(self, *args):
        return _DkamSDK.StringVector_resize(self, *args)

    def insert(self, *args):
        return _DkamSDK.StringVector_insert(self, *args)

    def reserve(self, n):
        return _DkamSDK.StringVector_reserve(self, n)

    def capacity(self):
        return _DkamSDK.StringVector_capacity(self)
    __swig_destroy__ = _DkamSDK.delete_StringVector

# Register StringVector in _DkamSDK:
_DkamSDK.StringVector_swigregister(StringVector)


def cdata(ptr, nelements=1):
    return _DkamSDK.cdata(ptr, nelements)

def memmove(data, indata):
    return _DkamSDK.memmove(data, indata)
IP_HEADER_LEN = _DkamSDK.IP_HEADER_LEN
UDP_HEADER_LEN = _DkamSDK.UDP_HEADER_LEN
IMAGE_PACKET_HEADER_LEN = _DkamSDK.IMAGE_PACKET_HEADER_LEN
BLOCK_HEAD_LEN = _DkamSDK.BLOCK_HEAD_LEN
GVCP_PORT = _DkamSDK.GVCP_PORT
SORT_BY_IP = _DkamSDK.SORT_BY_IP
SORT_BY_SERIAL_NUMBER = _DkamSDK.SORT_BY_SERIAL_NUMBER
PACK_START = _DkamSDK.PACK_START
DISCOVERY_CMD = _DkamSDK.DISCOVERY_CMD
FORCEIP_CMD = _DkamSDK.FORCEIP_CMD
READREG_CMD = _DkamSDK.READREG_CMD
WRITEREG_CMD = _DkamSDK.WRITEREG_CMD
READMEM_CMD = _DkamSDK.READMEM_CMD
WRITEMEM_CMD = _DkamSDK.WRITEMEM_CMD
PACKETRESEND_CMD = _DkamSDK.PACKETRESEND_CMD
Control_Channel_Privilage_Reg = _DkamSDK.Control_Channel_Privilage_Reg
GVCP_Capability_Reg = _DkamSDK.GVCP_Capability_Reg
Number_of_Message_Channels_Reg = _DkamSDK.Number_of_Message_Channels_Reg
Number_of_Stream_Channels_Reg = _DkamSDK.Number_of_Stream_Channels_Reg
First_Url_Reg = _DkamSDK.First_Url_Reg
Second_Url_Reg = _DkamSDK.Second_Url_Reg
Heartbeat_Timeout_Reg = _DkamSDK.Heartbeat_Timeout_Reg
Source_Port_Reg = _DkamSDK.Source_Port_Reg
Stream_Channel_0_Port_Reg = _DkamSDK.Stream_Channel_0_Port_Reg
Stream_Channel_0_Destination_Address_Reg = _DkamSDK.Stream_Channel_0_Destination_Address_Reg
Stream_Channel_Packet_Size_Reg = _DkamSDK.Stream_Channel_Packet_Size_Reg
Model_Adder = _DkamSDK.Model_Adder
IP_Adder = _DkamSDK.IP_Adder
Mask_Adder = _DkamSDK.Mask_Adder
Gate_Adder = _DkamSDK.Gate_Adder
class RoiPoint(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    size_x = property(_DkamSDK.RoiPoint_size_x_get, _DkamSDK.RoiPoint_size_x_set)
    size_y = property(_DkamSDK.RoiPoint_size_y_get, _DkamSDK.RoiPoint_size_y_set)
    offset_x = property(_DkamSDK.RoiPoint_offset_x_get, _DkamSDK.RoiPoint_offset_x_set)
    offset_y = property(_DkamSDK.RoiPoint_offset_y_get, _DkamSDK.RoiPoint_offset_y_set)

    def __init__(self):
        _DkamSDK.RoiPoint_swiginit(self, _DkamSDK.new_RoiPoint())
    __swig_destroy__ = _DkamSDK.delete_RoiPoint

# Register RoiPoint in _DkamSDK:
_DkamSDK.RoiPoint_swigregister(RoiPoint)

RECIEVE_TIME_STATISTICS_LENGTH = _DkamSDK.RECIEVE_TIME_STATISTICS_LENGTH
class StatisticsData(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    offset = property(_DkamSDK.StatisticsData_offset_get, _DkamSDK.StatisticsData_offset_set)
    bin_steps = property(_DkamSDK.StatisticsData_bin_steps_get, _DkamSDK.StatisticsData_bin_steps_set)
    n_bins = property(_DkamSDK.StatisticsData_n_bins_get, _DkamSDK.StatisticsData_n_bins_set)
    max = property(_DkamSDK.StatisticsData_max_get, _DkamSDK.StatisticsData_max_set)
    min = property(_DkamSDK.StatisticsData_min_get, _DkamSDK.StatisticsData_min_set)
    count = property(_DkamSDK.StatisticsData_count_get, _DkamSDK.StatisticsData_count_set)
    add_more = property(_DkamSDK.StatisticsData_add_more_get, _DkamSDK.StatisticsData_add_more_set)
    add_less = property(_DkamSDK.StatisticsData_add_less_get, _DkamSDK.StatisticsData_add_less_set)
    bins = property(_DkamSDK.StatisticsData_bins_get, _DkamSDK.StatisticsData_bins_set)

    def __init__(self):
        _DkamSDK.StatisticsData_swiginit(self, _DkamSDK.new_StatisticsData())
    __swig_destroy__ = _DkamSDK.delete_StatisticsData

# Register StatisticsData in _DkamSDK:
_DkamSDK.StatisticsData_swigregister(StatisticsData)

class StatisticsDataCSharp(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    offset = property(_DkamSDK.StatisticsDataCSharp_offset_get, _DkamSDK.StatisticsDataCSharp_offset_set)
    bin_steps = property(_DkamSDK.StatisticsDataCSharp_bin_steps_get, _DkamSDK.StatisticsDataCSharp_bin_steps_set)
    n_bins = property(_DkamSDK.StatisticsDataCSharp_n_bins_get, _DkamSDK.StatisticsDataCSharp_n_bins_set)
    max = property(_DkamSDK.StatisticsDataCSharp_max_get, _DkamSDK.StatisticsDataCSharp_max_set)
    min = property(_DkamSDK.StatisticsDataCSharp_min_get, _DkamSDK.StatisticsDataCSharp_min_set)
    count = property(_DkamSDK.StatisticsDataCSharp_count_get, _DkamSDK.StatisticsDataCSharp_count_set)
    add_more = property(_DkamSDK.StatisticsDataCSharp_add_more_get, _DkamSDK.StatisticsDataCSharp_add_more_set)
    add_less = property(_DkamSDK.StatisticsDataCSharp_add_less_get, _DkamSDK.StatisticsDataCSharp_add_less_set)

    def __init__(self):
        _DkamSDK.StatisticsDataCSharp_swiginit(self, _DkamSDK.new_StatisticsDataCSharp())
    __swig_destroy__ = _DkamSDK.delete_StatisticsDataCSharp

# Register StatisticsDataCSharp in _DkamSDK:
_DkamSDK.StatisticsDataCSharp_swigregister(StatisticsDataCSharp)

class PhotoInfo(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    pixel = property(_DkamSDK.PhotoInfo_pixel_get, _DkamSDK.PhotoInfo_pixel_set)
    pixel_length = property(_DkamSDK.PhotoInfo_pixel_length_get, _DkamSDK.PhotoInfo_pixel_length_set)
    pixel_format = property(_DkamSDK.PhotoInfo_pixel_format_get, _DkamSDK.PhotoInfo_pixel_format_set)
    pixel_width = property(_DkamSDK.PhotoInfo_pixel_width_get, _DkamSDK.PhotoInfo_pixel_width_set)
    pixel_height = property(_DkamSDK.PhotoInfo_pixel_height_get, _DkamSDK.PhotoInfo_pixel_height_set)
    cloud_unit = property(_DkamSDK.PhotoInfo_cloud_unit_get, _DkamSDK.PhotoInfo_cloud_unit_set)
    payload_size = property(_DkamSDK.PhotoInfo_payload_size_get, _DkamSDK.PhotoInfo_payload_size_set)
    timestamp_high = property(_DkamSDK.PhotoInfo_timestamp_high_get, _DkamSDK.PhotoInfo_timestamp_high_set)
    timestamp_low = property(_DkamSDK.PhotoInfo_timestamp_low_get, _DkamSDK.PhotoInfo_timestamp_low_set)
    roi = property(_DkamSDK.PhotoInfo_roi_get, _DkamSDK.PhotoInfo_roi_set)
    block_id = property(_DkamSDK.PhotoInfo_block_id_get, _DkamSDK.PhotoInfo_block_id_set)
    stream_channel_index_ = property(_DkamSDK.PhotoInfo_stream_channel_index__get, _DkamSDK.PhotoInfo_stream_channel_index__set)

    def __init__(self):
        _DkamSDK.PhotoInfo_swiginit(self, _DkamSDK.new_PhotoInfo())
    __swig_destroy__ = _DkamSDK.delete_PhotoInfo

# Register PhotoInfo in _DkamSDK:
_DkamSDK.PhotoInfo_swigregister(PhotoInfo)

class PhotoInfoCSharp(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    pixel_length = property(_DkamSDK.PhotoInfoCSharp_pixel_length_get, _DkamSDK.PhotoInfoCSharp_pixel_length_set)
    pixel_format = property(_DkamSDK.PhotoInfoCSharp_pixel_format_get, _DkamSDK.PhotoInfoCSharp_pixel_format_set)
    pixel_width = property(_DkamSDK.PhotoInfoCSharp_pixel_width_get, _DkamSDK.PhotoInfoCSharp_pixel_width_set)
    pixel_height = property(_DkamSDK.PhotoInfoCSharp_pixel_height_get, _DkamSDK.PhotoInfoCSharp_pixel_height_set)
    cloud_unit = property(_DkamSDK.PhotoInfoCSharp_cloud_unit_get, _DkamSDK.PhotoInfoCSharp_cloud_unit_set)
    payload_size = property(_DkamSDK.PhotoInfoCSharp_payload_size_get, _DkamSDK.PhotoInfoCSharp_payload_size_set)
    timestamp_high = property(_DkamSDK.PhotoInfoCSharp_timestamp_high_get, _DkamSDK.PhotoInfoCSharp_timestamp_high_set)
    timestamp_low = property(_DkamSDK.PhotoInfoCSharp_timestamp_low_get, _DkamSDK.PhotoInfoCSharp_timestamp_low_set)
    roi = property(_DkamSDK.PhotoInfoCSharp_roi_get, _DkamSDK.PhotoInfoCSharp_roi_set)
    block_id = property(_DkamSDK.PhotoInfoCSharp_block_id_get, _DkamSDK.PhotoInfoCSharp_block_id_set)
    stream_channel_index_ = property(_DkamSDK.PhotoInfoCSharp_stream_channel_index__get, _DkamSDK.PhotoInfoCSharp_stream_channel_index__set)

    def __init__(self):
        _DkamSDK.PhotoInfoCSharp_swiginit(self, _DkamSDK.new_PhotoInfoCSharp())
    __swig_destroy__ = _DkamSDK.delete_PhotoInfoCSharp

# Register PhotoInfoCSharp in _DkamSDK:
_DkamSDK.PhotoInfoCSharp_swigregister(PhotoInfoCSharp)

class RecvDataBuff(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    status = property(_DkamSDK.RecvDataBuff_status_get, _DkamSDK.RecvDataBuff_status_set)
    head_packet_flag = property(_DkamSDK.RecvDataBuff_head_packet_flag_get, _DkamSDK.RecvDataBuff_head_packet_flag_set)
    data = property(_DkamSDK.RecvDataBuff_data_get, _DkamSDK.RecvDataBuff_data_set)
    block_head = property(_DkamSDK.RecvDataBuff_block_head_get, _DkamSDK.RecvDataBuff_block_head_set)
    next = property(_DkamSDK.RecvDataBuff_next_get, _DkamSDK.RecvDataBuff_next_set)

    def __init__(self):
        _DkamSDK.RecvDataBuff_swiginit(self, _DkamSDK.new_RecvDataBuff())
    __swig_destroy__ = _DkamSDK.delete_RecvDataBuff

# Register RecvDataBuff in _DkamSDK:
_DkamSDK.RecvDataBuff_swigregister(RecvDataBuff)

class RecvDataTemp(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    head_packet_flag = property(_DkamSDK.RecvDataTemp_head_packet_flag_get, _DkamSDK.RecvDataTemp_head_packet_flag_set)
    resend_check_point = property(_DkamSDK.RecvDataTemp_resend_check_point_get, _DkamSDK.RecvDataTemp_resend_check_point_set)
    out_of_time_check = property(_DkamSDK.RecvDataTemp_out_of_time_check_get, _DkamSDK.RecvDataTemp_out_of_time_check_set)
    block_id = property(_DkamSDK.RecvDataTemp_block_id_get, _DkamSDK.RecvDataTemp_block_id_set)
    recv_packet_num = property(_DkamSDK.RecvDataTemp_recv_packet_num_get, _DkamSDK.RecvDataTemp_recv_packet_num_set)
    all_data_size = property(_DkamSDK.RecvDataTemp_all_data_size_get, _DkamSDK.RecvDataTemp_all_data_size_set)
    all_packet_num = property(_DkamSDK.RecvDataTemp_all_packet_num_get, _DkamSDK.RecvDataTemp_all_packet_num_set)
    recv_packet_id = property(_DkamSDK.RecvDataTemp_recv_packet_id_get, _DkamSDK.RecvDataTemp_recv_packet_id_set)
    data = property(_DkamSDK.RecvDataTemp_data_get, _DkamSDK.RecvDataTemp_data_set)
    block_head = property(_DkamSDK.RecvDataTemp_block_head_get, _DkamSDK.RecvDataTemp_block_head_set)
    next = property(_DkamSDK.RecvDataTemp_next_get, _DkamSDK.RecvDataTemp_next_set)

    def __init__(self):
        _DkamSDK.RecvDataTemp_swiginit(self, _DkamSDK.new_RecvDataTemp())
    __swig_destroy__ = _DkamSDK.delete_RecvDataTemp

# Register RecvDataTemp in _DkamSDK:
_DkamSDK.RecvDataTemp_swigregister(RecvDataTemp)

class DiscoveryInfo(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    camera_ip = property(_DkamSDK.DiscoveryInfo_camera_ip_get, _DkamSDK.DiscoveryInfo_camera_ip_set)
    camera_mask = property(_DkamSDK.DiscoveryInfo_camera_mask_get, _DkamSDK.DiscoveryInfo_camera_mask_set)
    camera_gateway = property(_DkamSDK.DiscoveryInfo_camera_gateway_get, _DkamSDK.DiscoveryInfo_camera_gateway_set)
    camera_mac_low = property(_DkamSDK.DiscoveryInfo_camera_mac_low_get, _DkamSDK.DiscoveryInfo_camera_mac_low_set)
    camera_mac_high = property(_DkamSDK.DiscoveryInfo_camera_mac_high_get, _DkamSDK.DiscoveryInfo_camera_mac_high_set)
    device_vendor_name = property(_DkamSDK.DiscoveryInfo_device_vendor_name_get, _DkamSDK.DiscoveryInfo_device_vendor_name_set)
    device_model_name = property(_DkamSDK.DiscoveryInfo_device_model_name_get, _DkamSDK.DiscoveryInfo_device_model_name_set)
    device_version = property(_DkamSDK.DiscoveryInfo_device_version_get, _DkamSDK.DiscoveryInfo_device_version_set)
    device_manufacturer_info = property(_DkamSDK.DiscoveryInfo_device_manufacturer_info_get, _DkamSDK.DiscoveryInfo_device_manufacturer_info_set)
    device_serial_number = property(_DkamSDK.DiscoveryInfo_device_serial_number_get, _DkamSDK.DiscoveryInfo_device_serial_number_set)
    device_user_id = property(_DkamSDK.DiscoveryInfo_device_user_id_get, _DkamSDK.DiscoveryInfo_device_user_id_set)
    computer_ip = property(_DkamSDK.DiscoveryInfo_computer_ip_get, _DkamSDK.DiscoveryInfo_computer_ip_set)
    computer_mask = property(_DkamSDK.DiscoveryInfo_computer_mask_get, _DkamSDK.DiscoveryInfo_computer_mask_set)
    computer_gateway = property(_DkamSDK.DiscoveryInfo_computer_gateway_get, _DkamSDK.DiscoveryInfo_computer_gateway_set)
    mtu = property(_DkamSDK.DiscoveryInfo_mtu_get, _DkamSDK.DiscoveryInfo_mtu_set)
    computer_adapter = property(_DkamSDK.DiscoveryInfo_computer_adapter_get, _DkamSDK.DiscoveryInfo_computer_adapter_set)

    def __init__(self):
        _DkamSDK.DiscoveryInfo_swiginit(self, _DkamSDK.new_DiscoveryInfo())
    __swig_destroy__ = _DkamSDK.delete_DiscoveryInfo

# Register DiscoveryInfo in _DkamSDK:
_DkamSDK.DiscoveryInfo_swigregister(DiscoveryInfo)

class PacketInfo(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    in_status = property(_DkamSDK.PacketInfo_in_status_get, _DkamSDK.PacketInfo_in_status_set)
    in_block_id = property(_DkamSDK.PacketInfo_in_block_id_get, _DkamSDK.PacketInfo_in_block_id_set)
    in_packet_id = property(_DkamSDK.PacketInfo_in_packet_id_get, _DkamSDK.PacketInfo_in_packet_id_set)
    packet_format = property(_DkamSDK.PacketInfo_packet_format_get, _DkamSDK.PacketInfo_packet_format_set)
    data_packet_len = property(_DkamSDK.PacketInfo_data_packet_len_get, _DkamSDK.PacketInfo_data_packet_len_set)

    def __init__(self):
        _DkamSDK.PacketInfo_swiginit(self, _DkamSDK.new_PacketInfo())
    __swig_destroy__ = _DkamSDK.delete_PacketInfo

# Register PacketInfo in _DkamSDK:
_DkamSDK.PacketInfo_swigregister(PacketInfo)

class CameraParameter(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    Kc = property(_DkamSDK.CameraParameter_Kc_get, _DkamSDK.CameraParameter_Kc_set)
    K = property(_DkamSDK.CameraParameter_K_get, _DkamSDK.CameraParameter_K_set)
    R = property(_DkamSDK.CameraParameter_R_get, _DkamSDK.CameraParameter_R_set)
    T = property(_DkamSDK.CameraParameter_T_get, _DkamSDK.CameraParameter_T_set)

    def __init__(self):
        _DkamSDK.CameraParameter_swiginit(self, _DkamSDK.new_CameraParameter())
    __swig_destroy__ = _DkamSDK.delete_CameraParameter

# Register CameraParameter in _DkamSDK:
_DkamSDK.CameraParameter_swigregister(CameraParameter)

class InstanceDevice(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    camera_ip = property(_DkamSDK.InstanceDevice_camera_ip_get, _DkamSDK.InstanceDevice_camera_ip_set)
    camera_mask = property(_DkamSDK.InstanceDevice_camera_mask_get, _DkamSDK.InstanceDevice_camera_mask_set)
    computer_ip = property(_DkamSDK.InstanceDevice_computer_ip_get, _DkamSDK.InstanceDevice_computer_ip_set)
    computer_mask = property(_DkamSDK.InstanceDevice_computer_mask_get, _DkamSDK.InstanceDevice_computer_mask_set)
    computer_mtu = property(_DkamSDK.InstanceDevice_computer_mtu_get, _DkamSDK.InstanceDevice_computer_mtu_set)
    recv_buffer_num = property(_DkamSDK.InstanceDevice_recv_buffer_num_get, _DkamSDK.InstanceDevice_recv_buffer_num_set)
    computer_adapter = property(_DkamSDK.InstanceDevice_computer_adapter_get, _DkamSDK.InstanceDevice_computer_adapter_set)

    def __init__(self):
        _DkamSDK.InstanceDevice_swiginit(self, _DkamSDK.new_InstanceDevice())
    __swig_destroy__ = _DkamSDK.delete_InstanceDevice

# Register InstanceDevice in _DkamSDK:
_DkamSDK.InstanceDevice_swigregister(InstanceDevice)

class DiscoverCmdPack(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    start = property(_DkamSDK.DiscoverCmdPack_start_get, _DkamSDK.DiscoverCmdPack_start_set)
    flag = property(_DkamSDK.DiscoverCmdPack_flag_get, _DkamSDK.DiscoverCmdPack_flag_set)
    command = property(_DkamSDK.DiscoverCmdPack_command_get, _DkamSDK.DiscoverCmdPack_command_set)
    length = property(_DkamSDK.DiscoverCmdPack_length_get, _DkamSDK.DiscoverCmdPack_length_set)
    req_id = property(_DkamSDK.DiscoverCmdPack_req_id_get, _DkamSDK.DiscoverCmdPack_req_id_set)

    def __init__(self):
        _DkamSDK.DiscoverCmdPack_swiginit(self, _DkamSDK.new_DiscoverCmdPack())
    __swig_destroy__ = _DkamSDK.delete_DiscoverCmdPack

# Register DiscoverCmdPack in _DkamSDK:
_DkamSDK.DiscoverCmdPack_swigregister(DiscoverCmdPack)

class ForceIpCmdPack(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    start = property(_DkamSDK.ForceIpCmdPack_start_get, _DkamSDK.ForceIpCmdPack_start_set)
    flag = property(_DkamSDK.ForceIpCmdPack_flag_get, _DkamSDK.ForceIpCmdPack_flag_set)
    command = property(_DkamSDK.ForceIpCmdPack_command_get, _DkamSDK.ForceIpCmdPack_command_set)
    length = property(_DkamSDK.ForceIpCmdPack_length_get, _DkamSDK.ForceIpCmdPack_length_set)
    req_id = property(_DkamSDK.ForceIpCmdPack_req_id_get, _DkamSDK.ForceIpCmdPack_req_id_set)
    reserved = property(_DkamSDK.ForceIpCmdPack_reserved_get, _DkamSDK.ForceIpCmdPack_reserved_set)
    mac_addr_high = property(_DkamSDK.ForceIpCmdPack_mac_addr_high_get, _DkamSDK.ForceIpCmdPack_mac_addr_high_set)
    mac_addr_low = property(_DkamSDK.ForceIpCmdPack_mac_addr_low_get, _DkamSDK.ForceIpCmdPack_mac_addr_low_set)
    reserved1 = property(_DkamSDK.ForceIpCmdPack_reserved1_get, _DkamSDK.ForceIpCmdPack_reserved1_set)
    ip = property(_DkamSDK.ForceIpCmdPack_ip_get, _DkamSDK.ForceIpCmdPack_ip_set)
    reserved2 = property(_DkamSDK.ForceIpCmdPack_reserved2_get, _DkamSDK.ForceIpCmdPack_reserved2_set)
    mask = property(_DkamSDK.ForceIpCmdPack_mask_get, _DkamSDK.ForceIpCmdPack_mask_set)
    reserved3 = property(_DkamSDK.ForceIpCmdPack_reserved3_get, _DkamSDK.ForceIpCmdPack_reserved3_set)
    gateway = property(_DkamSDK.ForceIpCmdPack_gateway_get, _DkamSDK.ForceIpCmdPack_gateway_set)

    def __init__(self):
        _DkamSDK.ForceIpCmdPack_swiginit(self, _DkamSDK.new_ForceIpCmdPack())
    __swig_destroy__ = _DkamSDK.delete_ForceIpCmdPack

# Register ForceIpCmdPack in _DkamSDK:
_DkamSDK.ForceIpCmdPack_swigregister(ForceIpCmdPack)

class ForceIpRebootCmdPack(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    start = property(_DkamSDK.ForceIpRebootCmdPack_start_get, _DkamSDK.ForceIpRebootCmdPack_start_set)
    flag = property(_DkamSDK.ForceIpRebootCmdPack_flag_get, _DkamSDK.ForceIpRebootCmdPack_flag_set)
    command = property(_DkamSDK.ForceIpRebootCmdPack_command_get, _DkamSDK.ForceIpRebootCmdPack_command_set)
    length = property(_DkamSDK.ForceIpRebootCmdPack_length_get, _DkamSDK.ForceIpRebootCmdPack_length_set)
    req_id = property(_DkamSDK.ForceIpRebootCmdPack_req_id_get, _DkamSDK.ForceIpRebootCmdPack_req_id_set)
    model_addr = property(_DkamSDK.ForceIpRebootCmdPack_model_addr_get, _DkamSDK.ForceIpRebootCmdPack_model_addr_set)
    model = property(_DkamSDK.ForceIpRebootCmdPack_model_get, _DkamSDK.ForceIpRebootCmdPack_model_set)
    ip_addr = property(_DkamSDK.ForceIpRebootCmdPack_ip_addr_get, _DkamSDK.ForceIpRebootCmdPack_ip_addr_set)
    ip = property(_DkamSDK.ForceIpRebootCmdPack_ip_get, _DkamSDK.ForceIpRebootCmdPack_ip_set)
    mask_addr = property(_DkamSDK.ForceIpRebootCmdPack_mask_addr_get, _DkamSDK.ForceIpRebootCmdPack_mask_addr_set)
    mask = property(_DkamSDK.ForceIpRebootCmdPack_mask_get, _DkamSDK.ForceIpRebootCmdPack_mask_set)
    gateway_addr = property(_DkamSDK.ForceIpRebootCmdPack_gateway_addr_get, _DkamSDK.ForceIpRebootCmdPack_gateway_addr_set)
    gateway = property(_DkamSDK.ForceIpRebootCmdPack_gateway_get, _DkamSDK.ForceIpRebootCmdPack_gateway_set)
    restart_addr = property(_DkamSDK.ForceIpRebootCmdPack_restart_addr_get, _DkamSDK.ForceIpRebootCmdPack_restart_addr_set)
    restart = property(_DkamSDK.ForceIpRebootCmdPack_restart_get, _DkamSDK.ForceIpRebootCmdPack_restart_set)

    def __init__(self):
        _DkamSDK.ForceIpRebootCmdPack_swiginit(self, _DkamSDK.new_ForceIpRebootCmdPack())
    __swig_destroy__ = _DkamSDK.delete_ForceIpRebootCmdPack

# Register ForceIpRebootCmdPack in _DkamSDK:
_DkamSDK.ForceIpRebootCmdPack_swigregister(ForceIpRebootCmdPack)

class WriteRegCmdPack(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    start = property(_DkamSDK.WriteRegCmdPack_start_get, _DkamSDK.WriteRegCmdPack_start_set)
    flag = property(_DkamSDK.WriteRegCmdPack_flag_get, _DkamSDK.WriteRegCmdPack_flag_set)
    command = property(_DkamSDK.WriteRegCmdPack_command_get, _DkamSDK.WriteRegCmdPack_command_set)
    length = property(_DkamSDK.WriteRegCmdPack_length_get, _DkamSDK.WriteRegCmdPack_length_set)
    req_id = property(_DkamSDK.WriteRegCmdPack_req_id_get, _DkamSDK.WriteRegCmdPack_req_id_set)
    register_addr = property(_DkamSDK.WriteRegCmdPack_register_addr_get, _DkamSDK.WriteRegCmdPack_register_addr_set)
    data = property(_DkamSDK.WriteRegCmdPack_data_get, _DkamSDK.WriteRegCmdPack_data_set)

    def __init__(self):
        _DkamSDK.WriteRegCmdPack_swiginit(self, _DkamSDK.new_WriteRegCmdPack())
    __swig_destroy__ = _DkamSDK.delete_WriteRegCmdPack

# Register WriteRegCmdPack in _DkamSDK:
_DkamSDK.WriteRegCmdPack_swigregister(WriteRegCmdPack)

class ReadRegCmdPack(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    start = property(_DkamSDK.ReadRegCmdPack_start_get, _DkamSDK.ReadRegCmdPack_start_set)
    flag = property(_DkamSDK.ReadRegCmdPack_flag_get, _DkamSDK.ReadRegCmdPack_flag_set)
    command = property(_DkamSDK.ReadRegCmdPack_command_get, _DkamSDK.ReadRegCmdPack_command_set)
    length = property(_DkamSDK.ReadRegCmdPack_length_get, _DkamSDK.ReadRegCmdPack_length_set)
    req_id = property(_DkamSDK.ReadRegCmdPack_req_id_get, _DkamSDK.ReadRegCmdPack_req_id_set)
    register_addr = property(_DkamSDK.ReadRegCmdPack_register_addr_get, _DkamSDK.ReadRegCmdPack_register_addr_set)

    def __init__(self):
        _DkamSDK.ReadRegCmdPack_swiginit(self, _DkamSDK.new_ReadRegCmdPack())
    __swig_destroy__ = _DkamSDK.delete_ReadRegCmdPack

# Register ReadRegCmdPack in _DkamSDK:
_DkamSDK.ReadRegCmdPack_swigregister(ReadRegCmdPack)

class ReadMemCmdPack(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    start = property(_DkamSDK.ReadMemCmdPack_start_get, _DkamSDK.ReadMemCmdPack_start_set)
    flag = property(_DkamSDK.ReadMemCmdPack_flag_get, _DkamSDK.ReadMemCmdPack_flag_set)
    command = property(_DkamSDK.ReadMemCmdPack_command_get, _DkamSDK.ReadMemCmdPack_command_set)
    length = property(_DkamSDK.ReadMemCmdPack_length_get, _DkamSDK.ReadMemCmdPack_length_set)
    req_id = property(_DkamSDK.ReadMemCmdPack_req_id_get, _DkamSDK.ReadMemCmdPack_req_id_set)
    address = property(_DkamSDK.ReadMemCmdPack_address_get, _DkamSDK.ReadMemCmdPack_address_set)
    reserved = property(_DkamSDK.ReadMemCmdPack_reserved_get, _DkamSDK.ReadMemCmdPack_reserved_set)
    count = property(_DkamSDK.ReadMemCmdPack_count_get, _DkamSDK.ReadMemCmdPack_count_set)

    def __init__(self):
        _DkamSDK.ReadMemCmdPack_swiginit(self, _DkamSDK.new_ReadMemCmdPack())
    __swig_destroy__ = _DkamSDK.delete_ReadMemCmdPack

# Register ReadMemCmdPack in _DkamSDK:
_DkamSDK.ReadMemCmdPack_swigregister(ReadMemCmdPack)

class WriteMemCmdPack(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    start = property(_DkamSDK.WriteMemCmdPack_start_get, _DkamSDK.WriteMemCmdPack_start_set)
    flag = property(_DkamSDK.WriteMemCmdPack_flag_get, _DkamSDK.WriteMemCmdPack_flag_set)
    command = property(_DkamSDK.WriteMemCmdPack_command_get, _DkamSDK.WriteMemCmdPack_command_set)
    length = property(_DkamSDK.WriteMemCmdPack_length_get, _DkamSDK.WriteMemCmdPack_length_set)
    req_id = property(_DkamSDK.WriteMemCmdPack_req_id_get, _DkamSDK.WriteMemCmdPack_req_id_set)
    address = property(_DkamSDK.WriteMemCmdPack_address_get, _DkamSDK.WriteMemCmdPack_address_set)
    reserved = property(_DkamSDK.WriteMemCmdPack_reserved_get, _DkamSDK.WriteMemCmdPack_reserved_set)
    count = property(_DkamSDK.WriteMemCmdPack_count_get, _DkamSDK.WriteMemCmdPack_count_set)
    data = property(_DkamSDK.WriteMemCmdPack_data_get, _DkamSDK.WriteMemCmdPack_data_set)

    def __init__(self):
        _DkamSDK.WriteMemCmdPack_swiginit(self, _DkamSDK.new_WriteMemCmdPack())
    __swig_destroy__ = _DkamSDK.delete_WriteMemCmdPack

# Register WriteMemCmdPack in _DkamSDK:
_DkamSDK.WriteMemCmdPack_swigregister(WriteMemCmdPack)

class PacketResendCmdPack(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    start = property(_DkamSDK.PacketResendCmdPack_start_get, _DkamSDK.PacketResendCmdPack_start_set)
    flag = property(_DkamSDK.PacketResendCmdPack_flag_get, _DkamSDK.PacketResendCmdPack_flag_set)
    command = property(_DkamSDK.PacketResendCmdPack_command_get, _DkamSDK.PacketResendCmdPack_command_set)
    length = property(_DkamSDK.PacketResendCmdPack_length_get, _DkamSDK.PacketResendCmdPack_length_set)
    req_id = property(_DkamSDK.PacketResendCmdPack_req_id_get, _DkamSDK.PacketResendCmdPack_req_id_set)
    stream_channel_index = property(_DkamSDK.PacketResendCmdPack_stream_channel_index_get, _DkamSDK.PacketResendCmdPack_stream_channel_index_set)
    block_id = property(_DkamSDK.PacketResendCmdPack_block_id_get, _DkamSDK.PacketResendCmdPack_block_id_set)
    first_packet_id = property(_DkamSDK.PacketResendCmdPack_first_packet_id_get, _DkamSDK.PacketResendCmdPack_first_packet_id_set)
    last_packet_id = property(_DkamSDK.PacketResendCmdPack_last_packet_id_get, _DkamSDK.PacketResendCmdPack_last_packet_id_set)

    def __init__(self):
        _DkamSDK.PacketResendCmdPack_swiginit(self, _DkamSDK.new_PacketResendCmdPack())
    __swig_destroy__ = _DkamSDK.delete_PacketResendCmdPack

# Register PacketResendCmdPack in _DkamSDK:
_DkamSDK.PacketResendCmdPack_swigregister(PacketResendCmdPack)


def DiscoverCamera():
    """
    The Function is： Discover Camera in the LAN.
    """
    return _DkamSDK.DiscoverCamera()

def CreateCamera():
    """
    The Function is: Create camera object.
    """
    return _DkamSDK.CreateCamera()

def DestroyCamera():
    """
    The Function is: Destroy camera object.
    """
    return _DkamSDK.DestroyCamera()

def CameraSort(sort_mode):
    """
    The Function is: Cameras can be sorted by IP or serial number.
    """
    return _DkamSDK.CameraSort(sort_mode)

def GetCameraCCPStatus(camera_index, data):
    """
    The Function is: Check the status of the camera CCP.
    """
    return _DkamSDK.GetCameraCCPStatus(camera_index, data)

def GetCameraXMLNodeNames(camera_index, node_names, len):
    """
    The Function is: Get the camera xml node names.
    """
    return _DkamSDK.GetCameraXMLNodeNames(camera_index, node_names, len)

def GetNodeMaxValue(camera_index, key):
    """
    The Function is: Get the camera max value of the xml node.
    """
    return _DkamSDK.GetNodeMaxValue(camera_index, key)

def GetNodeMinValue(camera_index, key):
    """
    The Function is: Get the camera min value of the xml node.
    """
    return _DkamSDK.GetNodeMinValue(camera_index, key)

def GetNodeIncValue(camera_index, key):
    """
    The Function is: Get the camera increase value of the xml node.
    """
    return _DkamSDK.GetNodeIncValue(camera_index, key)

def ReadStringRegister(camera_index, key, reg_str):
    """
    The Function is: Get the camera string types register.
    """
    return _DkamSDK.ReadStringRegister(camera_index, key, reg_str)

def CameraIP(camera_index):
    """
    The Function is: Looking the camera IP in the LAN.
    """
    return _DkamSDK.CameraIP(camera_index)

def SetLogLevel(error, debug, warnning, info):
    """
    The Function is: Open different kinds of logs for the camera, open is 1,close is 0.
    """
    return _DkamSDK.SetLogLevel(error, debug, warnning, info)

def CameraConnect(camera_index):
    """
    The Function is: Connect the camera.
    """
    return _DkamSDK.CameraConnect(camera_index)

def StreamOn(camera_index, channel_index):
    """
    The Function is: Open the camera`s point cloud、gray、RGB data stream channel.
    """
    return _DkamSDK.StreamOn(camera_index, channel_index)

def AcquisitionStart(camera_index):
    """
    The Function is: The camera start to acquisition data.
    """
    return _DkamSDK.AcquisitionStart(camera_index)

def FlushBuffer(camera_index, channel_index):
    """
    The Function is: Clear Buffer Data from the camera.
    """
    return _DkamSDK.FlushBuffer(camera_index, channel_index)

def SetMaxBufferLength(camera_index, channel_index, size):
    """
    The Function is: Set the camera maximum buffer length.
    """
    return _DkamSDK.SetMaxBufferLength(camera_index, channel_index, size)

def GetMaxBufferLength(camera_index, channel_index):
    """
    The Function is: Get the camera maximum buffer length.
    """
    return _DkamSDK.GetMaxBufferLength(camera_index, channel_index)

def SetPacketResendRatio(camera_index, channel_index, ratio):
    """
    The Function is: Set the camera packet resend ratio.
    """
    return _DkamSDK.SetPacketResendRatio(camera_index, channel_index, ratio)

def GetPacketResendRatio(camera_index, channel_index):
    """
    The Function is: Get the camera packet resend ratio.
    """
    return _DkamSDK.GetPacketResendRatio(camera_index, channel_index)

def SetSocketSelectTimeout(camera_index, channel_index, timeout):
    """
    The Function is: Set the camera socket select timeout.
    """
    return _DkamSDK.SetSocketSelectTimeout(camera_index, channel_index, timeout)

def GetSocketSelectTimeout(camera_index, channel_index):
    """
    The Function is: Get the camera socket select timeout.
    """
    return _DkamSDK.GetSocketSelectTimeout(camera_index, channel_index)

def SetPacketTimeout(camera_index, channel_index, timeout):
    """
    The Function is: Set the camera packet timeout.
    """
    return _DkamSDK.SetPacketTimeout(camera_index, channel_index, timeout)

def GetPacketTimeout(camera_index, channel_index):
    """
    The Function is: Get the camera packet timeout.
    """
    return _DkamSDK.GetPacketTimeout(camera_index, channel_index)

def SetBlockTimeout(camera_index, channel_index, timeout):
    """
    The Function is: Set the camera block timeout.
    """
    return _DkamSDK.SetBlockTimeout(camera_index, channel_index, timeout)

def GetBlockTimeout(camera_index, channel_index):
    """
    The Function is: Get the camera block timeout.
    """
    return _DkamSDK.GetBlockTimeout(camera_index, channel_index)

def GetBlockStatistics(camera_index, channel_index, completed_buffers, failures, timeouts, underruns, aborteds, missing_frames, block_camera_wrong, size_mismatch_errors):
    """
    The Function is: Get the camera block statistics.
    """
    return _DkamSDK.GetBlockStatistics(camera_index, channel_index, completed_buffers, failures, timeouts, underruns, aborteds, missing_frames, block_camera_wrong, size_mismatch_errors)

def GetPacketStatistics(camera_index, channel_index, received_packets, missing_packets, error_packets, ignored_packets, resend_requests, resent_packets, duplicated_packets):
    """
    The Function is: Get the camera packet statistics.
    """
    return _DkamSDK.GetPacketStatistics(camera_index, channel_index, received_packets, missing_packets, error_packets, ignored_packets, resend_requests, resent_packets, duplicated_packets)

def GetRecieveTimeStatistics(camera_index, channel_index, o_statistics_data):
    """
    The Function is: Get the camera recieve time statistics.
    """
    return _DkamSDK.GetRecieveTimeStatistics(camera_index, channel_index, o_statistics_data)

def GetNetSpeed(camera_index, channel_index):
    """
    The Function is: Get the camera net speed.
    """
    return _DkamSDK.GetNetSpeed(camera_index, channel_index)

def GetBlockRate(camera_index, channel_index):
    """
    The Function is: Get the camera block rate.
    """
    return _DkamSDK.GetBlockRate(camera_index, channel_index)

def Capture(camera_index, channel_index, raw_data):
    """
    The Function is: The camera capture data.Blocking occurs when no data is available. point cloud channel:1 gray channel:0 RGB channel:2.
    """
    return _DkamSDK.Capture(camera_index, channel_index, raw_data)

def TryCapture(camera_index, channel_index, raw_data):
    """
    The Function is: The camera try capture data.Return an error code when no data is available. point cloud channel:1 gray channel:0 RGB channel:2.
    """
    return _DkamSDK.TryCapture(camera_index, channel_index, raw_data)

def TimeoutCapture(camera_index, channel_index, raw_data, timeout):
    """
    The Function is: The camera timeout capture data.When no data is available, it will wait. If the wait timeout, an error code will be returned. point cloud channel:1 gray channel:0 RGB channel:2.
    """
    return _DkamSDK.TimeoutCapture(camera_index, channel_index, raw_data, timeout)

def Convert3DPointFromCharToFloat(camera_index, raw_data, output):
    """
    The Function is: Convert point cloud data from char to float.
    """
    return _DkamSDK.Convert3DPointFromCharToFloat(camera_index, raw_data, output)

def RawdataToRgb888(camera_index, rgb_data):
    """
    The Function is: Convert raw data to RGB888.
    """
    return _DkamSDK.RawdataToRgb888(camera_index, rgb_data)

def GetCloudPlaneX(camera_index, raw_data, imagedata):
    """
    The Function is: Get the camera point cloud x plane data.
    """
    return _DkamSDK.GetCloudPlaneX(camera_index, raw_data, imagedata)

def GetCloudPlaneY(camera_index, raw_data, imagedata):
    """
    The Function is: Get the camera point cloud y plane data.
    """
    return _DkamSDK.GetCloudPlaneY(camera_index, raw_data, imagedata)

def GetCloudPlaneZ(camera_index, raw_data, imagedata):
    """
    The Function is: Get the camera point cloud z plane data.
    """
    return _DkamSDK.GetCloudPlaneZ(camera_index, raw_data, imagedata)

def SaveCloudPlane(camera_index, raw_data, imagedata, path_name):
    """
    The Function is: Save the camera point cloud x/y/z plane data.
    """
    return _DkamSDK.SaveCloudPlane(camera_index, raw_data, imagedata, path_name)

def AcquisitionStop(camera_index):
    """
    The Function is: The camera stop to acquisition data.
    """
    return _DkamSDK.AcquisitionStop(camera_index)

def StreamOff(camera_index, channel_index):
    """
    The Function is: Close the camera`s point cloud、gray、RGB data stream channel.
    """
    return _DkamSDK.StreamOff(camera_index, channel_index)

def CameraDisconnect(camera_index):
    """
    The Function is: Disconnect the camera.
    """
    return _DkamSDK.CameraDisconnect(camera_index)

def GetCamInternelParameter(camera_index, camera_cnt, Kc, K):
    """
    The Function is: Get the camera internel parameter.
	Kc is lens distortion parameter,K is focal length,main point parameter.
    """
    return _DkamSDK.GetCamInternelParameter(camera_index, camera_cnt, Kc, K)

def GetCamExternelParameter(camera_index, camera_cnt, R, T):
    """
    The Function is: Get the camera externel parameter.
	R is gray camera relative RGB camera rotation matrix,
	T is gray camera relative RGB camera translation matrix.
    """
    return _DkamSDK.GetCamExternelParameter(camera_index, camera_cnt, R, T)

def GetRegisterAddr(camera_index, key):
    """
    The Function is: Get the camera register address.
    """
    return _DkamSDK.GetRegisterAddr(camera_index, key)

def WriteRegister(camera_index, register_addr, data):
    """
    The Function is: Write value to the camera register.
    """
    return _DkamSDK.WriteRegister(camera_index, register_addr, data)

def ReadRegister(camera_index, register_addr, data):
    """
    The Function is: Read the value of the camera register.
    """
    return _DkamSDK.ReadRegister(camera_index, register_addr, data)

def ForceIP(camera_index, ip, mask, gateway):
    """
    The Function is: Force the camera IP.When the camera is restarted, the IP is changed back to the original IP.
    """
    return _DkamSDK.ForceIP(camera_index, ip, mask, gateway)

def WhetherIsSameSegment(camera_index):
    """
    The Function is: Check whether the camera and the host computer are in the same network segment.
    """
    return _DkamSDK.WhetherIsSameSegment(camera_index)

def SetHeartBeatTimeout(camera_index, value):
    """
    The Function is: Set the camera heart beat timeout.
    """
    return _DkamSDK.SetHeartBeatTimeout(camera_index, value)

def GetHeartBeatTimeout(camera_index):
    """
    The Function is: Get the camera heart beat timeout.
    """
    return _DkamSDK.GetHeartBeatTimeout(camera_index)

def SetAutoExposure(camera_index, status, camera_cnt):
    """
    The Function is: Set the camera auto or manual exposure.
	status: 1 manual, 0 auto.
    """
    return _DkamSDK.SetAutoExposure(camera_index, status, camera_cnt)

def GetAutoExposure(camera_index, camera_cnt):
    """
    The Function is: Get the camera auto or manual exposure.
    """
    return _DkamSDK.GetAutoExposure(camera_index, camera_cnt)

def SetCamExposureGainLevel(camera_index, camera_cnt, level):
    """
    The Function is: Set the RGB camera gain level.
	level >= 1
    """
    return _DkamSDK.SetCamExposureGainLevel(camera_index, camera_cnt, level)

def GetCamExposureGainLevel(camera_index, camera_cnt):
    """
    The Function is: Get the RGB camera gain level.
    """
    return _DkamSDK.GetCamExposureGainLevel(camera_index, camera_cnt)

def SetMutipleExposure(camera_index, status):
    """
    The Function is: Set the camera multiple exposures.
	status>0
    """
    return _DkamSDK.SetMutipleExposure(camera_index, status)

def GetMutipleExposure(camera_index):
    """
    The Function is: Get the camera multiple exposures.
    """
    return _DkamSDK.GetMutipleExposure(camera_index)

def SetExposureTime(camera_index, utime, camera_cnt):
    """
    The Function is: Set the camera exposure time.
    """
    return _DkamSDK.SetExposureTime(camera_index, utime, camera_cnt)

def GetExposureTime(camera_index, camera_cnt):
    """
    The Function is: Get the camera exposure time.
    """
    return _DkamSDK.GetExposureTime(camera_index, camera_cnt)

def SetGain(camera_index, mode, value, camera_cnt):
    """
    The Function is: Set the camera gain.
	mode: analog gain and digital gain
    """
    return _DkamSDK.SetGain(camera_index, mode, value, camera_cnt)

def GetGain(camera_index, mode, camera_cnt):
    """
    The Function is: Get the camera gain.
    """
    return _DkamSDK.GetGain(camera_index, mode, camera_cnt)

def SetTriggerMode(camera_index, mode):
    """
    The Function is: Set the gray camera trigger mode.
	mode: 0 is continue,1 is trigger. 
    """
    return _DkamSDK.SetTriggerMode(camera_index, mode)

def SetTriggerSource(camera_index, sourcetype):
    """
    The Function is: Set the camera soft or hard trigger mode.
	sourcetype: 0 is soft trigger,1 is hard trigger 
    """
    return _DkamSDK.SetTriggerSource(camera_index, sourcetype)

def SetRGBTriggerMode(camera_index, mode):
    """
    The Function is: Set the RGB camera trigger mode.
	mode: 0 is continue,1 is trigger.
    """
    return _DkamSDK.SetRGBTriggerMode(camera_index, mode)

def SetTriggerCount(camera_index, count):
    """
    The Function is: Set the gray camera trigger count.
    """
    return _DkamSDK.SetTriggerCount(camera_index, count)

def SetRGBTriggerCount(camera_index, count):
    """
    The Function is: Set the RGB camera trigger count.
    """
    return _DkamSDK.SetRGBTriggerCount(camera_index, count)

def SetResendRequest(camera_index, channel_index, resend_flag):
    """
    The Function is: Set the camera resend request.
	resend_flag: 0 is close,1 is open.
    """
    return _DkamSDK.SetResendRequest(camera_index, channel_index, resend_flag)

def GetResendRequest(camera_index, channel_index):
    """
    The Function is: Get the camera resend request.
    """
    return _DkamSDK.GetResendRequest(camera_index, channel_index)

def SetRoi(camera_index, channel_index, size_x, size_y, offset_x, offset_y):
    """
    The Function is: Set the camera ROI range.
    """
    return _DkamSDK.SetRoi(camera_index, channel_index, size_x, size_y, offset_x, offset_y)

def SetTimestamp(camera_index, status):
    """
    The Function is: Set the camera timestamp.
    """
    return _DkamSDK.SetTimestamp(camera_index, status)

def GetTimestamp(camera_index):
    """
    The Function is: Get the camera timestamp.
    """
    return _DkamSDK.GetTimestamp(camera_index)

def GetTimestampStatus(camera_index):
    """
    The Function is: Get the camera timestamp status.
    """
    return _DkamSDK.GetTimestampStatus(camera_index)

def SetTimestampControlLatch(camera_index):
    """
    The Function is: Set the camera timestamp control latch.
    """
    return _DkamSDK.SetTimestampControlLatch(camera_index)

def GetTimestampValue(camera_index):
    """
    The Function is: Get the camera timestamp value.
    """
    return _DkamSDK.GetTimestampValue(camera_index)

def GetTimestampTickFrequency(camera_index):
    """
    The Function is: Get the camera timestamp tick frequency.
    """
    return _DkamSDK.GetTimestampTickFrequency(camera_index)

def SetStrobeLEDswitch(camera_index, status):
    """
    The Function is: Set the camera LED strobe switch.
    """
    return _DkamSDK.SetStrobeLEDswitch(camera_index, status)

def GetStrobeLEDswitch(camera_index):
    """
    The Function is: Get the camera LED strobe switch.
    """
    return _DkamSDK.GetStrobeLEDswitch(camera_index)

def SetLaserbrightness(camera_index, value):
    """
    The Function is: Set the camera laser brightness.
	1 <= value <= 100 
    """
    return _DkamSDK.SetLaserbrightness(camera_index, value)

def GetLaserbrightness(camera_index):
    """
    The Function is: Get the camera laser brightness.
    """
    return _DkamSDK.GetLaserbrightness(camera_index)

def SetStrobeLEDbrightress(camera_index, value):
    """
    The Function is: Set the camera LED strobe brightress.
	1 <= value <= 100
    """
    return _DkamSDK.SetStrobeLEDbrightress(camera_index, value)

def GetStrobeLEDbrightress(camera_index):
    """
    The Function is: Get the camera LED strobe brightress.
    """
    return _DkamSDK.GetStrobeLEDbrightress(camera_index)

def FirmwareUpgrade(camera_index, localfilename):
    """
    The Function is: The camera firmware upgrade.
    """
    return _DkamSDK.FirmwareUpgrade(camera_index, localfilename)

def SaveXmlToLocal(camera_index, pathname):
    """
    The Function is: Save the camera xml to local.
    """
    return _DkamSDK.SaveXmlToLocal(camera_index, pathname)

def SavePointCloudToPcd(camera_index, raw_data, path_name):
    """
    The Function is: Save the camera point cloud to pcd format.
    """
    return _DkamSDK.SavePointCloudToPcd(camera_index, raw_data, path_name)

def SavePointCloudToTxt(camera_index, raw_data, path_name):
    """
    The Function is: Save the camera point cloud to txt format.
    """
    return _DkamSDK.SavePointCloudToTxt(camera_index, raw_data, path_name)

def SavePointCloudToPly(camera_index, raw_data, path_name):
    """
    The Function is: Save the camera point cloud to ply format.
    """
    return _DkamSDK.SavePointCloudToPly(camera_index, raw_data, path_name)

def FilterPointCloud(camera_index, raw_data, level):
    """
    The Function is: Filter the camera point cloud.
    """
    return _DkamSDK.FilterPointCloud(camera_index, raw_data, level)

def SpatialFilterPointcloud(camera_index, raw_data, Area_PointCloudCount):
    return _DkamSDK.SpatialFilterPointcloud(camera_index, raw_data, Area_PointCloudCount)

def SaveToBMP(camera_index, data, path_name):
    """
    The Function is: Save the camera gray/RGB image to bmp format.
    """
    return _DkamSDK.SaveToBMP(camera_index, data, path_name)

def SaveDepthToPng(camera_index, raw_data, path_name):
    """
    The Function is: Save the camera depth to png format.
    """
    return _DkamSDK.SaveDepthToPng(camera_index, raw_data, path_name)

def FusionImageTo3D(camera_index, image_data, raw_data, image_cloud):
    """
    The Function is: Fusion the camera point cloud/gray or point cloud/RGB.
    """
    return _DkamSDK.FusionImageTo3D(camera_index, image_data, raw_data, image_cloud)

def Fusion3DToRGB(camera_index, rgb_data, raw_data, xyz):
    """
    The Function is: Rearrange the point cloud according to RGB.
    """
    return _DkamSDK.Fusion3DToRGB(camera_index, rgb_data, raw_data, xyz)

def PixelSwell(camera_index, roi_output, target_data):
    """
    The Function is: Expand the highlighted part of the image.
    """
    return _DkamSDK.PixelSwell(camera_index, roi_output, target_data)

def PixelCorrosion(camera_index, roi_output, target_data):
    """
    The Function is: Minimize the highlighted part of the image.
    """
    return _DkamSDK.PixelCorrosion(camera_index, roi_output, target_data)

def ROIMappingCoordinate(camera_index, roi_output, target_data, point_output):
    """
    The Function is: According to the set RGB or RGB area of interest, corresponding to a specific region in the infrared or RGB image.
    """
    return _DkamSDK.ROIMappingCoordinate(camera_index, roi_output, target_data, point_output)

def ROIPixelMapping(camera_index, point_data, source_data, target_data, roi_input, ROI_output):
    """
    The Function is: Retrieve ROI regions from point cloud, infrared, and RGB.
    """
    return _DkamSDK.ROIPixelMapping(camera_index, point_data, source_data, target_data, roi_input, ROI_output)

def SavePointCloudWithImageToTxt(camera_index, raw_data, rgb_cloud, path_name):
    """
    The Function is: Save the camera point cloud/gray or point cloud/RGB fusion image to txt.
    """
    return _DkamSDK.SavePointCloudWithImageToTxt(camera_index, raw_data, rgb_cloud, path_name)

def CameraVerions(camera_index):
    """
    The Function is: Get th camera version.
    """
    return _DkamSDK.CameraVerions(camera_index)

def SDKVersion(camera_index):
    """
    The Function is: Get th camera SDK version.
    """
    return _DkamSDK.SDKVersion(camera_index)

def GetCameraXMLNodeNamesCSharp(camera_index, node_names):
    """
    The Function is: Get the camera xml node names in csharp version.
    """
    return _DkamSDK.GetCameraXMLNodeNamesCSharp(camera_index, node_names)

def GetRecieveTimeStatisticsCSharp(camera_index, channel_index, o_statistics_data, bins_b):
    """
    The Function is: Get the camera recieve time statistics in csharp version.
    """
    return _DkamSDK.GetRecieveTimeStatisticsCSharp(camera_index, channel_index, o_statistics_data, bins_b)

def CaptureCSharp(camera_index, channel_index, raw_data_info, xyz, pixel_size):
    """
    The Function is: The camera capture data in csharp version.
    """
    return _DkamSDK.CaptureCSharp(camera_index, channel_index, raw_data_info, xyz, pixel_size)

def TryCaptureCSharp(camera_index, channel_index, raw_data_info, xyz, pixel_size):
    """
    The Function is: The camera try capture data in csharp version.
    """
    return _DkamSDK.TryCaptureCSharp(camera_index, channel_index, raw_data_info, xyz, pixel_size)

def TimeoutCaptureCSharp(camera_index, channel_index, raw_data_info, xyz, pixel_size, timeout):
    """
    The Function is: The camera timeout capture data in csharp version.
    """
    return _DkamSDK.TimeoutCaptureCSharp(camera_index, channel_index, raw_data_info, xyz, pixel_size, timeout)

def Convert3DPointFromCharToFloatCSharp(camera_index, raw_data_info, xyz, pixel_size):
    """
    The Function is: Convert point cloud data from char to float in csharp version.
    """
    return _DkamSDK.Convert3DPointFromCharToFloatCSharp(camera_index, raw_data_info, xyz, pixel_size)

def RawdataToRgb888CSharp(camera_index, raw_data_info, xyz, pixel_size):
    """
    The Function is: Convert raw data to RGB888 in csharp version.
    """
    return _DkamSDK.RawdataToRgb888CSharp(camera_index, raw_data_info, xyz, pixel_size)

def GetCloudPlaneXCSharp(camera_index, raw_data_info, xyz, pixel_size, imagedata):
    """
    The Function is: Get the camera point cloud x plane data in csharp version.
    """
    return _DkamSDK.GetCloudPlaneXCSharp(camera_index, raw_data_info, xyz, pixel_size, imagedata)

def GetCloudPlaneYCSharp(camera_index, raw_data_info, xyz, pixel_size, imagedata):
    """
    The Function is: Get the camera point cloud y plane data in csharp version.
    """
    return _DkamSDK.GetCloudPlaneYCSharp(camera_index, raw_data_info, xyz, pixel_size, imagedata)

def GetCloudPlaneZCSharp(camera_index, raw_data_info, xyz, pixel_size, imagedata):
    """
    The Function is: Get the camera point cloud z plane data in csharp version.
    """
    return _DkamSDK.GetCloudPlaneZCSharp(camera_index, raw_data_info, xyz, pixel_size, imagedata)

def SaveCloudPlaneCSharp(camera_index, raw_data_info, xyz, pixel_size, imagedata, path_name):
    """
    The Function is: Save the camera point cloud x/y/z plane data in csharp version.
    """
    return _DkamSDK.SaveCloudPlaneCSharp(camera_index, raw_data_info, xyz, pixel_size, imagedata, path_name)

def SavePointCloudToPcdCSharp(camera_index, raw_data_info, xyz, pixel_size, path_name):
    """
    The Function is: Save the camera point cloud to pcd format in csharp version.
    """
    return _DkamSDK.SavePointCloudToPcdCSharp(camera_index, raw_data_info, xyz, pixel_size, path_name)

def SavePointCloudToTxtCSharp(camera_index, raw_data_info, xyz, pixel_size, path_name):
    """
    The Function is: Save the camera point cloud to txt format in csharp version.
    """
    return _DkamSDK.SavePointCloudToTxtCSharp(camera_index, raw_data_info, xyz, pixel_size, path_name)

def SavePointCloudToPlyCSharp(camera_index, raw_data_info, xyz, pixel_size, path_name):
    """
    The Function is: Save the camera point cloud to ply format in csharp version.
    """
    return _DkamSDK.SavePointCloudToPlyCSharp(camera_index, raw_data_info, xyz, pixel_size, path_name)

def FilterPointCloudCSharp(camera_index, raw_data_info, xyz, pixel_size, level):
    """
    The Function is: Filter the camera point cloud in csharp version.
    """
    return _DkamSDK.FilterPointCloudCSharp(camera_index, raw_data_info, xyz, pixel_size, level)

def SpatialFilterPointcloudCSharp(camera_index, raw_data_info, xyz, pixel_size, Area_PointCloudCount):
    return _DkamSDK.SpatialFilterPointcloudCSharp(camera_index, raw_data_info, xyz, pixel_size, Area_PointCloudCount)

def SaveToBMPCSharp(camera_index, raw_data_info, xyz, pixel_size, path_name):
    """
    The Function is: Save the camera gray/RGB image to bmp format in csharp version.
    """
    return _DkamSDK.SaveToBMPCSharp(camera_index, raw_data_info, xyz, pixel_size, path_name)

def SaveDepthToPngCSharp(camera_index, raw_data_info, xyz, pixel_size, path_name):
    """
    The Function is: Save the camera depth to png format in csharp version.
    """
    return _DkamSDK.SaveDepthToPngCSharp(camera_index, raw_data_info, xyz, pixel_size, path_name)

def FusionImageTo3DCSharp(camera_index, image_data_info, image_pixel, image_pixel_size, point_data_info, point_pixel, point_pixel_size):
    """
    The Function is: Fusion the camera point cloud/gray or point cloud/RGB in csharp version.
    """
    return _DkamSDK.FusionImageTo3DCSharp(camera_index, image_data_info, image_pixel, image_pixel_size, point_data_info, point_pixel, point_pixel_size)

def Fusion3DToRGBCSharp(camera_index, image_data_info, image_pixel, image_pixel_size, point_data_info, point_pixel, point_pixel_size, xyz_data_info, xyz, xyz_size):
    """
    The Function is: Rearrange the point cloud according to RGB in csharp version.
    """
    return _DkamSDK.Fusion3DToRGBCSharp(camera_index, image_data_info, image_pixel, image_pixel_size, point_data_info, point_pixel, point_pixel_size, xyz_data_info, xyz, xyz_size)

def PixelSwellCSharp(camera_index, roi_output, target_data, target_pixel_size):
    """
    The Function is: Expand the highlighted part of the image in csharp version.
    """
    return _DkamSDK.PixelSwellCSharp(camera_index, roi_output, target_data, target_pixel_size)

def PixelCorrosionCSharp(camera_index, roi_output, target_data, target_pixel_size):
    """
    The Function is: Minimize the highlighted part of the image in csharp version.
    """
    return _DkamSDK.PixelCorrosionCSharp(camera_index, roi_output, target_data, target_pixel_size)

def ROIMappingCoordinateCSharp(camera_index, roi_output_size, target_data, target_pixel_size, point_output):
    return _DkamSDK.ROIMappingCoordinateCSharp(camera_index, roi_output_size, target_data, target_pixel_size, point_output)

def ROIPixelMappingCSharp(camera_index, point_data, point_pixel, point_pixel_size, source_data, source_data_pixel, source_pixel_size, target_data, target_data_pixel, target_pixel_size, roi_input, ROI_output_size):
    return _DkamSDK.ROIPixelMappingCSharp(camera_index, point_data, point_pixel, point_pixel_size, source_data, source_data_pixel, source_pixel_size, target_data, target_data_pixel, target_pixel_size, roi_input, ROI_output_size)

def SavePointCloudWithImageToTxtCSharp(camera_index, point_data_info, point_pixel, point_pixel_size, path_name):
    """
    The Function is: Save the camera point cloud/gray or point cloud/RGB fusion image to txt in csharp version.
    """
    return _DkamSDK.SavePointCloudWithImageToTxtCSharp(camera_index, point_data_info, point_pixel, point_pixel_size, path_name)

def new_intArray(nelements):
    return _DkamSDK.new_intArray(nelements)

def delete_intArray(ary):
    return _DkamSDK.delete_intArray(ary)

def intArray_getitem(ary, index):
    return _DkamSDK.intArray_getitem(ary, index)

def intArray_setitem(ary, index, value):
    return _DkamSDK.intArray_setitem(ary, index, value)

def new_floatArray(nelements):
    return _DkamSDK.new_floatArray(nelements)

def delete_floatArray(ary):
    return _DkamSDK.delete_floatArray(ary)

def floatArray_getitem(ary, index):
    return _DkamSDK.floatArray_getitem(ary, index)

def floatArray_setitem(ary, index, value):
    return _DkamSDK.floatArray_setitem(ary, index, value)

def new_unsignedintArray(nelements):
    return _DkamSDK.new_unsignedintArray(nelements)

def delete_unsignedintArray(ary):
    return _DkamSDK.delete_unsignedintArray(ary)

def unsignedintArray_getitem(ary, index):
    return _DkamSDK.unsignedintArray_getitem(ary, index)

def unsignedintArray_setitem(ary, index, value):
    return _DkamSDK.unsignedintArray_setitem(ary, index, value)

def new_longlongArray(nelements):
    return _DkamSDK.new_longlongArray(nelements)

def delete_longlongArray(ary):
    return _DkamSDK.delete_longlongArray(ary)

def longlongArray_getitem(ary, index):
    return _DkamSDK.longlongArray_getitem(ary, index)

def longlongArray_setitem(ary, index, value):
    return _DkamSDK.longlongArray_setitem(ary, index, value)


import os.path
def findDir():
	print(os.path.dirname(__file__))
