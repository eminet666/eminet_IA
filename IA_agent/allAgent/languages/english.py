# languages/english.py
# ============================================================
# Configuration ANGLAISE — tous les paramètres propres à l'anglais
# ============================================================

EMAIL_RECIPIENTS = [
    "ebardet02@gmail.com"
]

LEVEL = "A2"
AUDIO_RATE = "-25%"
PAUSE_DURATION = 1000

ACCENT_COLOR  = "#cf142b"
AGENT_PREFIX  = "engAgent"
OUTPUT_PREFIX = "dialogue_anglais"
VOCAB_HEADER  = "Vocabulary"
VOCAB_COL1    = "English"

CHARACTERS = {
    "Jack":  {"voice": "en-GB-RyanNeural"},
    "Emily": {"voice": "en-GB-SoniaNeural"},
}

CONTEXT = """
CHARACTER CONTEXT:
- Jack and Emily are two British friends living in London
- Natural, warm and encouraging tone — suitable for a beginner learner
"""

GRAMMAR_FOCUS = """
RÈGLES STRICTES POUR LE CHOIX DES MOTS :
1. Sélectionne uniquement les mots utiles et un peu difficiles du dialogue — pas les mots ultra-basiques
2. Pour les VERBES : donner l'infinitif + le past simple
   Exemple : <strong>to go → went</strong>, <strong>to buy → bought</strong>, <strong>to say → said</strong>
3. Pour les NOMS : inclure l'article défini (a / an / the)
   Exemple : <strong>the market</strong>, <strong>a shop</strong>
4. Pour les expressions utiles : les donner telles quelles
   Exemple : <strong>How much is it?</strong>, <strong>I would like...</strong>, <strong>What about you?</strong>
5. AUCUNE REDONDANCE : chaque mot ou expression une seule fois
6. Environ 20-25 entrées, toutes issues du dialogue
"""

TOPICS = [
    "Introducing yourself and your family",
    "Ordering food and drinks at a café",
    "Shopping at the supermarket",
    "Asking for directions in the city",
    "Talking about weekend activities",
    "Describing your home or flat",
    "Talking about the weather",
    "Buying clothes in a shop",
    "Taking public transport",
    "Booking a hotel room",
    "Talking about favourite music",
    "A typical day at work or school",
    "Talking about holiday plans",
    "At the doctor's",
    "A day at the beach",
    "Favourite sports and hobbies",
    "Cooking a meal together",
    "A birthday party",
    "At the bank",
    "Talking about British traditions",
    "Visiting a museum in London",
    "A walk in the countryside",
    "Christmas traditions in the UK",
    "Talking about daily routine",
    "A picnic in the park",
    "Visiting Buckingham Palace",
    "A trip to Edinburgh",
    "A night at the theatre",
    "Planning a road trip in England",
    "Talking about dreams and ambitions",
]

PROMPT_TEMPLATE = """
Create a dialogue in English (level {level}) between Jack and Emily,
on the following topic: {sujet}

{context}

LANGUAGE RULES FOR LEVEL {level}:
- Simple everyday vocabulary, short sentences
- Tenses: present simple, present continuous, past simple, going to
- No subjunctive, no complex conditionals
- Natural and useful everyday expressions

The dialogue should be around 400-500 words.

FORMATTING:
- Title in English: <h3>Title in English</h3>
- Each line: <p><strong>Name:</strong> text</p>
- Example: <p><strong>Jack:</strong> Hi Emily! How are you?</p>

VOCABULARY:
After the dialogue, add a "{vocab_header}" section with an HTML table.
Columns: {vocab_col1} | French translation | Example

{grammar_focus}

<table class="vocab-table">
  <thead><tr><th>{vocab_col1}</th><th>French</th><th>Example</th></tr></thead>
  <tbody><tr><td><strong>word</strong></td><td>translation</td><td>example</td></tr></tbody>
</table>

GRAMMAR POINT:
After the vocabulary, identify ONE grammar structure present in the dialogue
suitable for level {level} (e.g. present continuous, past simple irregular verbs,
countable/uncountable nouns, prepositions of place...).
Add a "Grammar" section in this format:

<div class="grammar-box">
  <h3>Grammar : [name of the point in English — French translation]</h3>
  <p class="grammar-intro">[Clear explanation in French, 2-3 sentences maximum]</p>

  <table class="grammar-table">
    <thead><tr><th>Form</th><th>Example in English</th><th>French translation</th></tr></thead>
    <tbody>
      <tr><td>...</td><td>...</td><td>...</td></tr>
    </tbody>
  </table>

  <p><strong>Examples from the dialogue:</strong></p>
  <ul>
    <li>[sentence from the dialogue in English] — [French translation]</li>
    <li>[sentence from the dialogue in English] — [French translation]</li>
  </ul>
</div>
"""
