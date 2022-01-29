from tkinter import *
import os
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from PyPDF2 import PdfFileWriter, PdfFileReader


def split_a_pdf(pdfname):
    inputpdf = PdfFileReader(open(pdfname, "rb"))
    for i in range(inputpdf.numPages):
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        fn           = pdfname.split(".")[0] + "_page" + str(i) + ".pdf"
        update_label = Label(root, text="page " + str(i))
        update_label.pack()
        with open(fn, "wb") as outputStream:
            output.write(outputStream)


# os.system("clear")

root = Tk()
root.title("PDF Splitter")
root.geometry("400x600")


myLabel = Label(root, text="Pick some PDFs to split:")


def update(file_name):
    update_label = Label(root, text="Splitting file " + file_name, anchor="w")
    update_label.pack()


def select_files():
    filetypes = (("pdfs", "*.pdf"), ("All files", "*.*"))
    filenames = fd.askopenfilenames(title="Open files", initialdir="/", filetypes=filetypes)
    for fn in filenames:
        update(fn)
        split_a_pdf(fn)


# open button
open_button = ttk.Button(root, text="Select PDF files to split", command=select_files)

open_button.pack(expand=True)


root.mainloop()

# myTextBox = Entry(root, width=50)
# myTextBox.pack()
# myButton = Button(root, text="click me", command=hello)
# myButton.pack()
