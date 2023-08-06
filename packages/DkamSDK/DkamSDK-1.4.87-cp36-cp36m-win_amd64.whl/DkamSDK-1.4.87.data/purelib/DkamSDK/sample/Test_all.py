

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
    width_register_addr = GetRegisterAddr(camera_ret, b"Width")
    height_register_addr = GetRegisterAddr(camera_ret, b"Height")
    width_gray = new_intArray(0)
    height_gray = new_intArray(0)
    ReadRegister(camera_ret, width_register_addr, width_gray)
    ReadRegister(camera_ret, height_register_addr, height_gray)
    width = intArray_getitem(width_gray, 0)
    height = intArray_getitem(height_gray, 0)
    print("Width=%d, height=%d" % (width, height))

    width_register_addr_rgb = GetRegisterAddr(camera_ret, b"Width") + 0x100
    height_register_addr_rgb = GetRegisterAddr(camera_ret, b"Height") + 0x100
    width_rgb = new_intArray(0)
    height_rgb = new_intArray(0)
    ReadRegister(camera_ret, width_register_addr_rgb, width_rgb)
    ReadRegister(camera_ret, height_register_addr_rgb, height_rgb)
    width_RGB = intArray_getitem(width_rgb, 0)
    height_RGB = intArray_getitem(height_rgb, 0)
    print("Width_rgb=%d, height_rgb=%d" % (width_RGB, height_RGB))

    point = PhotoInfoCSharp()
    gray = PhotoInfoCSharp()
    rgb = PhotoInfoCSharp()

    point_num = width * height * 6
    pointpixel = bytes(point_num)

    gray_num = width * height
    graypixel = bytes(gray_num)

    rgb_num = width_RGB * height_RGB * 3
    rgbpixel = bytes(rgb_num)

    
    rgb_cloud = np.zeros((width * height * 6), dtype=np.float32)
    gray_cloud = np.zeros((width * height * 6), dtype=np.float32)
  
    # set TriggerMode
    tirggerMode1 = SetTriggerMode(camera_ret, 1)
    print("tirggerMode=", tirggerMode1)

    tirggerMode = SetRGBTriggerMode(camera_ret, 1)
    print("tirggerModeRGB=", tirggerMode)

    # StreamOn
    stream_point = StreamOn(camera_ret, 1)
    print("stream_point=", stream_point)

    stream_gray = StreamOn(camera_ret, 0)
    print("stream_gray=", stream_gray)

    stream_RGB = StreamOn(camera_ret, 2)
    print("stream_RGB=", stream_RGB)

    acquistion = AcquisitionStart(camera_ret)
    print("acquistion=", acquistion)

    # SetAutoExposure 0->auto 1->Manual
    setauto = SetAutoExposure(camera_ret, 0, 0)
    print("Set Auto Exposure=", setauto)
    getauto = GetAutoExposure(camera_ret, 0)
    print("Get Auto Exposure=", getauto)

    setautorgb = SetAutoExposure(camera_ret, 0, 1)
    print("Set Auto Exposure RGB=", setautorgb)
    getautorgb = GetAutoExposure(camera_ret, 1)
    print("Get Auto Exposure RGB=", getautorgb)   

    # SetMutipleExposure
    setmutiple=SetMutipleExposure(camera_ret,5)
    print("SetMutipleExposure:", setmutiple)
    getmutiple = GetMutipleExposure(camera_ret)
    print("GetMutipleExposure:", getmutiple)

    # SetExposureTime
    setExtime = SetExposureTime(camera_ret, 7000,0)
    print("SetExposureTime:", setExtime)
    getExtime = GetExposureTime(camera_ret,0)
    print("GetExposureTime:", getExtime)

    print("WhetherIsSameSegment:",WhetherIsSameSegment(camera_ret))
    print("save XML:",SaveXmlToLocal(camera_ret, b"D:\\"))
    print("cameraVersion:",CameraVerions(camera_ret))
    print("SDK version:",SDKVersion(camera_ret))
    # SetTriggerCount
    triggerCount = SetTriggerCount(camera_ret, 1)
    print("triggerCount:", triggerCount)

    triggerCountRGB = SetRGBTriggerCount(camera_ret, 1)
    print("triggerCountRGB:", triggerCountRGB)


    pcd_name = b"1.pcd"
    gray_name = b"1.bmp"
    rgb_name = b"1_rgb.bmp"
    gray_cloud_name = b"1_gray.txt"
    rgb_cloud_name = b"1_rgb.txt"
    filter_name = b"1_filter.pcd"
    depth_name = b"1.png"

    # save point cloud
    capturePoint = CaptureCSharp(camera_ret, 1, point, pointpixel, point_num)
    print("capture_Pointimage: ", capturePoint)
    savepcd = SavePointCloudToPcdCSharp(camera_ret, point, pointpixel, point_num, pcd_name)
    print("save pcd=", savepcd)

    # save gray
    capturegray = CaptureCSharp(camera_ret, 0, gray, graypixel, gray_num)
    print("capture_Gray: ", capturegray)
    savebmp = SaveToBMPCSharp(camera_ret, gray, graypixel, gray_num, gray_name)
    print("save gray=", savebmp)

    # save  RGB
    captureRGB = CaptureCSharp(camera_ret, 2, rgb, rgbpixel, rgb_num)
    print("capture RGB=", captureRGB)
    savergb = SaveToBMPCSharp(camera_ret, rgb, rgbpixel, rgb_num, rgb_name)
    print("save rgb=", savergb)
  

    # FilterPointCloud
    FilterPointCloudCSharp(camera_ret,point,pointpixel,point_num,1)
    savefilter = SavePointCloudToPcdCSharp(camera_ret, point, pointpixel, point_num, filter_name)
    print("save Filter Point=",savefilter)
    # save depth
    savedepth=SaveDepthToPngCSharp(camera_ret,point,pointpixel,point_num,depth_name)
    print("save Depth=",savedepth)

    # point cloud fusion gray
    FusionImageTo3DCSharp(camera_ret, gray, graypixel, gray_num, point, pointpixel,  gray_cloud)
    savegray_cloud = SavePointCloudWithImageToTxtCSharp(camera_ret, point, pointpixel, gray_cloud, gray_cloud_name)
    print("save Gray_cloud=", savegray_cloud)

    # point cloud fusion rgb
    FusionImageTo3DCSharp(camera_ret, rgb, rgbpixel, rgb_num, point, pointpixel, rgb_cloud)
    savergb_cloud = SavePointCloudWithImageToTxtCSharp(camera_ret, point, pointpixel, rgb_cloud, rgb_cloud_name)
    print("save RGB_cloud=", savergb_cloud)


    streamoff_gray = StreamOff(camera_ret, 0)
    print("streamoff_gray=", streamoff_gray)

    streamoff_point = StreamOff(camera_ret, 1)
    print("streamoff_point=", streamoff_point)

    streamoff_rgb = StreamOff(camera_ret, 2)
    print("streamoff_rgb=", streamoff_rgb)

    disconnect = CameraDisconnect(camera_ret)
    print("disconnect=", disconnect)

    DestroyCamera()



