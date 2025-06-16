import cv2
from picamera2 import Picamera2
import time

# Inicializa a câmera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))
picam2.start()

time.sleep(2)  # Tempo para estabilizar

print("Pressione 'q' para sair")

try:
    while True:
        frame = picam2.capture_array()
        cv2.imshow("Visualização da Câmera", frame)

        # cv2.waitKey deve ser chamado com algum tempo (>1)
        # e retorna -1 se nada for pressionado
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Interrompido com Ctrl+C")

finally:
    picam2.stop()
    cv2.destroyAllWindows()
