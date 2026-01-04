// ==================== INITIALISATION ====================

// Message de bienvenue au chargement
window.addEventListener('DOMContentLoaded', function() {
    const welcomeMsg = 'Χαίρε! Είμαι ο Σωκράτης 2.0, και ναι, ακόμα φοράω σανδάλια. ' +
                       'Πώς θα μπορούσα να σε βοηθήσω σήμερα; ' +
                       'Ω μήπως πρώτα θα έπρεπε να ρωτήσω: τι σημαίνει βοήθεια για σένα;';
    addMessage(welcomeMsg, false, []);
    userInput.focus();
});

// Event listeners
sendBtn.addEventListener('click', sendMessage);
micBtn.addEventListener('click', toggleRecording);
emailBtn.addEventListener('click', emailPDF);

userInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !sendBtn.disabled) {
        sendMessage();
    }
});