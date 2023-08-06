
from DkamSDK import *
import numpy as np
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

    # get width and height
    width_register_addr_rgb = GetRegisterAddr(camera_ret, b"Width") + 0x100
    height_register_addr_rgb = GetRegisterAddr(camera_ret, b"Height") + 0x100
    width_rgb = new_intArray(0)
    height_rgb = new_intArray(0)
    ReadRegister(camera_ret, width_register_addr_rgb, width_rgb)
    ReadRegister(camera_ret, height_register_addr_rgb, height_rgb)
    width_RGB = intArray_getitem(width_rgb, 0)
    height_RGB = intArray_getitem(height_rgb, 0)
    print("Width_rgb=%d, height_rgb=%d" % (width_RGB, height_RGB))

   
    rgb = PhotoInfoCSharp()   
    rgb_num = width_RGB * height_RGB * 3
    rgbpixel = bytes(rgb_num)
  
    # SetRGBTriggerMode   
    tirggerMode = SetRGBTriggerMode(camera_ret, 1)
    print("tirggerModeRGB=", tirggerMode)

    # StreamOn 
    stream_RGB = StreamOn(camera_ret, 2)
    print("stream_RGB=", stream_RGB)

    acquistion = AcquisitionStart(camera_ret)
    print("acquistion=", acquistion)
   
    print("cameraVersion:",CameraVerions(camera_ret))

    # SetRGBTriggerCount
    triggerCountRGB = SetRGBTriggerCount(camera_ret, 1)
    print("triggerCountRGB:", triggerCountRGB)
  
    rgb_name = b"1_rgb.bmp"   
	FlushBuffer(camera_ret,2)
    # save RGB
    captureRGB = CaptureCSharp(camera_ret, 2, rgb, rgbpixel, rgb_num)
    print("capture RGB=", captureRGB)
    savergb = SaveToBMPCSharp(camera_ret, rgb, rgbpixel, rgb_num, rgb_name)
    print("save rgb=", savergb)
   
   
    streamoff_rgb = StreamOff(camera_ret, 2)
    print("streamoff_rgb=", streamoff_rgb)

    disconnect = CameraDisconnect(camera_ret)
    print("disconnect=", disconnect)

    DestroyCamera()



