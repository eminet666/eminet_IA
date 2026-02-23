#!/usr/bin/env python3
"""
Script principal pour analyser un modèle Teachable Machine complet
"""
import sys
from pathlib import Path


def main():
    """Exécute tous les scripts d'analyse"""
    
    import sys
    
    # Récupérer le dossier du modèle depuis les arguments
    if len(sys.argv) > 1:
        model_dir = Path(sys.argv[1])
        print(f"ℹ️  Analyse du modèle dans: {model_dir}\n")
    else:
        model_dir = Path("/mnt/user-data/uploads")
        print(f"ℹ️  Aucun dossier spécifié, utilisation du dossier par défaut: {model_dir}\n")
    
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "ANALYSE COMPLÈTE DU MODÈLE TEACHABLE MACHINE" + " " * 15 + "║")
    print("╚" + "═" * 78 + "╝")
    
    # Vérifier la présence des fichiers
    required_files = {
        'metadata': model_dir / "metadata.json",
        'model': model_dir / "model.json",
        'weights': model_dir / "weights.bin"
    }
    
    print("\n🔍 Vérification des fichiers...\n")
    files_present = {}
    
    for file_type, file_path in required_files.items():
        exists = file_path.exists()
        files_present[file_type] = exists
        status = "✓" if exists else "✗"
        print(f"  {status} {file_type}.json" if file_type != 'weights' 
              else f"  {status} weights.bin")
    
    print("\n" + "─" * 80 + "\n")
    
    # Obtenir le dossier où se trouve ce script
    script_dir = Path(__file__).parent
    
    # 1. Analyse des métadonnées
    if files_present['metadata']:
        print("▶️  ÉTAPE 1: Analyse des métadonnées\n")
        import subprocess
        result = subprocess.run([sys.executable, str(script_dir / "1_analyze_metadata.py"), str(model_dir)], 
                              capture_output=False)
        print("\n" + "─" * 80 + "\n")
        input("Appuyez sur Entrée pour continuer...")
        print("\n" + "─" * 80 + "\n")
    
    # 2. Analyse de l'architecture
    if files_present['model']:
        print("▶️  ÉTAPE 2: Analyse de l'architecture du modèle\n")
        result = subprocess.run([sys.executable, str(script_dir / "2_analyze_model_architecture.py"), str(model_dir)],
                              capture_output=False)
        print("\n" + "─" * 80 + "\n")
        input("Appuyez sur Entrée pour continuer...")
        print("\n" + "─" * 80 + "\n")
    
    # 3. Visualisation du réseau
    if files_present['model']:
        print("▶️  ÉTAPE 3: Visualisation du flux du réseau\n")
        result = subprocess.run([sys.executable, str(script_dir / "3_visualize_network.py"), str(model_dir)],
                              capture_output=False)
        print("\n" + "─" * 80 + "\n")
        input("Appuyez sur Entrée pour continuer...")
        print("\n" + "─" * 80 + "\n")
    
    # 4. Analyse des poids (si disponible)
    if files_present['weights']:
        print("▶️  ÉTAPE 4: Analyse des poids (weights.bin)\n")
        result = subprocess.run([sys.executable, str(script_dir / "4_analyze_weights.py"), str(model_dir)],
                              capture_output=False)
        print("\n" + "─" * 80 + "\n")
    else:
        print("⚠️  ÉTAPE 4: Analyse des poids (IGNORÉE)\n")
        print("   Le fichier weights.bin n'est pas disponible.")
        print("   Uploadez weights.bin pour une analyse complète des poids.\n")
        print("─" * 80 + "\n")
    
    # Résumé final
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 32 + "ANALYSE TERMINÉE" + " " * 30 + "║")
    print("╚" + "═" * 78 + "╝")
    
    print("\n📋 RÉSUMÉ:")
    print(f"  • Métadonnées analysées: {'✓' if files_present['metadata'] else '✗'}")
    print(f"  • Architecture analysée: {'✓' if files_present['model'] else '✗'}")
    print(f"  • Poids analysés: {'✓' if files_present['weights'] else '✗'}")
    
    print("\n💡 PROCHAINES ÉTAPES POSSIBLES:")
    print("  1. Charger le modèle avec TensorFlow.js pour faire des prédictions")
    print("  2. Convertir le modèle pour l'utiliser avec Python/TensorFlow")
    print("  3. Analyser les performances du modèle sur un jeu de test")
    print("  4. Fine-tuner le modèle avec de nouvelles données")
    
    if not files_present['weights']:
        print("\n⚠️  N'oubliez pas d'uploader weights.bin pour une analyse complète!")
    
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()
