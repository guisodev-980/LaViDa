from PySide6.QtWidgets import QLabel, QDialog, QPushButton, QCheckBox, QSpinBox, QVBoxLayout, QHBoxLayout, QFrame, QGridLayout, QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt
from datetime import time
from pathlib import Path
import json

from data import models
from services import data_manager
from screens import pop_messages
from data.models import Const_Vars as Vars


class Schedule_Dialog(QDialog):
    ICON_PATH = "imgs/icons/"
    def __init__(self, parent= None):
       super().__init__(parent)
       self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
       
       self.setFixedSize(900, 600)

       self.ui_schedule_screen()

       self.js_videos = []
       self.unselected_videos = []
       self.selected_videos = models.Current_Js_Data.js_files_to_do.copy()
    
       self.btn_save.clicked.connect(self.sch_save)
       self.btn_cancel.clicked.connect(self.sch_cancel)
       self.btn_clear.clicked.connect(self.sch_clear)
       self.btn_time_edit.clicked.connect(self.time_edit)
       self.btn_add_files.clicked.connect(lambda: self.move_selected(self.tab_files, self.tab_files_to_do, "add"))
       self.btn_rem_files.clicked.connect(lambda: self.move_selected(self.tab_files_to_do, self.tab_files, "rem"))
       self.ckb_filter.clicked.connect(self.fill_table)

    def ui_schedule_screen(self):
        self.setup_labels()
        self.setup_buttons()
        self.setup_misc()
        self.setup_frames()
        self.setup_layout()
        self.set_data_ui()
        self.fill_table()

    def setup_labels(self):
        self.lbl_title = QLabel("Agendamentos", alignment=Qt.AlignCenter)
        self.lbl_time = QLabel("Horário")
        self.lbl_spin_hour = QLabel("Horas")
        self.lbl_spin_min = QLabel("Minutos")
        self.lbl_sched_by = QLabel("Agendado Por: ")

    def setup_buttons(self):
        self.btn_time_edit = QPushButton("Editar")
        self.btn_time_edit.setFixedSize(60, 30)
        self.btn_time_edit.setCheckable(True)
        self.btn_add_files = QPushButton("+") # Mudar para QPixmap ou QIcon "->"
        self.btn_rem_files = QPushButton("-") # Mudar para QPixmap ou QIcon "<-"
        self.btn_save = QPushButton("Salvar")
        self.btn_save.setFixedSize(120, 30)
        self.btn_cancel = QPushButton("Cancelar / Sair")
        self.btn_cancel.setFixedSize(120, 30)
        self.btn_clear = QPushButton("Limpar")
        self.btn_clear.setFixedSize(120, 30)


    def setup_misc(self):
        self.tab__headers = ["Sujeito", "Grupo", "Dia", "Tentativa", "Video"]
        self.colum_count = len(self.tab__headers)

        self.ckb_filter = QCheckBox("Pendentes")
        
        self.ckb_shut_after = QCheckBox("Desligar após Finalizar")
        self.ckb_shut_after.setEnabled(False)

        self.tab_files = QTableWidget()
        self.tab_files.setColumnCount(self.colum_count)
        self.tab_files.setHorizontalHeaderLabels(self.tab__headers)
        
        self.tab_files.setEditTriggers(QTableWidget.NoEditTriggers)  # Avoid Item Table Edit
        self.tab_files.setSelectionBehavior(QTableWidget.SelectRows)

        self.tab_files_to_do = QTableWidget()
        self.tab_files_to_do.setColumnCount(self.colum_count)
        self.tab_files_to_do.setHorizontalHeaderLabels(self.tab__headers)
        self.tab_files_to_do.setEditTriggers(QTableWidget.NoEditTriggers)  # Avoid Item Table Edit
        self.tab_files_to_do.setSelectionBehavior(QTableWidget.SelectRows)
        self.tab_files_to_do.resizeColumnsToContents()
        self.tab_files_to_do.horizontalHeader().setStretchLastSection(True)

        self.spn_hour = QSpinBox()
        self.spn_hour.setFixedWidth(40)
        self.spn_hour.setEnabled(False)
        self.spn_hour.setRange(-1,23)
        self.spn_hour.setSpecialValueText("-")
        self.spn_hour.setAlignment(Qt.AlignCenter)

        self.spn_min = QSpinBox()
        self.spn_min.setFixedWidth(40)
        self.spn_min.setEnabled(False)
        self.spn_min.setRange(-1,59)
        self.spn_min.setSpecialValueText("-")
        self.spn_min.setAlignment(Qt.AlignCenter)

    def setup_frames(self):
        
        # Header
        self.frm_header = QFrame()
        self.frm_header.setMaximumHeight(70)
        self.frm_header_v_layout = QVBoxLayout()
        self.frm_header_v_layout.addWidget(self.lbl_title)
        self.frm_header.setLayout(self.frm_header_v_layout)

        #Config
        self.frm_config = QFrame()
        self.frm_config.setFixedHeight(100)
        self.frm_config_g_layout = QGridLayout()
        self.frm_config_g_layout.addWidget(self.lbl_time, 0, 0, 1, 2, alignment=Qt.AlignCenter)
        self.frm_config_g_layout.addWidget(self.spn_hour, 1, 0)
        self.frm_config_g_layout.addWidget(self.spn_min, 1, 1)
        self.frm_config_g_layout.addWidget(self.ckb_shut_after, 0, 2)
        self.frm_config_g_layout.addWidget(self.btn_time_edit, 1, 2, alignment=Qt.AlignLeft)
        self.frm_config_g_layout.addWidget(self.lbl_sched_by, 1, 4, 2, 1, alignment=Qt.AlignCenter)
        self.frm_config_g_layout.addWidget(self.lbl_spin_hour, 3, 0, alignment=Qt.AlignCenter)
        self.frm_config_g_layout.addWidget(self.lbl_spin_min, 3, 1, alignment=Qt.AlignCenter)

        self.frm_config.setLayout(self.frm_config_g_layout)

        #Tables
        self.frm_tables = QFrame()
        self.frm_tables_g_layout = QGridLayout()
        self.frm_tables_g_layout.addWidget(self.ckb_filter, 0, 0, alignment=Qt.AlignRight)
        self.frm_tables_g_layout.addWidget(self.tab_files, 1, 0, 5, 1)
        self.frm_tables_g_layout.addWidget(self.btn_add_files, 2, 1)
        self.frm_tables_g_layout.addWidget(self.btn_rem_files, 4, 1)
        self.frm_tables_g_layout.addWidget(self.tab_files_to_do, 1, 2, 5, 1)
        self.frm_tables.setLayout(self.frm_tables_g_layout)

        #Buttons
        self.frm_btns = QFrame()
        self.frm_btns.setMaximumHeight(80)
        self.frm_btns_h_layout = QHBoxLayout()
        self.frm_btns_h_layout.addStretch(1)
        self.frm_btns_h_layout.addWidget(self.btn_save)
        self.frm_btns_h_layout.addWidget(self.btn_cancel)
        self.frm_btns_h_layout.addWidget(self.btn_clear)
        self.frm_btns_h_layout.addStretch(1)
        self.frm_btns.setLayout(self.frm_btns_h_layout)


    def setup_layout(self):
        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.frm_header)
        self.v_layout.addWidget(self.frm_config)
        self.v_layout.addWidget(self.frm_tables)
        self.v_layout.addWidget(self.frm_btns)
        
        self.setLayout(self.v_layout)

    def set_data_ui(self):
        js_data = models.Current_Js_Data
        time = js_data.js_time.split(":")
        js_hour = int(time[0])
        js_min = int(time[1])
        self.spn_hour.setValue(js_hour)
        self.spn_min.setValue(js_min)

        js_sched_by = js_data.js_sched_by
        self.lbl_sched_by.setText(f"Agendado por: \n {js_sched_by}")

        self.ckb_shut_after.setChecked(js_data.js_shut)
        self.js_videos = js_data.js_files_to_do

    def fill_table(self):
        js_data = models.Current_Js_Data
        video_data = data_manager.get_video_data()
        video_files = data_manager.get_exists_files()
        self.js_videos = js_data.js_files_to_do
        self.tab_files.setSortingEnabled(False)
        self.tab_files.setRowCount(0)
        self.tab_files_to_do.setSortingEnabled(False)
        self.tab_files_to_do.setRowCount(0)

        for test, subject, group, day, try_n, video, status, cad_by in video_data:
            
            #Check if video exists
            if not video in video_files:
                continue
            
            # chek if video has been registered
            if not data_manager.is_video_cad(video):
                continue

            #check if video has mask
            if not data_manager.get_exists_mask(video):
                continue

            # Check already in schedule
            if video in self.js_videos:
                self.fill_to_do(test, subject, group, day, try_n, video, status, cad_by)
                continue

            # check box filter option
            if self.ckb_filter.isChecked() and not status == "pendente":
                continue

            row = self.tab_files.rowCount()
            self.tab_files.insertRow(row)
            self.tab_files.setItem(row, 0, QTableWidgetItem(subject))
            self.tab_files.setItem(row, 1, QTableWidgetItem(group))
            self.tab_files.setItem(row, 2, QTableWidgetItem(day))
            self.tab_files.setItem(row, 3, QTableWidgetItem(try_n))
            self.tab_files.setItem(row, 4, QTableWidgetItem(video))

        self.tab_files.setSortingEnabled(True)
        self.tab_files.resizeColumnsToContents()
        self.tab_files.horizontalHeader().setStretchLastSection(True)
        self.tab_files_to_do.setSortingEnabled(True)
        self.tab_files_to_do.resizeColumnsToContents()
        self.tab_files_to_do.horizontalHeader().setStretchLastSection(True)

    def fill_to_do(self, test, subject, group, day, try_n, video, status, cad_by):
        
        row_to_do = self.tab_files_to_do.rowCount()
        self.tab_files_to_do.insertRow(row_to_do)
        self.tab_files_to_do.setItem(row_to_do, 0, QTableWidgetItem(subject))
        self.tab_files_to_do.setItem(row_to_do, 1, QTableWidgetItem(group))
        self.tab_files_to_do.setItem(row_to_do, 2, QTableWidgetItem(day))
        self.tab_files_to_do.setItem(row_to_do, 3, QTableWidgetItem(try_n))
        self.tab_files_to_do.setItem(row_to_do, 4, QTableWidgetItem(video))
    
    def sch_cancel(self):
        if pop_messages.message_box("As Alterações Não Salvas Serão Perdidas ",'<b>Deseja Cancelar Assim Mesmo?</b>', "info"):
            self.close()
        
    def sch_save(self):
        if self.spn_hour.text() == "-" or self.spn_min.text() == "-":
            pop_messages.message_box("Precisa Definir Horário para Agenda", "Clique em Qualquer Botão!", "info")
            return
        if self.tab_files_to_do.rowCount() < 1:
            pop_messages.message_box("Precisa Haver ao menos um arquivo Agendado", "Clique em Qualquer Botão!", "info")
            return
        if not pop_messages.message_box("Salvar Alterações de Agendameto? ",'', "info"):
            return
        json_data = models.Current_Js_Data
        current_user = models.Current_User

        self.time = "-1:-1"
        if not self.spn_hour.text() == "-" or not self.spn_min.text() == "-":
            self.time = f"{self.spn_hour.text().zfill(2)}:{self.spn_min.text().zfill(2)}"
            
        json_data.js_time = self.time
        
        self.shut = self.ckb_shut_after.isChecked() if data_manager.os_check() else False
        json_data.js_shut = self.shut

        self.sched_by = current_user.user_name if self.tab_files_to_do.rowCount() > 0 else "0"
        json_data.js_sched_by = self.sched_by
        
        self.js_videos = [] #Clear video list to refresh with actual selected

        for row in range(self.tab_files_to_do.rowCount()):
            item =  self.tab_files_to_do.item(row, 4)
            if item:
                self.js_videos.append(item.text())

        json_data.js_files_to_do = self.js_videos
        
        data_manager.update_shc_status(self.unselected_videos, self.selected_videos)
        data_manager.update_json()
        self.set_data_ui()
        self.unselected_videos = []
        self.selected_videos = self.js_videos.copy()
        
    def sch_clear(self):
        if pop_messages.message_box("Apagará todos os dados de agendamento ",'<b>Continuar?</b>', "warn"):

            js_data = models.Current_Js_Data
            for item in js_data.js_files_to_do:
                data_manager.update_csv_status(item, "pendente")
            
            js_data.js_files_to_do = []
            js_data.js_sched_by = "0"
            js_data.js_shut = "0"
            js_data.js_time = "-1:-1"
            data_manager.update_json()
            self.set_data_ui()
            self.tab_files_to_do.setRowCount(0)
            self.fill_table()

    def move_selected(self, origin_tab, dest_tab, op):

        origin_tab.setSortingEnabled(False)
        dest_tab.setSortingEnabled(False)

        selected_rows = sorted({idx.row() for idx in origin_tab.selectionModel().selectedRows()})
        if not selected_rows:
            return
        
        # Get values on Select Origin
        for row in selected_rows:
            values = [origin_tab.item(row, col).text() for col in range(self.colum_count)]
        
            # Create new Line on Destination
            dest_row = dest_tab.rowCount()
            dest_tab.insertRow(dest_row)

            file = origin_tab.item(row, 4).text()
        
            #Populate lists to csv file status
            if op == "add":
                if file in self.unselected_videos:
                    self.unselected_videos.remove(file)
                if file not in self.selected_videos:
                    self.selected_videos.append(file)
            
            if op == "rem":
                if file in self.selected_videos:
                    self.selected_videos.remove(file)
                if file not in self.unselected_videos:
                    self.unselected_videos.append(file)

        #Populate Items in Destination
            for col, text in enumerate(values):
                new_item = QTableWidgetItem(text)
                dest_tab.setItem(dest_row, col, new_item)

        # Remove from Origin Table
        for row in sorted(selected_rows, reverse=True):
            origin_tab.removeRow(row)

        origin_tab.setSortingEnabled(True)
        dest_tab.setSortingEnabled(True)
        dest_tab.resizeColumnsToContents()
        dest_tab.horizontalHeader().setStretchLastSection(True)


    def time_edit(self):
        is_checkable = data_manager.os_check()
        self.ckb_shut_after.setToolTip("Funcionalidade Apenas para Windows") if not is_checkable else self.ckb_shut_after.setToolTip("")
        edit_time = self.btn_time_edit.isChecked()
        if self.spn_hour.value() == -1 or self.spn_min.value() == -1:
            self.set_time = None
        else:
            self.set_time = time(self.spn_hour.value(), self.spn_min.value())
            
        self.spn_hour.setEnabled(edit_time)
        self.spn_min.setEnabled(edit_time)
        self.ckb_shut_after.setEnabled(edit_time and is_checkable)
        self.btn_time_edit.setText("Salvar" if edit_time else "Editar")

  


        

        