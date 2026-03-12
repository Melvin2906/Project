const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const main = document.getElementById('main')
const signIn = document.getElementById('signin-form')
const signUp = document.getElementById('signup-form')

// async function createHashPasswd(passwd) {
//     const salt = randomBytes(16).toString('hex')
//     const passwd_hash = await scryptAsyns(passwd, salt, 64)
//     return [passwd_hash, salt]
// }

signUpButton.addEventListener('click', () => {
    main.classList.add("right-panel-active")
})

signInButton.addEventListener('click', () => {
    main.classList.remove("right-panel-active")
})

signUp.addEventListener('submit', (e) => {
    e.preventDefault();

    fetch("http://localhost:3000/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: document.getElementById("name_input").value.trim(),
            email: document.getElementById("email_input").value.trim(),
            password: document.getElementById("passwd_input").value.trim()
        })
    })
    .then(res => res.text())
    .then(data => console.log(data))
    .catch(error => console.error('Error: ', error));
});

signIn.addEventListener('submit', e => {
    e.preventDefault();

    fetch("http://localhost:3000/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: document.getElementById("signin-mail").value.trim(),
            password: document.getElementById("login-pass").value.trim()
        })
    })
    .then(res => res.text())
    .then(console.log)
    .then(console.error);
})
