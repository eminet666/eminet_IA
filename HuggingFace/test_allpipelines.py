from transformers import pipeline

def main():
    print("Bienvenue dans le mini-guide Hugging Face !")
    print("Choisissez une option :")
    print("1. Analyse de sentiment")
    print("2. Génération de texte")
    print("3. Traduction anglais -> français")
    print("4. Reconnaissance d'entités nommées (NER)")
    print("0. Quitter")

    choice = input("Votre choix : ")

    if choice == "1":
        sentiment_analyzer = pipeline("sentiment-analysis")
        text = input("Entrez un texte à analyser : ")
        result = sentiment_analyzer(text)
        print("Résultat :", result)

    elif choice == "2":
        text_generator = pipeline("text-generation", model="gpt2")
        prompt = input("Entrez un prompt pour générer du texte : ")
        generated = text_generator(prompt, max_length=50, num_return_sequences=1)
        print("Texte généré :", generated[0]['generated_text'])

    elif choice == "3":
        translator = pipeline("translation_en_to_fr")
        text = input("Entrez un texte en anglais à traduire : ")
        result = translator(text)
        print("Traduction :", result[0]['translation_text'])

    elif choice == "4":
        ner_pipeline = pipeline("ner", grouped_entities=True)
        text = input("Entrez un texte pour la reconnaissance d'entités : ")
        entities = ner_pipeline(text)
        print("Entités reconnues :")
        for entity in entities:
            print(entity)

    elif choice == "0":
        print("Au revoir !")
        return

    else:
        print("Choix invalide.")

    print("\n----------------------------\n")
    main()  # relance le menu

if __name__ == "__main__":
    main()
