import os
import json

# Fonction pour lister les fichiers .jpg dans un répertoire
def list_images(directory):
    return [f for f in os.listdir(directory) if f.endswith('.jpg')]

# Chemins des répertoires à scanner
train_target_dir = 'dataset/train/target'
train_other_dir = 'dataset/train/others'

# Vérifier si les répertoires existent
if not os.path.exists(train_target_dir):
    print(f"Le répertoire {train_target_dir} n'existe pas.")
    exit()

if not os.path.exists(train_other_dir):
    print(f"Le répertoire {train_other_dir} n'existe pas.")
    exit()

# Lister les fichiers .jpg dans les répertoires
target_images = list_images(train_target_dir)
other_images = list_images(train_other_dir)

# Structure du fichier JSON
dataset = {
    'train': {
        'target': target_images,
        'others': other_images
    }
}

# Sauvegarder les données dans un fichier dataset.json
output_file = 'dataset.json'
with open(output_file, 'w') as f:
    json.dump(dataset, f, indent=2)

print(f"Le fichier {output_file} a été généré avec succès!")
