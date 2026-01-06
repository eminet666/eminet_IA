// ==================== GÉNÉRATION PDF AVEC PDFMAKE ====================

/**
 * Générer un PDF avec la conversation et le vocabulaire enrichi
 * @returns {Promise<Blob|null>} Le blob PDF généré ou null
 */
async function generatePDF() {
    if (chatBox.children.length === 0) {
        alert('Aucune conversation à exporter !');
        return null;
    }
    
    try {
        // 1. Enrichir le vocabulaire avec exemples et conjugaisons
        const uniqueWords = [...new Set(allVocabulary.map(v => v.word))];
        let enrichedVocab = [];
        
        if (uniqueWords.length > 0) {
            const vocabResponse = await fetch('/enrich-vocabulary', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ words: uniqueWords })
            });
            
            const vocabData = await vocabResponse.json();
            if (vocabData.success) {
                enrichedVocab = vocabData.words;
            }
        }
        
        // 2. Construire le contenu du PDF
        const content = [];
        
        // En-tête
        content.push({
            text: '🇬🇷 Conversation avec Σωκράτης 2.0',
            style: 'header',
            alignment: 'center',
            margin: [0, 0, 0, 10]
        });
        
        // Date
        const dateStr = new Date().toLocaleDateString('fr-FR', { 
            weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' 
        });
        content.push({
            text: dateStr,
            style: 'date',
            alignment: 'center',
            margin: [0, 0, 0, 20]
        });
        
        // Messages
        const messages = chatBox.querySelectorAll('.message');
        
        messages.forEach(function(msg) {
            const isUser = msg.classList.contains('user');
            const textEl = msg.querySelector('.message-text');
            const text = textEl ? textEl.textContent.trim() : '';
            
            if (!text) return;
            
            // Label
            content.push({
                text: isUser ? 'Vous:' : 'Σωκράτης:',
                style: isUser ? 'userLabel' : 'botLabel',
                margin: [0, 10, 0, 3]
            });
            
            // Texte du message
            content.push({
                text: text,
                style: 'message',
                margin: [10, 0, 0, 5]
            });
        });
        
        // Section vocabulaire
        if (enrichedVocab.length > 0) {
            content.push({
                text: '📚 Vocabulaire de la session',
                style: 'vocabHeader',
                margin: [0, 30, 0, 10],
                pageBreak: 'before'
            });
            
            content.push({
                canvas: [
                    {
                        type: 'line',
                        x1: 0, y1: 0,
                        x2: 515, y2: 0,
                        lineWidth: 2,
                        lineColor: '#6674EA'
                    }
                ],
                margin: [0, 0, 0, 15]
            });
            
            // Chaque mot en format compact
            enrichedVocab.forEach(function(word, index) {
                const wordContent = [];
                
                // Format compact sur une ligne
                let compactLine = '';
                
                if (word.verb_forms) {
                    // Format verbe: présent/aoriste = traduction, exemple
                    compactLine = `${word.verb_forms} = ${word.translation}, ${word.example}`;
                } else {
                    // Format nom/adjectif: mot = traduction, exemple
                    compactLine = `${word.word} = ${word.translation}, ${word.example}`;
                }
                
                wordContent.push({
                    text: compactLine,
                    style: 'vocabCompact',
                    margin: [0, index > 0 ? 8 : 0, 0, 0]
                });
                
                content.push(...wordContent);
            });
        }
        
        // 3. Définir le document
        const docDefinition = {
            content: content,
            styles: {
                header: {
                    fontSize: 20,
                    bold: true,
                    color: '#6674EA'
                },
                date: {
                    fontSize: 10,
                    color: '#666666'
                },
                userLabel: {
                    fontSize: 10,
                    bold: true,
                    color: '#6674EA'
                },
                botLabel: {
                    fontSize: 10,
                    bold: true,
                    color: '#464646'
                },
                message: {
                    fontSize: 11,
                    color: '#323232'
                },
                vocabHeader: {
                    fontSize: 16,
                    bold: true,
                    color: '#6674EA'
                },
                vocabCompact: {
                    fontSize: 10,
                    color: '#323232'
                }
            },
            defaultStyle: {
                font: 'Roboto'
            },
            pageMargins: [40, 40, 40, 40]
        };
        
        // 4. Créer le PDF et retourner un Blob
        return new Promise((resolve, reject) => {
            try {
                const pdfDocGenerator = pdfMake.createPdf(docDefinition);
                pdfDocGenerator.getBlob((blob) => {
                    resolve(blob);
                });
            } catch (error) {
                reject(error);
            }
        });
        
    } catch (error) {
        console.error('Erreur génération PDF:', error);
        throw error;
    }
}

// ==================== TÉLÉCHARGEMENT PDF ====================

/**
 * Générer et télécharger le PDF directement
 */
async function emailPDF() {
    emailBtn.disabled = true;
    emailBtn.textContent = 'Génération...';
    
    try {
        // 1. Générer le PDF
        const pdfBlob = await generatePDF();
        if (!pdfBlob) return;
        
        // 2. Télécharger directement
        const url = URL.createObjectURL(pdfBlob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `Socrate_${new Date().toISOString().split('T')[0]}.pdf`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        alert('✅ PDF téléchargé !');
        
    } catch (error) {
        console.error('Erreur:', error);
        alert('❌ Erreur: ' + error.message);
    } finally {
        emailBtn.disabled = false;
        emailBtn.textContent = 'PDF';
    }
}