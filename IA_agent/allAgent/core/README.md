

### arborescence
IA_agent/
│
├── config.py                        ← mise en page PDF uniquement
│
├── core/                            ← moteur commun, ne change jamais
│   ├── main.py                      ← point d'entrée : python core/main.py greek
│   ├── dialogue_generator.py
│   ├── audio_generator.py
│   ├── pdf_generator.py
│   └── email_sender.py
│
├── languages/                       ← 1 fichier par langue, tout y est
│   ├── greek.py                     ← EMAIL_RECIPIENTS, LEVEL, AUDIO_RATE...
│   ├── italian.py
│   ├── spanish.py
│   └── english.py
│
└── .github/workflows/
    ├── daily_greek.yml              ← cron 6h → python core/main.py greek
    ├── daily_italian.yml            ← cron 7h → python core/main.py italian
    ├── daily_spanish.yml            ← cron 8h → python core/main.py spanish
    └── daily_english.yml            ← cron 9h → python core/main.py english