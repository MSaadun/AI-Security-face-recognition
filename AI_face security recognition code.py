#Import necesarry libraries
from imageai.Detection import VideoObjectDetection
from collections import defaultdict
import os
import cv2
import face_recognition
import sys
import time
from os import system
import ctypes
from win32com.client import Dispatch

#Set the path to the folder where the python file runs as a variable
execution_path = os.getcwd()

#Define an OpenCV VideoCapture instance and load the default device camera into it
camera = cv2.VideoCapture(0)

#Function for locking the workstation
def lock():
    ctypes.windll.user32.LockWorkStation()

#Function for playing a pre-defined text
def identification():
    speak = Dispatch("SAPI.SpVoice")
    speak.Speak("Identify yourself by looking into the camera please")

#Function for sending an email using a gmail account 
def send_mail():
        import smtplib # import necessary libraries to be able to send an email. 
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from email.mime.base import MIMEBase
        from email import encoders

        email_user = 'Put own e-mail address here' #Define a variable for the email adress. 
        email_password = 'PASSWORD' #Define the matching password for the emailadress. 
        email_send = 'E-MAILADDRESS' #Define the adress the mail will get send to if the codeblock gets activated. 

        subject = 'Security warning! Possible unknown person detected.' #Define the subject of the email. 

        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_send
        msg['Subject'] = subject

        body = "Your AI-CAM has detected a possible unknown person, please look at the image added in this email to see who triggered this email." #Define the body of the email
        msg.attach(MIMEText(body,'plain'))

        filename='Resources/Unknown Person/Unknown_person.jpg' #Define a variable to the path of the image file
        attachment  =open(filename,'rb') 

        part = MIMEBase('application','octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',"attachment; filename= "+filename)

        msg.attach(part)
        text = msg.as_string()
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(email_user,email_password)


        server.sendmail(email_user,email_send,text)
        server.quit()


# This program is designed as a security system. The program processes frames from live video of who is using the computer.It detects faces in these frames and    compares these against known faces in the database.
# If it is someone who's photo is 
# added in the database nothing will happen. But is a person who's photo is not in the database is using the computer the system will activate.
# The system will send a SMS, Whatsapp and email to the predetermined contacts.
# The email will contain a snapshot of a frame of the unkown user, so the predetermined contact can see who is using the system. 
# The system will also tell the unknown person using the system it does not recognize him/her. 

