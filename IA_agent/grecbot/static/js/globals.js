// ==================== VARIABLES GLOBALES ====================

// Éléments DOM
const chatBox = document.getElementById('chatBox');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const micBtn = document.getElementById('micBtn');
const loading = document.getElementById('loading');
const emailBtn = document.getElementById('emailBtn');

// Configuration
const SPEECH_RATE = 0.8; // Vitesse de lecture vocale (ajustable)

// État de l'application
let allVocabulary = []; // Stockage du vocabulaire de toute la session

// Détection iOS
const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) || 
              (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);

// ==================== FONCTIONS UTILITAIRES ====================

/**
 * Afficher/masquer l'indicateur de chargement
 */
function showLoading(show) {
    loading.style.display = show ? 'block' : 'none';
    if (show) {
        chatBox.appendChild(loading);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

/**
 * Fermer tous les tooltips de vocabulaire
 */
function closeAllTooltips() {
    document.querySelectorAll('.vocab-word.show-tooltip').forEach(function(w) {
        w.classList.remove('show-tooltip');
    });
}

// Fermer les tooltips en cliquant ailleurs
document.addEventListener('click', closeAllTooltips);