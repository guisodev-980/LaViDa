from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QProgressBar
from PySide6.QtCore import Qt, QTimer, Signal


class Wait_Dialog(QDialog):
    cancelled = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog | Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.ApplicationModal)

        self.setup_ui()
        self.btn_cancel.clicked.connect(self._cancel)

    def setup_ui(self):
        self.setup_components()
        self.setup_layout()
        self.ani_timer()

    def setup_components(self):
        self.lbl_message = QLabel("Processando....")
        self.lbl_message.setAlignment(Qt.AlignCenter)
        self.btn_cancel = QPushButton("Cancel")
        self.prg_bar = QProgressBar()
        self.prg_bar.setVisible(True)
        self.prg_bar.setRange(0, 0)
    
    def setup_layout(self):
        self.v_layout = QVBoxLayout()
        self.v_layout.setContentsMargins(30, 20, 30, 20)
        self.v_layout.setSpacing(15)
        self.v_layout.addWidget(self.lbl_message)
        self.v_layout.addWidget(self.prg_bar)
        self.v_layout.addWidget(self.btn_cancel)
        self.setLayout(self.v_layout)

    def ani_timer(self):
        self._dots = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.ani_text)
        self.timer.start(400)

    def ani_text(self):
        self._dots = (self._dots + 1) % 4
        base = self.lbl_message.text().split('.')[0]
        self.lbl_message.setText(base + '.' * self._dots)

    def set_progress(self, current, total):
        if not self.prg_bar.isVisible():
            self.prg_bar.setVisible(True)
            self.prg_bar.setRange(0, total)
        self.prg_bar.setValue(current)
        self.lbl_message.setText(f"Processando vídeo {current} de {total}...")

    def closeEvent(self, event):
        self.timer.stop()
        super().closeEvent(event)

    def _cancel(self):
        self.cancelled.emit()