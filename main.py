"""
sources:

matching:
https://www.tutorialspoint.com/template-matching-using-opencv-in-python
https://docs.opencv.org/master/d4/dc6/tutorial_py_template_matching.html

video frames:
https://www.geeksforgeeks.org/python-process-images-of-a-video-using-opencv/

inserting text:
https://www.learningaboutelectronics.com/Articles/How-to-add-text-to-an-image-in-Python-OpenCV.php
"""
import glob
import cv2
import numpy as np
import os

if __name__ == '__main__':

    # Creating a VideoCapture object to read the video
    cap = cv2.VideoCapture('Sprung.wm')

    # getting all template images
    templates = glob.glob(os.getcwd() + "\\templates\\*.png")  # searching for all .png files
    print("Found template images: " + str(templates))

    # Loop untill the end of the video
    while cap.isOpened():

        # Capture frame-by-frame
        ret, frame = cap.read()
        # converting to grayscale
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        for template in templates:

            print(template)

            # templateImage = cv2.imread("D:\\Users\\Q\\PycharmProjects\\MET_05_tagging\\templates\\helmet.PNG", 0)
            templateImage = cv2.imread(template, 0)  # splitting all the .pdf up

            width, height = templateImage.shape[::-1]  # getting the width and height

            # matching the template using cv2.matchTemplate
            match = cv2.matchTemplate(gray_image, templateImage,
                                      cv2.TM_CCOEFF_NORMED)  # matching with horizontal template image

            threshold = 0.92  # it is critical to tune the threshold

            position = np.where(match >= threshold)  # getting the location of template in the image

            if len(position[0]) != 0:

                for point in zip(*position[::-1]):  # draw the rectangle around the matched template
                    cv2.rectangle(frame, point, (point[0] + width, point[1] + height), (0, 255, 255), 2)
                    cv2.putText(frame, text='red helmet', org=(point[0] + 10 + width, point[1] + height),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 255, 255),
                                thickness=2, lineType=cv2.LINE_AA)

                break

        frame = cv2.resize(frame, (540, 380), fx=0, fy=0,
                           interpolation=cv2.INTER_CUBIC)

        cv2.imshow('Tagging', frame)
        # define q as the exit button
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # release the video capture object
    cap.release()
    # Closes all the windows currently opened.
    cv2.destroyAllWindows()
