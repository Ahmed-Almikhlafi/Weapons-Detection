
# bot_token = "7796257205:AAHHhb-Tr74c9-7GRXYcUnOfj_QyEseoWYk"
# chat_id = "1125122304"

import cv2
import numpy as np
import requests
import os
import time

# تحميل أسماء الكائنات (COCO dataset يحتوي على بعض الأشياء الخطرة)
labelsPath = "coco.names"
LABELS = open(labelsPath).read().strip().split("\n")

# تحميل YOLOv4
net = cv2.dnn.readNet("yolov4.weights", "yolov4.cfg")
layer_names = net.getLayerNames()
layer_names = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# قائمة الأشياء الخطرة
dangerous_items = ["knife", "fire", "scissors", "gun", "fork", "broken glass"]

# بيانات التليجرام
bot_token = "7796257205:AAHHhb-Tr74c9-7GRXYcUnOfj_QyEseoWYk"
chat_id = "1125122304"

# إرسال رسالة إلى التليجرام
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': message}
    requests.post(url, data=payload)

# إرسال صورة إلى التليجرام
def send_image_to_telegram(image_path):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    with open(image_path, 'rb') as image_file:
        payload = {'chat_id': chat_id}
        requests.post(url, data=payload, files={'photo': image_file})

# إرسال فيديو إلى التليجرام
def send_video_to_telegram(video_path):
    url = f"https://api.telegram.org/bot{bot_token}/sendVideo"
    with open(video_path, 'rb') as video_file:
        payload = {'chat_id': chat_id}
        requests.post(url, data=payload, files={'video': video_file})

# التقاط صورة وتخزينها
def capture_and_save_image(image_path, frame):
    cv2.imwrite(image_path, frame)

# تسجيل فيديو لمدة 10 ثوانٍ
def capture_video(video_path, cap, duration=10):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_path, fourcc, 20.0, (640, 480))
    start_time = time.time()

    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
    out.release()

# التحقق من وجود أمر
last_update_id = None
def listen_for_command():
    global last_update_id
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    response = requests.get(url).json()
    messages = response.get('result', [])

    for message in reversed(messages):
        update_id = message['update_id']
        if update_id == last_update_id:
            break

        last_update_id = update_id
        text = message.get('message', {}).get('text', "")
        if text.lower() == "اعطني صورة":
            return "image"
        elif text.lower() == "اعطني فيديو":
            return "video"
    return None

# فتح الكاميرا
cap = cv2.VideoCapture(0)

# حفظ الصورة المؤقتة
saved_image_path = "detected_object.jpg"
saved_video_path = "recorded_video.avi"

while True:
    ret, frame = cap.read()
    if not ret:
        break

    (H, W) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layerOutputs = net.forward(layer_names)

    boxes = []
    confidences = []
    classIDs = []

    # تحليل النتائج
    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            if confidence > 0.5 and LABELS[classID] in dangerous_items:
                send_telegram_message(f"⚠️ تحذير: تم اكتشاف {LABELS[classID]}!")

                # حفظ الصورة عند اكتشاف شيء
                capture_and_save_image(saved_image_path, frame)

                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    # تطبيق Non-Maximum Suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)

    # رسم الصناديق حول الكائنات الخطرة
    if len(indices) > 0:
        for i in indices.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            color = (0, 0, 255)  # لون أحمر للتحذير
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            text = f"{LABELS[classIDs[i]]}: {confidences[i]:.2f}"
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imshow("Dangerous Objects Detection", frame)

    # التحقق من الأوامر باستمرار
    request_type = listen_for_command()

    if request_type == "image":
        if os.path.exists(saved_image_path):
            send_image_to_telegram(saved_image_path)  # إرسال الصورة المخزنة
        else:
            capture_and_save_image("request_image.jpg", frame)
            send_image_to_telegram("request_image.jpg")
            os.remove("request_image.jpg")

    elif request_type == "video":
        capture_video(saved_video_path, cap, duration=10)  # تسجيل فيديو 10 ثوانٍ
        send_video_to_telegram(saved_video_path)
        os.remove(saved_video_path)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
