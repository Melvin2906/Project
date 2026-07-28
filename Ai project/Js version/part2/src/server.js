const express = require("express")
const mysql = require("mysql2")
const bcrypt = require("bcrypt")
const cors = require("cors")
const jwt = require("jsonwebtoken")
const rateLimit = require("express-rate-limit")

const app = express()

const JWT_SECRET = process.env.JWT_SECRET_KEY
if (!JWT_SECRET) {
    console.error(
        "ERREUR: JWT_SECRET_KEY non défini. Définis la même valeur ici et côté API Python " +
        "(sinon les tokens émis ici ne seront jamais valides pour l'API Python)."
    )
    process.exit(1)
}

app.use(express.json())
app.use(cors({
    origin: process.env.CORS_ORIGIN || "http://localhost:5500",
}))

const authLimiter = rateLimit({
    windowMs: 60 * 1000,
    max: 10,
    message: { error: "Trop de tentatives, réessaie dans une minute" }
})

const db = mysql.createConnection({
    host: process.env.DB_HOST || "localhost",
    user: process.env.DB_USER || "root",
    password: process.env.DB_PASSWORD || "",
    database: process.env.DB_NAME || "chatbot"
})

db.connect(err => {
    if (err) {
        console.error("Database error:", err)
        return
    }
    console.log("MySQL connected")
})

app.post("/register", authLimiter, async (req, res) => {
    const username = (req.body.username || "").trim()
    const email = (req.body.email || "").trim().toLowerCase()
    const password = req.body.password || ""

    if (!username || !email || !password) {
        return res.status(400).json({ error: "Champs manquants" })
    }
    if (password.length < 8) {
        return res.status(400).json({ error: "Le mot de passe doit faire au moins 8 caractères" })
    }

    const hash = await bcrypt.hash(password, 10)
    const sql = "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)"
    db.query(sql, [username, email, hash], (err, result) => {
        if (err) {
            if (err.code === "ER_DUP_ENTRY") {
                return res.status(409).json({ error: "Nom d'utilisateur ou email déjà utilisé" })
            }
            console.error("DB Error:", err)
            return res.status(500).json({ error: "Erreur serveur" })
        }
        res.json({ message: "Compte créé" })
    })
})

app.post("/login", authLimiter, (req, res) => {
    const email = (req.body.email || "").trim().toLowerCase()
    const password = req.body.password || ""

    if (!email || !password) {
        return res.status(400).json({ error: "Champs manquants" })
    }

    const sql = "SELECT * FROM users WHERE email = ?"
    db.query(sql, [email], async (err, results) => {
        if (err) {
            console.error("DB Error:", err)
            return res.status(500).json({ error: "Erreur serveur" })
        }
        if (results.length === 0) {
            return res.status(401).json({ error: "Email ou mot de passe incorrect" })
        }
        const user = results[0]
        const match = await bcrypt.compare(password, user.password_hash)
        if (!match) {
            return res.status(401).json({ error: "Email ou mot de passe incorrect" })
        }
        const token = jwt.sign(
            { id: user.id, username: user.username, email: user.email },
            JWT_SECRET,
            { expiresIn: "7d" }
        )

        res.json({ token, username: user.username, email: user.email })
    })
})

app.listen(process.env.PORT || 3000, () => {
    console.log(`Serveur d'auth actif sur le port ${process.env.PORT || 3000}`)
})
