// ==================== INITIALISATION ====================

// Message de bienvenue au chargement
window.addEventListener('DOMContentLoaded', function() {
    const welcomeMsg = 'Χαίρε! Είμαι ο Σωκράτης - ναι, εκείνος με τα σανδάλια. ' +
                       'Ζω εδώ στην Αθήνα, κοντά στην Ακρόπολη. ' +
                       'Πώς θα μπορούσα να σε βοηθήσω σήμερα; ' +
                       'Ή μήπως πρέπει πρώτα να ρωτήσω: τι σημαίνει βοήθεια για σένα;';
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