from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QComboBox, QFileDialog, QLabel
from PyQt5 import uic
import sys
from PyPDF2 import PdfFileWriter, PdfFileReader
from splitter import Ui_MainWindow
import qdarkstyle

# pyuic5 -x splitter.ui -o splitter.py
# pyinstaller.exe --noconsole --onefile pdf_splitterQT.py


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # uic.loadUi("splitter.ui", self)
        self.button = self.findChild(QPushButton, "pushButton")
        self.label  = self.findChild(QLabel     , "label")
        self.combo  = self.findChild(QComboBox  , "comboBox")
        self.combo.addItems(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
        self.label_2 = self.findChild(QLabel, "label_2")
        self.button.clicked.connect(self.clicker)
        self.show()

    def split_a_pdf(self):
        pdfname = self.label_2.text()
        if pdfname and len(pdfname) > 0:
            num_pages       = int(self.combo.currentText())
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
                self.label_2.setText(fn)
                start_page += num_pages
                with open(fn, "wb") as outputStream:
                    output.write(outputStream)

    def clicker(self):
        fname = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF files (*.pdf)")
        self.label_2.setText("splitting ...")
        if fname:
            if len(fname[0]) > 0:
                self.label_2.setText(fname[0])
                self.split_a_pdf()
                self.label_2.setText("done splitting: " + fname[0])
            else:
                self.label_2.setText("no file selected")
        else:
            self.label_2.setText("not splitting anything.")


app = QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
UIWindow = UI()
app.exec_()

# app = QApplication([])
# app.setStyle('Fusion')
# cb = QComboBox()
# cb.addItems(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])

# dlg = QFileDialog()
# dlg.setFileMode(QFileDialog.AnyFile)
# # dlg.setFilter("Text files (*.txt)")
# # filenames = QStringList()
# #    if dlg.exec_():
# #       filenames = dlg.selectedFiles()


# window = QWidget()
# layout = QVBoxLayout()
# layout.addWidget(QPushButton('Top'))
# # layout.addWidget(QPushButton('Bottom'))
# layout.addWidget(cb)
# layout.addWidget(dlg)
# window.setLayout(layout)
# window.show()
# app.exec()
