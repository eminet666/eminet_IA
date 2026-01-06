// ==================== RECONNAISSANCE VOCALE ====================

let recognition = null;
let isRecording = false;
let mediaRecorder = null;
let audioChunks = [];

// Initialiser la reconnaissance vocale (Desktop)
if (!isIOS && ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.lang = 'el-GR';
    recognition.continuous = false;
    recognition.interimResults = true; // Afficher les résultats intermédiaires
    recognition.maxAlternatives = 3; // Plus d'alternatives pour améliorer la précision
    
    recognition.onresult = function(event) {
        let interimTranscript = '';
        let finalTranscript = '';
        
        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript;
            } else {
                interimTranscript += transcript;
            }
        }
        
        // Afficher les résultats intermédiaires
        if (interimTranscript) {
            userInput.value = interimTranscript;
            userInput.style.color = '#999'; // Gris pour indiquer que c'est temporaire
        }
        
        // Résultat final
        if (finalTranscript) {
            userInput.value = finalTranscript;
            userInput.style.color = ''; // Couleur normale
            isRecording = false;
            micBtn.classList.remove('recording');
            // Ne pas envoyer automatiquement - laisser l'utilisateur vérifier
            userInput.focus();
        }
    };
    
    recognition.onerror = function(event) {
        console.error('Erreur reconnaissance vocale:', event.error);
        isRecording = false;
        micBtn.classList.remove('recording');
        userInput.style.color = '';
        
        if (event.error === 'no-speech') {
            alert('Aucune parole détectée. Parlez plus fort ou rapprochez-vous du micro.');
        } else if (event.error === 'audio-capture') {
            alert('Erreur micro. Vérifiez les permissions.');
        } else if (event.error === 'network') {
            alert('Erreur réseau. Vérifiez votre connexion.');
        }
    };
    
    recognition.onend = function() {
        isRecording = false;
        micBtn.classList.remove('recording');
        userInput.style.color = '';
    };
}

// ==================== ENREGISTREMENT MOBILE (iOS/Safari) ====================

async function startMobileRecording() {
    try {
        // Afficher un message de feedback
        userInput.value = '🎤 Enregistrement en cours...';
        userInput.style.color = '#ff4444';
        
        const stream = await navigator.mediaDevices.getUserMedia({ 
            audio: {
                echoCancellation: true,
                noiseSuppression: true,
                autoGainControl: true,
                sampleRate: 48000 // Meilleure qualité audio
            } 
        });
        
        const options = { mimeType: 'audio/webm' };
        if (!MediaRecorder.isTypeSupported(options.mimeType)) {
            options.mimeType = 'audio/mp4';
        }
        
        mediaRecorder = new MediaRecorder(stream, options);
        audioChunks = [];
        
        mediaRecorder.ondataavailable = function(event) {
            audioChunks.push(event.data);
        };
        
        mediaRecorder.onstop = async function() {
            userInput.value = '⏳ Transcription en cours...';
            
            const audioBlob = new Blob(audioChunks, { type: mediaRecorder.mimeType });
            
            const reader = new FileReader();
            reader.onloadend = async function() {
                const base64Audio = reader.result;
                
                try {
                    const response = await fetch('/transcribe', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ 
                            audio: base64Audio,
                            prompt: 'Transcription en grec moderne, niveau C1. Mots courants: φιλοσοφία, σοφία, αρετή, γνώση' // Aide à la reconnaissance
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        userInput.value = data.text;
                        userInput.style.color = '#4CAF50'; // Vert pour indiquer succès
                        // Ne pas envoyer automatiquement - laisser l'utilisateur vérifier
                        userInput.focus();
                        
                        // Remettre la couleur normale après 2 secondes
                        setTimeout(() => {
                            userInput.style.color = '';
                        }, 2000);
                    } else {
                        userInput.value = '';
                        userInput.style.color = '';
                        alert('Erreur de transcription: ' + (data.error || 'Inconnu'));
                    }
                } catch (error) {
                    console.error('Transcription error:', error);
                    userInput.value = '';
                    userInput.style.color = '';
                    alert('Erreur lors de la transcription. Vérifiez votre connexion.');
                }
            };
            reader.readAsDataURL(audioBlob);
            
            stream.getTracks().forEach(track => track.stop());
        };
        
        mediaRecorder.start();
        isRecording = true;
        micBtn.classList.add('recording');
        
        // Auto-stop après 10 secondes maximum
        setTimeout(() => {
            if (isRecording && mediaRecorder && mediaRecorder.state === 'recording') {
                stopMobileRecording();
            }
        }, 10000);
        
    } catch (error) {
        console.error('Erreur micro:', error);
        userInput.value = '';
        userInput.style.color = '';
        
        if (error.name === 'NotAllowedError') {
            alert('Permission micro refusée. Autorisez l\'accès au micro dans les paramètres de votre navigateur.');
        } else {
            alert('Impossible d\'accéder au microphone: ' + error.message);
        }
    }
}

