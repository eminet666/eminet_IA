import psutil
import platform
import subprocess
import sys
import shutil

def get_size(bytes, suffix="o"):
    """Convertit les octets en format lisible (Go, Mo, etc.)"""
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f} {unit}{suffix}"
        bytes /= factor

def get_gpu_info():
    """Récupère les infos GPU. Priorité à NVIDIA pour ComfyUI."""
    gpus = []
    
    # Tentative 1 : Via nvidia-smi (Le plus fiable pour la VRAM réelle)
    try:
        cmd = "nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader"
        output = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
        lines = output.split('\n')
        for line in lines:
            name, total_mem, driver = line.split(',')
            gpus.append({
                "source": "NVIDIA Driver",
                "name": name.strip(),
                "vram": total_mem.strip(), # Déjà en MiB via nvidia-smi
                "driver": driver.strip()
            })
        return gpus
    except:
        pass # Si pas de nvidia-smi, on passe à la méthode générique Windows

    # Tentative 2 : Méthode générique Windows (wmic)
    # Note : Moins précis pour la VRAM (affiche souvent 4Go max sur les vieux API)
    try:
        cmd = "wmic path win32_VideoController get name, adapterram"
        output = subprocess.check_output(cmd, shell=True).decode("utf-8").strip().split('\n')
        # On saute l'en-tête
        for line in output[1:]:
            if line.strip():
                parts = line.split('  ') # Séparation approximative
                # Nettoyage simple
                parts = [p.strip() for p in parts if p.strip()]
                if len(parts) >= 1:
                    # Conversion approximative de l'adapterram si présent
                    vram_readable = "Inconnu"
                    if len(parts) > 1 and parts[-1].isdigit():
                        vram_readable = get_size(int(parts[-1]))
                    
                    gpus.append({
                        "source": "Windows API",
                        "name": parts[0],
                        "vram": vram_readable,
                        "driver": "N/A"
                    })
        return gpus
    except:
        return [{"source": "Erreur", "name": "Non détecté", "vram": "0", "driver": "N/A"}]

def system_inventory():
    print("="*40)
    print(f"RAPPORT DE CONFIGURATION POUR COMFYUI")
    print("="*40)

    # 1. Système OS
    uname = platform.uname()
    print(f"\n[SYSTÈME]")
    print(f"OS       : {uname.system} {uname.release}")
    print(f"Version  : {uname.version}")
    print(f"Machine  : {uname.machine}")

    # 2. Processeur (CPU)
    print(f"\n[PROCESSEUR - CPU]")
    print(f"Modèle   : {uname.processor}")
    print(f"Cœurs    : {psutil.cpu_count(logical=False)} Physiques / {psutil.cpu_count(logical=True)} Logiques")
    
    # 3. Mémoire Vive (RAM)
    svmem = psutil.virtual_memory()
    print(f"\n[MÉMOIRE VIVE - RAM]")
    print(f"Totale   : {get_size(svmem.total)}")
    print(f"Dispo.   : {get_size(svmem.available)}")
    print(f"Utilisée : {svmem.percent}%")
    
    if svmem.total < 16 * 1024 * 1024 * 1024:
        print("⚠️  ATTENTION : Moins de 16 Go de RAM détectés. Risque de lenteur sur SDXL/Flux.")

    # 4. Carte Graphique (GPU)
    print(f"\n[CARTE GRAPHIQUE - GPU]")
    gpus = get_gpu_info()
    for i, gpu in enumerate(gpus):
        print(f"--- GPU #{i+1} ({gpu['source']}) ---")
        print(f"Modèle   : {gpu['name']}")
        print(f"VRAM     : {gpu['vram']}")
        
        # Analyse rapide pour ComfyUI
        vram_val = 0
        if "MiB" in gpu['vram']:
            vram_val = int(gpu['vram'].replace(' MiB', ''))
        
        if vram_val > 0:
            if vram_val < 6000:
                print(">> RECO : Utilisez SD 1.5. SDXL sera très lent (Low VRAM mode).")
            elif vram_val < 10000:
                print(">> RECO : Confortable pour SD 1.5. OK pour SDXL.")
            else:
                print(">> RECO : Excellent. Prêt pour SDXL, Flux et l'entraînement.")

    # 5. Disque Dur (Espace libre où le script tourne)
    print(f"\n[STOCKAGE]")
    total, used, free = shutil.disk_usage(".")
    print(f"Espace libre ici : {get_size(free)}")
    if free < 20 * 1024 * 1024 * 1024: # Moins de 20 Go
         print("⚠️  ATTENTION : Espace disque faible pour télécharger des modèles.")

    print("\n" + "="*40)

if __name__ == "__main__":
    system_inventory()
    input("\nAppuyez sur Entrée pour quitter...")