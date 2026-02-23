import psutil
import subprocess
import webbrowser

def get_vram_mib():
    """Récupère la VRAM en MiB via nvidia-smi (NVIDIA uniquement)."""
    try:
        cmd = "nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits"
        output = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
        # Prend la première carte trouvée
        return int(output.split('\n')[0])
    except:
        return 0

def analyze_config():
    print("Analyse du matériel en cours...", end="\r")
    
    # 1. Récupération des données
    vram = get_vram_mib()
    ram_gb = psutil.virtual_memory().total / (1024**3)
    
    print(" " * 40, end="\r") # Efface la ligne
    print(f"--- MATÉRIEL DÉTECTÉ ---")
    print(f"GPU VRAM : {vram} MiB ({vram/1024:.1f} Go)" if vram > 0 else "GPU VRAM : Non détecté (ou non-NVIDIA)")
    print(f"RAM Sys. : {ram_gb:.1f} Go")
    print("-" * 30)
    print("\n>>> RAPPORT DE RECOMMANDATION <<<\n")

    # LOGIQUE DE DÉCISION
    
    # CAS 1 : Pas de GPU NVIDIA ou VRAM < 4Go
    if vram < 4000:
        print("1_ FAISABILITÉ : ❌ DÉCONSEILLÉ (Mode CPU)")
        print("   Votre carte graphique est trop faible ou n'est pas une NVIDIA.")
        print("   ComfyUI tournera sur le processeur (CPU), ce sera extrêmement lent (min au lieu de sec).")
        print("\n2_ MODÈLE PRÉCONISÉ : SD 1.5 (Turbo/LCM)")
        print("   Si vous voulez vraiment essayer, utilisez des modèles ultra-légers.")
        print("\n3_ LIEN HUGGING FACE :")
        print("   https://huggingface.co/latent-consistency/lcm-lora-sdv1-5")
        
    # CAS 2 : VRAM 4Go - 6Go (Entrée de gamme)
    elif vram < 7000:
        print("1_ FAISABILITÉ : ✅ ENVISAGEABLE (Mode Low VRAM)")
        print("   ComfyUI fonctionnera, mais vous devrez utiliser l'argument '--lowvram'.")
        print("   La génération sera lente pour les images haute définition.")
        print("\n2_ MODÈLE PRÉCONISÉ : Stable Diffusion 1.5")
        print("   SDXL est possible mais risque de planter ou d'être très lent.")
        print("\n3_ LIEN HUGGING FACE (Fichier à télécharger) :")
        print("   Modèle : v1-5-pruned-emaonly.safetensors")
        print("   URL : https://huggingface.co/runwayml/stable-diffusion-v1-5/tree/main")

    # CAS 3 : VRAM 8Go (Standard)
    elif vram < 11000:
        print("1_ FAISABILITÉ : 🚀 OUI (Standard)")
        print("   C'est la configuration standard. Tout fonctionne correctement.")
        print("\n2_ MODÈLE PRÉCONISÉ : SDXL (Stable Diffusion XL)")
        print("   C'est le meilleur compromis qualité/performance actuel pour 8Go.")
        print("   (Note: Pour FLUX.1, utilisez les versions compressées GGUF).")
        print("\n3_ LIEN HUGGING FACE (Fichier à télécharger) :")
        print("   Modèle : sd_xl_base_1.0.safetensors")
        print("   URL : https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/tree/main")

    # CAS 4 : VRAM 12Go - 16Go+ (Idéal)
    else:
        print("1_ FAISABILITÉ : 🌟 EXCELLENTE (High Performance)")
        print("   Vous pouvez tout faire tourner, y compris les modèles de nouvelle génération.")
        print("\n2_ MODÈLE PRÉCONISÉ : FLUX.1 [dev]")
        print("   Actuellement le modèle le plus puissant (photoréalisme, respect du texte).")
        print("   Nécessite le 'clip_l.safetensors' et 't5xxl_fp16.safetensors' en plus.")
        print("\n3_ LIEN HUGGING FACE (Fichier à télécharger) :")
        print("   Modèle : flux1-dev.safetensors (attention, il fait ~23 Go !)")
        print("   URL : https://huggingface.co/black-forest-labs/FLUX.1-dev/tree/main")
        print("   Alternative SDXL (plus léger) : sd_xl_base_1.0.safetensors")

    print("\n" + "="*40)

if __name__ == "__main__":
    analyze_config()
    input("\nAppuyez sur Entrée pour fermer...")