

from DkamSDK import *
import numpy as np
SetLogLevel(1,0,0,1)
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

    width_register_addr_rgb = GetRegisterAddr(camera_ret, b"Width") + 0x100
    height_register_addr_rgb = GetRegisterAddr(camera_ret, b"Height") + 0x100
    width_rgb = new_intArray(0)
    height_rgb = new_intArray(0)
    ReadRegister(camera_ret, width_register_addr_rgb, width_rgb)
    ReadRegister(camera_ret, height_register_addr_rgb, height_rgb)
    width_RGB = intArray_getitem(width_rgb, 0)
    height_RGB = intArray_getitem(height_rgb, 0)
    print"Width_rgb=%d, height_rgb=%d" % (width_RGB, height_RGB)

    point = PhotoInfoCSharp()
    gray = PhotoInfoCSharp()
    rgb = PhotoInfoCSharp()

    point_num = width * height * 6
    pointpixel = np.zeros(point_num, dtype=np.int8).tobytes()

    gray_num = width * height
    graypixel = np.zeros(gray_num, dtype=np.int8).tobytes()

    rgb_num = width_RGB * height_RGB * 3
    rgbpixel = np.zeros(rgb_num, dtype=np.int8).tobytes()  

    # SetTriggerMode
    tirggerMode1 = SetTriggerMode(camera_ret, 1)
    print"tirggerMode=", tirggerMode1
          
    tirggerMode = SetRGBTriggerMode(camera_ret, 1)
    print"tirggerModeRGB=", tirggerMode

    # StreamOn
    stream_point = StreamOn(camera_ret, 1)
    print"stream_point=", stream_point

    stream_gray = StreamOn(camera_ret, 0)
    print"stream_gray=", stream_gray

    stream_RGB = StreamOn(camera_ret, 2)
    print"stream_RGB=", stream_RGB

    acquistion = AcquisitionStart(camera_ret)
    print"acquistion=", acquistion

   
    # SetTriggerCount
    triggerCount = SetTriggerCount(camera_ret, 1)
    print"triggerCount:", triggerCount

    triggerCountRGB = SetRGBTriggerCount(camera_ret, 1)
    print"triggerCountRGB:", triggerCountRGB


    pcd_name = b"1.pcd"
    gray_name = b"1.bmp"
    rgb_name = b"1_rgb.bmp"
    
    # save point cloud
    capturePoint = CaptureCSharp(camera_ret, 1, point, pointpixel, point_num)
    print"capture_Pointimage: ", capturePoint
    savepcd = SavePointCloudToPcdCSharp(camera_ret, point, pointpixel, point_num, pcd_name)
    print"save pcd=", savepcd

    # save gray
    capturegray = CaptureCSharp(camera_ret, 0, gray, graypixel, gray_num)
    print"capture_Gray: ", capturegray
    savebmp = SaveToBMPCSharp(camera_ret, gray, graypixel, gray_num, gray_name)
    print"save gray=", savebmp

    # save RGB
    captureRGB = CaptureCSharp(camera_ret, 2, rgb, rgbpixel, rgb_num)
    print"capture RGB=", captureRGB
    savergb = SaveToBMPCSharp(camera_ret, rgb, rgbpixel, rgb_num, rgb_name)
    print"save rgb=", savergb

    # set ROI
    roi_input=RoiPoint()
    roi_input.size_x=443
    roi_input.size_y=566
    roi_input.offset_x=442
    roi_input.offset_y=260
    ROI_output_num = rgb.pixel_width * rgb.pixel_height
    ROI_output = np.zeros(ROI_output_num,dtype=np.int32)

    ROIPixelMappingCSharp(camera_ret,point,pointpixel,point_num,gray,graypixel,gray_num,rgb,rgbpixel,rgb_num,roi_input,ROI_output)
  
    roi_output=RoiPoint()
    ROIMappingCoordinateCSharp(camera_ret,ROI_output,rgb,rgb_num,roi_output)
    print"size_x:",roi_output.size_x
    print"size_y:",roi_output.size_y
    print"offset_x:",roi_output.offset_x
    print"offset_y:",roi_output.offset_y



    streamoff_gray = StreamOff(camera_ret, 0)
    print"streamoff_gray=", streamoff_gray

    streamoff_point = StreamOff(camera_ret, 1)
    print"streamoff_point=", streamoff_point

    streamoff_rgb = StreamOff(camera_ret, 2)
    print"streamoff_rgb=", streamoff_rgb

    disconnect = CameraDisconnect(camera_ret)
    print"disconnect=", disconnect

    DestroyCamera()



