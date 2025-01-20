import cv2
import numpy as np
import math as m
import requests as rq

def main():
#Initilize cam
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Camera not accessible.")
        exit()

    while True:
        ret, frame = cam.read()
        if ret is None:
            print("Frame not captured.")
            continue

        # request WebServer to verify connection
        try:
            rq.get("http://192.168.4.1")
        except:
            print("ESP_WebServer unavailable. (HTTP code :400+)")
            exit(1)

        # define region of interest (hand region)
        cv2.rectangle(frame, (50, 200), (300, 500), (0, 255, 0), 0)
        crop_img = frame[200:500, 50:300]
        # convert to grey
        grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        value35 = (35, 35)
        # apply gaussian blur to enhance contours
        blurred = cv2.GaussianBlur(grey, value35, 0)
        _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    #Perform contour analysis
        #extract contours
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        if contours is None or len(contours) == 0:
            print("No contours found in region of interest.")
            continue
        else:
            print("Contours found.")
        #find largest contour
        max_cnt = max(contours, key = lambda X: cv2.contourArea(X))
        #draw bounding rect on hand region
        x, y, w, h = cv2.boundingRect(max_cnt)
        cv2.rectangle(crop_img, (x, y), (x+w, y+h), (0, 0, 255), 0)
        #compute convex hull
        hull = cv2.convexHull(max_cnt)
        drawing = np.zeros(crop_img.shape, np.uint8)
        #draw hand contours and convex hull on image
        cv2.drawContours(drawing, [max_cnt], 0, (0, 255, 0), 0)
        cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 0)
        hull = cv2.convexHull(max_cnt, returnPoints=False)
        defects = cv2.convexityDefects(max_cnt, hull)

        if defects is None:
            print("No convexity defects found.")
            continue

        count_defects = 0
        cv2.drawContours(thresh, contours, -1, (0, 255, 0), 3)

    #finger finder
        #iterate through convexity defects to compute angles
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(max_cnt[s][0])
            end = tuple(max_cnt[e][0])
            far = tuple(max_cnt[f][0])
            a = m.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b = m.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c = m.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
            angle = m.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57

            # if angle is greater than 90 a finger is found
            if angle <= 90:
                #draw circle at defect points
                count_defects += 1
                cv2.circle(crop_img, far, 1, [0, 0, 255], -1)
            #connect defect points with a line
            cv2.line(crop_img, start, end, [0, 255, 0], 2)

        #display finger count
        if count_defects == 0:
            cv2.putText(frame, "1", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255))
            LED1 = rq.get("http://192.168.4.1/led1/On")
            led2 = rq.get("http://192.168.4.1/led2/Off")
            led3 = rq.get("http://192.168.4.1/led3/Off")
            led4 = rq.get("http://192.168.4.1/led4/Off")
            led5 = rq.get("http://192.168.4.1/led5/Off")
        elif count_defects == 1:
            cv2.putText(frame, "2 ", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255))
            LED2 = rq.get("http://192.168.4.1/led2/On")
            LED1 = rq.get("http://192.168.4.1/led1/On")
            led3 = rq.get("http://192.168.4.1/led3/Off")
            led4 = rq.get("http://192.168.4.1/led4/Off")
            led5 = rq.get("http://192.168.4.1/led5/Off")
        elif count_defects == 2:
            cv2.putText(frame, "3 ", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255))
            LED3 = rq.get("http://192.168.4.1/led3/On")
            LED2 = rq.get("http://192.168.4.1/led2/On")
            LED1 = rq.get("http://192.168.4.1/led1/On")
            led4 = rq.get("http://192.168.4.1/led4/Off")
            led5 = rq.get("http://192.168.4.1/led5/Off")

        elif count_defects == 3:
            cv2.putText(frame, "4 ", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255))
            LED4 = rq.get("http://192.168.4.1/led4/On")
            LED3 = rq.get("http://192.168.4.1/led3/On")
            LED2 = rq.get("http://192.168.4.1/led2/On")
            LED1 = rq.get("http://192.168.4.1/led1/On")
            led5 = rq.get("http://192.168.4.1/led5/Off")

        elif count_defects == 4:
            cv2.putText(frame, "5 ", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255))
            LED5 = rq.get("http://192.168.4.1/led5/On")
            LED4 = rq.get("http://192.168.4.1/led4/On")
            LED3 = rq.get("http://192.168.4.1/led3/On")
            LED2 = rq.get("http://192.168.4.1/led2/On")
            LED1 = rq.get("http://192.168.4.1/led1/On")

        else:
            cv2.putText(frame, "No fingers detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255))

        cv2.imshow("Hand Gesture Recognition", frame)
        all_img = np.hstack((drawing, crop_img))
        cv2.imshow("Contours", all_img)
        k = cv2.waitKey(1)
        if k == ord("q"):
            break

    cv2.destroyAllWindows()
    cam.release()

if __name__ == "__main__":
    main()