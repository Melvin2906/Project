from PyPDF2 import PdfReader, PdfWriter

# pdf_writer = PdfWriter()
# for pdf in ["test(1).pdf", "test(2).pdf", "test(3).pdf"]:
#     pdf_reader = PdfReader(pdf)
#     for part in range(len(pdf_reader.pages)):
#         print(part)
#         pdf_writer.add_page(pdf_reader.pages[part])

# pdf_writer.encrypt("this is the merged file")

# with open("merge.pdf", "wb") as out:
#     pdf_writer.write(out)

pdf_reader = PdfReader("test(3).pdf")

for part in range(len(pdf_reader.pages)):
    print(pdf_reader.pages[part].extract_text())