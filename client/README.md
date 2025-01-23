# How to fix that problem

sudo apt-get update
sudo apt-get install v4l-utils

v4l2-ctl --list-formats-ext
#0: YUYV 4:2:2
  Size: 640x480
  Size: 1280x720
  Size: 1920x1080

swiftPro@swiftPro:~/swiftPro/client$ v4l2-ctl --list-formats-ext
ioctl: VIDIOC_ENUM_FMT
	Type: Video Capture

	[0]: 'YU12' (Planar YUV 4:2:0)
		Size: Stepwise 32x32 - 3280x2464 with step 2/2
	[1]: 'YUYV' (YUYV 4:2:2)
		Size: Stepwise 32x32 - 3280x2464 with step 2/2
	[2]: 'RGB3' (24-bit RGB 8-8-8)
		Size: Stepwise 32x32 - 3280x2464 with step 2/2
	[3]: 'JPEG' (JFIF JPEG, compressed)
		Size: Stepwise 32x32 - 3280x2464 with step 2/2
	[4]: 'H264' (H.264, compressed)
		Size: Stepwise 32x32 - 3280x2464 with step 2/2
	[5]: 'MJPG' (Motion-JPEG, compressed)
		Size: Stepwise 32x32 - 3280x2464 with step 2/2
	[6]: 'YVYU' (YVYU 4:2:2)
		Size: Stepwise 32x32 - 3280x2464 with step 2/2
	[7]: 'VYUY' (VYUY 4:2:2)
		Size: Stepwise 32x32 - 3280x2464 with step 2/2
	[8]: 'UYVY' (UYVY 4:2:2)
		Size: Stepwise 32x32 - 3280x2464 with step 2/2
	[9]: 'NV12' (Y/CbCr 4:2:0)
		Size: Stepwise 32x32 - 3280x2464 with step 2/2
	[10]: 'BGR3' (24-bit BGR 8-8-8)
		Size: Stepwise 32x32 - 3280x2464 with step 2/2
	[11]: 'YV12' (Planar YVU 4:2:0)
		Size: Stepwise 32x32 - 3280x2464 with step 2/2
	[12]: 'NV21' (Y/CrCb 4:2:0)
		Size: Stepwise 32x32 - 3280x2464 with step 2/2
	[13]: 'RX24' (32-bit XBGR 8-8-8-8)
		Size: Stepwise 32x32 - 3280x2464 with step 2/2
swiftPro@swiftPro:~/swiftPro/client$ 

From the output of `v4l2-ctl --list-formats-ext`, it looks like your camera supports various formats, including `YUYV`, `MJPG`, and `JPEG`. For streaming video or images, `MJPG` is often a good choice because it's compressed and doesn't require as much CPU power as formats like `YUYV` or `H264`. Let's try forcing the `MJPG` format in your OpenCV code to see if it works.

### 1. **Force MJPEG Format**
You can explicitly set the video format to `MJPG` by using the `cv2.VideoCapture` property `CAP_PROP_FOURCC`. Here's how you can modify your code to use `MJPG`:
