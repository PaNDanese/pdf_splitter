from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QPushButton,
    QComboBox,
    QFileDialog,
    QLabel,
    QProgressBar,
)
from PyQt5 import uic, QtCore
from PyQt5.QtCore import pyqtSignal
import sys
from PyPDF2 import PdfFileWriter, PdfFileReader
from splitter import Ui_MainWindow
import qdarkstyle
import time

# pyuic5 -x splitter.ui -o splitter.py
# pyinstaller.exe --noconsole --onefile pdf_splitterqt.py


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.file_names = ""
        # uic.loadUi("splitter.ui", self)
        self.button = self.findChild(QPushButton, "pushButton")
        self.label  = self.findChild(QLabel     , "label")
        self.combo  = self.findChild(QComboBox  , "comboBox")
        self.combo.addItems(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
        self.label_2      = self.findChild(QLabel      , "label_2")
        self.label_3      = self.findChild(QLabel      , "label_3")
        self.label_4      = self.findChild(QLabel      , "label_4")
        self.button_2     = self.findChild(QPushButton , "pushButton_2")
        self.progress_bar = self.findChild(QProgressBar, "progressBar")
        self.progress_bar.setValue(0)
        self.button.clicked.connect(self.clicker)
        self.button_2.clicked.connect(self.split_em_up)
        self.show()

    def finished_splitting(self):
        self.label_4.setText("Done splitting")
        self.progress_bar.setValue(100)

    def split_a_pdf(self, fn):
        self.label_4.setText("")
        self.label_3.setText("")
        if fn and len(fn) > 0:
            self.worker = ThreadClass(fn, int(self.combo.currentText()))
            self.worker.start()
            self.worker.finished.connect(self.finished_splitting)
            self.worker.most_recent_file.connect(self.label_3.setText)
            self.worker.progress.connect(self.progress_bar.setValue)
        else:
            self.label_3.setText("Nothing to split")
            self.progress_bar.setValue(0)

    def split_em_up(self):
        fns = self.file_names.split(",")
        fns = [x.strip() for x in fns]
        for fn in fns:
            self.split_a_pdf(fn)

    def clicker(self):
        fname = QFileDialog.getOpenFileName(self, "Select PDF File", "", "PDF files (*.pdf)")
        fname = list(fname)
        names = "No file selected"
        if fname and len(fname[0]) > 0:
            names           = fname[0]
            self.file_names = names
            self.label_2.setText("File to split: " + names)
        else:
            self.label_2.setText("No file selected")
            self.label_3.setText("")
            self.label_4.setText("")
            self.file_names = ""


class ThreadClass(QtCore.QThread):
    most_recent_file = pyqtSignal(str)
    progress         = pyqtSignal(int)

    def __init__(self, file_name, num_pages):
        super(ThreadClass, self).__init__()
        self.file_name = file_name
        self.num_pages = num_pages

    def run(self):
        pdfname = self.file_name
        if pdfname and len(pdfname) > 0:
            num_pages       = self.num_pages
            start_page      = 0
            inputpdf        = PdfFileReader(open(pdfname, "rb"))
            number_of_pages = inputpdf.getNumPages()
            while start_page < number_of_pages:
                output = PdfFileWriter()
                for page in range(0, num_pages):
                    if start_page + page < number_of_pages:
                        cp = start_page + page
                        output.addPage(inputpdf.getPage(cp))
                fn = pdfname.split(".")[0] + "_page_" + str(start_page) + ".pdf"
                self.most_recent_file.emit("Splitting ... " + fn)
                start_page += num_pages
                prog = 100 * float(start_page) / float(number_of_pages)
                prog = int(prog)
                self.progress.emit(prog)
                with open(fn, "wb") as outputStream:
                    output.write(outputStream)


app = QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
UIWindow = UI()
app.exec_()
