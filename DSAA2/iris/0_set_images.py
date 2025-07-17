import cv2
import os
import numpy as np

# Dossiers des images
input_dirs = ["dataset/train/target", "dataset/train/others",
              "dataset/test/target", "dataset/test/others"]
output_size = 224  # Taille finale

def resize_with_padding(img, size):
    h, w = img.shape[:2]

    # Calcul du ratio pour garder les proportions
    scale = size / max(h, w)
    new_w, new_h = int(w * scale), int(h * scale)

    # Redimensionnement sans déformation
    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # Création d'un fond noir (ou blanc : remplacer 0 par 255)
    delta_w = size - new_w
    delta_h = size - new_h
    top, bottom = delta_h // 2, delta_h - (delta_h // 2)
    left, right = delta_w // 2, delta_w - (delta_w // 2)

    padded = cv2.copyMakeBorder(resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0, 0, 0))  # Noir
    return padded

# Parcourir les dossiers et appliquer le padding
for input_dir in input_dirs:
    for filename in os.listdir(input_dir):
        img_path = os.path.join(input_dir, filename)

        img = cv2.imread(img_path)
        if img is None:
            continue

        img_padded = resize_with_padding(img, output_size)

        # Sauvegarde (remplace l’original)
        cv2.imwrite(img_path, img_padded)

print("Redimensionnement terminé sans distorsion ! ✅")
