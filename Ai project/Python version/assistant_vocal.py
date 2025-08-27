import customtkinter as ctk
from youtube_search import YoutubeSearch
import speech_recognition as sr
import webbrowser
# permet à la machine de "parler"
import pyttsx3
# Initialiser l'application

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("My little vocal assisatant")
app.geometry("500x400")

# Initialise la reconnaissance vocale et la synthèse vocale
recognizer = sr.Recognizer()
engine = pyttsx3.init()


# Fonction pour parler (synthèse vocale)
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Fonction pour écouter et reconnaître la voix
def recognize_speech():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("\033[1;31mParlez maintenant\033[0m")
        
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio, language="fr-FR")
            print(f"Vous avez dit: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Je n'ai pas compris, répétez s'il vous plaît")
            return recognize_speech()
        except sr.RequestError:
            speak("Erreur de connexion")
            return ""

def in_word(words, cmd):
    for word in words:
        if word in cmd:
            return 1, word
        else:
            continue
    return 0, ""

# Fonction pour exécuter des commandes vocales
def execute_command():
    cmd = recognize_speech()
    order = ["joue", "cherche", "play", "lance", "find"]
    order2 = ["mets-toi en veille", "repose toi", "ferme", "quit", "exit", "c'est bon tu me saoules"]
    verif, its = in_word(order, cmd)
    verif2 = in_word(order2, cmd)
    sites = {
        "youtube": "https://www.youtube.com/",
        "instagram": "https://www.instagram.com/",
        "you": "https://www.youtube.com/",
        "spotify": "https://open.spotify.com/",
        "l'intra": "https://intra.epitech.eu/",
        "l'intranet": "https://intra.epitech.eu/",
        "mon my epitech": "https://my.epitech.eu/",
        "movie box": "https://moviebox.ng/fr",
        "datacamp": "https://app.datacamp.com/",
        "chat gpt": "https://chatgpt.com/",
        "github": "https://github.com/",
    }

    if verif == 1:
        song_name = cmd.replace(its, "").strip()
        speak(f"Recherche de {song_name} sur Youtube.")

        # Recher Youtube
        results = YoutubeSearch(song_name, max_results=1).to_dict()
        if results:
            video_url = f"https://www.youtube.com/watch?v={results[0]['id']}"
            speak(f"Lecture de {results[0]['title']}.")
            webbrowser.open(video_url)
        else:
            speak("Aucune vidéo trouvée")
    elif "ouvre" in cmd:
        site = cmd.replace("ouvre", "").strip()
        speak(f"Ouverture de {site}.")
        if site in sites.keys():
            webbrowser.open(sites[site])
        else:
            print("Sorry, nous ne reconnaissons pas cette plateform")
            return ""
    elif verif2[0] == 1:
        speak("Fermeture de l'application")
        app.quit()
    else:
        speak("Command non reconnue, essayez encore")

# Label d'instructions

label = ctk.CTkLabel(app, text='Cliquez sur le bouton pour écouter une commande', font=("Helvetica", 16))
label.pack(pady=30)

# Bouton pour activer la reconnaissance vocale

ecoute = ctk.CTkButton(app, text='Ecouter', command=execute_command, font=("Arial", 14), height=50, width=200)
ecoute.pack(pady=20)

# Bouton pour quitter l'application

ex_btn = ctk.CTkButton(app, text="Quitter...", command=app.quit, font=("TimesNewRomans", 16), height=30, width=150, fg_color="green", hover_color="red")
ex_btn.pack(pady=40)

app.mainloop()