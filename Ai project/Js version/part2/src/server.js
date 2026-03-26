const express = require("express")
const mysql = require("mysql2")
const bcrypt = require("bcrypt")
const cors = require("cors")

const app = express()

app.use(express.json())
app.use(cors())

const db = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "root",
    database: "chatbot"
})

db.connect(err => {
    if (err) {
        console.log("Database error:", err)
        return
    }
    console.log("MySQL connected")
})

app.post("/register", async (req, res) => {
    const { username, email, password } = req.body
    if (!username || !email || !password) {
        return;
    }
    const hash = await bcrypt.hash(password, 10)
    const sql = `
        INSERT INTO users (username, email, password_hash)
        VALUES (?, ?, ?)
    `
    db.query(sql, [username, email, hash], (err, result) => {

        if (err) {
            return res.status(500).send("Database error")
        }
        res.send("User created")
    })
})

app.post("/login", (req, res) => {
    const { email, password } = req.body
    const sql = "SELECT * FROM users WHERE email = ?"
    db.query(sql, [email], async (err, results) => {
        if (err) {
            console.error("DB Error:", err);
            if (err.code === "DB Error:", err) {
                return res.status(409).send("Username or Email already taken")
            }
            return res.status(500).send("Database error")
        }
        if (results.length === 0) {
            return res.status(401).send("Invalid credentials")
        }
        const user = results[0]
        const match = await bcrypt.compare(password, user.password_hash)
        if (!match) {
            return res.status(401).send("Invalid credentials")
        }
        res.send("Login success")
    })
})

app.listen(3000, () => {
    console.log("Server running on port 3000")
})
