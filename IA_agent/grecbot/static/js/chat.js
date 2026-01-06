// ==================== GESTION DES MESSAGES ====================

/**
 * Ajouter un message dans le chat
 * @param {string} content - Contenu du message
 * @param {boolean} isUser - true si message de l'utilisateur
 * @param {Array} vocabulary - Liste des mots de vocabulaire (optionnel)
 */
function addMessage(content, isUser, vocabulary) {
    vocabulary = vocabulary || [];
    
    const messageDiv = document.createElement('div');
    messageDiv.className = isUser ? 'message user' : 'message bot';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';
    
    // Enrichir avec vocabulaire si message du bot
    if (!isUser && vocabulary.length > 0) {
        const words = content.split(/\s+/);
        const vocabMap = new Map();
        vocabulary.forEach(function(v) {
            vocabMap.set(v.word.toLowerCase(), v.translation);
        });
        
        words.forEach(function(word, index) {
            const cleanWord = word.replace(/[.,;:!?""]/g, '').toLowerCase();
            
            if (vocabMap.has(cleanWord)) {
                const vocabSpan = document.createElement('span');
                vocabSpan.className = 'vocab-word';
                vocabSpan.textContent = word;
                
                const tooltip = document.createElement('span');
                tooltip.className = 'vocab-tooltip';
                tooltip.textContent = vocabMap.get(cleanWord);
                vocabSpan.appendChild(tooltip);
                
                vocabSpan.addEventListener('click', function(e) {
                    e.stopPropagation();
                    document.querySelectorAll('.vocab-word.show-tooltip').forEach(function(w) {
                        if (w !== vocabSpan) w.classList.remove('show-tooltip');
                    });
                    vocabSpan.classList.toggle('show-tooltip');
                });
                
                textDiv.appendChild(vocabSpan);
            } else {
                textDiv.appendChild(document.createTextNode(word));
            }
            
            if (index < words.length - 1) {
                textDiv.appendChild(document.createTextNode(' '));
            }
        });
    } else {
        textDiv.textContent = content;
    }
    
    contentDiv.appendChild(textDiv);
    
    // Ajouter les boutons d'action pour les messages du bot
    if (!isUser) {
        const actionsDiv = document.createElement('div');
        actionsDiv.className = 'message-actions';
        
        const speakBtn = document.createElement('button');
        speakBtn.className = 'btn-icon';
        speakBtn.textContent = '🔊';
        speakBtn.title = 'Écouter';
        speakBtn.onclick = function() { speakText(content); };
        
        const translateBtn = document.createElement('button');
        translateBtn.className = 'btn-icon';
        translateBtn.textContent = '🇫🇷';
        translateBtn.title = 'Traduire en français';
        translateBtn.onclick = function() { translateText(content, messageDiv); };
        
        actionsDiv.appendChild(speakBtn);
        actionsDiv.appendChild(translateBtn);
        contentDiv.appendChild(actionsDiv);
    }
    
    messageDiv.appendChild(contentDiv);
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// ==================== TRADUCTION ====================

/**
 * Traduire un message en français
 */
async function translateText(text, messageElement) {
    const existingTranslation = messageElement.querySelector('.translation');
    if (existingTranslation) {
        existingTranslation.remove();
        return;
    }
    
    try {
        const response = await fetch('/translate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });
        
        const data = await response.json();
        
        if (data.success) {
            const translationDiv = document.createElement('div');
            translationDiv.className = 'translation';
            translationDiv.textContent = data.translation;
            messageElement.appendChild(translationDiv);
        } else {
            alert('Erreur de traduction');
        }
    } catch (error) {
        alert('Erreur: ' + error.message);
    }
}

// ==================== ENVOI DE MESSAGE ====================

/**
 * Envoyer un message au serveur
 */
async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;
    
    addMessage(message, true);
    userInput.value = '';
    
    // Réinitialiser la hauteur du textarea
    userInput.style.height = 'auto';
    
    sendBtn.disabled = true;
    showLoading(true);
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        showLoading(false);
        
        if (data.success) {
            const cleanResponse = String(data.response || '').trim();
            const cleanVocabulary = Array.isArray(data.vocabulary) ? data.vocabulary : [];
            
            // Stocker le vocabulaire pour l'export PDF
            cleanVocabulary.forEach(function(vocab) {
                if (!allVocabulary.find(v => v.word === vocab.word)) {
                    allVocabulary.push(vocab);
                }
            });
            
            addMessage(cleanResponse, false, cleanVocabulary);
        } else {
            addMessage('Σφάλμα: ' + (data.error || 'Κάτι πήγε στραβά'), false);
        }
    } catch (error) {
        showLoading(false);
        console.error('Error:', error);
        addMessage('Σφάλμα σύνδεσης: ' + error.message, false);
    } finally {
        sendBtn.disabled = false;
        userInput.focus();
    }
}