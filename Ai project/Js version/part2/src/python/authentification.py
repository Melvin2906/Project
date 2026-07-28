import os
import jwt

# Doit être EXACTEMENT la même valeur que JWT_SECRET_KEY côté serveur Node
# (server.js) : c'est lui qui émet les tokens, l'API Python se contente de
# les vérifier — une seule base d'utilisateurs (MySQL, gérée par Node).
JWT_SECRET = os.environ.get("JWT_SECRET_KEY")
if not JWT_SECRET:
    raise RuntimeError(
        "JWT_SECRET_KEY manquant : il doit avoir la même valeur que côté "
        "serveur Node (server.js), sinon les tokens ne seront jamais valides ici."
    )

JWT_ALGORITHM = "HS256"


def decode_token(token):
    """Vérifie un token émis par le serveur Node. Retourne le payload
    ({'id':.., 'username':.., 'email':..}) ou lève ValueError si invalide."""
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expiré, reconnecte-toi")
    except jwt.InvalidTokenError:
        raise ValueError("Token invalide")
