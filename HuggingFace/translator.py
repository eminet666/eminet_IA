translator = pipeline("translation_en_to_fr")

result = translator("Hello world! Hugging Face makes NLP easy.")
print(result[0]['translation_text'])