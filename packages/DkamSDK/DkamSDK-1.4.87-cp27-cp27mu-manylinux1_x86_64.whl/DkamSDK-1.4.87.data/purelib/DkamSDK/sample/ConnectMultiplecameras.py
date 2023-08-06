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
    if CameraIP(i) == b'10.0.0.140':
        k = i
    if CameraIP(i) == b'10.0.0.119':
        n = i
CreateCamera()
connect = CameraConnect(k)
connect1 = CameraConnect(n)
print"camera 1 connect=", connect
print"camera 2 connect=", connect1
if connect == 0 & connect1 == 0:
    print"----------camera 1 CCP status---------"   

    # get ccp
    data_ccp = new_intArray(0)
    GetCameraCCPStatus(k, data_ccp)
    data = intArray_getitem(data_ccp, 0)
    print"camera 1 GetCameraCCPStatus:", data

    print"----------camera 2 CCP status---------" 

    data_ccp1 = new_intArray(0)
    GetCameraCCPStatus(n, data_ccp1)
    data1 = intArray_getitem(data_ccp1, 0)
    print"camera 2 GetCameraCCPStatus:", data1

    print"----------camera 1 width and height---------"
    # camera1 get width and height
    width_register_addr = GetRegisterAddr(k, b"Width")
    height_register_addr = GetRegisterAddr(k, b"Height")
    width_gray = new_intArray(0)
    height_gray = new_intArray(0)
    ReadRegister(k, width_register_addr, width_gray)
    ReadRegister(k, height_register_addr, height_gray)
    width = intArray_getitem(width_gray, 0)
    height = intArray_getitem(height_gray, 0)
    print" camera 1 Width=%d, height=%d" % (width, height)

    width_register_addr_rgb = GetRegisterAddr(k, b"Width") + 0x100
    height_register_addr_rgb = GetRegisterAddr(k, b"Height") + 0x100
    width_rgb = new_intArray(0)
    height_rgb = new_intArray(0)
    ReadRegister(k, width_register_addr_rgb, width_rgb)
    ReadRegister(k, height_register_addr_rgb, height_rgb)
    width_RGB = intArray_getitem(width_rgb, 0)
    height_RGB = intArray_getitem(height_rgb, 0)
    print"camera 1 Width_rgb=%d, height_rgb=%d" % (width_RGB, height_RGB)

    point_data = PhotoInfoCSharp()
    gray_data = PhotoInfoCSharp()
    rgb_data = PhotoInfoCSharp()

    point_num = width * height * 6
    pointpixel = np.zeros(point_num, dtype=np.int8).tobytes()

    gray_num = width * height
    graypixel = np.zeros(gray_num, dtype=np.int8).tobytes()

    rgb_num = width_RGB * height_RGB * 3
    rgbpixel = np.zeros(rgb_num, dtype=np.int8).tobytes()

    rgb_cloud = np.zeros((width * height * 6), dtype=np.float32)
    gray_cloud = np.zeros((width * height * 6), dtype=np.float32)

    print"----------camera 2 width and height---------"
    # camera1 get width and height
    width_register_addr1 = GetRegisterAddr(n, b"Width")
    height_register_addr1 = GetRegisterAddr(n, b"Height")
    width_gray1 = new_intArray(0)
    height_gray1 = new_intArray(0)
    ReadRegister(n, width_register_addr1, width_gray1)
    ReadRegister(n, height_register_addr1, height_gray1)
    width1 = intArray_getitem(width_gray1, 0)
    height1 = intArray_getitem(height_gray1, 0)
    print" camera 2 Width=%d, height=%d" % (width1, height1)

    width_register_addr_rgb1 = GetRegisterAddr(n, b"Width") + 0x100
    height_register_addr_rgb1 = GetRegisterAddr(n, b"Height") + 0x100
    width_rgb1 = new_intArray(0)
    height_rgb1 = new_intArray(0)
    ReadRegister(n, width_register_addr_rgb1, width_rgb1)
    ReadRegister(n, height_register_addr_rgb1, height_rgb1)
    width_RGB1 = intArray_getitem(width_rgb1, 0)
    height_RGB1 = intArray_getitem(height_rgb1, 0)
    print"camera 2 Width_rgb=%d, height_rgb=%d" % (width_RGB1, height_RGB1)

    point_data1 = PhotoInfoCSharp()
    gray_data1 = PhotoInfoCSharp()
    rgb_data1 = PhotoInfoCSharp()

    point_num1 = width1 * height1 * 6
    pointpixel1 = np.zeros(point_num1, dtype=np.int8).tobytes()

    gray_num1 = width1 * height1
    graypixel1 = np.zeros(gray_num1, dtype=np.int8).tobytes()

    rgb_num1 = width_RGB1 * height_RGB1 * 3
    rgbpixel1= np.zeros(rgb_num1, dtype=np.int8).tobytes()


    rgb_cloud1 = np.zeros((width1 * height1 * 6), dtype=np.float32)
    gray_cloud1 = np.zeros((width1 * height1 * 6), dtype=np.float32)

    print"-------camera 1 tirgger mode and stream on-------"
    # camera1 SetTriggerMode
    tirggerMode = SetTriggerMode(k, 1)
    print"tirggerMode=", tirggerMode

    tirggerModeRGB = SetRGBTriggerMode(k, 1)
    print"tirggerModeRGB=", tirggerModeRGB

    # camera1 StreamOn
    stream_point = StreamOn(k, 1)
    print"stream_point=", stream_point

    stream_gray = StreamOn(k, 0)
    print"stream_gray=", stream_gray

    stream_RGB = StreamOn(k, 2)
    print"stream_RGB=", stream_RGB

    acquistion = AcquisitionStart(k)
    print"acquistion=", acquistion

    print("-------camera 2 tirgger mode and stream on-------")
    # camera2 SetTriggerMode
    tirggerMode1 = SetTriggerMode(n, 1)
    print"tirggerMode1=", tirggerMode1

    tirggerModeRGB1 = SetRGBTriggerMode(n, 1)
    print"tirggerModeRGB1=", tirggerModeRGB1

    #camera2 StreamOn
    stream_point1 = StreamOn(n, 1)
    print"stream_point1=", stream_point

    stream_gray1 = StreamOn(n, 0)
    print"stream_gray1=", stream_gray

    stream_RGB1 = StreamOn(n, 2)
    print"stream_RGB1=", stream_RGB

    acquistion1 = AcquisitionStart(n)
    print"acquistion1=", acquistion

    print("------------camera 1 tirgger and save--------")
    # camera1 SetTriggerCount
    triggerCount = SetTriggerCount(k, 1)
    print"triggerCount:", triggerCount

    triggerCountRGB = SetRGBTriggerCount(k, 1)
    print"triggerCountRGB:", triggerCountRGB

    pcd_name = b"1.pcd"
    gray_name = b"1.bmp"
    rgb_name = b"1_rgb.bmp"
    gray_cloud_name = b"1_gray.txt"
    rgb_cloud_name = b"1_rgb.txt"
    filter_name = b"1_filter.pcd"
    depth_name = b"1.png"

    # save point cloud
    capturePoint = CaptureCSharp(k, 1, point_data, pointpixel, point_num)
    print"capture_Pointimage: ", capturePoint
    savepcd = SavePointCloudToPcdCSharp(k, point_data, pointpixel, point_num, pcd_name)
    print"save pcd=", savepcd

    # save gray
    capturegray = CaptureCSharp(k, 0, gray_data, graypixel, gray_num)
    print"capture_Gray: ", capturegray
    savebmp = SaveToBMPCSharp(k, gray_data, graypixel, gray_num, gray_name)
    print"save gray=", savebmp

    # save RGB
    captureRGB = CaptureCSharp(k, 2, rgb_data, rgbpixel, rgb_num)
    print"capture RGB=", captureRGB
    savergb = SaveToBMPCSharp(k, rgb_data, rgbpixel, rgb_num, rgb_name)
    print"save rgb=", savergb
   

    # filter point cloud
    FilterPointCloudCSharp(k, point_data, pointpixel, point_num, 1)
    savefilter = SavePointCloudToPcdCSharp(k, point_data, pointpixel, point_num, filter_name)
    print"save Filter Point=", savefilter
    # save depth
    savedepth = SaveDepthToPngCSharp(k, point_data, pointpixel, point_num, depth_name)
    print"save Depth=", savedepth

    # point cloud fusion gray
    FusionImageTo3DCSharp(k, gray_data, graypixel, gray_num, point_data, pointpixel, gray_cloud)
    savegray_cloud = SavePointCloudWithImageToTxtCSharp(k, point_data, pointpixel,gray_cloud,
                                                        gray_cloud_name)
    print"save Gray_cloud=", savegray_cloud

    # point cloud fusion rgb
    FusionImageTo3DCSharp(k, rgb_data, rgbpixel, rgb_num, point_data, pointpixel,  rgb_cloud)
    savergb_cloud = SavePointCloudWithImageToTxtCSharp(k, point_data, pointpixel, rgb_cloud,
                                                       rgb_cloud_name)
    print"save RGB_cloud=", savergb_cloud


    print"------------camera 2 tirgger and save--------"
    #camer1 SetTriggerCount
    triggerCount1 = SetTriggerCount(n, 1)
    print"triggerCount1:", triggerCount1

    triggerCountRGB1 = SetRGBTriggerCount(n, 1)
    print"triggerCountRGB1:", triggerCountRGB1

    pcd_name1 = b"2.pcd"
    gray_name1 = b"2.bmp"
    rgb_name1 = b"2_rgb.bmp"
    gray_cloud_name1 = b"2_gray.txt"
    rgb_cloud_name1 = b"2_rgb.txt"
    filter_name1 = b"2_filter.pcd"
    depth_name1 = b"2.png"

    # save point cloud 
    capturePoint1 = CaptureCSharp(n, 1, point_data1, pointpixel1, point_num1)
    print"capture_Pointimage1: ", capturePoint1
    savepcd1 = SavePointCloudToPcdCSharp(n, point_data1, pointpixel1, point_num1, pcd_name1)
    print"save pcd1=", savepcd1

    # save gray
    capturegray1 = CaptureCSharp(n, 0, gray_data1, graypixel1, gray_num1)
    print"capture_Gray1: ", capturegray1
    savebmp1 = SaveToBMPCSharp(n, gray_data1, graypixel1, gray_num1, gray_name1)
    print"save gray1=", savebmp1

    # save RGB
    captureRGB1 = CaptureCSharp(n, 2, rgb_data1, rgbpixel1, rgb_num1)
    print"capture RGB1=", captureRGB1
    savergb1 = SaveToBMPCSharp(n, rgb_data1, rgbpixel1, rgb_num1, rgb_name1)
    print"save rgb1=", savergb1
   
    # filter point cloud
    FilterPointCloudCSharp(n, point_data1, pointpixel1, point_num1, 1)
    savefilter1 = SavePointCloudToPcdCSharp(n, point_data1, pointpixel1, point_num1, filter_name1)
    print"save Filter Point1=", savefilter1
    # save depth
    savedepth1 = SaveDepthToPngCSharp(n, point_data1, pointpixel1, point_num1, depth_name1)
    print"save Depth1=", savedepth1

    # point cloud fusion gray
    FusionImageTo3DCSharp(n, gray_data1, graypixel1, gray_num1, point_data1, pointpixel1,  gray_cloud1)
    savegray_cloud1 = SavePointCloudWithImageToTxtCSharp(n, point_data1, pointpixel1,  gray_cloud1,
                                                        gray_cloud_name1)
    print"save Gray_cloud1=", savegray_cloud1

    # point cloud fusion rgb
    FusionImageTo3DCSharp(n, rgb_data1, rgbpixel1, rgb_num1, point_data1, pointpixel1, rgb_cloud1)
    savergb_cloud1 = SavePointCloudWithImageToTxtCSharp(n, point_data1, pointpixel1,  rgb_cloud1,
                                                       rgb_cloud_name1)
    print"save RGB_cloud1=", savergb_cloud1

    print"---------camera 1 stream off----------"

    streamoff_gray = StreamOff(k, 0)
    print"streamoff_gray=", streamoff_gray

    streamoff_point = StreamOff(k, 1)
    print"streamoff_point=", streamoff_point

    streamoff_rgb = StreamOff(k, 2)
    print"streamoff_rgb=", streamoff_rgb
   
    disconnect = CameraDisconnect(k)
    print"disconnect=", disconnect

    print"---------camera 2 stream off----------"

    streamoff_gray1 = StreamOff(n, 0)
    print"streamoff_gray1=", streamoff_gray1

    streamoff_point1 = StreamOff(n, 1)
    print"streamoff_point1=", streamoff_point1

    streamoff_rgb1 = StreamOff(n, 2)
    print"streamoff_rgb1=", streamoff_rgb1
    
    disconnect1 = CameraDisconnect(n)
    print"disconnect1=", disconnect1
    DestroyCamera()
