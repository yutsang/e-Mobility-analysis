import cv2

file_name = "E:/e-Mobility-analysis/HighwaysDepartmentImage/2296c.jpg"
img = cv2.imread(file_name)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

CarDetction = cv2.CascadeClassifier('Car_Detection_System.xml')

while True:
    ret, frames = img.read()
    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
    cars = CarDetction.detectMultiScale(gray, 1.1, 9)
    # if str(np.array(cars).shape[0]) == '1':
    #     i += 1
    #     continue
    for (x,y,w,h) in cars:
        plate = frames[y:y + h, x:x + w]
        cv2.rectangle(frames,(x,y),(x +w, y +h) ,(51 ,51,255),2)
        cv2.rectangle(frames, (x, y - 40), (x + w, y), (51,51,255), -2)
        cv2.putText(frames, 'Car', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.imshow('car',plate)

    # lab1 = "Car Count: " + str(i)
    # cv2.putText(frames, lab1, (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (147, 20, 255), 3)
    frames = cv2.resize(frames,(600,400))
    cv2.imshow('Car Detection System', frames)
    # cv2.resizeWindow('Car Detection System', 600, 600)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cv2.destroyAllWindows()

