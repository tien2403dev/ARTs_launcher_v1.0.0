from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton
)
from PyQt5.QtCore import Qt


class LauncherWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ARTs App")
        self.setFixedSize(420, 180)

        self.lbl_title = QLabel("ARTs App")
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.lbl_title.setStyleSheet(
            "font-size: 18px; font-weight: bold;"
        )

        self.lbl_status = QLabel("Đang kiểm tra phiên bản...")
        self.lbl_status.setAlignment(Qt.AlignCenter)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)

        self.btn_close = QPushButton("Đóng")
        self.btn_close.clicked.connect(self.close)
        self.btn_close.hide()

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_title)
        layout.addWidget(self.lbl_status)
        layout.addWidget(self.progress)
        layout.addWidget(self.btn_close)

        self.setLayout(layout)

    def set_status(self, text):
        self.lbl_status.setText(text)

    def set_error(self, text):
        self.progress.hide()
        self.lbl_status.setText(text)
        self.btn_close.show()

    def set_done(self, text):
        self.progress.hide()
        self.lbl_status.setText(text)