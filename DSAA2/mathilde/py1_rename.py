import os

datasets = ["train", "test"]
categories = ["target", "others"]
base_dir = 'dataset'

for dataset in datasets:
    for category in categories:
        category_path = os.path.join(base_dir, dataset, category)
        
        if not os.path.exists(category_path):
            print(f"Le dossier {category_path} n'existe pas.")
            continue

        valid_extensions = ('.jpg',)
        images = [f for f in os.listdir(category_path) if f.lower().endswith(valid_extensions)]
        images.sort()

        for idx, img_file in enumerate(images):
            new_name = f"img_{idx}.jpg"
            src = os.path.join(category_path, img_file)
            dst = os.path.join(category_path, new_name)

            os.rename(src, dst)
            print(f"Renommé: {dataset}/{category}/{img_file} --> {new_name}")

print("Renommage terminé.")
