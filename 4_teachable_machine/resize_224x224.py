import os
from PIL import Image

INPUT_DIR = "./tuto1/dataset/cats_and_dogs"
OUTPUT_DIR = "./tuto1/dataset/cats_and_dogs_resized"
TARGET_SIZE = (224, 224)

for root, _, files in os.walk(INPUT_DIR):
    for file in files:
        if file.lower().endswith((".jpg", ".jpeg")):
            input_path = os.path.join(root, file)

            # Recrée l’arborescence
            relative_path = os.path.relpath(root, INPUT_DIR)
            output_dir = os.path.join(OUTPUT_DIR, relative_path)
            os.makedirs(output_dir, exist_ok=True)

            output_path = os.path.join(output_dir, file)

            try:
                with Image.open(input_path) as img:
                    img = img.convert("RGB")
                    img = img.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
                    img.save(output_path, "JPEG")
            except Exception as e:
                print(f"✖ Erreur sur {input_path} : {e}")
