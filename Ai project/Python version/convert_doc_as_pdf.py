from PyPDF2 import PdfWriter

file = open("assistant_vocal.py", "r")
content = file.read()
print(content)

with open("assistant_vocal.pdf", "wb") as out:
    file.write(out)