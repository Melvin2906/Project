import { sendMessage } from './script2.js';

document.addEventListener("DOMContentLoaded", () => {
    initSpeech();
});

function initSpeech() {
    // Check if we're on localhost or HTTPS
    const isSecure = window.location.protocol === 'https:' || 
                     window.location.hostname === 'localhost' || 
                     window.location.hostname === '127.0.0.1';
    
    if (!isSecure) {
        console.warn("Speech recognition may not work on non-HTTPS connections");
    }
    
    // Check for browser support
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        console.error("SpeechRecognition not supported");
        const micButton = document.getElementById("audio-part");
        if (micButton) {
            micButton.disabled = true;
            micButton.title = "Speech recognition not supported in this browser";
        }
        return;
    }
    
    if (!('speechSynthesis' in window)) {
        console.warn("SpeechSynthesis not supported");
    }
    
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;
    
    // Function to create a new recognition instance
    function createRecognition() {
        const newRecognition = new SpeechRecognition();
        newRecognition.continuous = false;
        newRecognition.interimResults = false;
        newRecognition.lang = 'en-US';
        newRecognition.maxAlternatives = 1;
        return newRecognition;
    }
    
    const recordButton = document.getElementById("audio-part");
    if (!recordButton) {
        console.error("Microphone button (audio-part) not found in DOM");
        return;
    }
    
    let isListening = false;
    let retryCount = 0;
    const MAX_RETRIES = 3;
    
    // Function to restart recognition after error
    function restartRecognition() {
        if (retryCount < MAX_RETRIES && isListening) {
            retryCount++;
            console.log(`Retrying speech recognition (${retryCount}/${MAX_RETRIES})...`);
            setTimeout(() => {
                if (isListening) {
                    try {
                        recognition = createRecognition();
                        setupRecognitionHandlers();
                        recognition.start();
                    } catch (error) {
                        console.error("Failed to restart recognition:", error);
                        isListening = false;
                        recordButton.style.opacity = "1";
                    }
                }
            }, 1000);
        } else if (retryCount >= MAX_RETRIES) {
            console.error("Max retries reached. Please click the mic button again.");
            isListening = false;
            recordButton.style.opacity = "1";
            retryCount = 0;
        }
    }
    
    function setupRecognitionHandlers() {
        if (!recognition) return;
        
        recognition.onstart = () => {
            console.log("Voice recognition started");
            recordButton.style.opacity = "0.7";
            recordButton.style.backgroundColor = "#ff4444";
            retryCount = 0;
        };
        
        recognition.onend = () => {
            console.log("Voice recognition ended");
            isListening = false;
            recordButton.style.opacity = "1";
            recordButton.style.backgroundColor = "";
        };
        
        recognition.onresult = async (event) => {
            if (!event.results || event.results.length === 0) {
                console.log("No results from speech recognition");
                return;
            }
            
            const transcript = event.results[0][0].transcript;
            const confidence = event.results[0][0].confidence;
            console.log(`Recognized text (confidence: ${confidence}):`, transcript);
            
            const userInput = document.getElementById("user-Input");
            if (userInput) {
                userInput.value = transcript;
            }
            
            // Auto-send if confidence is high enough
            if (confidence > 0.5 && transcript.trim()) {
                await processCommand(transcript);
            } else if (transcript.trim()) {
                // Just fill the input field for user to review
                console.log("Low confidence, waiting for user to send manually");
            }
        };
        
        recognition.onerror = (event) => {
            console.error("Speech recognition error:", event.error, event.message);
            
            // Handle specific errors
            switch(event.error) {
                case 'no-speech':
                    console.log("No speech detected. Please try again.");
                    // Don't retry for no-speech, just reset
                    isListening = false;
                    recordButton.style.opacity = "1";
                    recordButton.style.backgroundColor = "";
                    break;
                    
                case 'audio-capture':
                    console.error("No microphone found. Please check your microphone connection.");
                    isListening = false;
                    recordButton.style.opacity = "1";
                    recordButton.style.backgroundColor = "";
                    alert("No microphone detected. Please connect a microphone and try again.");
                    break;
                    
                case 'not-allowed':
                    console.error("Microphone access denied by user.");
                    isListening = false;
                    recordButton.style.opacity = "1";
                    recordButton.style.backgroundColor = "";
                    alert("Microphone access is required for voice input. Please allow microphone access in your browser settings.");
                    break;
                    
                case 'network':
                    console.error("Network error occurred. This might be due to missing API credentials or network issues.");
                    // Try to restart for network errors
                    if (retryCount < MAX_RETRIES) {
                        restartRecognition();
                    } else {
                        isListening = false;
                        recordButton.style.opacity = "1";
                        recordButton.style.backgroundColor = "";
                        alert("Speech recognition network error. Please check your internet connection and try again.");
                    }
                    break;
                    
                default:
                    console.error(`Unhandled error: ${event.error}`);
                    isListening = false;
                    recordButton.style.opacity = "1";
                    recordButton.style.backgroundColor = "";
            }
        };
    }
    
    recordButton.addEventListener("click", () => {
        if (isListening) {
            // Stop listening
            if (recognition) {
                try {
                    recognition.stop();
                } catch (error) {
                    console.error("Error stopping recognition:", error);
                }
            }
            isListening = false;
            recordButton.style.opacity = "1";
            recordButton.style.backgroundColor = "";
        } else {
            // Start listening
            try {
                // Create fresh recognition instance
                recognition = createRecognition();
                setupRecognitionHandlers();
                recognition.start();
                isListening = true;
                console.log("Started listening...");
            } catch (error) {
                console.error("Error starting recognition:", error);
                isListening = false;
                
                // Check if it's a permission issue
                if (error.name === 'NotAllowedError') {
                    alert("Please allow microphone access to use voice input.");
                } else if (error.name === 'NotSupportedError') {
                    alert("Speech recognition is not supported in this browser. Please use Chrome, Edge, or Safari.");
                } else {
                    alert(`Failed to start speech recognition: ${error.message}`);
                }
            }
        }
    });
    
    async function processCommand(transcript) {
        try {
            // Show loading state
            recordButton.style.opacity = "0.5";
            
            const response = await sendMessage(transcript);
            
            if (response && window.speechSynthesis) {
                await speak(response);
            } else if (!response) {
                console.log("No response to speak");
            }
        } catch (error) {
            console.error("Error processing command:", error);
        } finally {
            recordButton.style.opacity = "1";
        }
    }
    
    async function speak(text) {
        return new Promise((resolve, reject) => {
            if (!window.speechSynthesis) {
                console.log("Speech synthesis not supported");
                resolve();
                return;
            }
            
            // Clean the text for speech
            const cleanText = text.replace(/[#*`]/g, '')
                                 .replace(/```[\s\S]*?```/g, '')
                                 .replace(/\[.*?\]\(.*?\)/g, '')
                                 .substring(0, 500); // Limit length
            
            const utterance = new SpeechSynthesisUtterance(cleanText);
            
            // Language detection
            if (/[\u0400-\u04FF]/.test(cleanText)) {
                utterance.lang = 'ru-RU';
            } else if (/[\u0600-\u06FF]/.test(cleanText)) {
                utterance.lang = 'ar-SA';
            } else if (/[\u4e00-\u9fff]/.test(cleanText)) {
                utterance.lang = 'zh-CN';
            } else if (/[áéíóúñ¿¡]/i.test(cleanText)) {
                utterance.lang = 'es-ES';
            } else if (/[àâäéèêëïîôöùûüÿç]/i.test(cleanText)) {
                utterance.lang = 'fr-FR';
            } else {
                utterance.lang = 'en-US';
            }
            
            // Try to find a good voice
            const voices = window.speechSynthesis.getVoices();
            const preferredVoice = voices.find(voice => 
                voice.lang.startsWith(utterance.lang.split('-')[0]) && 
                (voice.name.includes('Google') || voice.name.includes('Natural') || voice.default)
            );
            
            if (preferredVoice) {
                utterance.voice = preferredVoice;
            }
            
            utterance.rate = 0.9; // Slightly slower for better clarity
            utterance.pitch = 1.0;
            utterance.volume = 1.0;
            
            utterance.onend = () => {
                console.log("Speech finished");
                resolve();
            };
            
            utterance.onerror = (event) => {
                console.error("Speech synthesis error:", event);
                reject(event);
            };
            
            // Cancel any ongoing speech
            window.speechSynthesis.cancel();
            
            // Small delay to ensure cancellation is processed
            setTimeout(() => {
                window.speechSynthesis.speak(utterance);
            }, 100);
        });
    }
    
    // Test if speech recognition is properly configured
    console.log("Speech recognition initialized. Click the microphone button to start.");
    
    // Add a visual indicator that voice is supported
    if (recordButton) {
        recordButton.title = "Click to speak (requires microphone access)";
    }
}