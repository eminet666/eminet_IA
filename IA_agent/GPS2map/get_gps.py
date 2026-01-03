import csv
import requests
import time
import sys
import os

# === Vérifier les arguments ===
if len(sys.argv) < 3:
    print("Usage : python geocode_osm.py <fichier_entree.csv> <fichier_sortie.csv>")
    sys.exit(1)

INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]

# Définir le séparateur CSV ("," ou ";")
SEPARATOR = ","  # Modifier si nécessaire

# === Fonction pour géocoder via Nominatim OSM ===
def geocode_osm(place_name, island):
    query = f"{place_name}, {island}, Greece"
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": query, "format": "json", "limit": 1}
    headers = {"User-Agent": "GeoCSV-Script/1.0"}
    try:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        if data:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            return lat, lon, "exact"
        else:
            return None, None, "not_found"
    except Exception as e:
        print(f"Erreur pour {place_name}: {e}")
        return None, None, "error"

# === Lire le fichier d'entrée ===
rows = []
with open(INPUT_FILE, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=SEPARATOR)
    for row in reader:
        name = row['Nom']
        island = row['Ile']
        print(f"Recherche coordonnées pour : {name} ({island})")
        lat, lon, precision = geocode_osm(name, island)
        row['Latitude'] = lat
        row['Longitude'] = lon
        row['Precision'] = precision
        rows.append(row)
        time.sleep(1)  # Pause pour respecter Nominatim (1 req/sec max)

# === Écrire le nouveau CSV ===
fieldnames = list(rows[0].keys())
with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"\nTerminé ! Fichier sauvegardé : {OUTPUT_FILE}")
