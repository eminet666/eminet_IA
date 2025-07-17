from PIL import Image
import os

# Jeux de données
datasets = ['train', 'test']
categories = ['target', 'others']
base_dir = 'dataset'

for dataset in datasets:
    for category in categories:
        category_path = os.path.join(base_dir, dataset, category)
        
        if not os.path.exists(category_path):
            print(f"Le dossier {category_path} n'existe pas.")
            continue

        for img_file in os.listdir(category_path):
            if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                img_path = os.path.join(category_path, img_file)
                new_img_path = os.path.splitext(img_path)[0] + ".jpg"

                try:
                    with Image.open(img_path) as img:
                        rgb_img = img.convert('RGB')
                        rgb_img.save(new_img_path, format='JPEG')
                    
                    if not img_file.lower().endswith('.jpg'):
                        os.remove(img_path)

                    print(f"Converti: {dataset}/{category}/{img_file} --> {os.path.basename(new_img_path)}")
                
                except Exception as e:
                    print(f"Erreur avec {dataset}/{category}/{img_file}: {e}")

print("Conversion terminée.")
