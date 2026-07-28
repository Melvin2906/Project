import { GoogleGenerativeAI } from "@google/generative-ai";

const api_key = document.getElementById("api-key").value
const sent = document.getElementById("sent-button")
//const fileInput = document.getElementById("add").files
const API_KEY = "";
const genAi = new GoogleGenerativeAI(API_KEY);
const model = genAi.getGenerativeModel({ 
    model: "gemini-2.5-flash",
    systemInstruction: buildSystemInstruction()
})

function getUserTimeZone() { 
    return Intl.DateTimeFormat().resolvedOptions().timeZone;
}

function getFormatteDate(timezone) {
    const now = new Date();
    const local = navigator.language || "en-US";

    const formatter = new Intl.DateTimeFormat(local, {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        timeZone: timezone,
        hour12: true
    })

    return formatter.format(now)
}

function buildSystemInstruction() {
    const timezone = getUserTimeZone();
    const dateStr = getFormatteDate(timezone)

    return `
Current date (provided by the application):
${dateStr}
User time zone: ${timezone}

STRICT rules:
- You have no direct access to the time or date
- You only use the date provided above
- You never attempt to access servers, metadata, or clocks
- If time information is not provided, you state that you do not know it
`;
}

let message = { 
    history: []
}

export async function sendMessage(userMessage) {
     if (userMessage.length) {
        try {
            document.getElementById("user-Input").value = "";
            document.getElementById("main-chat").insertAdjacentHTML("beforeend", `
                <div class="user">
                    <p>${userMessage}</p>
                </div>
            `)
            
            document.getElementById("main-chat").insertAdjacentHTML("beforeend", `
                <div id="loader" class="loader"></div>
            `)

            const chat = model.startChat({ message });

            document.getElementById("main-chat").insertAdjacentHTML("beforeend", `
                <div class="model">
                    <p class="bot-response" id="last-response"></p>
                </div>
            `)


            // méthode pour donner l'impression au user que l'ia lui écrit plutôt que d'attendre tout le text
            let result = await chat.sendMessageStream(userMessage);
            let buffer = ""

            // sélectionne la dernière réponse
            const modelMessages = document.querySelectorAll(".chat-window .chat div.model");
            const lastResponse = modelMessages[modelMessages.length - 1].querySelector(".bot-response");

            // lit le stream chunk par chunk
            for await (const chunk of result.stream) {
                buffer += chunk.text();

                // parse markdown → html
                lastResponse.innerHTML = marked.parse(buffer);

                lastResponse.scrollIntoView({ behavior: "smooth", block: "end" });
            }

            // mets à jour l’historique
            message.history.push({
                role: "user",
                parts: [{ text: userMessage }],
            });
            message.history.push({
                role: "model",
                parts: [{ text: buffer }],
            });

        } catch (error) {
            document.getElementById("main-chat").insertAdjacentHTML("beforeend", `
                <div class="error">
                    <p>The message could not be sent. Please try again.</p>
                </div>
            `);
        } finally {
        // retire loader
            const loader = document.getElementById("loader");
            if (loader) loader.remove();
        }

    };
}

sent.addEventListener("click", () => {
    const userMessage = document.getElementById("user-Input").value; 
    sendMessage(userMessage)
});

document.querySelector(".chat-button")
.addEventListener("click", () => {
    document.querySelector("body").classList.add("chat-open")
})

document.querySelector(".chat-window button.close")
.addEventListener("click", () => {
    document.querySelector("body").classList.remove("chat-open")
})

document.getElementById("add-button").addEventListener("click", () => {
    document.getElementById("upload").click()
})

document.getElementById("full-screen").addEventListener("click", () => {
    document.getElementById("screen").click()    
})
