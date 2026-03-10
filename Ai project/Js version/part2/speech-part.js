//import * as scr from './script.js';
import { franc } from "https://esm.sh/franc"
import { sendMessage } from "./script2.js"

document.addEventListener("DOMContentLoaded", () => {
    initSpeech();
});

function initSpeech() {
    window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    window.SpeechSynthesis = window.SpeechSynthesis || window.webkitSpeechSynthesis;
    
    if (!window.SpeechRecognition) {
        console.log("SpeechRecognition not supported");
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;

    const record = document.getElementById("audio-part");
    if (!record) {
        console.log("audio-part not found");
        return;
    }

    record.addEventListener("click", () => {
        recognition.start();
    });

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        processCommand(transcript);
    };

    async function processCommand(transcript) {
        const res = await sendMessage(transcript);


        speak(res);
    }

    const speak = (text) => {
        const language = franc(text)
        const synthesys = new SpeechSynthesisUtterance(text);
        synthesys.lang = iso3ToIso1(language);
        synthesys.voice = voices[0];
        window.speechSynthesis.speak(synthesys);
    }
}
