
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

	# get camera InternelParameter
    kc=new_floatArray(5)
    kk=new_floatArray(9)
    print("GetCamInternelParameter:",GetCamInternelParameter(camera_ret,0,kc,kk))
    for i in range(5):
        print("kc:%e" %floatArray_getitem(kc,i))
    for n in range(9):
        print("kk:%e" %floatArray_getitem(kk, n))
    delete_floatArray(kc)
    delete_floatArray(kk)
     # get camera ExternelParameter
    R = new_floatArray(9)
    T = new_floatArray(3)
    print("GetCamExternelParameter:",GetCamExternelParameter(camera_ret,0,R,T))
    for j in range(0,9):
        print("R:%e" % floatArray_getitem(R, j))
    for m in range(0,3):
        print("T:%e" % floatArray_getitem(T, m))
    delete_floatArray(R)
    delete_floatArray(T)

    disconnect = CameraDisconnect(camera_ret)
    print("disconnect=", disconnect)

    DestroyCamera()
	
