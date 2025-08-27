import yt_dlp

def telecharger_video(url, dossier_sortie="./Videos"):
    options = {
        'outtmpl': f'{dossier_sortie}/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'cookies': 'cookies.txt',  # Le fichier exporté
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

lien = input("Entrez le lien de la vidéo : ")
telecharger_video(lien)
