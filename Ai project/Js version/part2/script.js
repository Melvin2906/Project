import { GoogleGenerativeAI } from "@google/generative-ai";

const sent = document.getElementById("sent button")
const fileInput = document.getElementById("add").files
const API_KEY = "";
const genAi = new GoogleGenerativeAI(API_KEY);
const model = genAi.getGenerativeModel({ 
    model: "gemini-2.5-pro",
    // formater les réponse du chatbot avec:
    //systemInstruction: example
})

let message = { 
    history: []
}

async function sendMessage() {
 
    console.log(message)
    const userMessage = document.querySelector(".chat-window input").value;

    if (userMessage.length) {
        try {
            document.querySelector(".chat-window input").value = "";
            document.querySelector(".chat-window .chat").insertAdjacentHTML("beforeend", `
                <div class="user">
                    <p>${userMessage}</p>
                </div>
            `)
            
            document.querySelector(".chat-window .chat").insertAdjacentHTML("beforeend", `
                <div class="loader"></div>
            `)

            const chat = model.startChat({ message });

            document.querySelector(".chat-window .chat").insertAdjacentHTML("beforeend", `
                <div class="model">
                    <p class="bot-response"></p>
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
                console.log(buffer)

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
            document.querySelector(".chat-window .chat").insertAdjacentHTML("beforeend", `
                <div class="error">
                    <p>The message could not be sent. Please try again.</p>
                </div>
            `);
        }

        // retire loader
        document.querySelector(".chat-window .chat .loader").remove();

    };
}

sent.addEventListener("click", () => sendMessage());

document.querySelector(".chat-button")
.addEventListener("click", () => {
    document.querySelector("body").classList.add("chat-open")
})

document.querySelector(".chat-window button.close")
.addEventListener("click", () => {
    document.querySelector("body").classList.remove("chat-open")
})

document.getElementById("add button").addEventListener("click", () => {
    document.getElementById("upload").click()
})