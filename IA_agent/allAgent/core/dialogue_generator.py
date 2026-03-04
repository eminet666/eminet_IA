# core/dialogue_generator.py
# Moteur générique de génération de dialogue — toutes les langues

from datetime import datetime
import re


def generate_dialogue(client, lang):
    """
    Génère un dialogue via Mistral AI à partir de la config de langue.
    Si lang.GRAMMAR_TOPICS existe (niveaux C), injecte un thème de grammaire
    indépendant du dialogue. Sinon, le point de grammaire est tiré du dialogue.
    """
    sujet = lang.TOPICS[datetime.now().day % len(lang.TOPICS)]

    # ── Thème de grammaire : indépendant (niveau C) ou lié au dialogue ──
    prompt_args = dict(
        sujet         = sujet,
        level         = lang.LEVEL,
        context       = lang.CONTEXT,
        grammar_focus = lang.GRAMMAR_FOCUS,
        vocab_header  = lang.VOCAB_HEADER,
        vocab_col1    = lang.VOCAB_COL1,
    )

    if hasattr(lang, "GRAMMAR_TOPICS") and lang.GRAMMAR_TOPICS:
        grammar_topic = lang.GRAMMAR_TOPICS[datetime.now().timetuple().tm_yday % len(lang.GRAMMAR_TOPICS)]
        prompt_args["grammar_topic"] = grammar_topic

    prompt = lang.PROMPT_TEMPLATE.format(**prompt_args)

    response = client.chat.complete(
        model    = "mistral-small-latest",
        messages = [{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def extract_title(html_content):
    """Extrait le titre depuis la balise <h3>"""
    match = re.search(r'<h3>(.*?)</h3>', html_content, re.IGNORECASE | re.DOTALL)
    if match:
        return re.sub(r'<[^>]+>', '', match.group(1)).strip()
    return None


def extract_dialogue_lines(html_content, lang):
    """
    Extrait les répliques du dialogue pour les personnages définis dans lang.CHARACTERS.
    """
    speakers      = list(lang.CHARACTERS.keys())
    pattern_names = "|".join(re.escape(s) for s in speakers)
    pattern       = rf'<p><strong>({pattern_names}):</strong>\s*(.*?)</p>'
    lines         = []

    for speaker, text in re.findall(pattern, html_content, re.IGNORECASE | re.DOTALL):
        clean = re.sub(r'<[^>]+>', '', text).strip()
        name  = next((s for s in speakers if s.lower() == speaker.lower()), speaker)
        lines.append((name, clean))

    return lines
