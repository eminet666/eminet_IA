import sys
import numpy as np

MAX_VALUES_TO_PRINT = 50  # pour éviter d'inonder le terminal


def inspect_numpy_file(path):
    data = np.load(path, allow_pickle=True)

    # Cas .npz (plusieurs tableaux)
    if isinstance(data, np.lib.npyio.NpzFile):
        print(f"Fichier .npz détecté : {path}")
        for name in data.files:
            print("\n" + "=" * 60)
            print(f"Tableau : {name}")
            inspect_array(data[name])
    else:
        print(f"Fichier .npy détecté : {path}")
        inspect_array(data)


def inspect_array(arr):
    print(f"Shape : {arr.shape}")
    print(f"Dtype global : {arr.dtype}")

    # Cas simple : un seul type
    if arr.dtype != object:
        print_numeric_array(arr)
        return

    # Cas tableau d'objets → on classe par type Python
    type_map = {}

    for x in arr.flatten():
        t = type(x).__name__
        type_map.setdefault(t, []).append(x)

    print("\nTypes détectés :")
    for t, values in type_map.items():
        print("\n" + "-" * 40)
        print(f"Type : {t}")
        print(f"Nombre de valeurs : {len(values)}")

        numeric_values = [v for v in values if isinstance(v, (int, float, np.number))]

        if numeric_values:
            print("Exemples de valeurs numériques :")
            for v in numeric_values[:MAX_VALUES_TO_PRINT]:
                print(v)
        else:
            print("Aucune valeur numérique pour ce type.")


def print_numeric_array(arr):
    flat = arr.flatten()

    print(f"Nombre total de valeurs : {flat.size}")
    print(f"Min : {np.min(flat)}")
    print(f"Max : {np.max(flat)}")
    print(f"Moyenne : {np.mean(flat)}")

    print("\nValeurs (premiers éléments) :")
    for v in flat[:MAX_VALUES_TO_PRINT]:
        print(v)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage : python inspect_numpy.py fichier.npy|fichier.npz")
        sys.exit(1)

    inspect_numpy_file(sys.argv[1])
