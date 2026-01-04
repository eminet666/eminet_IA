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
    recognition.interimResults = false;
    
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        userInput.value = transcript;
        isRecording = false;
        micBtn.classList.remove('recording');
        sendMessage();
    };
    
    recognition.onerror = function(event) {
        console.error('Erreur reconnaissance vocale:', event.error);
        isRecording = false;
        micBtn.classList.remove('recording');
        if (event.error === 'no-speech') {
            alert('Aucune parole détectée. Réessayez.');
        }
    };
    
    recognition.onend = function() {
        isRecording = false;
        micBtn.classList.remove('recording');
    };
}

// ==================== ENREGISTREMENT MOBILE (iOS/Safari) ====================

async function startMobileRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
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
            const audioBlob = new Blob(audioChunks, { type: mediaRecorder.mimeType });
            
            const reader = new FileReader();
            reader.onloadend = async function() {
                const base64Audio = reader.result;
                
                try {
                    const response = await fetch('/transcribe', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ audio: base64Audio })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        userInput.value = data.text;
                        sendMessage();
                    } else {
                        alert('Erreur de transcription: ' + (data.error || 'Inconnu'));
                    }
                } catch (error) {
                    console.error('Transcription error:', error);
                    alert('Erreur lors de la transcription');
                }
            };
            reader.readAsDataURL(audioBlob);
            
            stream.getTracks().forEach(track => track.stop());
        };
        
        mediaRecorder.start();
        isRecording = true;
        micBtn.classList.add('recording');
        
    } catch (error) {
        console.error('Erreur micro:', error);
        alert('Impossible d\'accéder au microphone: ' + error.message);
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
    }
}

// ==================== SYNTHÈSE VOCALE (TEXT-TO-SPEECH) ====================

function speakText(text) {
    if (!('speechSynthesis' in window)) {
        alert('Synthèse vocale non supportée.');
        return;
    }
    
    window.speechSynthesis.cancel();
    
    // Nettoyer le texte des emojis
    const cleanText = text.replace(/[🔊🇫🇷🎤➤😉!.…]/g, ' ').trim();
    
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