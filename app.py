from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget, QFileDialog,
    QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox)
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtCore import Qt

import pandas as pd

import os

import generar_pdf

class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.resize(371, 447)

        self.VLAYOUT_widget = QVBoxLayout(self)
        self.VLAYOUT_widget.setObjectName(u"VLAYOUT_widget")

        self.tabwidget = QTabWidget(self)
        self.tabwidget.setObjectName(u"tabwidget")

        self.tab1 = QWidget()
        self.tab1.setObjectName(u"tab1")

        self.VLAYOUT_tab1 = QVBoxLayout(self.tab1)
        self.VLAYOUT_tab1.setObjectName(u"VLAYOUT_tab1")

        self.txt_introduzca = QLabel(self.tab1)
        self.txt_introduzca.setObjectName(u"txt_introduzca")
        self.txt_introduzca.setText("Introduzca un archivo .csv")

        self.VLAYOUT_tab1.addWidget(self.txt_introduzca)

        self.HLAYOUT_csv = QHBoxLayout()
        self.HLAYOUT_csv.setObjectName(u"HLAYOUT_csv")

        self.insert_csv_file = QLineEdit(self.tab1)
        self.insert_csv_file.setObjectName(u"insert_csv_file")
        self.insert_csv_file.setText("")
        self.insert_csv_file.setEnabled(False)

        self.HLAYOUT_csv.addWidget(self.insert_csv_file)

        self.btn_browse_csv = QPushButton(self.tab1)
        self.btn_browse_csv.setObjectName(u"btn_browse_csv")
        self.btn_browse_csv.setText("Buscar")
        self.btn_browse_csv.clicked.connect(self.open_file)

        self.HLAYOUT_csv.addWidget(self.btn_browse_csv)

        self.VLAYOUT_tab1.addLayout(self.HLAYOUT_csv)

        self.txt_select = QLabel(self.tab1)
        self.txt_select.setObjectName(u"txt_select")
        self.txt_select.setText("Seleccione un paciente cuyo reporte desea generar.")
        self.VLAYOUT_tab1.addWidget(self.txt_select)

        self.cbox_patients = QComboBox(self.tab1)
        self.cbox_patients.addItem("Test1")
        self.cbox_patients.addItem("Test2")
        self.cbox_patients.addItem("Test3")
        self.cbox_patients.setObjectName(u"cbox_patients")

        self.VLAYOUT_tab1.addWidget(self.cbox_patients)

        self.txt_receta = QLabel(self.tab1)
        self.txt_receta.setObjectName(u"txt_receta")
        self.txt_receta.setText("Receta médica:")

        self.VLAYOUT_tab1.addWidget(self.txt_receta)

        self.tedit_receta = QTextEdit(self.tab1)
        self.tedit_receta.setObjectName(u"tedit_receta")
        self.tedit_receta.setText("1\n2\n3\n")

        self.VLAYOUT_tab1.addWidget(self.tedit_receta)

        self.tabwidget.addTab(self.tab1, "Tab 1")
        self.tab2 = QWidget()
        self.tab2.setObjectName(u"tab2")
        self.VLAYOUT_tab2 = QVBoxLayout(self.tab2)
        self.VLAYOUT_tab2.setObjectName(u"VLAYOUT_tab2")
        self.tabwidget.addTab(self.tab2, "Tab 2")

        self.VLAYOUT_widget.addWidget(self.tabwidget)

        self.btn_generate = QPushButton(self)
        self.btn_generate.setObjectName(u"btn_generate")
        self.btn_generate.setText("Generar PDF")

        self.VLAYOUT_widget.addWidget(self.btn_generate)

        self.tabwidget.setCurrentIndex(0)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Abrir archivo .CSV", "", "Archivos .csv (*.csv)"
        )
        if filename:
            df = pd.read_csv(filename)
            basename = os.path.basename(filename)
            self.insert_csv_file.setText(basename)
            self.insert_csv_file.setStyleSheet("background-color: #dbdbdb; color: black;")
            msg = 'Archivo cargado exitosamente.'
            msgbox = Mensaje(msg)
            print(df)

    
            
class Mensaje(QMessageBox):
    def __init__(self, message):
        super().__init__()

        self.setIcon(QMessageBox.Information)
        self.setText(message)
        self.setWindowTitle("Atención!")
        self.setStandardButtons(QMessageBox.Ok)
        self.exec()

app = QApplication()
w = MainWindow()
w.show()
app.exec()