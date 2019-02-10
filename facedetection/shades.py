         
from .my_cnn_model import *
import cv2
import numpy as np



def detectface():

    import tensorflow as tf 
    tf.reset_default_graph() 

    #loding model build in previous class
    my_model=load_my_cnn_model('/home/devilshacker/ecommerce/src/facedetection/my_model')

    # face_cascade=cv2.CascadeClassifier('xml/haarcascade_frontalface_default.xml')
    face_cascade = cv2.CascadeClassifier('/home/devilshacker/ecommerce/src/facedetection/haarcascade_frontalface_default.xml')


    # Define a 5x5 kernel for erosion and dilation
    kernel = np.ones((5, 5), np.uint8)

    filters=['/home/devilshacker/ecommerce/src/facedetection/images/sunglasses_2.png']
    filterIndex=0

    #load the video
    camera=cv2.VideoCapture(0)
    while(camera.isOpened()):
        (grabbed,frame)=camera.read()
        frame=cv2.flip(frame,1)
        frame2 = np.copy(frame)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.25, 6)
        
        
        for (x, y, w, h) in faces:
            # Grab the face
            gray_face = gray[y:y+h, x:x+w]
            color_face = frame[y:y+h, x:x+w]

            # Normalize to match the input format of the model - Range of pixel to [0, 1]
            gray_normalized = gray_face / 255

            # Resize it to 96x96 to match the input format of the model
            original_shape = gray_face.shape # A Copy for future reference
            face_resized = cv2.resize(gray_normalized, (96, 96), interpolation = cv2.INTER_AREA)
            face_resized_copy = face_resized.copy()
            face_resized = face_resized.reshape(1, 96, 96, 1)
            
            # Predicting the keypoints using the model
            keypoints = my_model.predict(face_resized)
            
            # De-Normalize the keypoints values
            keypoints = keypoints * 48 + 48
            
            # Map the Keypoints back to the original image
            face_resized_color = cv2.resize(color_face, (96, 96), interpolation = cv2.INTER_AREA)
            face_resized_color2 = np.copy(face_resized_color)
            
            # Pair them together
            points = []
            for i, co in enumerate(keypoints[0][0::2]):
                points.append((co, keypoints[0][1::2][i]))
                
            # Add FILTER to the frame
            sunglasses = cv2.imread(filters[filterIndex], cv2.IMREAD_UNCHANGED)
            sunglass_width = int((points[7][0]-points[9][0])*1.1)
            sunglass_height = int((points[10][1]-points[8][1])/1.1)
            sunglass_resized = cv2.resize(sunglasses, (sunglass_width, sunglass_height), interpolation = cv2.INTER_CUBIC)
            transparent_region = sunglass_resized[:,:,:3] != 0
            face_resized_color[int(points[9][1]):int(points[9][1])+sunglass_height, int(points[9][0]):int(points[9][0])+sunglass_width,:][transparent_region] = sunglass_resized[:,:,:3][transparent_region]

        
            # Resize the face_resized_color image back to its original shape
            frame[y:y+h, x:x+w] = cv2.resize(face_resized_color, original_shape, interpolation = cv2.INTER_CUBIC)
            
            # Add KEYPOINTS to the frame2
            for keypoint in points:
                cv2.circle(face_resized_color2, keypoint, 1, (0,255,0), 1)

            frame2[y:y+h, x:x+w] = cv2.resize(face_resized_color2, original_shape, interpolation = cv2.INTER_CUBIC)

            # Show the frame and the frame2
            filters_frame=cv2.imshow("Selfie Filters", frame)
            facial=cv2.imshow("Facial Keypoints", frame2)

        # If the 'q' key is pressed, stop the loop
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return filters_frame


        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
