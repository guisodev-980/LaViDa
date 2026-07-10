import sys
from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame, QCheckBox, QComboBox, QHeaderView, QCompleter
from PySide6.QtCore import Qt

from data import models
from services import data_manager
from screens import pop_messages
import re, unicodedata


class Cad_Video(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setFixedSize(1100, 500)

        self.test_group = set()
        self.group_completer = QCompleter(sorted(self.test_group))
        self.group_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.subject_group = set()
        self.sub_completer = QCompleter(sorted(self.subject_group))
        self.sub_completer.setCaseSensitivity(Qt.CaseInsensitive)

        self.ui_cad_video_dialog()
        self.fill_table()

        #Connections
        self.btn_close.clicked.connect(self.cad_close)
        self.video_tab.clicked.connect(self.get_selected_item)
        self.btn_save.clicked.connect(self.save_video_data)
        self.ckb_filter.clicked.connect(self.fill_table)

        #Setup UI
    def ui_cad_video_dialog(self):
        self.setup_labels()
        self.setup_btns()
        self.setup_inputs()
        self.setup_misc()
        self.setup_frames()
        self.setup_layout()

    def setup_labels(self):
        self.lbl_title = QLabel("Cadastro de Vídeos")
        self.lbl_title.setStyleSheet("font-size: 16px")
        self.lbl_tab_title = QLabel("Vídeos")
        self.lbl_cad_title = QLabel("Dados Necessários")
        self.lbl_video_name = QLabel("Video:")
        self.lbl_video_test = QLabel("Teste:")
        self.lbl_video_subject = QLabel("Sujeito:")
        self.lbl_video_group = QLabel("Grupo:")
        self.lbl_video_day = QLabel("Dia:")
        self.lbl_video_try_n = QLabel("Tentativa:")
        self.lbl_cad_by = QLabel("Cad Por:")

    def setup_inputs(self):
        self.txt_video_name = QLineEdit()
        self.txt_video_name.setEnabled(False)
        self.txt_video_name.setStyleSheet("color: black")
        self.txt_video_subject = QLineEdit()
        self.txt_video_subject.setCompleter(self.sub_completer)
        self.txt_video_group = QLineEdit()
        self.txt_video_group.setCompleter(self.group_completer)
        self.txt_video_day = QLineEdit()
        self.txt_video_try_n = QLineEdit()
        self.txt_cad_by = QLineEdit()
        self.txt_cad_by.setEnabled(False)
        self.txt_cad_by.setStyleSheet("color: black")

    def setup_btns(self):
        self.btn_save = QPushButton("Salvar")
        self.btn_save.setFixedSize(100, 30)
        self.btn_close = QPushButton("Fechar")
        self.btn_close.setFixedSize(100, 30)

    def setup_misc(self):

        self.video_tab = QTableWidget()
        self.tab_headers = ["Teste", "Sujeito", "Grupo", "Dia", "Tentativa", "Arquivo", "Status", "Cad Por"]
        self.video_tab.setColumnCount(len(self.tab_headers))
        self.video_tab.setHorizontalHeaderLabels(self.tab_headers)
        self.video_tab.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.video_tab.setEditTriggers(QTableWidget.NoEditTriggers)  # Avoid Item Table Edit
        self.video_tab.setSelectionBehavior(QTableWidget.SelectRows)
        self.video_tab.setSelectionMode(QTableWidget.SingleSelection) # Force One Row Selection
        self.video_tab.setSortingEnabled(True)
        self.ckb_filter = QCheckBox("Não Cadastrados")
        self.cbx_test = QComboBox()
        test_types = ["Sem Cad", "Nado", "Probatorio"]
        self.cbx_test.addItems(test_types)

    def setup_frames(self):
        #Header
        self.frm_header = QFrame()
        self.frm_header_v_layout = QVBoxLayout()
        self.frm_header_v_layout.addWidget(self.lbl_title, alignment=Qt.AlignCenter)
        self.frm_header.setLayout(self.frm_header_v_layout)

        #Table
        self.frm_tab = QFrame()
        self.frm_tab.setFixedWidth(800)
        self.frm_tab_v_Layout = QVBoxLayout()
        self.frm_tab_v_Layout.addWidget(self.lbl_tab_title, alignment=Qt.AlignCenter)
        self.frm_tab_v_Layout.addWidget(self.ckb_filter, alignment=Qt.AlignRight)
        self.frm_tab_v_Layout.addWidget(self.video_tab)
        self.frm_tab.setLayout(self.frm_tab_v_Layout)

        #Entry Data
        self.frm_data = QFrame()
        self.frm_data_g_layout = QGridLayout()
        self.frm_data_g_layout.setVerticalSpacing(20)
        self.frm_data_g_layout.setAlignment(Qt.AlignTop)
        self.frm_data_g_layout.addWidget(self.lbl_cad_title, 0, 0, 1, 3, alignment=Qt.AlignCenter | Qt.AlignTop)
        self.frm_data_g_layout.setRowMinimumHeight(0, 100)
        self.frm_data_g_layout.addWidget(self.lbl_video_name, 2, 0)
        self.frm_data_g_layout.addWidget(self.txt_video_name, 2, 1, 1, 2)
        self.frm_data_g_layout.addWidget(self.lbl_video_test, 3, 0)
        self.frm_data_g_layout.addWidget(self.cbx_test, 3, 1, 1, 2)
        self.frm_data_g_layout.addWidget(self.lbl_video_subject, 4, 0)
        self.frm_data_g_layout.addWidget(self.txt_video_subject, 4, 1, 1, 2)
        self.frm_data_g_layout.addWidget(self.lbl_video_group, 5, 0)
        self.frm_data_g_layout.addWidget(self.txt_video_group, 5, 1, 1, 2)
        self.frm_data_g_layout.addWidget(self.lbl_video_day, 6, 0)
        self.frm_data_g_layout.addWidget(self.txt_video_day, 6, 1, 1, 2)
        self.frm_data_g_layout.addWidget(self.lbl_video_try_n, 7, 0)
        self.frm_data_g_layout.addWidget(self.txt_video_try_n, 7, 1, 1, 2)
        self.frm_data_g_layout.addWidget(self.lbl_cad_by, 8, 0)
        self.frm_data_g_layout.addWidget(self.txt_cad_by, 8, 1, 1, 2)
        self.frm_data_g_layout.addWidget(self.btn_save, 9, 1)
        self.frm_data_g_layout.addWidget(self.btn_close, 9, 2)
        self.frm_data_g_layout.setRowStretch(7, 1)
        self.frm_data.setLayout(self.frm_data_g_layout)

    def setup_layout(self):
        self.v_layout = QVBoxLayout()
        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(self.frm_tab)
        self.h_layout.addWidget(self.frm_data)

        self.v_layout.addWidget(self.frm_header)
        self.v_layout.addLayout(self.h_layout)
        self.setLayout(self.v_layout)

    def fill_table(self):
        video_data = data_manager.get_video_data()
        video_files = data_manager.get_exists_files()
        self.video_tab.setRowCount(0)
        row = 0
        for test, subject, group, day, try_n, video, status, cad_by in video_data:
            if not video in video_files:
                continue

            if not data_manager.is_video_cad(video):
                test = "-"
                subject = "-"
                group = "-"
                day = "0"
                try_n = "0"

            if self.ckb_filter.isChecked() and not cad_by == "No_Cad":
                continue
            self.video_tab.insertRow(row)
            self.video_tab.setItem(row, 0, QTableWidgetItem(test))
            self.video_tab.setItem(row, 1, QTableWidgetItem(subject))
            self.video_tab.setItem(row, 2, QTableWidgetItem(group))
            self.video_tab.setItem(row, 3, QTableWidgetItem(day))
            self.video_tab.setItem(row, 4, QTableWidgetItem(try_n))
            self.video_tab.setItem(row, 5, QTableWidgetItem(video))
            self.video_tab.setItem(row, 6, QTableWidgetItem(status))
            self.video_tab.setItem(row, 7, QTableWidgetItem(cad_by))
            if not group == "No_Cad_Group":
                self.test_group.add(group)
            if not subject == "No_Cad_Sub":
                self.subject_group.add(subject)
        self.group_completer.model().setStringList(sorted(self.test_group))
        self.sub_completer.model().setStringList(sorted(self.subject_group))


    def get_selected_item(self):
        self.txt_video_group.clear()
        self.txt_video_subject.clear()
        self.txt_video_day.clear()
        self.txt_video_try_n.clear()
        self.cbx_test.setCurrentIndex(0)
        selected_row = set()
        selected_file = set()
        for item in self.video_tab.selectedItems():
            selected_row.add(item.row())

        for row in sorted(selected_row):
            test_text = self.video_tab.item(row, 0).text().strip()
            test = test_text != "-"
            self.cbx_test.setStyleSheet("color: red" if not test else "color: black")
            selected_file = self.video_tab.item(row, 5).text()
            file_cad = self.video_tab.item(row, 7).text()
            if selected_file:
                self.txt_video_name.setText(selected_file)
            
            if file_cad == "No_Cad" or file_cad == "":
                file_cad = models.Current_User.user_name
                self.txt_cad_by.setText(file_cad)
            else:
                self.txt_cad_by.setText(file_cad)
            if test:
                self.cbx_test.setCurrentText(test_text)
                self.txt_video_subject.setText(self.video_tab.item(row, 1).text())
                self.txt_video_group.setText(self.video_tab.item(row, 2).text())
                self.txt_video_day.setText(self.video_tab.item(row, 3).text())
                self.txt_video_try_n.setText(self.video_tab.item(row, 4).text())
            

    def save_video_data(self):
        user = models.Current_User.user_name
        existing_files = data_manager.get_exists_files()
        test_index = self.cbx_test.currentIndex()
        has_input = test_index != 0 and self.txt_video_subject.text() and self.txt_video_group.text() and self.txt_video_day.text() and self.txt_video_try_n.text()
        if not has_input:
            pop_messages.message_box("Precisa Preencher Todos os Campos ", "", "info")
            return
        
        video_name = self.txt_video_name.text()
        day = self.txt_video_day.text().strip()
        try_n = self.txt_video_try_n.text().strip()
        test = self.cbx_test.currentText().strip()
        group = self.txt_video_group.text().strip()
        subject = self.txt_video_subject.text().strip()
        cad_by = user
        test_out = "Nado" if test == "Nado" else "Prob"
        _, ext = video_name.split(".")
        raw_name = f"{test_out}-S{subject.lower()}-G{group.lower()}-D{day}-T{try_n}"
        new_name = f"{self.normalize_field(raw_name)}.{ext}"
        if new_name in existing_files:
            pop_messages.message_box("Já Existe esse cadastro ", "Confira todos os campos", "warn")
            return
         
        data_manager.update_video_data(video_name, test, group, day, try_n, subject, cad_by, new_name)
        data_manager.redefine_files(video_name, new_name)
        self.txt_video_group.clear()
        self.txt_video_day.clear()
        self.txt_video_try_n.clear()
        self.txt_video_subject.clear()
        self.cbx_test.setCurrentIndex(0)
        self.fill_table()

    
    def normalize_field(self, s: str) -> str:
        # Remove accent marks
        s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()

        # Change spaces for underlines
        s = s.replace(" ", "_")

        # Remove unwanted files caracter
        s = re.sub(r"[^A-Za-z0-9_\-]", "", s)

        # Avoid Double __
        s = re.sub(r"_+", "_", s)

        return s

    
    def cad_close(self):
        self.accept()
