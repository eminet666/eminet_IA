import pandas as pd
import folium
import sys
from pathlib import Path

# Arguments
if len(sys.argv) != 3:
    print("Usage: python generate_folium_map.py <csv> <html>")
    sys.exit(1)

CSV_FILE = sys.argv[1]
HTML_FILE = sys.argv[2]

CATEGORY_COLORS = {"Archeologie": "red", "Eglise": "blue", "Chapelle": "green"}

df = pd.read_csv(CSV_FILE)
center_lat = df["Latitude"].mean()
center_lng = df["Longitude"].mean()

# Carte interactive avec numéros VISIBLES
m = folium.Map(location=[center_lat, center_lng], zoom_start=11)

for idx, row in df.iterrows():
    num = idx + 1
    categorie = row["Categorie"]
    color = CATEGORY_COLORS.get(categorie, "purple")
    
    popup_html = f"""
    <div style="min-width:250px">
        <b>{row['Nom']}</b><br>
        – {row['Lumiere idéale']}<br>
        – {row['Remarques']}
    </div>
    """
    
    # Numéro VISIBLE dans cercle coloré
    html_num = f"""
    <div style="
        background-color: {color}; 
        width: 32px; height: 32px; 
        border-radius: 50%; 
        border: 3px solid white; 
        color: white; 
        font-weight: bold; 
        font-size: 16px; 
        text-align: center; 
        line-height: 26px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    ">{num}</div>
    """
    
    folium.Marker(
        [row["Latitude"], row["Longitude"]],
        popup=folium.Popup(popup_html, max_width=280),
        tooltip=f"{num} - {row['Nom']}",
        icon=folium.DivIcon(html=html_num)
    ).add_to(m)

m.save(HTML_FILE)
print(f"Carte HTML avec numéros générée : {HTML_FILE}")
print("Ouvrir dans navigateur pour voir fond OpenStreetMap + numéros colorés !")