#Face detection function 
def face():
    # Let user know the system is activated, make a reference to the webcam. 
    print("Activating AI-CAM")  #Tell user that the system is live.
    video_capture = cv2.VideoCapture(0)             #Opening the webcam
    identification()
    # In the below codeblock the imagefiles of the persons who can use the system are added. It loads the images and gets the encodings for the images.
    jer_image = face_recognition.load_image_file("Resources/Images/jer_B.jpg")
    jer_face_encoding = face_recognition.face_encodings(jer_image)[0]
    
    
    # In the below codeblock the imagefiles of the persons who can use the system are added. It loads the images and gets the encodings for the images.
    samuel_image = face_recognition.load_image_file("Resources/Images/samuel_L.jpg")
    samuel_face_encoding = face_recognition.face_encodings(samuel_image)[0]
    
    # In the below codeblock the imagefiles of the persons who can use the system are added. It loads the images and gets the encodings for the images.
    burg_image = face_recognition.load_image_file("Resources/Images/burg_B.jpg")
    burg_face_encoding = face_recognition.face_encodings(burg_image)[0]
    
       
    
    # Make an array of the face encodings and the names
    known_face_encodings = [
        jer_face_encoding,
        samuel_face_encoding,
        burg_face_encoding,    
    ]
    known_face_names = [
        "Jer",
        "Samuel",
        "Burg",
    ]
    
    # Creating some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    
     # start a while loop
    while True:
        # Take one single frame from the live video.
        ret, frame = video_capture.read()
    
        # Make the frame smaller (1/4) to speed up the process. 
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    
        # OpenCV uses BGR colour, this code transforms this BGR colour to RGB colour. Because face_recognition uses RGB. 
        rgb_small_frame = small_frame[:, :, ::-1]
    
        # Only analyse every other frame to make the code faster.
        if process_this_frame:
    
            # Locate faces and their encodings in the current frame
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
    
            for face_encoding in face_encodings:
    
                # Check if they match the known faces added in the database
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, 0.55)
                distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    
                name = "Unknown"
    
                # If there is a match in the known face encodings, take the one with the minimum face distance (most close match)
                if True in matches:
                    best_match_index = distances.argmin()
                    name = known_face_names[best_match_index]
    
                face_names.append(name)
                #a=name
            #if a != name
            #count = 0 
            
    
        process_this_frame = not process_this_frame
    
    
    
        # Show the results 
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Go frome the (1/4) scale for faster processing back to normal.
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
    
            # Create a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
    
            # Create a label with name
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), 5)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    
    
        cv2.imshow('Camera', frame)
        if 'Unknown' in face_names:
             # Add some time, to prevent when the unknown face is present in multiple frames the system does not give repeated warnings     
    	    if (time.time()-os.path.getmtime("Resources/Unknown Person/Unknown_person.jpg")) > 30:   
        		img = cv2.imwrite("Resources/Unknown Person/Unknown_person.jpg",frame)
        		send_mail(),lock()
            
    
    
    
        # Hit q to stop the system, does not work 100% yet. 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Stop connection with webcam.
    video_capture.release()
    cv2.destroyAllWindows()

#Funtion that executes after each detected second of the video
def forSeconds(second_number, output_arrays, count_arrays, average_output_count):
    print("SECOND : ", second_number) #position number of the second
    print("Array for the outputs of each frame ", output_arrays) #An array of dictionaries whose keys are position number of each frame
    print("Array for output count for unique objects in each frame : ", count_arrays) #An array of dictionaries, with each dictionary corresponding to each frame and the keys of each dictionary are the name of the number of unique objects detected in each frame, and the key values are the number of instances of the objects found in the frame
    my_dict_list = defaultdict(list) #Initialise 'defaultdict' with the factory  function 'list' to group a sequence of key-value pairs into a dictionary of lists
    for value in count_arrays: #loop over the key-value pairs of the array of dictionaries.
        for k,v in value.items():
            my_dict_list[k].append(v) 
    detecteer_persoon = my_dict_list['person'] #Group for each frame the values of the 'Person' key in a list
    if detecteer_persoon.count(1) == 6: #Count the unique objects found in each frame. Since 8 frames are deteced in each second, in each frame a person should be detected to run function face().
        #time.sleep(5)
        #camera.release()
        face()
    if detecteer_persoon.count(1) == 6:
        print("Person detected")
    else:
        print("No person, or just a passerby detected")
    print(my_dict_list['person'])
    print("Output average count for unique objects in the last second: ", average_output_count)
    print("***************End of a second***************")

detector = VideoObjectDetection() #Object detection class for videos and camera live stream inputs in the ImageAI library
detector.setModelTypeAsRetinaNet() #Function to set which model is used for detection
detector.setModelPath(os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
detector.loadModel(detection_speed="fastest") #Load the model. Detection speed of the model can be varied by passing 'detection_speed' to the function. The available values are “normal”, “fast”, “faster”, “fastest” and “flash”.
custom = detector.CustomObjects(person=True) #Detect only custom objects. Here the custom object is the value 'Person'. Rest of the values are 'False' by default. 

video_path = detector.detectCustomObjectsFromVideo(custom_objects=custom, camera_input=camera, output_file_path=os.path.join(execution_path, "video_analysis"), frames_per_second=6,  log_progress=True, per_second_function=forSeconds, minimum_percentage_probability=50)

