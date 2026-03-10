// translations.js
const translations = {
    en: {
        "welcome.title": "Welcome to our website!",
        "welcome.subtitle": "We are glad to see you here.",
        "main.content": "This is the main content of the page."
    },
    es: {
        "welcome.title": "¡Bienvenido a nuestro sitio web!",
        "welcome.subtitle": "Estamos encantados de verte aquí.",
        "main.content": "Este es el contenido principal de la página."
    },
    fr: {
        "welcome.title": "Bienvenue sur notre site web!",
        "welcome.subtitle": "Nous sommes ravis de vous voir ici.",
        "main.content": "Ceci est le contenu principal de la page."
    }
};

// script.js

// Function to change the language
function changeLanguage(lang) {
    const elements = document.querySelectorAll('[data-i18n]');
    elements.forEach(element => {
        const key = element.getAttribute('data-i18n');
        if (translations[lang] && translations[lang][key]) {
            element.innerHTML = translations[lang][key];
        }
    });
    // Update the HTML lang attribute for accessibility and SEO
    document.documentElement.lang = lang;
    // Optional: save the user's preference in localStorage
    localStorage.setItem('preferredLang', lang);
}

// Function to load the user's preferred language on page load
function loadPreferredLanguage() {
    const preferredLang = localStorage.getItem('preferredLang') || 'en'; // Default to English
    changeLanguage(preferredLang);
}

// Load language on page load
document.addEventListener('DOMContentLoaded', loadPreferredLanguage);

