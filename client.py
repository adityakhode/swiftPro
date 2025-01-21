#!/usr/bin/python3

import cv2
import socket
import pickle
import argparse

# Set up argument parser to accept server IP and port as arguments
parser = argparse.ArgumentParser(description="UDP Video Stream Client")
parser.add_argument("ip", help="IP address of the server to send data to")
args = parser.parse_args()

# Set up the UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10000000)  # Set buffer size for sending
serverip = args.ip #"10.42.0.1"  # Server IP (e.g., ROS master)
serverport = 5000  # Port number (same as server)

# Initialize OpenCV VideoCapture with CAP_V4L2 for efficient camera access
#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(0,cv2.CAP_V4L2)  # 0 is the default camera; adjust if needed
if not cap.isOpened():
    print("Error: Camera not found or unable to open.")
    exit()

# Set camera properties (optional for adjusting camera settings like resolution)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set frame width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Set frame height

while True:
    # Capture frame from the camera
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image.")
        break

    # Encode the captured frame to JPEG format
    ret, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
    if not ret:
        print("Error: Failed to encode image.")
        break

    # Convert the encoded frame to byte format
    x_as_bytes = pickle.dumps(buffer)

    # Send the byte data over UDP to the server
    s.sendto(x_as_bytes, (serverip, serverport))

# Release the camera and close the socket when done
cap.release()
s.close()
