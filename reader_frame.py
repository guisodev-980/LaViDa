from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QTableWidget, QSizePolicy
from PySide6.QtCore import Qt , QPoint, QPointF, QTimer, QTime, Signal
from PySide6.QtGui import QPixmap, QPainter, QPen, QImage, QColor

from screens import pop_messages
from screens import waiting_message
from screens.clickable_label import ClickableLabel
from screens.cad_video_dialog import Cad_Video
from services import data_manager
from data import models
from data.models import Const_Vars as Vars
from data.models import Pmap_Scale
from pathlib import Path
import numpy as np
from math import dist
import cv2
import os


class Reader_Frame(QWidget):
    read_now = Signal(object)
    ICON_PATH = "imgs/icons/"
    IMG_PATH = "imgs/"
    def __init__(self, parent=None):
       super().__init__(parent)
       self.sch_timer = QTimer()
       self.sch_timer.timeout.connect(self._is_time_now)
       
       self.ui_reader_screen()

       self.tab_files.clicked.connect(self.fill_with_select)
       self.btn_mask.clicked.connect(self.construct_mask)
       self.btn_read.clicked.connect(self.select_to_read)
       self.btn_cad_video.clicked.connect(self.cad_video)
       self.btn_discard.clicked.connect(self.discard_data)
       self.btn_copy_mask.clicked.connect(self.copy_mask)
       self.btn_paste_mask.clicked.connect(self.paste_mask)

    def ui_reader_screen(self):
        self.setup_labels()
        self.setup_btns()
        self.setup_misc()
        self.setup_frames()
        self.setup_layout()
        
        data_manager.get_video_thumb()
        self.fill_table()

    def setup_labels(self):
        self.lbl_files_table = QLabel("Arquivos")
        self.lbl_traj_title = QLabel("Trajetória")
        self.lbl_analytics = QLabel("Tabela Analítica")
        self.lbl_thumb_name = QLabel("Thumb Name")

    def setup_btns(self):
        self.btn_cad_video = QPushButton("Cadastrar Video")
        self.btn_read = QPushButton("Analisar")
        self.btn_mask = QPushButton("Criar Máscara")
        self.btn_copy_mask = QPushButton("Copiar Máscara")
        self.btn_paste_mask = QPushButton("Colar Máscara")
        self.btn_discard = QPushButton("Descartar")

    def setup_misc(self):
        self.tab_files = QTableWidget()
        self.tab_files_headers = ["Sujeito", "Grupo", "Dia", "Tentativa","Arquivo", "Status"]
        self.tab_files.setColumnCount(len(self.tab_files_headers))
        self.tab_files.setHorizontalHeaderLabels(self.tab_files_headers)
        self.tab_files.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tab_files.setEditTriggers(QTableWidget.NoEditTriggers)  # Impede edição direta
        self.tab_files.setSelectionBehavior(QTableWidget.SelectRows)
        self.tab_files.setSortingEnabled(True)
        self.tab_analytics = QTableWidget()
        self.tab_analytics_header = ["Sujeito", "Grupo", "Dia", "Tentativa", "Tempo /s", "Velocidade /cm/s", "Distância /cm", "Q1 /s", "Q2 /s", "Q3 /s", "Q4 /s", "Thigmo T /s","Thigmo /%", "Centro T /s"]
        self.tab_analytics.setColumnCount(len(self.tab_analytics_header))
        self.tab_analytics.setHorizontalHeaderLabels(self.tab_analytics_header)
        self.tab_analytics.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.pmap_traj_img = QPixmap(f'{self.ICON_PATH}Image_Holder.png').scaledToHeight(Pmap_Scale)
        self.lbl_traj_img = ClickableLabel()
        self.lbl_traj_img.setAlignment(Qt.AlignCenter)
        self.lbl_traj_img.setPixmap(QPixmap(self.pmap_traj_img))

    def setup_frames(self):
        self.frm_tab_files = QFrame()
        self.frm_tab_files.setMaximumWidth(650)
        self.frm_traj_img = QFrame()
        self.frm_traj_img.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.frm_tab_analytics = QFrame()
        self.frm_btns = QFrame()

    def setup_layout(self):

        # Image and Analytics
        self.img_res_frm_v_layout = QVBoxLayout()
        self.img_res_frm_v_layout.addWidget(self.lbl_traj_title, alignment=Qt.AlignCenter)
        self.img_res_frm_v_layout.addWidget(self.lbl_traj_img)
        self.img_res_frm_v_layout.addWidget(self.lbl_thumb_name, alignment=Qt.AlignCenter)
        self.frm_traj_img.setLayout(self.img_res_frm_v_layout)

        self.tab_res_frm_v_layout = QVBoxLayout()
        self.tab_res_frm_v_layout.addWidget(self.lbl_analytics)
        self.tab_res_frm_v_layout.addWidget(self.tab_analytics)
        self.frm_tab_analytics.setLayout(self.tab_res_frm_v_layout)

        self.res_v_layout = QVBoxLayout()
        self.res_v_layout.addWidget(self.frm_traj_img)

        #Files Table

        self.tab_files_v_layout = QVBoxLayout()
        self.tab_files_v_layout.addWidget(self.lbl_files_table)
        self.tab_files_v_layout.addWidget(self.tab_files)
        self.frm_tab_files.setLayout(self.tab_files_v_layout)
        
        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(self.frm_tab_files)
        self.h_layout.addLayout(self.res_v_layout)

        # Buttons
        self.btns_frm_h_layout = QHBoxLayout()
        self.btns_frm_h_layout.addWidget(self.btn_cad_video)
        self.btns_frm_h_layout.addWidget(self.btn_mask)
        self.btns_frm_h_layout.addWidget(self.btn_copy_mask)
        self.btns_frm_h_layout.addWidget(self.btn_paste_mask)
        self.btns_frm_h_layout.addWidget(self.btn_read)
        self.btns_frm_h_layout.addWidget(self.btn_discard)
        self.frm_btns.setLayout(self.btns_frm_h_layout)
        
        #General
        
        self.v_layout = QVBoxLayout()
        self.v_layout.addLayout(self.h_layout)
        self.v_layout.addWidget(self.frm_tab_analytics)
        self.v_layout.addWidget(self.frm_btns)
        
        self.setLayout(self.v_layout)

    def fill_table(self):
        video_data = data_manager.get_video_data()
        video_files = data_manager.get_exists_files()
        self.tab_files.setRowCount(0)
        
        for row, (test, subject, group, day, try_n, video, status, cad_by) in enumerate(video_data):
            if not video in video_files:
                continue

            if not data_manager.is_video_cad(video):
                subject = "-"
                group = "-"
                day = "0"
                try_n = "0"

            row = self.tab_files.rowCount()
            self.tab_files.insertRow(row)
            self.tab_files.setItem(row, 0, QTableWidgetItem(subject))
            self.tab_files.setItem(row, 1, QTableWidgetItem(group))
            self.tab_files.setItem(row, 2, QTableWidgetItem(day))
            self.tab_files.setItem(row, 3, QTableWidgetItem(try_n))
            self.tab_files.setItem(row, 4, QTableWidgetItem(video))
            self.tab_files.setItem(row, 5, QTableWidgetItem(status))
    
    def get_selected_item(self):
        selected_files = set()
        selected_row = set()
        for item in self.tab_files.selectedItems():
            selected_row.add(item.row())
        
        for row in sorted(selected_row):
            selected_file = self.tab_files.item(row, 4).text()
            selected_files.add(selected_file)

        return selected_files, selected_row

    def fill_with_select(self):
        selected_files, selected_rows = self.get_selected_item()
        if selected_rows:
                file_to_set = next(iter(selected_files))
                img = data_manager.set_thumb_img(file_to_set)
                self.lbl_traj_img.setPixmap(QPixmap(img).scaledToHeight(Pmap_Scale))
                
                data_manager.set_c_video(file_to_set)
                self.c_video = models.Current_Video
                self.lbl_thumb_name.setText(f'{file_to_set}  - {self.c_video.test}' if self.c_video.test != "No_Cad_Test" else f"{file_to_set}  -  Não Cadastrado")
                if data_manager.get_exists_mask(file_to_set):
                    self.lbl_traj_img.mask_loader(int(self.c_video.mask_x), int(self.c_video.mask_y), int(self.c_video.mask_r))
                if data_manager.has_results(file_to_set):
                    self.fill_result_tab()
                else:
                    self.tab_analytics.setRowCount(0)
        
    def fill_result_tab(self):
        c_video = models.Current_Video
        self.tab_analytics.setRowCount(0)
        row = 0
        
        self.tab_analytics.insertRow(row)
        self.tab_analytics.setItem(row, 0, QTableWidgetItem(c_video.subject))
        self.tab_analytics.setItem(row, 1, QTableWidgetItem(c_video.group))
        self.tab_analytics.setItem(row, 2, QTableWidgetItem(c_video.day))
        self.tab_analytics.setItem(row, 3, QTableWidgetItem(c_video.try_n))
        self.tab_analytics.setItem(row, 4, QTableWidgetItem(c_video.time))
        self.tab_analytics.setItem(row, 5, QTableWidgetItem(c_video.speed))
        self.tab_analytics.setItem(row, 6, QTableWidgetItem(c_video.distance))
        self.tab_analytics.setItem(row, 7, QTableWidgetItem(c_video.q1))
        self.tab_analytics.setItem(row, 8, QTableWidgetItem(c_video.q2))
        self.tab_analytics.setItem(row, 9, QTableWidgetItem(c_video.q3))
        self.tab_analytics.setItem(row, 10, QTableWidgetItem(c_video.q4))
        self.tab_analytics.setItem(row, 11, QTableWidgetItem(c_video.tgm_t))
        self.tab_analytics.setItem(row, 12, QTableWidgetItem(c_video.tgm_r))
        self.tab_analytics.setItem(row, 13, QTableWidgetItem(c_video.center_t_))

    def construct_mask(self): #call on btn_mask.clicked
        selected_files, _ = self.get_selected_item()

        if not selected_files or len(selected_files) > 1:
            pop_messages.message_box("Precisa Selecionar um único arquivo",'', "info")
            return
        pop_messages.message_box("Clique no Centro do Tanque e <br> Posteriormente em uma das bordas",'', "info")
        data_manager.set_c_video(next(iter(selected_files)))
        
    def cad_video(self):
        self.setEnabled(False)
        dialog = Cad_Video(self)
        if dialog.exec():
            self.setEnabled(True)
            self.fill_table()

    def _on_cancel_requested(self):
        self._cancel_requested = True

    def select_to_read(self):
        selected_files, _ = self.get_selected_item()
        if not selected_files:
            pop_messages.message_box("Precisa Selecionar ao menos um arquivo",'', "info")
            return
        for file in selected_files:
            data_manager.set_c_video(file)
            if not data_manager.is_video_cad(file) or not data_manager.get_exists_mask(file):
                pop_messages.message_box("Impossível Analisar Videos não Cadastrados <br> ou sem Máscara",'', "info")
                return
            if data_manager.has_results(file):
                pop_messages.message_box(f"Há Video(s) Selecionado(s) que Já possui Resultados <br> Descartar manualmente antes de Reanalise",'Pressione Qualquer Botão', "warn")
                return
        
        self.read_video(selected_files)

    def read_video(self, files):

        #Wating Message
        self._cancel_requested = False
        total_selected = len(files)
        wait = waiting_message.Wait_Dialog(parent=self)
        wait.cancelled.connect(self._on_cancel_requested)
        wait.show()
            
        self.setWindowOpacity(0.8)
        for i, file in enumerate(files, start=1):
            if self._cancel_requested:
                break
            wait.set_progress(i, total_selected)
            data_manager.set_c_video(file)
            for row in range(self.tab_files.rowCount()):
                item = self.tab_files.item(row, 4)
                if item and item.text() == file:
                    self.tab_files.selectRow(row)
                    self.fill_with_select()
            self.process_files(file)
        wait.close()
        self.setWindowOpacity(1.0)

    def process_files(self, file):

        c = models.Current_Video

        self._reset_video_data()
        if self._cancel_requested:
            return
    
        video_path = Path(Vars.PATH_TO_VIDEOS) / file
        traj_img_dir = Path(Vars.PATH_TO_VIDEO_IMGS)
        traj_img_dir.mkdir(parents=True, exist_ok=True)
        traj_img_path = Path(Vars.PATH_TO_VIDEO_IMGS) / f"{Path(file).stem}.png"
        

        vid_cap = cv2.VideoCapture(video_path)
        if not vid_cap.isOpened():
            pop_messages.message_box("Erro ao Abrir o Arquivo", file, "warn")
            return

        traj_canvas, traj_painter = self._create_canvas_from_video(vid_cap)
        self._draw_mask(traj_painter, c.mask_x, c.mask_y, c.mask_r)

        metrics = self._process_video_frames(vid_cap, traj_painter, traj_canvas)

        vid_cap.release()
        traj_painter.end()

        # Save Final Image (Canvas with trajetory)
        traj_canvas.save(str(traj_img_path))

        self._finalize_results(traj_img_path, metrics)

    def _reset_video_data(self):
        c = models.Current_Video
        c.distance = c.time = c.speed = 0
        c.q1 = c.q2 = c.q3 = c.q4 = 0
        c.tgm_t = c.tgm_r = c.center_t_ = 0
        c.img_traj = None

    def _create_canvas_from_video(self, vid_cap):
        #"""Create Transparent Canvas to Trajetory Draw."""

        ret, frame = vid_cap.read()
        if not ret:
            raise ValueError("Vídeo vazio ou corrompido.")

        h, w, ch = frame.shape

        traj_canvas = QPixmap(w, h)
        traj_canvas.fill(Qt.transparent)

        traj_painter = QPainter(traj_canvas)
        traj_painter.setRenderHint(QPainter.Antialiasing)
        traj_painter.setPen(QPen(QColor("#00ff66"), 6))

        # Back Video to Begining
        vid_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        return traj_canvas, traj_painter

    def _process_video_frames(self, vid_cap, traj_painter, traj_canvas):
        c = models.Current_Video

        mask_x = int(c.mask_x)
        mask_y = int(c.mask_y)
        mask_r = int(c.mask_r)

        #Plataform Position
        plat_r = mask_r * 0.145
        offset_x = -mask_r * 0.12
        offset_y = mask_r * 0.44
        px = mask_x + offset_x
        py = mask_y + offset_y

        first_pos = None
        total_distance = 0.0
        dist_now = 0
        idle_frame = 0
        last_pos = None
        quadrants = [0, 0, 0, 0]
        tmg_time = 0.0
        total_frames = 0

        pool_size_cm = Vars.POOL_DIAMETER_CM
        pool_size_px = mask_r * 2   # Diamenter in px (ray * 2)
        px_to_cm = pool_size_cm / pool_size_px
        LIMIAR_CM = 0.5

        fps = vid_cap.get(cv2.CAP_PROP_FPS)

        while True:

            if self._cancel_requested:
                break
            ret, frame = vid_cap.read()
            if not ret:
                break

            total_frames += 1
            QApplication.processEvents()

            masked = self._apply_mask(frame, mask_x, mask_y, mask_r)
            cx, cy = self._detect_object(masked)
            
            if cx is not None:
                if first_pos is None:
                    first_pos = (cx, cy)

                traj_painter.drawEllipse(QPoint(cx, cy), 3, 3)

                if last_pos:
                    total_distance += dist(last_pos, (cx, cy))
                    dist_now = dist(last_pos, (cx, cy)) * px_to_cm
                    on_plataform = dist((cx, cy), (px, py)) < plat_r
                    if on_plataform and dist_now < LIMIAR_CM:
                        idle_frame += 1 
                    else:
                        idle_frame = 0
                
                last_pos = (cx, cy)

                self._update_quadrants(cx, cy, mask_x, mask_y, quadrants)

                if abs(dist((cx, cy), (mask_x, mask_y)) - mask_r) <= 25:
                    tmg_time += 1

            if total_frames % 50 == 0:
                self._update_live_preview(masked, traj_canvas)

            if idle_frame > fps * 1.0: #Um segundo
                break

        #Draw Firs Position
        if first_pos:
            traj_painter.setPen(QPen(Qt.blue, 6))
            traj_painter.drawEllipse(QPoint(*first_pos), 4, 4)
        #Draw Final Position
        if last_pos:
            traj_painter.setPen(QPen(Qt.red, 6))
            traj_painter.drawEllipse(QPoint(*last_pos), 4, 4)
            
        # Restore trajectory color
        traj_painter.setPen(QPen(QColor("#00ff66"), 6))

        return {
            "frames": total_frames,
            "fps": fps,
            "distance": total_distance,
            "quadrants": quadrants,
            "tgm_time": tmg_time,
            "px_to_cm": px_to_cm
            }
    
    def _apply_mask(self, frame, mx, my, mr):
        mask = np.zeros(frame.shape[:2], dtype="uint8")
        cv2.circle(mask, (mx, my), mr, 255, -1)
        return cv2.bitwise_and(frame, frame, mask=mask)

    def _detect_object(self, masked):
        hsv = cv2.cvtColor(masked, cv2.COLOR_BGR2HSV)

        # White Filter (Mouse)
        
        lower_white = np.array([0, 0, 140]) 
        upper_white = np.array([179, 80, 255])

        thresh = cv2.inRange(hsv, lower_white, upper_white)

        # Try to remove ramdom reflexes and noises
        kernel = np.ones((5,5), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not cnts:
            return None, None

        c = max(cnts, key=cv2.contourArea)
        M = cv2.moments(c)
        if M["m00"] == 0:
            return None, None

        return int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])

    def _update_quadrants(self, cx, cy, mx, my, quadrants):
        if cx <= mx and cy <= my: quadrants[0] += 1  # Q1
        elif cx >= mx and cy <= my: quadrants[1] += 1  # Q2
        elif cx <= mx and cy >= my: quadrants[2] += 1  # Q3
        else: quadrants[3] += 1  # Q4

    def _update_live_preview(self, masked, traj_canvas):
        rgb = cv2.cvtColor(masked, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        ui_img = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        frame_pmap = QPixmap.fromImage(ui_img)

        painter = QPainter(frame_pmap)
        painter.drawPixmap(0, 0, traj_canvas)
        painter.end()

        self.lbl_traj_img.setPixmap(frame_pmap.scaledToHeight(Pmap_Scale))

    def _finalize_results(self, traj_img_path, m):
        c = models.Current_Video

        tgm_time = m["tgm_time"] / m["fps"]
        real_distance = m["distance"] * m["px_to_cm"]
        total_time = round(m["frames"] / m["fps"], 3) #In seconds
        c.distance = round(real_distance, 3)
        c.time = round(total_time, 3)
        c.speed = round((real_distance) / total_time, 3) if total_time else 0.0
        c.q1, c.q2, c.q3, c.q4 = [round(q / m["fps"], 3) for q in m["quadrants"]]
        c.tgm_t = round(tgm_time, 3)
        c.tgm_r = round((tgm_time / total_time) * 100, 3) if total_time else 0.0
        c.center_t_ = round(total_time - tgm_time, 3)
        c.video_status = "pronto"
        c.img_traj = traj_img_path.name

        data_manager.results_to_csv()
        self.fill_with_select()

    def discard_data(self):
        selected_files, _ = self.get_selected_item()
        if not selected_files:
            pop_messages.message_box("Nenhum Arquivo Selecionado",'Pressione Qualquer Botão', "info")
            return
        if pop_messages.message_box("Todos os dados de leitura dos videos<br>Selecionados serão Descartados",'<b>Continuar?</b>', "info"):
            for video in selected_files:
                data_manager.erase_video_results(video)
                self.fill_table()
                self.fill_with_select()
    
    def _draw_mask(self, painter, mx, my, r):
        x = int(mx)
        y = int(my)
        r = int(r)

        #Poll Mask
        painter.setPen(QPen(QColor("#9b3a3a"), 2))
        painter.drawEllipse(QPointF(x, y), r, r)

        #Wall Huggins Mask
        inner_r = r * 0.85
        painter.setPen(QPen(QColor("#9b663a"), 1))
        painter.drawEllipse(QPointF(x, y), inner_r, inner_r)

        #Quadrant Lines
        painter.setPen(QPen(QColor("#65bcb5"), 1))
        painter.drawLine(x, y - r, x, y + r)
        painter.setPen(QPen(QColor("#65bc8b"), 1))
        painter.drawLine(x - r, y, x + r, y)

        #Quadrants Labels
        painter.setPen(QPen(QColor("#9b3a3a")))
        painter.drawText(int(x - r/2), int(y - r/2), "Q1")
        painter.drawText(int(x + r/2), int(y - r/2), "Q2")
        painter.drawText(int(x - r/2), int(y + r/2), "Q3")
        painter.drawText(int(x + r/2), int(y + r/2), "Q4")

        #Plataform Identification
        plat_r = r * 0.145
        offset_x = -r * 0.12
        offset_y = r * 0.44
        px = x + offset_x
        py = y + offset_y
        painter.setPen(QPen(QColor("#689179")))
        painter.drawEllipse(QPointF(px,py), plat_r, plat_r)

    def copy_mask(self):
        selected_files, _ = self.get_selected_item()
        if not selected_files or len(selected_files) > 1:
            pop_messages.message_box("Selecione um Único Arquivo","Pressione Qualquer Botão","info")
            return
        
        video = next(iter(selected_files)) # List to Item

        if not data_manager.get_exists_mask(video):
            pop_messages.message_box("Arquivo Selecionado não possui Máscara", "Pressione Qualquer Botão", "info")
            return
        data_manager.set_c_video(video)
        data_manager.set_hold_mask(video)
        pop_messages.message_box(f"Máscara copiada do video{video} com sucesso", "Pressione Qualquer Botão", "info", time_out=5)

    def paste_mask(self):
        has_mask = 0
        hold_mask = models.current_mask_holder
        selected_files, _ = self.get_selected_item()
        
        if not selected_files:
            pop_messages.message_box("Selecione ao Menos um Arquivo", "Pressione Qualquer Botão", "info")
            return
        
        if not hold_mask:
            pop_messages.message_box("Nenhuma Máscara Copiada", "Pressione Qualquer Botão", "info")
            return

        has_mask = sum(1 for v in selected_files if data_manager.get_exists_mask(v))
        
        if has_mask > 0:
            if not pop_messages.message_box(f"{has_mask} Video(s) Selecionado(s) já Possue(m) Máscaras", "Deseja continuar?", "warn"):
                return
        for video in selected_files:
            data_manager.save_mask(video, hold_mask.mask_x, hold_mask.mask_y, hold_mask.mask_z)
    
    
    def check_time_start(self):
        c_js_data = models.Current_Js_Data
        time = c_js_data.js_time
        if time == "-1:-1" or not c_js_data.js_files_to_do: # "-1:-1" is default from no schedule and js_files_to_do is a list of videos to read
            self.timer_stop()
            return
        sch_time = QTime.fromString(time, "HH:mm")
        now = QTime.currentTime()
        if sch_time.hour() < now.hour() or (sch_time.hour() <= now.hour() and sch_time.minute() < now.minute()):
            pop_messages.message_box(f"Agenda Perdida!<br>Haviam análises agendadas para às {time}<br> mas o software não estava ativo ", "Pressione Qualquer Botão", "warm", parent=self)
        self.timer_start()

    def _is_time_now(self):
        c_json_time = models.Current_Js_Data.js_time
        sch_time = QTime.fromString(c_json_time, "HH:mm")
        now = QTime.currentTime()

        if now.hour() == sch_time.hour() and now.minute() == sch_time.minute():
            self.timer_stop()
            self.do_files_to_do()

    def timer_start(self):
        self.sch_timer.setInterval(58000)
        self.sch_timer.start()
        
    def timer_stop(self):
        self.sch_timer.stop()
      
    def do_files_to_do(self):
      c_json = models.Current_Js_Data
      videos = c_json.js_files_to_do
      if not pop_messages.message_box("As Análises Agendadas começarão Agora", "Deseja Continuar?", "info", time_out=10, parent=self):
          return
      self.read_now.emit(self)
      self.timer_stop()
      self.read_video(videos)
      if c_json.js_shut:
          QTimer.singleShot(0, self.shut_os)
      self.sch_clear()
      self.fill_table()
      
    def shut_os(self):
        self.sch_clear()
        if pop_messages.message_box("Desligar o Computador?", "Cancelar para interromper", "info", time_out=10, parent=self):
            if os.name == 'nt':
                os.system("shutdown -s -t 60")

    def sch_clear(self):
        js_data = models.Current_Js_Data
        js_data.js_files_to_do = []
        js_data.js_sched_by = "0"
        js_data.js_shut = "0"
        js_data.js_time = "-1:-1"
        data_manager.update_json()
        
        

            