import cv2
import os
import numpy as np

# Caminho do dataset
dataset_dir = "dataset"

# Inicializa o reconhecedor LBPH
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Para guardar rostos e seus respectivos labels (IDs numéricos)
faces = []
ids = []

# Cria um dicionário para mapear user_id (string) para um label numérico
label_map = {}
current_label = 0

# Percorre pastas dos usuários
for user_id in os.listdir(dataset_dir):
    user_path = os.path.join(dataset_dir, user_id)
    if not os.path.isdir(user_path):
        continue

    if user_id not in label_map:
        label_map[user_id] = current_label
        current_label += 1
    label = label_map[user_id]

    # Percorre imagens na pasta do usuário
    for image_name in os.listdir(user_path):
        image_path = os.path.join(user_path, image_name)
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        faces.append(img)
        ids.append(label)

print(f"Treinando com {len(faces)} imagens...")

# Treina o reconhecedor
recognizer.train(faces, np.array(ids))

# Salva o modelo treinado
recognizer.save("modelo_lbph.yml")

# Salva o mapeamento de labels para nomes em um arquivo texto
with open("labels.txt", "w") as f:
    for user, label in label_map.items():
        f.write(f"{label}:{user}\n")

print("Treinamento concluído e modelo salvo!")
