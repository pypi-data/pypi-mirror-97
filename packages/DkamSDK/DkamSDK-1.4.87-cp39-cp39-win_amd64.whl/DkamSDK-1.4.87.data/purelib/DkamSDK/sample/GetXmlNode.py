
from DkamSDK import *
camera_num = DiscoverCamera()
print("camera_num=", camera_num)
if camera_num > 0:
    camera_sort = CameraSort(0)
    print("camera_sort=", camera_sort)
for i in range(camera_num):
    print("IP:", CameraIP(i))
    if CameraIP(i) == b'10.0.0.97':
        camera_ret = i
CreateCamera()
connect = CameraConnect(camera_ret)
print("connect=", connect)
if connect == 0:  

   # get XMLNode
    node_name = StringVector(0)
    GetCameraXMLNodeNamesCSharp(camera_ret,node_name)
    for a in range(node_name.size()):
        print("node name:",node_name.__getitem__(a))
    print(GetNodeMaxValue(camera_ret,b"analoggain"))
    print(GetNodeMinValue(camera_ret,b"digitalgain_rgb"))
    print(GetNodeIncValue(camera_ret,b"OffsetY"))

    disconnect = CameraDisconnect(camera_ret)
    print("disconnect=", disconnect)

    DestroyCamera()
