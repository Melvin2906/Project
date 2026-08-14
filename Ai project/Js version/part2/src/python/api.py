from dotenv import load_dotenv
load_dotenv()  # doit être fait AVANT d'importer auth/chatbot_base, qui lisent os.environ à l'import

from fastapi import FastAPI, Request, UploadFile, File, Form, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.middleware.sessions import SessionMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel
from configparser import ConfigParser
from chatbot_base import ChatBot
import sugestions as db
import authentification as auth
import io
import os
import secrets

config = ConfigParser()
config.read("Gemini.ini")

api_key = os.environ.get("GEMINI_API_KEY") or config.get("gemini", "api_key", fallback=None)
if not api_key:
    raise RuntimeError(
        "Clé API Gemini manquante : définis la variable d'env GEMINI_API_KEY "
        "ou ajoute-la dans Gemini.ini sous [gemini] api_key=... "
        "(peut être une valeur bidon si tu utilises un LLM local)"
    )

secret_key = os.environ.get("SESSION_SECRET_KEY")
if not secret_key:
    secret_key = secrets.token_hex(32)
    print(
        "ATTENTION: SESSION_SECRET_KEY non défini dans l'environnement, une clé "
        "temporaire a été générée (les sessions seront invalidées à chaque redémarrage)."
    )

chatbot = ChatBot(api_key=api_key)
chatbot.start_convertion()

db.init_db()

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=secret_key)

def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentification requise")

    token = authorization.split(" ", 1)[1]
    try:
        payload = auth.decode_token(token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    return payload

def _owned_conversation_or_404(conversation_id, user_id):
    conversation = db.get_conversation(conversation_id)
    if not conversation or conversation["user_id"] != user_id:
        raise HTTPException(status_code=404, detail="Conversation introuvable")
    return conversation


class TimezoneBody(BaseModel):
    timezone: str | None = None


class AskBody(BaseModel):
    message: str = ""
    conversation_id: int


class GenerateImageBody(BaseModel):
    prompt: str = ""


class GenerateDocBody(BaseModel):
    prompt: str = ""
    type: str = "pdf"


class ConversationBody(BaseModel):
    title: str = "Nouvelle conversation"

@app.get("/conversations")
async def get_conversations(user=Depends(get_current_user)):
    return db.list_conversations(user["id"])


@app.post("/conversations")
async def create_conversation(body: ConversationBody, user=Depends(get_current_user)):
    conv_id = db.create_conversation(user["id"], body.title)
    return {"id": conv_id, "title": body.title}


@app.get("/conversations/{conv_id}/messages")
async def get_conversation_messages(conv_id: int, user=Depends(get_current_user)):
    _owned_conversation_or_404(conv_id, user["id"])
    return db.get_messages(conv_id)


@app.delete("/conversations/{conv_id}")
async def delete_conversation(conv_id: int, user=Depends(get_current_user)):
    _owned_conversation_or_404(conv_id, user["id"])
    db.delete_conversation(conv_id)
    return {"status": "ok"}

@app.post("/update-timezone")
async def update_timezone(body: TimezoneBody, request: Request):
    timezone = body.timezone
    if not timezone:
        return JSONResponse({"error": "No timzone provided"}, status_code=400)

    request.session["timezone"] = timezone
    chatbot.update_datetime(timezone=timezone)
    return {"status": "ok", "timezone": timezone}

@app.post("/ask")
@limiter.limit("20/minute")
async def ask(body: AskBody, request: Request, user=Depends(get_current_user)):
    user_message = body.message
    conversation_id = body.conversation_id

    _owned_conversation_or_404(conversation_id, user["id"])

    if user_message:
        db.record_question(user_message)

    timezone = request.session.get("timezone", "UTC")
    context = chatbot.update_datetime(timezone)

    history = db.get_messages(conversation_id)
    full_messages = list(chatbot._conversation_history) + history + [
        {"role": "user", "content": context + user_message}
    ]

    response = chatbot.send_prompt_with_history(full_messages)

    db.add_message(conversation_id, "user", user_message)
    db.add_message(conversation_id, "assistant", response)

    return {"reply": response, "conversation_id": conversation_id}


@app.post("/ask-image")
@limiter.limit("10/minute")
async def ask_image(
    request: Request,
    message: str = Form(""),
    conversation_id: int = Form(...),
    image: UploadFile = File(...),
    user=Depends(get_current_user),
):
    _owned_conversation_or_404(conversation_id, user["id"])

    timezone = request.session.get("timezone", "UTC")
    context = chatbot.update_datetime(timezone)
    final_message = context + message
    image_bytes = await image.read()

    response = chatbot.send_prompt_with_image(final_message, image_bytes)

    db.add_message(conversation_id, "user", f"[Image envoyée] {message}")
    db.add_message(conversation_id, "assistant", response)

    return {"reply": response}


@app.get("/suggest")
async def suggest(q: str = ""):
    return db.suggest(q)


@app.post("/generate-image")
@limiter.limit("5/minute")
async def create_image(request: Request, body: GenerateImageBody, user=Depends(get_current_user)):
    prompt = body.prompt
    if not prompt:
        return JSONResponse({"error": "Prompt manquant"}, status_code=400)

    image_bytes = chatbot.generate_image(prompt)
    if image_bytes:
        return StreamingResponse(io.BytesIO(image_bytes), media_type="image/png")
    return JSONResponse({"error": "La génération d'image a échoué"}, status_code=500)


@app.post("/generate-doc")
@limiter.limit("5/minute")
async def generate_doc(request: Request, body: GenerateDocBody, user=Depends(get_current_user)):
    prompt = body.prompt
    file_type = body.type

    if file_type not in ("pdf", "docx", "xlsx"):
        return JSONResponse({"error": "Type de fichier non supporté"}, status_code=400)
    if not prompt:
        return JSONResponse({"error": "Prompt vide"}, status_code=400)

    try:
        file_bytes = chatbot.generate_document(prompt, file_type)
        if file_bytes:
            mime_types = {
                "pdf": "application/pdf",
                "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            }
            return StreamingResponse(
                io.BytesIO(file_bytes),
                media_type=mime_types.get(file_type, "application/octet-stream"),
                headers={"Content-Disposition": f'attachment; filename="generated_file.{file_type}"'},
            )
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/ask-document")
@limiter.limit("10/minute")
async def ask_document(
    request: Request,
    message: str = Form("Analyse ce document"),
    conversation_id: int = Form(...),
    file: UploadFile = File(...),
    user=Depends(get_current_user),
):
    _owned_conversation_or_404(conversation_id, user["id"])

    file_bytes = await file.read()
    mime_type = file.content_type
    response = chatbot.read_document(message, file_bytes, mime_type)

    db.add_message(conversation_id, "user", f"[Document envoyé] {message}")
    db.add_message(conversation_id, "assistant", response)

    return {"reply": response}


@app.get("/")
async def root():
    return {"message": "Serveur FastAPI actif. Utilise POST /ask pour parler au bot."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
