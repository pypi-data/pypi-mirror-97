

from DkamSDK import *
import numpy as np
SetLogLevel(1,0,0,1)
camera_num = DiscoverCamera()
print("camera_num=", camera_num)
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
   
    gray = PhotoInfoCSharp()
    gray_num = width * height
    graypixel = np.zeros(gray_num, dtype=np.int8).tobytes()
   
    tirggerMode = SetTriggerMode(camera_ret, 1)
    print"tirggerMode=", tirggerMode

    # stream on 
    stream_gray = StreamOn(camera_ret, 0)
    print"stream_gray=", stream_gray
    
    acquistion = AcquisitionStart(camera_ret)
    print"acquistion=", acquistion
    
    print"cameraVersion:",CameraVerions(camera_ret)
   
    # set ttigger count
    triggerCount = SetTriggerCount(camera_ret, 1)
    print"triggerCount:", triggerCount
    
    gray_name = b"1.bmp"

    # save gray
    capturegray = CaptureCSharp(camera_ret, 0, gray, graypixel, gray_num)
    print"capture_Gray: ", capturegray
    savebmp = SaveToBMPCSharp(camera_ret, gray, graypixel, gray_num, gray_name)
    print"save gray=", savebmp  
    
    streamoff_gray = StreamOff(camera_ret, 0)
    print"streamoff_gray=", streamoff_gray
 
    disconnect = CameraDisconnect(camera_ret)
    print"disconnect=", disconnect

    DestroyCamera()



