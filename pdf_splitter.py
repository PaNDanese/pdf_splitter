from tkinter import *
import os
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from PyPDF2 import PdfFileWriter, PdfFileReader

# pyinstaller.exe --noconsole --onefile pdf_splitter.py


def split_a_pdf(pdfname, num_pages):
    start_page      = 0
    inputpdf        = PdfFileReader(open(pdfname, "rb"))
    number_of_pages = inputpdf.getNumPages()
    while start_page < number_of_pages:
        output = PdfFileWriter()
        for page in range(0, num_pages):
            if start_page + page < number_of_pages:
                cp = start_page + page
                output.addPage(inputpdf.getPage(cp))
        fn = pdfname.split(".")[0] + "_page" + str(start_page) + ".pdf"
        start_page += num_pages
        update_label = Label(root, text="page " + str(start_page))
        update_label.pack()
        with open(fn, "wb") as outputStream:
            output.write(outputStream)


root = Tk()
root.title("PDF Splitter")
root.geometry("400x600")


OPTIONS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # etc


variable = StringVar(root)
variable.set(OPTIONS[0])  # default value

w = OptionMenu(root, variable, *OPTIONS)
w.place(x=68, y=70)
# w.pack()


label_2 = Label(root, text="How many pages split PDF?", width=30, font=("bold", 10))
label_2.place(x=68, y=50)


myLabel = Label(root, text="Pick some PDFs to split:")


def update(file_name):
    update_label = Label(root, text="Splitting file " + file_name, anchor="w")
    update_label.pack()


def select_files():
    filetypes = (("pdfs", "*.pdf"), ("All files", "*.*"))
    filenames = fd.askopenfilenames(title="Open files", initialdir="/", filetypes=filetypes)
    for fn in filenames:
        update(fn)
        split_a_pdf(fn, int(variable.get()))


# open button
open_button = ttk.Button(root, text="Select PDF files to split", command=select_files)

open_button.pack(expand=True)


root.mainloop()

# myTextBox = Entry(root, width=50)
# myTextBox.pack()
# myButton = Button(root, text="click me", command=hello)
# myButton.pack()
