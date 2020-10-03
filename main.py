import cv2
import numpy as np

net = cv2.dnn.readNet('yolov3.weights','yolov3.cfg')
classes = []
with open('coco.names','r') as f:
    classes = f.read().splitlines()
#print(classes)

cap = cv2.VideoCapture('video.mp4') # camera dtect cap = cv2.VideoCapture(0)
#img = cv2.imread('image.jpg')

while True:
    _,img = cap.read()
    height,widht, _ = img.shape

    blob = cv2.dnn.blobFromImage(img,1/255,(416,416),(0,0,0),swapRB=True,crop=False)

    #for b in blob:
    #    for n, img_blob in enumerate(b):
    #        cv2.imshow(str(n),img_blob)

    net.setInput(blob)
    output_layers_names = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(output_layers_names)

    boxes = []
    confidences = []
    class_ids = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0]*widht)
                center_y = int(detection[1]*height)
                w = int(detection[2]*widht)
                h = int(detection[3]*height)

                x= int(center_x - w/2)
                y = int(center_y - h/2)
                boxes.append([x,y,w,h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)

    #print(len(boxes))
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    #print(indexes.flatten())
    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0,255, size=(len(boxes),3))

    if len(indexes) > 0:
        for i in indexes.flatten():
            x,y,w,h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence= str(round(confidences[i],2))
            color= colors[i]
            cv2.rectangle(img,(x,y),(x+w, y+h), color, 2)
            cv2.putText(img,label+ " "+ confidence, (x, y+20),font, 2,(225,225,225),2)

        cv2.imshow('image',img)
        key = cv2.waitKey(1)
        if key==5:
            break
cap.release()
cv2.destroyAllWindows()
