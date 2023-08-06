

from DkamSDK import *
import numpy as np
camera_num = DiscoverCamera()
print"camera_num=", camera_num
if camera_num > 0:
    camera_sort = CameraSort(0)
    print"camera_sort=", camera_sort
for i in range(camera_num):
    print"IP:", CameraIP(i)
    if CameraIP(i) == b'10.0.0.97':
        camera_ret = i
CreateCamera()
connect = CameraConnect(camera_ret)
print"connect=", connect
if connect == 0:   


    # get width and height
    width_register_addr = GetRegisterAddr(camera_ret, b"Width")
    height_register_addr = GetRegisterAddr(camera_ret, b"Height")
    width_gray = new_intArray(0)
    height_gray = new_intArray(0)
    ReadRegister(camera_ret, width_register_addr, width_gray)
    ReadRegister(camera_ret, height_register_addr, height_gray)
    width = intArray_getitem(width_gray, 0)
    height = intArray_getitem(height_gray, 0)
    print"Width=%d, height=%d" % (width, height)
  

    point = PhotoInfoCSharp()
    point_num = width * height * 6
    pointpixel = np.zeros(point_num, dtype=np.int8).tobytes()

    
    # SetTriggerMode
    tirggerMode = SetTriggerMode(camera_ret, 1)
    print"tirggerMode=", tirggerMode


    # StreamOn
    stream_point = StreamOn(camera_ret, 1)
    print"stream_point=", stream_point
   
    acquistion = AcquisitionStart(camera_ret)
    print"acquistion=", acquistion
   
    print"WhetherIsSameSegment:",WhetherIsSameSegment(camera_ret)  
    print"cameraVersion:",CameraVerions(camera_ret)
    print"SDK version:",SDKVersion(camera_ret)
    # SetTriggerCount
    triggerCount = SetTriggerCount(camera_ret, 1)
    print"triggerCount:", triggerCount

    pcd_name = b"1.pcd"
   

    # save point cloud
    capturePoint = TimeoutCaptureCSharp(camera_ret, 1, point, pointpixel, point_num,3000000)
    print"capture_Pointimage: ", capturePoint
    savepcd = SavePointCloudToPcdCSharp(camera_ret, point, pointpixel, point_num, pcd_name)
    print"save pcd=", savepcd 
       

    streamoff_point = StreamOff(camera_ret, 1)
    print"streamoff_point=", streamoff_point  

    disconnect = CameraDisconnect(camera_ret)
    print"disconnect=", disconnect

    DestroyCamera()



