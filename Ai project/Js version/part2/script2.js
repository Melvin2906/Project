async function sendMessage(userMessage) {
    if (!userMessage.trim()) return;

    try {
        // Réinitialiser l'input
        document.getElementById("user-Input").value = "";

        // Ajouter le message de l'utilisateur
        document.getElementById("main-chat").insertAdjacentHTML("beforeend", `
            <div class="user">
                <p>${userMessage}</p>
            </div>
        `);

        // Ajouter un indicateur de chargement
        document.getElementById("main-chat").insertAdjacentHTML("beforeend", `
            <div class="loader"></div>
        `);

        // Ajouter un conteneur pour la réponse
        document.getElementById("main-chat").insertAdjacentHTML("beforeend", `
            <div class="model">
                <p class="bot-response"></p>
            </div>
        `);

        const modelMessage = document.querySelectorAll(".main-IA .chat-container .chat div.model");
        const lastResponse = modelMessage[modelMessage.length - 1].querySelector(".bot-response");

        // === ICI le fetch vers le backend Python ===
        let res = await fetch("http://127.0.0.1:5000/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userMessage })
        });

        let data = await res.json();

        if (data.reply) {
            lastResponse.innerHTML = marked.parse(data.reply);
        } else {
            lastResponse.innerHTML = `<p class="error">Erreur: ${data.error || "pas de réponse du serveur"}</p>`;
        }

    } catch (error) {
        console.error("Error:", error);
        document.getElementById("main-chat").insertAdjacentHTML("beforeend", `
            <div class="error">
                <p>The message could not be sent. Please try again.</p>
            </div>
        `);
    } finally {
        // Retirer l'indicateur de chargement
        const loader = document.querySelector(".loader");
        if (loader) loader.remove();
    }
}

async function copyElementContentToClipboard(elementClass) {
    console.log("click")
  try {
    const element = document.querySelector(elementClass);
    if (!element) {
      console.error(`Element with ID '${elementClass}' not found.`);
      return;
    }
    const textToCopy = element.textContent; // Or element.value for input/textarea
    await navigator.clipboard.writeText(textToCopy);
    console.log('Content copied to clipboard!');
  } catch (err) {
    console.error('Failed to copy content:', err);
  }
}

document.addEventListener("DOMContentLoaded", () => {
    const sendButton = document.getElementById("send-button");
    const userInput = document.getElementById("user-Input");
    const userFile = document.getElementById("join").files
    
    // Événement pour le bouton d'envoi
    sendButton.addEventListener("click", () => {
        const message = userInput.value.trim();
        if (message) {
            sendMessage(message);
        }
    });
    
    // Événement pour la touche Entrée
    userInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            const message = userInput.value.trim();
            if (message) {
                sendMessage(message);
            }
        }
    });
});

// Classe pour l'auto-agrandissement du textarea
class Autogrow extends HTMLTextAreaElement {
    constructor() {
        super();
        this.onInput = this.onInput.bind(this);
    }

    connectedCallback() {
        this.addEventListener("input", this.onInput);
        // Initialiser la hauteur
        setTimeout(() => this.onInput(), 0);
    }

    disconnectedCallback() {
        this.removeEventListener("input", this.onInput);
    }

    onInput() {
        this.style.height = "auto";
        this.style.height = this.scrollHeight + "px";
    }
}

const copyButt = document.querySelector("copy")

if (copyButt) {
    copyButt.addEventListener("click", () => {
        copyElementContentToClipboard(".bot-response")
        console.log("click")
    })
}
// Définir le custom element
customElements.define("textarea-autogrow", Autogrow, { extends: "textarea" });

document.getElementById("add-button").addEventListener("click", () => {
    document.getElementById("join").click()
})

document.getElementById("extend").addEventListener("click", () => {
    document.getElementById("side").style="display: yes;";
    document.getElementById("reduct").style="display: none;"
})

document.getElementById("close-side").addEventListener("click", () => {
    document.getElementById("side").style="display: none;"
    document.getElementById("reduct").style="display: yes;"
})

const open_u = document.getElementById("open-u");
const user_o = document.getElementById("user-o");

if (user_o.className == "user-option-close") {
    open_u.addEventListener("click", () => {
        user_o.style="display: yes;"
        user_o.className = "user-option-open"
    })
} else {
    open_u.addEventListener("click", () => {
        user_o.style="display: none;"
        user_o.className="user-option-close"
        console.log(user_o.className)
    })
}
