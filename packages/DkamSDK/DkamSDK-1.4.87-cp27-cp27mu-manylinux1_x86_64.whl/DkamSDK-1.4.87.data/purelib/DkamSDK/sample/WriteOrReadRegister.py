from DkamSDK import *
import numpy as np
camera_num = DiscoverCamera()
print"camera_num=", camera_num
if camera_num > 0:
    camera_sort = CameraSort(0)
    print"camera_sort=", camera_sort
for i in range(camera_num):
    print"IP:", CameraIP(i)
    if CameraIP(i) == b'10.0.0.74':
        camera_ret = i
CreateCamera()
connect = CameraConnect(camera_ret)
print"connect=", connect
if connect == 0:
    # GetRegisterAddr
    tirggerMode_addr = GetRegisterAddr(camera_ret, b"TriggerMode")
    tirgger_data = new_intArray(0)
    ReadRegister(camera_ret, tirggerMode_addr, tirgger_data)

    # get stringRegister
    key_str = np.zeros(255, dtype=np.int8).tobytes()
    ReadStringRegister(camera_ret, b"DeviceManufacturerInfo", key_str)
    print"ReadStringRegister:", key_str.decode("utf-8", 'strict')
    # WriteRegister
    print"WriteRegister:", WriteRegister(camera_ret, 0xB010, 1)
	
	disconnect = CameraDisconnect(camera_ret)
    print"disconnect=", disconnect

    DestroyCamera()
