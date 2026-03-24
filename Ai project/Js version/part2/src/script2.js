const getUserTimeZone = () => Intl.DateTimeFormat().resolvedOptions().timeZone;

document.getElementById("update-timezone").addEventListener("click", async () => {
    const timezone = getUserTimeZone();

    try {
        const res = await fetch("http://127.0.0.1:5000/update-timezone", {         
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ timezone })
        });

        const data = await res.json();
        console.log("Fuseau mis à jour :", data.timezone);

    } catch (err) {
        console.error("Erreur mise ) jour fuseau :", err);
    }
});

async function sendMessage(userMessage) {
    const fileInput = document.getElementById("join");
    const file = fileInput.files[0] || null;

    if (!userMessage.trim()) return null; // Return null for empty messages
    
    try {
        // Réinitialiser l'input
        document.getElementById("user-Input").value = "";

        // Ajouter le message de l'utilisateur
        document.getElementById("main-chat").insertAdjacentHTML("beforeend", `
            <div class="user">
                <p>${escapeHtml(userMessage)}</p>
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

        let res;
        let responseData;
        
        if (file) {
            const formData = new FormData();
            formData.append("message", userMessage);
            formData.append("image", file);

            res = await fetch("http://127.0.0.1:5000/ask-image", {
                method: "POST",
                body: formData
            });
            fileInput.value = "";
        } else {
            res = await fetch("http://127.0.0.1:5000/ask", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userMessage })
            });
        }

        let data = await res.json();
        let replyText = "";
        
        if (data.reply) {
            replyText = data.reply;
            if (data.reply.includes("```")) {
                const pre = document.createElement("pre");
                const code = document.createElement("code");
                code.textContent = data.reply;
                pre.appendChild(code);
                lastResponse.innerHTML = "";
                lastResponse.appendChild(pre);
            } else {
                lastResponse.innerHTML = marked.parse(data.reply);
            }
        } else {
            replyText = `Error: ${data.error || "No response from server"}`;
            lastResponse.innerHTML = `<p class="error">${replyText}</p>`;
        }
        
        return replyText; // Return the response for speech

    } catch (error) {
        console.error("Error:", error);
        const errorMsg = "The message could not be sent. Please try again.";
        document.getElementById("main-chat").insertAdjacentHTML("beforeend", `
            <div class="error">
                <p>${errorMsg}</p>
            </div>
        `);
        return errorMsg;
    } finally {
        // Retirer l'indicateur de chargement
        const loader = document.querySelector(".loader");
        if (loader) loader.remove();
    }
}

// Add this helper function to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

document.getElementById("join").addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (file) {
        console.log("Image sélectionnée :", file.name);
    }
});

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
const show_option = document.getElementById("show-option");

const toggleUserOptions = () => {
    if (user_o.style.display === "none" || user_o.style.display === "") {
        user_o.style.display = "block";
        user_o.className = "user-option-open";
    } else {
        user_o.style.display = "none";
        user_o.className = "user-option-close";
    }
}

open_u.addEventListener("click", toggleUserOptions);
show_option.addEventListener("click", toggleUserOptions);

const overlay = document.getElementById("overlay");

document.getElementById("set-but").addEventListener("click", () => {
    overlay.style.display = "block"
    document.getElementById("display-general").style.display = "block"
    user_o.style.display = "none"
    user_o.className = "user-option-close"
})

const click_to_display = () => {
    const list = ["general", "notifications","personalization","apps","data-control","security","parental-control","account"];

    list.forEach(id => {
        document.getElementById(id).addEventListener("click", () => {
            list.forEach(x => {
                document.getElementById("display-" + x).style.display =
                    x === id ? "block" : "none";
            });
        });
    });
}

document.getElementById("close-setting-table").addEventListener("click", () => {
    let list = ["notifications", "personalization", "apps", "data-control", "security", "parental-control", "account"];

    for (let i = 0; i < list.length; i++) {
        if (document.getElementById("display-" + list[i]).style.display === "block") {
            document.getElementById("display-" + list[i]).style.display = "none"
        }
    }
    overlay.style.display = "none"
})

document.getElementById("user-profil").addEventListener("click", () => {
    overlay.style.display = "block"
    document.getElementById("display-account").style.display = "block"
    user_o.style.display = "none"
    user_o.className = "user-option-close"
})


const signIn = document.getElementById('sign-in');
const signUp = document.getElementById('sign-up');

signIn.addEventListener('click', () => {
    document.getElementById('login-interface').click();
})

signUp.addEventListener('click', () => {
    document.getElementById('signup-interface').click();
})

// Pour gérer les bouton du setting pannel
click_to_display()

export { sendMessage }