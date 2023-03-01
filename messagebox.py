from PySide6.QtWidgets import QMessageBox

class Mensaje(QMessageBox):
    def __init__(self, message : str, icon : QMessageBox.Icon = QMessageBox.Information):
        super().__init__()

        self.setIcon(icon)
        self.setText(message)
        self.setWindowTitle("Atención!")
        self.setStandardButtons(QMessageBox.Ok)
        self.exec()
