from PySide6.QtWidgets import QMessageBox, QPushButton
from PySide6.QtCore import Qt, QTimer


def message_box(msg_text, msg_quest, msg_ico, time_out=None, parent=None):

    
    btn_ok = QPushButton("Ok")
    btn_ok.setFixedSize(80, 20)
    btn_ok.setContentsMargins(10, 10, 50, 5)
    btn_cancel = QPushButton("Cancelar")
    btn_cancel.setFixedSize(70,20)
    btn_cancel.setContentsMargins(50, 10, 10, 5)
    msg_box = QMessageBox(parent=parent)
    msg_box.setTextFormat(Qt.RichText)
    msg_box.setObjectName("s_msg_box")
    msg_box.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
    msg_box.setText(f'<h3><center>{msg_text}</center></h3>')
    msg_box.setInformativeText(f'<p><center>{msg_quest}</center></p>')
    msg_box.setWindowTitle("LaViDa")
    msg_box.setContentsMargins(10, 10, 10, 10)
    msg_box.addButton(btn_ok, QMessageBox.ButtonRole.AcceptRole)
    msg_box.addButton(btn_cancel, QMessageBox.ButtonRole.RejectRole)

    msg_box.adjustSize()
    if msg_ico == "info":
        msg_box.setIcon(QMessageBox.Information)
    if msg_ico == "crit":
        msg_box.setIcon(QMessageBox.Critical)
    if msg_ico == "warn":
        msg_box.setIcon(QMessageBox.Warning)
        #Insert more conditions if necessary "Warning, Question, or custom"

    if not time_out:
        msg_box.exec()
        return msg_box.clickedButton() is btn_ok
    
    close_by_timer = True
    
    def _on_button_clicked():
        nonlocal close_by_timer
        close_by_timer = False

    btn_ok.clicked.connect(_on_button_clicked)
    btn_cancel.clicked.connect(_on_button_clicked)

    msg_timer = QTimer()
    msg_timer.setInterval(time_out * 1000)
    msg_timer.setSingleShot(True)
    msg_timer.timeout.connect(msg_box.close)
    msg_timer.start()

    msg_box.exec()
    
    if close_by_timer:
        return True
    
    return msg_box.clickedButton() is btn_ok