function stopMobileRecording() {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        isRecording = false;
        micBtn.classList.remove('recording');
    }
}

// ==================== TOGGLE ENREGISTREMENT ====================

function toggleRecording() {
    // Sur iOS/mobile, utiliser MediaRecorder + Groq
    if (isIOS || !recognition) {
        if (isRecording) {
            stopMobileRecording();
        } else {
            startMobileRecording();
        }
        return;
    }
    
    // Sur desktop, utiliser Web Speech API
    if (isRecording) {
        recognition.stop();
    } else {
        recognition.start();
        isRecording = true;
        micBtn.classList.add('recording');
        userInput.value = '🎤 Parlez maintenant...';
        userInput.style.color = '#ff4444';
    }
}

// ==================== SYNTHÈSE VOCALE (TEXT-TO-SPEECH) ====================

/**
 * Lire un texte avec Edge TTS (via serveur)
 * Fallback vers Web Speech API si Edge TTS n'est pas disponible
 */
async function speakText(text) {
    try {
        // Essayer d'abord avec Edge TTS
        const response = await fetch('/speak', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });
        
        const data = await response.json();
        
        if (data.success && data.audio) {
            // Décoder et jouer l'audio MP3
            const audioData = atob(data.audio);
            const arrayBuffer = new ArrayBuffer(audioData.length);
            const view = new Uint8Array(arrayBuffer);
            for (let i = 0; i < audioData.length; i++) {
                view[i] = audioData.charCodeAt(i);
            }
            
            const blob = new Blob([arrayBuffer], { type: 'audio/mp3' });
            const audioUrl = URL.createObjectURL(blob);
            const audio = new Audio(audioUrl);
            
            audio.onended = function() {
                URL.revokeObjectURL(audioUrl);
            };
            
            audio.play();
            return;
        }
    } catch (error) {
        console.warn('Edge TTS non disponible, fallback vers Web Speech API:', error);
    }
    
    // Fallback vers Web Speech API
    speakTextFallback(text);
}

/**
 * Fallback : Synthèse vocale avec Web Speech API
 */
function speakTextFallback(text) {
    if (!('speechSynthesis' in window)) {
        alert('Synthèse vocale non supportée.');
        return;
    }
    
    window.speechSynthesis.cancel();
    
    // Nettoyer le texte des emojis
    const cleanText = text.replace(/[🔊🇫🇷🎤➤😉!.…⏳]/g, ' ').trim();
    
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = 'el-GR';
    utterance.rate = SPEECH_RATE;
    utterance.pitch = 0.8; // Voix plus grave (Socrate)
    utterance.volume = 1;
    
    // Charger les voix et sélectionner une voix grecque masculine si possible
    if (window.speechSynthesis.getVoices().length === 0) {
        window.speechSynthesis.onvoiceschanged = function() {
            const voices = window.speechSynthesis.getVoices();
            let greekVoice = voices.find(v => v.lang.startsWith('el') && v.name.toLowerCase().includes('male'));
            if (!greekVoice) {
                greekVoice = voices.find(v => v.lang.startsWith('el'));
            }
            if (greekVoice) {
                utterance.voice = greekVoice;
            }
            window.speechSynthesis.speak(utterance);
        };
    } else {
        const voices = window.speechSynthesis.getVoices();
        let greekVoice = voices.find(v => v.lang.startsWith('el') && v.name.toLowerCase().includes('male'));
        if (!greekVoice) {
            greekVoice = voices.find(v => v.lang.startsWith('el'));
        }
        if (greekVoice) {
            utterance.voice = greekVoice;
            console.log('Voix sélectionnée:', greekVoice.name);
        }
        window.speechSynthesis.speak(utterance);
    }
}