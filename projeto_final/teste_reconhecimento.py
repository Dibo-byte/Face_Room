import cv2
from picamera2 import Picamera2
import time

# Inicializa a câmera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))
picam2.start()
time.sleep(2)

# Carrega classificador de rosto e modelo treinado
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("modelo_lbph.yml")

# Carrega labels do arquivo
label_map = {}
with open("labels.txt", "r") as f:
    for line in f:
        label, user = line.strip().split(":")
        label_map[int(label)] = user

print("Reconhecimento iniciado. Pressione 'q' para sair.")

while True:
    frame = picam2.capture_array()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        rosto = gray[y:y+h, x:x+w]
        rosto = cv2.resize(rosto, (200, 200))

        label, confidence = recognizer.predict(rosto)
        name = label_map.get(label, "Desconhecido")

        # Mostrar resultado
        cv2.putText(frame, f"{name} ({confidence:.2f})", (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Reconhecimento Facial", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.stop()
cv2.destroyAllWindows()
