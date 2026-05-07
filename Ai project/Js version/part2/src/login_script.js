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

signUp.addEventListener('submit', (e) => {
    e.preventDefault();

    const email = document.getElementById("email_input").value.trim()
    const password = document.getElementById("passwd_input").value.trim()

    fetch("http://localhost:3000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            username: document.getElementById("name_input").value.trim(),
            email,
            password
        })
    })
    .then(res => {
        if (!res.ok) return res.text().then(msg => { throw new Error(msg) })
        return res.text()
    })
    .then(() => {
        // Auto-login right after register
        return fetch("http://localhost:3000/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        })
    })
    .then(res => {
        if (!res.ok) return res.text().then(msg => { throw new Error(msg) })
        return res.json()
    })
    .then(data => {
        localStorage.setItem("token", data.token)
        localStorage.setItem("username", data.username)
        localStorage.setItem("email", data.email)
        window.location.href = "full-screen.html"
    })
    .catch(error => {
        console.error('Error:', error.message)
        alert("Error: " + error.message)
    });
});

signIn.addEventListener('submit', e => {
    e.preventDefault();

    fetch("http://localhost:3000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            email: document.getElementById("signin-mail").value.trim(),
            password: document.getElementById("login-pass").value.trim()
        })
    })
    .then(res => {
        if (!res.ok) return res.text().then(msg => { throw new Error(msg) })
        return res.json()
    })
    .then(data => {
        // Store token and user info
        localStorage.setItem("token", data.token)
        localStorage.setItem("username", data.username)
        localStorage.setItem("email", data.email)

        // Redirect to main chatbot page
        window.location.href = "full-screen.html"
    })
    .catch(error => {
        console.error('Login error:', error.message)
        alert("Login failed: " + error.message)
    })
})
