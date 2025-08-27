const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");
const chatbox = document.querySelector(".chatbox");
let userMessage = null;

const API_KEY = ""; // Mets ta clé Gemini ici

const generateResponse = () => {
    // Utilisation de l'API Gemini pour générer des réponses
    const API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + API_KEY;

    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            contents: [{ parts: [{ text: userMessage }] }]
        })
    }

    fetch(API_URL, requestOptions)
        .then(res => res.json())
        .then(data => {
            // Récupérer la réponse de Gemini
            const geminiResponse = data.candidates?.[0]?.content?.parts?.[0]?.text || "Erreur de réponse Gemini";
            // Remplacer le "Thinking..." par la vraie réponse
            const thinkingLi = chatbox.querySelector(".incoming:last-child");
            if (thinkingLi) thinkingLi.querySelector("p").textContent = geminiResponse;
        })
        .catch((error) => {
            console.log(error);
        });
}
const createChatLi = (message, className) => {
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", className);
    let chatContent = className === "outgoing" ? `<p>${message}</p>` : `<span class="material-symbols-outlined">smart_toy</span><p>${message}</p>`;
    chatLi.innerHTML = chatContent;
    return chatLi;
}

const handleChat = () => {
    userMessage = chatInput.value.trim();
    if (!userMessage) return;
    // Ajouter l'entrer de l'utilisateur dans le chatbox
    chatbox.appendChild(createChatLi(userMessage, "outgoing"));
    
    //Afficher le message "réflexion pour simuler une réflexion de l'IA"
    setTimeout(() => {
        chatbox.appendChild(createChatLi("Thinking...", "incoming"))
    }, 600);
    generateResponse();
}

sendChatBtn.addEventListener("click", handleChat);