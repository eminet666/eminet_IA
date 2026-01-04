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
            
            // Chaque mot
            enrichedVocab.forEach(function(word, index) {
                const wordContent = [];
                
                // Mot grec
                wordContent.push({
                    text: word.word,
                    style: 'vocabWord',
                    margin: [0, index > 0 ? 15 : 0, 0, 3]
                });
                
                // Traduction
                wordContent.push({
                    text: '→ ' + word.translation,
                    style: 'vocabTranslation',
                    margin: [5, 0, 0, 3]
                });
                
                // Formes verbales
                if (word.verb_forms) {
                    wordContent.push({
                        text: '⚡ ' + word.verb_forms,
                        style: 'vocabVerb',
                        margin: [5, 0, 0, 3]
                    });
                }
                
                // Exemple
                if (word.example) {
                    wordContent.push({
                        text: '💬 ' + word.example,
                        style: 'vocabExample',
                        margin: [5, 0, 0, 2]
                    });
                    
                    // Traduction de l'exemple
                    if (word.example_translation) {
                        wordContent.push({
                            text: '   ' + word.example_translation,
                            style: 'vocabExampleTranslation',
                            margin: [10, 0, 0, 0]
                        });
                    }
                }
                
                content.push(...wordContent);
                
                // Séparateur
                if (index < enrichedVocab.length - 1) {
                    content.push({
                        canvas: [
                            {
                                type: 'line',
                                x1: 0, y1: 0,
                                x2: 515, y2: 0,
                                lineWidth: 0.5,
                                lineColor: '#DDDDDD'
                            }
                        ],
                        margin: [0, 8, 0, 0]
                    });
                }
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
                vocabWord: {
                    fontSize: 13,
                    bold: true,
                    color: '#323232'
                },
                vocabTranslation: {
                    fontSize: 11,
                    italics: true,
                    color: '#646464'
                },
                vocabVerb: {
                    fontSize: 11,
                    color: '#0066CC'
                },
                vocabExample: {
                    fontSize: 11,
                    color: '#505050'
                },
                vocabExampleTranslation: {
                    fontSize: 10,
                    color: '#787878'
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

// ==================== ENVOI PAR EMAIL ====================

/**
 * Générer le PDF et l'envoyer par email
 */
async function emailPDF() {
    emailBtn.disabled = true;
    emailBtn.innerHTML = '<span>⏳</span><span>Envoi...</span>';
    
    try {
        // 1. Générer le PDF
        const pdfBlob = await generatePDF();
        if (!pdfBlob) return;
        
        // 2. Extraire le dialogue pour le corps de l'email
        const messages = chatBox.querySelectorAll('.message');
        let dialogueText = '';
        
        messages.forEach(function(msg) {
            const isUser = msg.classList.contains('user');
            const textEl = msg.querySelector('.message-text');
            const text = textEl ? textEl.textContent.trim() : '';
            
            if (text) {
                if (isUser) {
                    dialogueText += `\nVous: ${text}\n`;
                } else {
                    dialogueText += `\nΣωκράτης: ${text}\n`;
                }
            }
        });
        
        // 3. Convertir le Blob en base64
        const reader = new FileReader();
        reader.onloadend = async function() {
            const pdfBase64 = reader.result;
            
            // 4. Envoyer par email
            try {
                const emailResponse = await fetch('/send-pdf-email', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        pdf: pdfBase64,
                        dialogue: dialogueText,
                        email: 'eminet666@gmail.com'
                    }),
                    signal: AbortSignal.timeout(120000)
                });
                
                if (!emailResponse.ok) {
                    const errorText = await emailResponse.text();
                    console.error('Erreur serveur:', errorText);
                    throw new Error(`Erreur serveur (${emailResponse.status})`);
                }
                
                const emailData = await emailResponse.json();
                
                if (emailData.success) {
                    alert('✅ PDF envoyé par email à eminet666@gmail.com !');
                } else {
                    throw new Error(emailData.error || 'Erreur inconnue');
                }
            } catch (emailError) {
                console.error('Erreur email:', emailError);
                
                const download = confirm(
                    '⚠️ Impossible d\'envoyer l\'email.\n\n' + 
                    emailError.message + 
                    '\n\nVoulez-vous télécharger le PDF localement ?'
                );
                
                if (download) {
                    // Télécharger le PDF
                    const url = URL.createObjectURL(pdfBlob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `Socrate_${new Date().toISOString().split('T')[0]}.pdf`;
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    URL.revokeObjectURL(url);
                    alert('✅ PDF téléchargé !');
                }
            } finally {
                emailBtn.disabled = false;
                emailBtn.innerHTML = '<span>📧</span><span>Email</span>';
            }
        };
        
        reader.readAsDataURL(pdfBlob);
        
    } catch (error) {
        console.error('Erreur:', error);
        alert('❌ Erreur: ' + error.message);
        emailBtn.disabled = false;
        emailBtn.innerHTML = '<span>📧</span><span>Email</span>';
    }
}