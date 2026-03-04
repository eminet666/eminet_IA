# languages/english.py
# ============================================================
# Configuration ANGLAISE — tous les paramètres propres à l'anglais
# ============================================================

# ── Paramètres modifiables facilement ───────────────────────

EMAIL_RECIPIENTS = [
    "eminet666@gmail.com",
]

LEVEL = "A2"

AUDIO_RATE = "-25%"

PAUSE_DURATION = 1000

# ── Identité de l'agent ──────────────────────────────────────
ACCENT_COLOR  = "#cf142b"
AGENT_PREFIX  = "engAgent"
OUTPUT_PREFIX = "dialogue_anglais"
VOCAB_HEADER  = "Vocabulary"
VOCAB_COL1    = "English"

# ── Personnages et voix ──────────────────────────────────────
CHARACTERS = {
    "Jack":  {"voice": "en-GB-RyanNeural"},
    "Emily": {"voice": "en-GB-SoniaNeural"},
}

# ── Contexte narratif ────────────────────────────────────────
CONTEXT = """
CHARACTER CONTEXT:
- Jack and Emily are two British friends living in London
- Natural, warm and encouraging tone — suitable for a beginner learner
"""

# ── Focus grammatical ────────────────────────────────────────
GRAMMAR_FOCUS = """
VOCABULARY RULES (level A2):
1. Useful or slightly tricky words only — not ultra-basic ones
2. For VERBS: infinitive + past simple form
   Example: to go -> went, to buy -> bought, to say -> said
3. For NOUNS: include the article (a/an/the) where relevant
4. For useful EXPRESSIONS: give them as they appear
   Example: How much is it?, I would like..., What about you?
5. NO REPETITION: each word or expression only once
6. Around 20-25 entries from the dialogue
"""

# ── Sujets ───────────────────────────────────────────────────
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

# ── Prompt ───────────────────────────────────────────────────
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
"""
