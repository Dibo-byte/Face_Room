import cv2
from picamera2 import Picamera2
import time
import os

# Inicializa a câmera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))
picam2.start()
time.sleep(2)

# Carrega o classificador de rosto
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Pede o ID do usuário
user_id = input("Digite o ID do usuário: ").strip()

# Cria pasta para o usuário, se não existir
dataset_dir = "dataset"
user_dir = os.path.join(dataset_dir, user_id)
os.makedirs(user_dir, exist_ok=True)

print("Posicione seu rosto na câmera. Capturando 30 imagens...")

count = 0
while count < 30:
    frame = picam2.capture_array()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        count += 1
        rosto = gray[y:y+h, x:x+w]
        rosto = cv2.resize(rosto, (200, 200))

        # Salva a imagem do rosto na pasta do usuário
        filename = os.path.join(user_dir, f"user.{user_id}.{count}.jpg")
        cv2.imwrite(filename, rosto)

        # Desenha retângulo no rosto detectado
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        print(f"Imagem {count} capturada")

    cv2.imshow("Coleta de rosto", frame)

    # Sai se apertar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Pequena pausa para não capturar todas muito rápido
    time.sleep(0.1)

print("Dataset criado com sucesso!")
picam2.stop()
cv2.destroyAllWindows()
