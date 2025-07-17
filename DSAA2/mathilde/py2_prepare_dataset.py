from PIL import Image
import os

datasets = ["train", "test"]
categories = ["target", "others"]
base_dir = "dataset"

output_size = (224, 224)  # Dimensions finales

def center_crop(im):
    width, height = im.size
    min_dim = min(width, height)
    left = (width - min_dim) / 2
    top = (height - min_dim) / 2
    right = (width + min_dim) / 2
    bottom = (height + min_dim) / 2
    return im.crop((left, top, bottom, right))

for dataset in datasets:
    for category in categories:
        category_path = os.path.join(base_dir, dataset, category)
        
        if not os.path.exists(category_path):
            print(f"Le dossier {category_path} n'existe pas.")
            continue

        images = [f for f in os.listdir(category_path) if f.lower().endswith('.jpg')]

        for img_file in images:
            img_path = os.path.join(category_path, img_file)

            try:
                with Image.open(img_path) as img:
                    # Recadrer l'image au centre (carré)
                    img = center_crop(img)

                    # Redimensionner à 224x224
                    img = img.resize(output_size, Image.Resampling.LANCZOS)

                    # Conversion en RGB forcée (au cas où)
                    img = img.convert('RGB')

                    # Sauvegarder l'image recadrée et redimensionnée
                    img.save(img_path, format='JPEG')

                print(f"Préparé : {dataset}/{category}/{img_file}")
            
            except Exception as e:
                print(f"Erreur avec {dataset}/{category}/{img_file}: {e}")

print("Préparation des images terminée.")