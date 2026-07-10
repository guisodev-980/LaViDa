import sys
from PySide6.QtWidgets import QLabel, QVBoxLayout, QDialog, QApplication, QFrame
from PySide6.QtCore import Qt, QSize,  QTimer
from PySide6.QtGui import QPixmap

from data import models

class Welcome_Screen(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.texts = ["Lendo os arquivos",
                      "Carregando os videos",
                      "Gravando os dados",
                      "Gerando as imagens",
                      "Estamos preparando tudo pra você"]
        
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(250,290)
        self.center_on_screen()

        self.ui_welcome_screen()

    def ui_welcome_screen(self):
        self.setup_labels()
        self.setup_frames()
        self.setup_layout()
        self.start_text_cycle()

    def setup_labels(self):
        self.pmap_logo = QPixmap(f'{models.Const_Vars.PATH_TO_IMGS}La viDa identidade-01.png').scaled(QSize(150, 150), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.lbl_logo = QLabel(pixmap=self.pmap_logo, alignment=Qt.AlignCenter)
        self.lbl_welc_text = QLabel(f'Aguarde!\n{self.texts[len(self.texts)-1]}...', alignment=Qt.AlignCenter)
        self.lbl_version = QLabel(f'Versão: {models.Const_Vars.VERSION}', alignment=Qt.AlignRight)
    
    def setup_frames(self):
        self.frm_logo = QFrame()
        self.frm_logo_v_Layout = QVBoxLayout()
        self.frm_logo_v_Layout.addWidget(self.lbl_logo)
        self.frm_logo.setLayout(self.frm_logo_v_Layout)
        self.frm_text = QFrame()
        self.frm_text_v_layout = QVBoxLayout()
        self.frm_text_v_layout.addWidget(self.lbl_welc_text)
        self.frm_text.setLayout(self.frm_text_v_layout)

    def setup_layout(self):
        self.v_layout_welc = QVBoxLayout()
        self.v_layout_welc.addWidget(self.frm_logo)
        self.v_layout_welc.addWidget(self.frm_text)
        self.v_layout_welc.addWidget(self.lbl_version)

        self.setLayout(self.v_layout_welc)

    def center_on_screen(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def start_text_cycle(self):
        self._text_new = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_text)
        self.timer.start(1800)
        
    def update_text(self):
        self.lbl_welc_text.setText(f'Aguarde!\n{self.texts[self._text_new]}...')
        self._text_new = (self._text_new +1) %len(self.texts)

    def closeEvent(self, event):
        if hasattr(self, "timer"):
            self.timer.stop()
        return super().closeEvent(event)
    
