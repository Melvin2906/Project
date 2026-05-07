const getUserTimeZone = () => Intl.DateTimeFormat().resolvedOptions().timeZone;

function loadUserInfo() {
    const token = localStorage.getItem("token")
    const username = localStorage.getItem("username")
    const email = localStorage.getItem("email")

    if (!token) {
        document.getElementById("sign-in").style.display = "block"
        document.getElementById("sign-up").style.display = "block"
        document.getElementById("open-u").style.display = "none"
        document.getElementById("show-option").style.display = "none"
        return
    }
    document.getElementById("sign-in").style.display = "none"
    document.getElementById("sign-up").style.display = "none"
    const label = username || email || "User"
    document.getElementById("open-u").textContent = label
    document.getElementById("show-option").textContent = label
    const accountPanel = document.getElementById("display-account")
    if (accountPanel) {
        accountPanel.innerHTML = `
            <h1 class="a-title">Account</h1>
            <p><strong>Username:</strong> ${username}</p>
            <p><strong>Email:</strong> ${email}</p>
        `
    }
}

document.getElementById("logout-bttn").addEventListener("click", () => {
    localStorage.removeItem("token")
    localStorage.removeItem("username")
    localStorage.removeItem("email")
    window.location.href = "login_signup.html"
})

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
        console.error("Erreur mise à jour fuseau :", err);
    }
});

async function sendMessage(userMessage) {
    const imgInput = document.getElementById("join-image");
    const docInput = document.getElementById("join-doc");
    const imgFile = imgInput.files[0];
    const docFile = docInput.files[0];

    if (!userMessage.trim() && !imgFile && !docFile) return;

    try {
        document.getElementById("user-Input").value = "";
        const chat = document.getElementById("main-chat");
        chat.insertAdjacentHTML("beforeend", `<div class="user"><p>${userMessage}</p></div><div class="loader"></div>`);
        
        let res;
        const lowerMsg = userMessage.toLowerCase();
        if (lowerMsg.startsWith("/image")) {
            res = await fetch("http://127.0.0.1:5000/generate-image", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ prompt: userMessage.replace("/image", "").trim() })
            });
            if (res.ok) {
                const blob = await res.blob();
                renderBotResponse(`<img src="${URL.createObjectURL(blob)}" style="max-width:100%; border-radius:10px;">`);
                return;
            }
        }
        else if (lowerMsg.startsWith("/pdf") || lowerMsg.startsWith("/doc") || lowerMsg.startsWith("/excel")) {
            let type = lowerMsg.startsWith("/pdf") ? "pdf" : lowerMsg.startsWith("/doc") ? "docx" : "xlsx";
            res = await fetch("http://127.0.0.1:5000/generate-doc", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ prompt: userMessage, type: type })
            });
            if (res.ok) {
                const blob = await res.blob();
                renderBotResponse(`<a href="${URL.createObjectURL(blob)}" download="export.${type}">Télécharger le fichier ${type.toUpperCase()}</a>`);
                return;
            }
        }
        else if (imgFile || docFile) {
            const formData = new FormData();
            formData.append("message", userMessage);
            
            if (imgFile) {
                formData.append("image", imgFile);
                res = await fetch("http://127.0.0.1:5000/ask-image", { method: "POST", body: formData });
                imgInput.value = "";
            } else {
                formData.append("file", docFile);
                res = await fetch("http://127.0.0.1:5000/ask-document", { method: "POST", body: formData });
                docInput.value = "";
            }
        }
        else {
            res = await fetch("http://127.0.0.1:5000/ask", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userMessage })
            });
        }

        const data = await res.json();
        renderBotResponse(marked.parse(data.reply || data.error));

    } catch (e) {
        console.error("Erreur:", e);
    } finally {
        document.querySelector(".loader")?.remove();
    }
}

function renderBotResponse(html) {
    document.getElementById("main-chat").insertAdjacentHTML("beforeend", `
        <div class="model"><div class="bot-response">${html}</div></div>
    `);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

document.getElementById("join-doc").addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (file) console.log("Document sélectionnée :", file.name);
});

document.getElementById("join-image").addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (file) console.log("Image sélectionnée :", file.name);
});

async function copyElementContentToClipboard(elementClass) {
    try {
        const element = document.querySelector(elementClass);
        if (!element) {
            console.error(`Element '${elementClass}' not found.`);
            return;
        }
        await navigator.clipboard.writeText(element.textContent);
        console.log('Content copied to clipboard!');
    } catch (err) {
        console.error('Failed to copy content:', err);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    loadUserInfo()

    const sendButton = document.getElementById("send-button");
    const userInput = document.getElementById("user-Input");

    sendButton.addEventListener("click", () => {
        const message = userInput.value.trim();
        if (message) sendMessage(message);
    });

    userInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            const message = userInput.value.trim();
            if (message) sendMessage(message);
        }
    });
});

class Autogrow extends HTMLTextAreaElement {
    constructor() {
        super();
        this.onInput = this.onInput.bind(this);
    }
    connectedCallback() {
        this.addEventListener("input", this.onInput);
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
customElements.define("textarea-autogrow", Autogrow, { extends: "textarea" });

const copyButt = document.querySelector("copy")
if (copyButt) {
    copyButt.addEventListener("click", () => {
        copyElementContentToClipboard(".bot-response")
    })
}

document.getElementById("btn-image").addEventListener("click", () => {
    document.getElementById("join-image").click()
})

document.getElementById("btn-doc").addEventListener("click", () => {
    document.getElementById("join-doc").click()
})

document.getElementById("extend").addEventListener("click", () => {
    document.getElementById("side").style = "display: block;";
    document.getElementById("reduct").style = "display: none;"
})

document.getElementById("close-side").addEventListener("click", () => {
    document.getElementById("side").style = "display: none;"
    document.getElementById("reduct").style = "display: block;"
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
    const list = ["general", "notifications", "personalization", "apps", "data-control", "security", "parental-control", "account"];
    list.forEach(id => {
        document.getElementById(id).addEventListener("click", () => {
            list.forEach(x => {
                document.getElementById("display-" + x).style.display = x === id ? "block" : "none";
            });
        });
    });
}

document.getElementById("close-setting-table").addEventListener("click", () => {
    let list = ["notifications", "personalization", "apps", "data-control", "security", "parental-control", "account", "general"];
    list.forEach(id => {
        document.getElementById("display-" + id).style.display = "none"
    })
    overlay.style.display = "none"
})

document.getElementById("user-profil").addEventListener("click", () => {
    overlay.style.display = "block"
    document.getElementById("display-account").style.display = "block"
    user_o.style.display = "none"
    user_o.className = "user-option-close"
    const username = localStorage.getItem("username")
    const email = localStorage.getItem("email")
    document.getElementById("display-account").innerHTML = `
        <h1 class="a-title">Account</h1>
        <p><strong>Username:</strong> ${username || "—"}</p>
        <p><strong>Email:</strong> ${email || "—"}</p>
    `
})

const signInBtn = document.getElementById('sign-in');
const signUpBtn = document.getElementById('sign-up');

signInBtn.addEventListener('click', () => {
    document.getElementById('login-interface').click();
})

signUpBtn.addEventListener('click', () => {
    document.getElementById('signup-interface').click();
})

click_to_display()

export { sendMessage }