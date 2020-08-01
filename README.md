# SecurAI
Realtime object detection with face recognition software for security environments: SecurAI

# Description
The code can be divided into two sections. 
The first part, for clarity purposes called CodeBlock A, is an object detection code to detect a custom object. For the intended purpose, the initialized custom object is a person. The adopted tool for real-time detection is a camera, by which CodeBlock A can observe the surroundings. CodeBlock A scans each frame for the initialized custom object and loops over the code for each second. For every passed second the number of detected custom object is counted. If the custom object is detected in each frame during the passed second, CodeBlock B runs. 
CodeBlock B asks the detected person to identify itself. The face of the detected person is scanned and compared to a database of known persons. If the face of the detected person and a known person is a match, continued access is granted by not locking the workstation. Simultaneously, if the detected person is an unknown person, continued access is denied by locking the workstation. In addition, an image of the unknown person is captured and sent to a pre-defined destination email address.


# Requirements
SecurAI requires that you have Python 3.5.1 installed as well as some other Python libraries and frame-works. 
Before using SecurAI, you must install the following dependencies:

•	pip3

•	Msgpack 0.6.0

•	Tensorflow 1.12.0 

•	Numpy 1.14.3

•	SciPy 1.1.0 or higher

•	OpenCV 3.4.5.20

•	Pillow 5.1.0

•	Matplotlib 2.2.2

•	h5py 2.7.1

•	Keras 2.2.4

•	ImageAI 2.0.2 or higher
pip3 install https://github.com/OlafenwaMoses/ImageAI/releases/download/2.0.2/imageai-2.0.2-py3-none-any.whl

•	CMake 3.13.3

•	Face_Recognition 1.2.3

The code should run on a Windows computer with a camera.

# Initialization
1.	Make sure that you fill in your own email address in line 38 in order to receive the a notification mail.

2.	To define a known user, make a clear picture of yourself and place it as a .jpg fie in the folder: ‘…/Resources/Images’

3.	Download the RetinaNet model via:  https://goo.gl/asRWzn 
    Place the file in the same location as the script.
    
4.	Change or place an additional codeblock with the same attributes as in def face() in line 77. Be aware, the code needs a correct relative path and filename.

5.	Run the code, unmute the volume and step away from the laptop/camera. 

6.	Aim the camera to a space. The software scans now for a person.

7.	Now test the code by letting a known or unknown person look in the camera or on the screen.  


Project by:

M Saadun
J Boateng
M El Kaddouri

