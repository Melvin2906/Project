import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pygame import mixer
import threading
from tkinter.simpledialog import askstring
from yt_dlp import YoutubeDL

# Initialisation de pygame mixer
mixer.init()

# Chemin par défaut
MUSIC_DIR = "C:/Users/Utilisateur/Music"

class SpotifyClone:
    def __init__(self, root):
        self.root = root
        self.root.title("PySpotify")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        self.playlist = []
        self.current_track = None
        self.is_playing = False

        self.check_music_end()
        self.create_widgets()
        self.load_local_music()

    def create_widgets(self):
        # Label
        self.track_label = tk.Label(self.root, text="Aucune musique", wraplength=350)
        self.track_label.pack(pady=20)

        # Playlist box
        self.listbox = tk.Listbox(self.root, width=50, height=15)
        self.listbox.pack()

        # Boutons de contrôle
        controls = tk.Frame(self.root)
        controls.pack(pady=20)

        tk.Button(controls, text="▶️ Play", width=8, command=self.play_music).grid(row=0, column=0, padx=5)
        tk.Button(controls, text="⏸️ Pause", width=8, command=self.pause_music).grid(row=0, column=1, padx=5)
        tk.Button(controls, text="⏹️ Stop", width=8, command=self.stop_music).grid(row=0, column=2, padx=5)
        tk.Button(controls, text="⏭️ Next", width=8, command=self.next_music).grid(row=0, column=3, padx=5)
        tk.Button(self.root, text="🌐 Rechercher sur YouTube", command=self.search_and_download).pack(pady=5)

        # Ajouter musique
        tk.Button(self.root, text="➕ Ajouter musique", command=self.add_music).pack(pady=10)

    def load_local_music(self):
        if not os.path.exists(MUSIC_DIR):
            os.makedirs(MUSIC_DIR)

        files = os.listdir(MUSIC_DIR)
        self.playlist = [f for f in files if f.endswith((".mp3", ".wav"))]
        self.listbox.delete(0, tk.END)
        for song in self.playlist:
            self.listbox.insert(tk.END, song)

    def play_music(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showinfo("Info", "Sélectionne une musique.")
            return

        song = self.playlist[selected[0]]
        self.current_track = os.path.join(MUSIC_DIR, song)

        try:
            mixer.music.load(self.current_track)
            mixer.music.play()
            self.track_label.config(text=f"🎵 En cours : {song}")
            self.is_playing = True
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def pause_music(self):
        if self.is_playing:
            mixer.music.pause()
            self.is_playing = False
        else:
            mixer.music.unpause()
            self.is_playing = True

    def stop_music(self):
        mixer.music.stop()
        self.track_label.config(text="Aucune musique")
        self.is_playing = False

    def next_music(self):
        current_index = self.listbox.curselection()
        if current_index:
            next_index = (current_index[0] + 1) % len(self.playlist)
            self.listbox.select_clear(0, tk.END)
            self.listbox.select_set(next_index)
            self.play_music()
    def check_music_end(self):
        if self.is_playing and not mixer.music.get_busy():
            self.next_music()
        self.root.after(1000, self.check_music_end)  # Vérifie toutes les secondes

    def add_music(self):
        filetypes = [("Fichiers audio", "*.mp3 *.wav")]
        files = filedialog.askopenfilenames(title="Choisir musique", filetypes=filetypes)
        for file in files:
            try:
                filename = os.path.basename(file)
                dest = os.path.join(MUSIC_DIR, filename)
                if not os.path.exists(dest):
                    with open(file, "rb") as src, open(dest, "wb") as dst:
                        dst.write(src.read())
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'ajouter : {e}")
        self.load_local_music()

    def search_and_download(self):
        query = askstring("Rechercher", "Entrez le nom d'une chanson :")
        if not query:
            return
        threading.Thread(target=self.download_music, args=(query,), daemon=True).start()

    def download_music(self, query):
        self.track_label.config(text="🔍 Recherche et téléchargement...")

        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'outtmpl': os.path.join(MUSIC_DIR, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch1:{query}", download=True)
                title = info['entries'][0]['title']
                self.track_label.config(text=f"✅ Téléchargé : {title}")
        except Exception as e:
            self.track_label.config(text="❌ Erreur lors du téléchargement")
            messagebox.showerror("Erreur", str(e))

        self.load_local_music()


if __name__ == "__main__":
    root = tk.Tk()
    app = SpotifyClone(root)
    root.mainloop()
