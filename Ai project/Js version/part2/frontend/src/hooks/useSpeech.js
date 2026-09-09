import { useCallback, useEffect, useRef, useState } from "react";

const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;

/** Dictée vocale. Renvoie supported=false si le navigateur ne suit pas. */
export function useSpeech({ lang = "fr-FR", onResult } = {}) {
  const [listening, setListening] = useState(false);
  const recognitionRef = useRef(null);
  const resultRef = useRef(onResult);
  resultRef.current = onResult;

  useEffect(() => () => recognitionRef.current?.abort(), []);

  const toggle = useCallback(() => {
    if (!Recognition) return;

    if (listening) {
      recognitionRef.current?.stop();
      setListening(false);
      return;
    }

    const recognition = new Recognition();
    recognition.lang = lang;
    recognition.interimResults = false;
    recognition.continuous = false;
    recognition.onresult = (event) => {
      const text = Array.from(event.results)
        .map((r) => r[0].transcript)
        .join(" ")
        .trim();
      if (text) resultRef.current?.(text);
    };
    recognition.onerror = () => setListening(false);
    recognition.onend = () => setListening(false);
    recognition.start();
    recognitionRef.current = recognition;
    setListening(true);
  }, [lang, listening]);

  const speak = useCallback((text, voiceLang = lang) => {
    if (!("speechSynthesis" in window) || !text) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = voiceLang;
    window.speechSynthesis.speak(utterance);
  }, [lang]);

  return { supported: Boolean(Recognition), listening, toggle, speak };
}
