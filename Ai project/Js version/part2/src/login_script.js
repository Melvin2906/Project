const AUTH_BASE = "http://localhost:3000";

const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const main = document.getElementById('main')
const signIn = document.getElementById('signin-form')
const signUp = document.getElementById('signup-form')

signUpButton.addEventListener('click', () => {
    main.classList.add("right-panel-active")
})

signInButton.addEventListener('click', () => {
    main.classList.remove("right-panel-active")
})

async function parseJsonOrThrow(res) {
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.error || "Erreur inconnue");
    return data;
}

signUp.addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById("email_input").value.trim()
    const password = document.getElementById("passwd_input").value.trim()

    try {
        await fetch(`${AUTH_BASE}/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                username: document.getElementById("name_input").value.trim(),
                email,
                password
            })
        }).then(parseJsonOrThrow)

        const data = await fetch(`${AUTH_BASE}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        }).then(parseJsonOrThrow)

        localStorage.setItem("token", data.token)
        localStorage.setItem("username", data.username)
        localStorage.setItem("email", data.email)
        window.location.href = "full-screen.html"

    } catch (error) {
        console.error('Error:', error.message)
        alert("Erreur : " + error.message)
    }
});

signIn.addEventListener('submit', async e => {
    e.preventDefault();

    try {
        const data = await fetch(`${AUTH_BASE}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                email: document.getElementById("signin-mail").value.trim(),
                password: document.getElementById("login-pass").value.trim()
            })
        }).then(parseJsonOrThrow)

        localStorage.setItem("token", data.token)
        localStorage.setItem("username", data.username)
        localStorage.setItem("email", data.email)

        window.location.href = "full-screen.html"

    } catch (error) {
        console.error('Login error:', error.message)
        alert("Connexion échouée : " + error.message)
    }
})
