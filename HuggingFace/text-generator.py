text_generator = pipeline("text-generation", model="gpt2")

prompt = "Dans un futur proche, les voitures volantes"
generated = text_generator(prompt, max_length=50, num_return_sequences=1)

print(generated[0]['generated_text'])
