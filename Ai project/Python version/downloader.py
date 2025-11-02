import yt_dlp
import sys

def telecharger_video(url, dossier_sortie="./Videos"):
    options = {
        'outtmpl': f'{dossier_sortie}/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'cookies': 'cookies.txt',  # Le fichier exporté
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

def main(lien):
    for i in range(len(lien)):
        telecharger_video(lien[i])

if __name__ == "__main__":
    lien = input("Saisissez vos liens : ").split(" ")

    if lien[0] == "exit" or lien[0] == "quit":
        sys.exit(0)
    else:
        main(lien)