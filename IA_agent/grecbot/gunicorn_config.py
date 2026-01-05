"""
Configuration Gunicorn pour Render
Augmente le timeout pour l'envoi d'emails
"""

# Timeout pour les workers (en secondes)
timeout = 120  # 2 minutes pour l'envoi d'emails

# Nombre de workers (recommandé : 2-4 workers pour Render)
workers = 2

# Bind
bind = "0.0.0.0:10000"

# Logs
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Worker class
worker_class = "sync"

# Graceful timeout
graceful_timeout = 120