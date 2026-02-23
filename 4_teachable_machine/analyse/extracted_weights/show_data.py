import sys
import numpy as np
import matplotlib.pyplot as plt

def visualize_numpy_file(path):
    data = np.load(path)

    # Cas .npz (archive de plusieurs tableaux)
    if isinstance(data, np.lib.npyio.NpzFile):
        print("Fichier .npz détecté. Tableaux disponibles :", data.files)
        for name in data.files:
            print(f"\nVisualisation de '{name}'")
            visualize_array(data[name], title=name)
    else:
        visualize_array(data, title=path)

def visualize_array(arr, title=""):
    print(f"Shape: {arr.shape}, dtype: {arr.dtype}")

    plt.figure()

    # 1D → courbe
    if arr.ndim == 1:
        plt.plot(arr)
        plt.ylabel("Valeur")
        plt.xlabel("Index")

    # 2D → image ou heatmap
    elif arr.ndim == 2:
        plt.imshow(arr, aspect="auto", cmap="viridis")
        plt.colorbar(label="Valeur")

    # 3D → visualisation d'une tranche
    elif arr.ndim == 3:
        slice_idx = arr.shape[0] // 2
        plt.imshow(arr[slice_idx], aspect="auto", cmap="viridis")
        plt.colorbar(label="Valeur")
        plt.title(f"{title} (slice {slice_idx})")

    else:
        print("Nombre de dimensions non pris en charge pour l'affichage.")
        return

    plt.title(title)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage : python visualize_numpy.py fichier.npy|fichier.npz")
        sys.exit(1)

    visualize_numpy_file(sys.argv[1])
