
from DkamSDK import *

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

	# get timestamp
    setTime=SetTimestamp(camera_ret,1)
    print"SetTimestamp:", setTime
    getTime = GetTimestamp(camera_ret)
    print"GetTimestamp:", getTime
    getTimestatus = GetTimestampStatus(camera_ret)
    print"GetTimestampStatus:", getTimestatus
    settimeLatch=SetTimestampControlLatch(camera_ret)
    print"SetTimestampControlLatch:", settimeLatch
    gettimevalue=GetTimestampValue(camera_ret)
    print"GetTimestampValue:", gettimevalue
    gettimeFrequency=GetTimestampTickFrequency(camera_ret)
    print"GetTimestampTickFrequency:", gettimeFrequency
	
    disconnect = CameraDisconnect(camera_ret)
    print"disconnect=",disconnect
    DestroyCamera()
