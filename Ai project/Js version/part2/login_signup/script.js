// import { scrypt, randomBytes, timingSafeEqual } from './node_modules/crypto';
// import { promisify } from './node_modules/util';

// const mysql = require('mysql2')
const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const main = document.getElementById('main')
const signIn = document.getElementById('sign-in')
const signUp = document.getElementById('sign-up')
// const scryptAsyns =  promisify(scrypt)

async function createHashPasswd(passwd) {
    const salt = randomBytes(16).toString('hex')
    const passwd_hash = await scryptAsyns(passwd, salt, 64)
    return [passwd, salt]
}

signUpButton.addEventListener('click', () => {
    main.classList.add("right-panel-active")
})

signInButton.addEventListener('click', () => {
    main.classList.remove("right-panel-active")
})

// signUp.addEventListener('click', () => {
//     let passwd = document.getElementById("password_input");
//     let result = createHashPasswd(passwd);
//     const connection = mysql.createConnection({
//         username: document.getElementById("name_input"),
//         password_hash: result[0],
//         hash_key: result[1],
//         email: document.getElementById("email_input"),
//     });

//     connection.connect((err) => {
//         if (err) {
//             console.log("Error when trying to connect to the database")
//             return;
//         }
//         console.log("Connect to MySql database")
//     })

//     connection.query('SELECT * FROM users', (err, result) => {
//         if (err) {
//             throw err;
//         }
//         console.log(result);
//     });
//     connection.end();
// })

// signIn.addEventListener('click', () => {})
