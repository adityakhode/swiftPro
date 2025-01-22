# PiCamera on Ubuntu 22.04

**# Author: Aditya Khode**

**# maintainer: khodeaditya7@gmail.com**

**# This documennt is having set of command that helps to set the PiCamera on Ubuntu 22.04**

**# The refernce is take from the youtube video https://www.youtube.com/watch?v=va7o7wzhEE4&t=49s**

**# This document is made for ros2 humble**

**# Ensure that system has internet connection.**

**# Assuming ros2 humble is already downloaded.**

## **Update and Upgarde the system**
```
sudo apt update && sudo apt upgrade
```


## **Install reqired library for raspberryPi, video for Linux and ros- humble camera**

```
sudo apt install libraspberrypi-bin v4l-utils ros-humble-v4l2-camera
```

## **Install ros humble transport plugin**

```
sudo apt install ros-humble-image-transport-plugin
```

## **If you are some another user or root user check you have camera and video access**

```
groups
```
- After listing you will see some list on screen ensure that **video** is present, if not present run the below command.

## **If group does not have *video* then run thos command (Optional)**

```
sudo usermod -aG video swiftPro
```
- Ensure the **video** is present in group. If your username is different then then use that name for swiftPro drone model username is swiftPro.

## **Download raspberry Pi congigurator tool to enable services***

```
sudo apt install raspi-config
```

## **open raspberry Pi configuratior**

```
sudo raspi-config
```
- **Enable legacy camera option SPI and I2C communication prototcol**
- Do the below process as shown.

![raspi-config](https://github.com/user-attachments/assets/94da1e0d-c62c-49a2-8545-7879a4317f84)
![interface-option](https://github.com/user-attachments/assets/47bdd073-8ba2-4bbb-a284-c2fa5ce6fb3f)
![Legacy-camera option](https://github.com/user-attachments/assets/78d2a8bb-6119-4a69-8bbf-a98a6ba5a63e)
![spi-option](https://github.com/user-attachments/assets/f97cba4c-870a-4229-b9a0-b7b2cc8c4c10)
![i2c-option](https://github.com/user-attachments/assets/469a1387-63ab-4593-adb2-76dd10a5d8ef)
![finish-option](https://github.com/user-attachments/assets/dd8f6bc4-658d-4a96-9263-15d853c3bc19)
![reboot](https://github.com/user-attachments/assets/395a7d66-2622-4065-aea7-362c2f8899a2)


## **Check the camera is properly connected**
```
vcgencmd get_camera
```
- ```# supported=1 dected=1 , libcamera interfaces=0 this should be the output.```

## **Source the ros2 humble bin path**

```
source /opt/ros/humble/setup.bash
```

## **Run the ROS node for using video for Linux**

```
ros2 run v4l2_camera v4l2_camera_node --ros-args -p image_size:="[640,480]"
```
- There should be some warning and errors you can safely ignore that as output is alreading publishing the sensor_msg.

##  **View Output** 
- Make a file
```
nano videoSubscriber.py
```
- write or copy paste the code given below in videoSubscriber.py
```
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge
import cv2

class CameraSubscriber(Node):

    def __init__(self):
        super().__init__('camera_subscriber')
        
        # Create a CvBridge object to convert ROS messages to OpenCV images
        self.bridge = CvBridge()

        # Subscribe to the /image_raw topic to get raw images
        self.image_sub = self.create_subscription(
            Image,
            '/image_raw',
            self.image_callback,
            10
        )

        # Subscribe to the /camera_info topic to get camera calibration data
        self.camera_info_sub = self.create_subscription(
            CameraInfo,
            '/camera_info',
            self.camera_info_callback,
            10
        )
        
        self.camera_info = None

    def image_callback(self, msg):
        # Convert ROS Image message to OpenCV image
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            
            # Display the image in an OpenCV window
            cv2.imshow("Camera Feed", cv_image)
            cv2.waitKey(1)  # Wait for 1 ms to display the image
        except Exception as e:
            self.get_logger().error(f"Error converting image: {e}")

    def camera_info_callback(self, msg):
        # Store the camera info (this is for debugging or future use)
        self.camera_info = msg
        self.get_logger().info(f"Camera Info received: {msg}")

def main(args=None):
    rclpy.init(args=args)

    camera_subscriber = CameraSubscriber()

    rclpy.spin(camera_subscriber)

    # Destroy the node explicitly (optional but good practice)
    camera_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

- Save it using `ctrl + x` -> `Y` -> `enter`.
  
## **Install dependancies**

```
pip3 install opencv-python cv-bridge rclpy sensor-msgs
```

## **Run the file**

```
python3 videoSubscriber.py
```
- You can see the window pop up showing camera feed.
