from mistralai import Mistral

# Remplacez par votre vraie clé API
api_key = "WDgXqzGTKhbMFtV90HdEFFrofkKlxVt3"

client = Mistral(api_key=api_key)

try:
    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": "Dis bonjour en grec"}]
    )
    print("✅ Clé API valide !")
    print("Réponse:", response.choices[0].message.content)
except Exception as e:
    print("❌ Erreur:", str(e))