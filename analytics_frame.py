from io import BytesIO
from PySide6.QtWidgets import QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt
import pyqtgraph
import pyqtgraph.exporters

from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from PIL import Image as pImage

from screens import pop_messages
from services import data_manager
from data import models
from pathlib import Path
from datetime import datetime, date

class Analytics_Frame(QWidget):
    ICON_PATH = "imgs/icons/"
    IMG_PATH = "imgs/"
    def __init__(self, parent=None):
       super().__init__(parent)
       
       self.ui_analytics_screen()

       self.tab_files.clicked.connect(self.get_select_items)
       self.btn_togle_test.clicked.connect(self.toggle_test_type)
       self.btn_export.clicked.connect(self.generate_pdfs)

    def ui_analytics_screen(self):
        self.setup_labels()
        self.setup_btns()
        self.setup_misc()
        self.setup_frames()
        self.setup_layout()
        self.toggle_test_type()

    def setup_labels(self):
        self.lbl_tab_files = QLabel("Arquivos Analisados")
        self.lbl_tab_res = QLabel("Análise Comparativa", alignment=Qt.AlignCenter)
        self.lbl_graph_01 = QLabel("Gráfico Comparativo")
        self.lbl_test_type = QLabel("Nado")
        
    def setup_btns(self):
        self.btn_export = QPushButton("Exportar")
        self.btn_export.setFixedSize(150, 30)
        self.btn_togle_test = QPushButton("N")
        self.btn_togle_test.setFixedSize(18,18)
        self.btn_togle_test.setCheckable(True)
        

    def setup_misc(self):
        self.tab_files_header = ["Teste", "Sujeito", "Grupo", "Dia", "Tentativa", "Video"]
        self.tab_files_collum_count = len(self.tab_files_header)

        self.tab_files = QTableWidget()
        self.tab_files.setColumnCount(self.tab_files_collum_count)
        self.tab_files.setHorizontalHeaderLabels(self.tab_files_header)
        self.tab_files.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tab_files.setEditTriggers(QTableWidget.NoEditTriggers)  # Avoid Item Table Edit
        self.tab_files.setSelectionBehavior(QTableWidget.SelectRows)
        
        self.tab_res = QTableWidget()
        self.tab_res_header = ["Sujeito", "Grupo", "Dia", "Tentativa", "Tempo /s", "Velocidade /cm/s", "Distância /cm", "Q1 /s", "Q2 /s", "Q3 /s", "Q4 /s", "Thigmo T /s","Thigmo /%", "Centro T /s"]
        
        self.tab_res_collum_count = len(self.tab_res_header)
        self.tab_res.setColumnCount(self.tab_res_collum_count)
        self.tab_res.setHorizontalHeaderLabels(self.tab_res_header)
        self.tab_res.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tab_res.setEditTriggers(QTableWidget.NoEditTriggers)  # Avoid Item Table Edit
        self.tab_res.setSelectionMode(QTableWidget.NoSelection) 
        self.tab_res.setSelectionBehavior(QTableWidget.SelectRows)

        self.graph_comp_01 = pyqtgraph.PlotWidget()
        self.graph_comp_01.setStyleSheet("border-radius: 0px; margin-bottom: -5px")
        self.graph_comp_01.setLimits(xMin=-10, yMin=-10)
        self.graph_comp_01.setMouseEnabled(x=False, y=False)
        
    def setup_frames(self):

        #Toggle Test Button
        self.frm_toggle_test = QFrame()
        self.frm_toggle_test.setObjectName("frm_toggle_test")
        self.frm_toggle_test.setFixedSize(50, 25)
        self.frm_toggle_test_h_layout = QHBoxLayout()
        self.frm_toggle_test_h_layout.setContentsMargins(0, 0, 0, 0)
        self.frm_toggle_test_h_layout.setSpacing(0)
        self.frm_toggle_test_h_layout.addWidget(self.btn_togle_test, alignment=Qt.AlignLeft)
        self.frm_toggle_test.setLayout(self.frm_toggle_test_h_layout)

        #Tab Files Header Info Layout
        self.tab_files_header_h_layout = QHBoxLayout()
        self.tab_files_header_h_layout.addWidget(self.lbl_tab_files)
        self.tab_files_header_h_layout.addWidget(self.lbl_test_type, alignment=Qt.AlignRight)
        self.tab_files_header_h_layout.addWidget(self.frm_toggle_test)

        #Table Files
        self.frm_tab_files = QFrame()
        self.frm_tab_files.setMaximumWidth(500)
        self.frm_tab_files_v_Layout = QVBoxLayout()
        self.frm_tab_files_v_Layout.addLayout(self.tab_files_header_h_layout)
        self.frm_tab_files_v_Layout.addWidget(self.tab_files)
        self.frm_tab_files.setLayout(self.frm_tab_files_v_Layout)
    
        #Analytics
        self.frm_analytics = QFrame()
        self.frm_analytics_v_layout = QVBoxLayout()
        self.frm_analytics_v_layout.addWidget(self.lbl_graph_01)
        self.frm_analytics_v_layout.addWidget(self.graph_comp_01)
        self.frm_analytics.setLayout(self.frm_analytics_v_layout)

        #Analitycs Res
        self.frm_tab_res = QFrame()
        self.frm_tab_res.setMinimumHeight(250)
        self.frm_tab_res_v_layout = QVBoxLayout()
        self.frm_tab_res_v_layout.addWidget(self.lbl_tab_res)
        self.frm_tab_res_v_layout.addWidget(self.tab_res)
        self.frm_tab_res.setLayout(self.frm_tab_res_v_layout)

        #Buttons
        self.frm_btns = QFrame()
        self.frm_btns_h_layout = QHBoxLayout()
        self.frm_btns_h_layout.addWidget(self.btn_export, alignment=Qt.AlignCenter)
        self.frm_btns.setLayout(self.frm_btns_h_layout)


    def setup_layout(self):
        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(self.frm_tab_files)
        self.h_layout.addWidget(self.frm_analytics)
        
        self.v_layout = QVBoxLayout()
        self.v_layout.addLayout(self.h_layout)
        self.v_layout.addWidget(self.frm_tab_res)
        self.v_layout.addWidget(self.frm_btns)
        
        self.setLayout(self.v_layout)

    def toggle_graph_theme(self):
        #Visuals
        theme = models.Current_User.user_theme
        self.graph_comp_01.showGrid(x=True, y=True)
        symbol_color = ['b', 'r', 'g']
        for i, item in enumerate(self.graph_comp_01.plotItem.listDataItems()):
            item.setPen(None)
            item.setSymbolBrush(pyqtgraph.mkBrush(symbol_color[i % len(symbol_color)]))
        if not theme:
            self.graph_comp_01.setBackground("#b0cccf")
            return
        if theme == 1:
            self.graph_comp_01.setBackground('#2f4e52')
        else:
            self.graph_comp_01.setBackground("#b0cccf")

    def toggle_test_type(self):
        if self.btn_togle_test.isChecked():
            self.frm_toggle_test_h_layout.setAlignment(self.btn_togle_test, Qt.AlignRight)
            self.btn_togle_test.setText("P")
            self.lbl_test_type.setText("Probatório")
        else:
            self.frm_toggle_test_h_layout.setAlignment(self.btn_togle_test, Qt.AlignLeft)
            self.btn_togle_test.setText("N")
            self.lbl_test_type.setText("Nado")

        self.tab_res.setRowCount(0)
        self.graph_comp_01.clear()
        self.fill_table()

    
    def fill_table(self):
        video_data = data_manager.get_video_data()
        self.tab_files.setSortingEnabled(False)
        self.tab_files.setRowCount(0)
        row = 0
        for test, subject, group, day, try_n, video, status, cad_by in video_data:
            if not data_manager.is_video_cad(video):
                continue
            if not status == "pronto":
                continue
            if self.btn_togle_test.isChecked() and test == "Nado":
                continue
            if not self.btn_togle_test.isChecked() and test == "Probatorio":
                continue
            self.tab_files.insertRow(row)
            self.tab_files.setItem(row, 0, QTableWidgetItem(test))
            self.tab_files.setItem(row, 1, QTableWidgetItem(subject))
            self.tab_files.setItem(row, 2, QTableWidgetItem(group))
            self.tab_files.setItem(row, 3, QTableWidgetItem(day))
            self.tab_files.setItem(row, 4, QTableWidgetItem(try_n))
            self.tab_files.setItem(row, 5, QTableWidgetItem(video))
            row +=1

        self.tab_files.setSortingEnabled(True)
        self.tab_files.resizeColumnsToContents()
        self.tab_files.horizontalHeader().setStretchLastSection(True)

    def fill_results(self):
        c_video = models.Current_Video

        row = self.tab_res.rowCount()
        self.tab_res.insertRow(row)

        self.tab_res.setItem(row, 0, QTableWidgetItem(c_video.subject))
        self.tab_res.setItem(row, 1, QTableWidgetItem(c_video.group))
        self.tab_res.setItem(row, 2, QTableWidgetItem(c_video.day))
        self.tab_res.setItem(row, 3, QTableWidgetItem(c_video.try_n))
        self.tab_res.setItem(row, 4, QTableWidgetItem(c_video.time))
        self.tab_res.setItem(row, 5, QTableWidgetItem(c_video.speed))
        self.tab_res.setItem(row, 6, QTableWidgetItem(c_video.distance))
        self.tab_res.setItem(row, 7, QTableWidgetItem(c_video.q1))
        self.tab_res.setItem(row, 8, QTableWidgetItem(c_video.q2))
        self.tab_res.setItem(row, 9, QTableWidgetItem(c_video.q3))
        self.tab_res.setItem(row, 10, QTableWidgetItem(c_video.q4))
        self.tab_res.setItem(row, 11, QTableWidgetItem(c_video.tgm_t))
        self.tab_res.setItem(row, 12, QTableWidgetItem(c_video.tgm_r))
        self.tab_res.setItem(row, 13, QTableWidgetItem(c_video.center_t_))

    def get_select_items(self):
        selected_rows = set()
        self.tab_res.setRowCount(0)
        self.graph_comp_01.clear()
        totals = []

        for item in self.tab_files.selectedItems():
            selected_rows.add(item.row())
 
        for row in sorted(selected_rows):
            video = self.tab_files.item(row, 5).text()
            if video:
                data_manager.set_c_video(video)
                self.fill_results()
                totals.append(models.Current_Video)
            else:
                self.tab_res.setColumnCount(0)
        if totals:
            result_totals = self.get_totals(totals)
            self.fill_totals(result_totals)
            self.fill_graph(result_totals, totals)

    def get_totals(self, videos):
        n = len(videos)
        sum_time = sum_speed = sum_dist = sum_q1 = sum_q2 = sum_q3 = sum_q4 = sum_tgm = sum_center_t = 0.0
        av_time = av_speed = av_dist = av_q1 = av_q2 = av_q3 = av_q4 = av_tgm = av_center_t = 0.0
        max_time = max_speed = max_dist = max_q1 = max_q2 = max_q3 = max_q4 = max_tgm = max_center_t = 0.0
        min_time = min_speed = min_dist = min_q1 = min_q2 = min_q3 = min_q4 = min_tgm = min_center_t = 0.0
        subject_out = group_out = day_out = try_n_out = ""
        times =set()
        speeds = set()
        dists = set()
        q1s = set()
        q2s = set()
        q3s = set()
        q4s = set()
        tgms= set()
        tgm_rs = set()
        centers = set()
        subject_ = set()
        group_ = set()
        day_ = set()
        try_n_ = set()

        for video in videos:
            sum_time += (float(video.time))
            sum_speed += (float(video.speed))
            sum_dist += (float(video.distance))
            sum_q1 += (float(video.q1))
            sum_q2 += (float(video.q2))
            sum_q3 += (float(video.q3))
            sum_q4 += (float(video.q4))
            sum_tgm += (float(video.tgm_t))
            sum_center_t += (float(video.center_t_))
            tgm_rs.add((float(video.tgm_t)*100) / float(video.time) if float(video.time) > 0 else 0.0)
            times.add(video.time)
            speeds.add(video.speed)
            dists.add(video.distance)
            q1s.add(video.q1)
            q2s.add(video.q2)
            q3s.add(video.q3)
            q4s.add(video.q4)
            tgms.add(video.tgm_t)
            centers.add(video.center_t_)
            subject_.add(video.subject)
            group_.add(video.group)
            day_.add(video.day)
            try_n_.add(video.try_n)

        av_time = sum_time / n
        av_speed = sum_speed / n
        av_dist = sum_dist / n
        av_q1 = sum_q1 / n
        av_q2 = sum_q2 / n
        av_q3 = sum_q3 / n
        av_q4 = sum_q4 / n
        av_tgm = sum_tgm / n
        av_tgm_r = (sum_tgm * 100) / sum_time if sum_tgm else "0"
        av_center_t = sum_center_t / n

        #Get Max Values 
        max_time = max(times)
        max_speed = max(speeds)
        max_dist = max(dists)
        max_q1 = max(q1s)
        max_q2 = max(q2s)
        max_q3 = max(q3s)
        max_q4 = max(q4s)
        max_tgm = max(tgms)
        max_center_t = max(centers)
        max_tgm_r = max(tgm_rs)

        #Get Min Values 
        min_time = min(times)
        min_speed = min(speeds)
        min_dist = min(dists)
        min_q1 = min(q1s)
        min_q2 = min(q2s)
        min_q3 = min(q3s)
        min_q4 = min(q4s)
        min_tgm = min(tgms)
        min_tgm_r = min(tgm_rs)
        min_center_t = min(centers)

        subject_out = next(iter(subject_)) if len(subject_) == 1 else "MEDIA"
        group_out = next(iter(group_)) if len(group_) == 1 else "MEDIA"
        day_out = next(iter(day_)) if len(day_) == 1 else "MEDIA"
        try_n_out = next(iter(try_n_)) if len(try_n_) == 1 else "MEDIA"

        return models.Result_Totals(av_time = av_time, max_time = max_time, min_time = min_time,
                        av_speed = av_speed, max_speed = max_speed, min_speed = min_speed,
                        av_dist = av_dist, max_dist = max_dist, min_dist = min_dist,
                        av_q1 = av_q1, max_q1 = max_q1, min_q1 = min_q1,
                        av_q2 = av_q2, max_q2 = max_q2, min_q2 = min_q2,
                        av_q3 = av_q3, max_q3 = max_q3, min_q3 = min_q3,
                        av_q4 = av_q4, max_q4 = max_q4, min_q4 = min_q4,
                        av_tgm = av_tgm, max_tgm = max_tgm, min_tgm = min_tgm,
                        av_tgm_r = av_tgm_r, max_tgm_r = max_tgm_r, min_tgm_r = min_tgm_r,
                        av_center_t = av_center_t, max_center_t = max_center_t, min_center_t = min_center_t,
                        subject_out = subject_out, group_out = group_out, day_out = day_out, try_n_out = try_n_out)

    def fill_totals(self, totals):
        row_count = self.tab_res.rowCount()
        if not row_count > 1:
            return
        self.tab_res.insertRow(row_count)
        self.tab_res.setItem(row_count, 0, QTableWidgetItem(totals.subject_out))
        self.tab_res.setItem(row_count, 1, QTableWidgetItem(totals.group_out))
        self.tab_res.setItem(row_count, 2, QTableWidgetItem(totals.day_out))
        self.tab_res.setItem(row_count, 3, QTableWidgetItem(totals.try_n_out))
        self.tab_res.setItem(row_count, 4, QTableWidgetItem(str(totals.av_time)))
        self.tab_res.setItem(row_count, 5, QTableWidgetItem(str(totals.av_speed)))
        self.tab_res.setItem(row_count, 6, QTableWidgetItem(str(totals.av_dist)))
        self.tab_res.setItem(row_count, 7, QTableWidgetItem(str(totals.av_q1)))
        self.tab_res.setItem(row_count, 8, QTableWidgetItem(str(totals.av_q2)))
        self.tab_res.setItem(row_count, 9, QTableWidgetItem(str(totals.av_q3)))
        self.tab_res.setItem(row_count, 10, QTableWidgetItem(str(totals.av_q4)))
        self.tab_res.setItem(row_count, 11, QTableWidgetItem(str(totals.av_tgm)))
        self.tab_res.setItem(row_count, 12, QTableWidgetItem(str(totals.av_tgm_r)))
        self.tab_res.setItem(row_count, 13, QTableWidgetItem(str(totals.av_center_t)))


        #Fill Table with Min Values

        row_count = self.tab_res.rowCount()
        if not row_count > 2:
            return
        self.tab_res.insertRow(row_count)
        self.tab_res.setItem(row_count, 0, QTableWidgetItem("MIN"))
        self.tab_res.setItem(row_count, 1, QTableWidgetItem("MIN"))
        self.tab_res.setItem(row_count, 2, QTableWidgetItem("MIN"))
        self.tab_res.setItem(row_count, 3, QTableWidgetItem("MIN"))
        self.tab_res.setItem(row_count, 4, QTableWidgetItem(str(totals.min_time)))
        self.tab_res.setItem(row_count, 5, QTableWidgetItem(str(totals.min_speed)))
        self.tab_res.setItem(row_count, 6, QTableWidgetItem(str(totals.min_dist)))
        self.tab_res.setItem(row_count, 7, QTableWidgetItem(str(totals.min_q1)))
        self.tab_res.setItem(row_count, 8, QTableWidgetItem(str(totals.min_q2)))
        self.tab_res.setItem(row_count, 9, QTableWidgetItem(str(totals.min_q3)))
        self.tab_res.setItem(row_count, 10, QTableWidgetItem(str(totals.min_q4)))
        self.tab_res.setItem(row_count, 11, QTableWidgetItem(str(totals.min_tgm)))
        self.tab_res.setItem(row_count, 12, QTableWidgetItem(str(totals.min_tgm_r)))
        self.tab_res.setItem(row_count, 13, QTableWidgetItem(str(totals.min_center_t)))

        #Fill Table with Max Values
        
        row_count = self.tab_res.rowCount()
        self.tab_res.insertRow(row_count)
        self.tab_res.setItem(row_count, 0, QTableWidgetItem("MAX"))
        self.tab_res.setItem(row_count, 1, QTableWidgetItem("MAX"))
        self.tab_res.setItem(row_count, 2, QTableWidgetItem("MAX"))
        self.tab_res.setItem(row_count, 3, QTableWidgetItem("MAX"))
        self.tab_res.setItem(row_count, 4, QTableWidgetItem(str(totals.max_time)))
        self.tab_res.setItem(row_count, 5, QTableWidgetItem(str(totals.max_speed)))
        self.tab_res.setItem(row_count, 6, QTableWidgetItem(str(totals.max_dist)))
        self.tab_res.setItem(row_count, 7, QTableWidgetItem(str(totals.max_q1)))
        self.tab_res.setItem(row_count, 8, QTableWidgetItem(str(totals.max_q2)))
        self.tab_res.setItem(row_count, 9, QTableWidgetItem(str(totals.max_q3)))
        self.tab_res.setItem(row_count, 10, QTableWidgetItem(str(totals.max_q4)))
        self.tab_res.setItem(row_count, 11, QTableWidgetItem(str(totals.max_tgm)))
        self.tab_res.setItem(row_count, 12, QTableWidgetItem(str(totals.max_tgm_r)))
        self.tab_res.setItem(row_count, 13, QTableWidgetItem(str(totals.max_center_t)))

        
        if self.tab_res.rowCount() == 2:
            last_row = self.tab_res.rowCount() -1
            self.tab_res.setSelectionMode(QTableWidget.SingleSelection)
            self.tab_res.selectRow(last_row)
            self.tab_res.setSelectionMode(QTableWidget.NoSelection)

        if self.tab_res.rowCount() > 2: # Avoid bugs but will be always > 1
            self.tab_res.setSelectionMode(QTableWidget.MultiSelection)

            last_row = self.tab_res.rowCount() -1
            for i in range(last_row - 2, last_row + 1):
                if i >= 0:
                    self.tab_res.selectRow(i)
            self.tab_res.setSelectionMode(QTableWidget.SingleSelection)
            self.tab_res.setSelectionMode(QTableWidget.NoSelection)

    def fill_graph(self, totals, q_totals):
        self.toggle_graph_theme()
        self.graph_comp_01.clear()
        labels = ["Tempo /s", "Velocidade /cm/s", "Distância /cm", "Q1 /s", "Q2 /s", "Q3 /s", "Q4 /s", "Thigmo T /s","Thigmo /%", "Centro T /s"]
        
        x = list(range(len(labels)))

        avs = [
            totals.av_time, totals.av_speed, totals.av_dist,
            totals.av_q1, totals.av_q2, totals.av_q3, totals.av_q4,
            totals.av_tgm, totals.av_tgm_r, totals.av_center_t
            ]
        
        maxs = [
            totals.max_time, totals.max_speed, totals.max_dist,
            totals.max_q1, totals.max_q2, totals.max_q3, totals.max_q4,
            totals.max_tgm, totals.max_tgm_r, totals.max_center_t
            ]
        mins = [
            totals.min_time, totals.min_speed, totals.min_dist,
            totals.min_q1, totals.min_q2, totals.min_q3, totals.min_q4,
            totals.min_tgm, totals.min_tgm_r, totals.min_center_t
            ]
        avs = [float(v) for v in avs]
        mins = [float(i) for i in mins]
        maxs = [float(a) for a in maxs]
        
        self.graph_comp_01.plot(x, avs, pen=pyqtgraph.mkPen(None), symbol='d', symbolBrush='b', name="Média")

        if len(q_totals) > 1:
            self.graph_comp_01.plot(x, maxs, pen=pyqtgraph.mkPen(None), symbol='t', symbolBrush='r', name="Máx")
            self.graph_comp_01.plot(x, mins, pen=pyqtgraph.mkPen(None), symbol='t1', symbolBrush='g', name="Mín")

        #Naming Axe X
        axis = self.graph_comp_01.getAxis('bottom')
        axis.setTicks([list(zip(range(len(labels)), labels))])

    def generate_pdfs(self):
        c_user = models.Current_User
        pdf_folder = Path(models.Const_Vars.PATH_TO_PDFS)
        pdf_folder.mkdir(parents=True, exist_ok=True)

        if self.tab_res.rowCount() <= 1:
            pop_messages.message_box(f"Precisa Selecionar ao menos dois itens na tabela","", "info")
            return
        if not pop_messages.message_box(f"O Relatório será criado na pasta LaViDa{chr(92)}{pdf_folder}",'<b>Criar Agora?</b>', "info"):
            return

        #Text and Text Variables
        test_type = "Probatório" if self.btn_togle_test.isChecked() else "Nado"
        version = models.Const_Vars.VERSION
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"{pdf_folder}/{c_user.user_name}_{ts}.pdf"
        doc = BaseDocTemplate(base_name,
                                pagesize=A4,
                                topMargin=110, bottomMargin=50,
                                leftMargin=60, rightMargin=60)
        
        frame = Frame(doc.leftMargin, doc.bottomMargin, 
              doc.width, doc.height, id='normal')

        template = PageTemplate(id='relatorio', frames=frame, onPage=self.header_footer_build)
        doc.addPageTemplates([template])
        story = []
        styles = getSampleStyleSheet()

        doc_title = f"Resultados de Análise Comparativa - <b><i>Teste Tipo: {test_type}</i></b>"
        doc_notation = f"""As análises foram realizadas a partir da leitura dos vídeos por meio da biblioteca OpenCV, utilizando o software
                        <b><i>LaVida</i></b>, versão <b><i>{version}</i></b>.<br/>
                        Os valores foram arredondados para três casas decimais.<br/>
                        <b><i>Não foram observadas discrepâncias nos resultados durante as verificações de repetibilidade, mantendo-se valores idênticos com precisão de até cinco casas decimais.</i></b><br/>
                        Além disso, a qualidade de fabricação das máscaras pode influenciar os resultados, particularmente em fenômenos associados ao comportamento <b><i>wall hugging</i></b>, podendo alterar sutis padrões de movimento ou interação com as bordas."""
        table_title = "Tabela com dados Selecionados para Comparação" #< - Decidir melhor após visualização
        graph_title = "Grafico com Médias, Mínimas e Máximas dos itens selecionados" #< - Decidir melhor após visualização#

        if pdf_folder.exists():

            #Results Table
            tab_headers = [self.tab_res.horizontalHeaderItem(c).text() for c in range(self.tab_res.columnCount())]
            rows = []
            for r in range(self.tab_res.rowCount()):
                row_data = []
                for c in range(self.tab_res.columnCount()):
                    item = self.tab_res.item(r, c)
                    row_data.append(item.text() if item else "")

                rows.append(row_data)
            table_data = [tab_headers] + rows
            report_table = Table(table_data)

            report_table.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('ALIGN', (0,0), (-1,0), 'CENTER'),  
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 3),
            ('RIGHTPADDING', (0,0), (-1,-1), 3),
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('BACKGROUND', (0,-3), (-1,-1), colors.lightgrey),
            ]))

            #Graphic Creation
            temp_graph = self.export_bw_graph()
            img_graph_bw = Image(temp_graph)
            img_graph_bw._restrictSize(500, 170)
            
            #***** Body *****#
            story.append(Paragraph(doc_title))
            story.append(Spacer(1, 12))

            #Table
            story.append(report_table)
            story.append(Paragraph(table_title, styles['Normal']))
            story.append(Spacer(1, 12))

            #Graphics
            story.append(img_graph_bw)
            story.append(Paragraph(graph_title, styles['Normal']))
            story.append(Spacer(1, 12))
            #Adicionar linha se possível

            #Notation
            story.append(Paragraph(doc_notation, styles['Normal']))
            story.append(Spacer(1, 12))

            #Se Possível criar marca d'agua com logo
            doc.build(story)
            temp_graph.unlink(missing_ok=True)

    def export_bw_graph(self):
        temps_folder = Path(models.Const_Vars.PATH_TO_TEMPS)
        temps_folder.mkdir(parents=True, exist_ok=True)

        #Render BW Graphic

        self.graph_comp_01.setBackground("#E5EAEB")
        brush_list = ["#494949", "#6A6A6A", "#b8b7b7"]

        for i, item in enumerate(self.graph_comp_01.plotItem.listDataItems()):
            item.setPen(None)
            item.setSymbolBrush(pyqtgraph.mkBrush(brush_list[i % len(brush_list)]))

        #BW Graphic to img
        temp_graph = Path(models.Const_Vars.PATH_TO_TEMPS) / "export_graph.png"
        graph_exporter = pyqtgraph.exporters.ImageExporter(self.graph_comp_01.plotItem)

        graph_exporter.parameters()['width'] = 800
        graph_exporter.export(str(temp_graph))
        
        self.toggle_graph_theme()

        return temp_graph

    def header_footer_build(self, canvas, doc):
        width, height = A4
        report_date = datetime.now().strftime("%d/%m/%Y - %H:%M")
        c_user = models.Current_User
        version = models.Const_Vars.VERSION
        test_type = "Probatório" if self.btn_togle_test.isChecked() else "Nado"

        #Metadata
        canvas.setTitle("LaViDa - Relatório de Análise Cruzada")
        canvas.setAuthor(f"{c_user.user_name}")
        canvas.setSubject("Relatório Gerado pelo Software LaViDa")
        canvas.setCreator(f"LaViDa - {version}")

        # ****Header ****#
        #Logo Tranform
        img_buffer = BytesIO()
        pil_logo = pImage.open("imgs/La viDa identidade-01.png").convert('L')
        pil_logo.save(img_buffer, format='PNG')
        img_buffer.seek(0)

        # Header Data and Text
        header_style = ParagraphStyle(name="HeaderText", fontSize=9, leading=11)
        header_data = [
            [
                Image(img_buffer, width=120, height=75),
                Paragraph(f"""
                <b>Software de Análise de Videos e Dados Laboratoriais</b><br/>
                Versão: <b>{version}</b><br/><br/>
                Exportado por: <b>{c_user.user_name}</b> Dia: {report_date}<br/>
                <b>Tipo de Teste: </b> {test_type}
                """, header_style)
            ]
        ]
        #Header Styles and layout
        header_table = Table(header_data, colWidths=[130, 370])
        header_table.setStyle(TableStyle([
            ("BOX", (0,0), (-1,-1), 1, colors.gray),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("LEFTPADDING", (0,0), (-1,-1), 3),
            ("RIGHTPADDING", (0,0), (-1,-1), 3),
            ("TOPPADDING", (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ]))


        canvas.saveState()
        w, h = header_table.wrap(doc.width, doc.topMargin)
        header_table.drawOn(canvas, doc.leftMargin, height - h - 20)
        canvas.restoreState()

        #***** Footer *****#
        #Footer Data
        footer_style = ParagraphStyle(name="FooterText", fontSize=9, leading=11)
        footer_data= [
            [
                Paragraph(f"""
                
                Relatório gerado automaticamente pelo <b><i>LaViDa</i></b> Versão: <b><i>{version}</i></b><br/>
                <b><i>(c) 2025 - LaViDa</i></b> é de uso pessoal e não possui distribuição comercial.<br/>
                Desenvolvido por <b><i>Guilherme S Oliveira</i></b>
                """, footer_style)
            ]
        ]
        #Footer Styles and Layout
        footer_table = Table(footer_data, colWidths=[500])
        footer_table.setStyle(TableStyle([
            ("BOX", (0,0), (-1,-1), 0.5, colors.gray),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("LEFTPADDING", (0,0), (-1,-1), 3),
            ("RIGHTPADDING", (0,0), (-1,-1), 3),
            ("TOPPADDING", (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ]))

        canvas.saveState()
        w, h = footer_table.wrap(doc.width, doc.bottomMargin)
        footer_table.drawOn(canvas, doc.leftMargin, 20)
        canvas.restoreState()










        






        

