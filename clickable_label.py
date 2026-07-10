from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, QPointF, QPoint
from PySide6.QtGui import QPainter, QPen, QColor
import math
from screens import pop_messages
from services import data_manager
from data import models

class ClickableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.points = []


    def mousePressEvent(self, event):
        
        if event.button() == Qt.LeftButton:
            offset_x = (self.width() - self.pixmap().width()) // 2
            offset_y = (self.height() - self.pixmap().height()) // 2
            
            x = event.position().x() - offset_x
            y = event.position().y() - offset_y
            self.points.append((x, y))

            if len(self.points) == 2:
                
                cx, cy = self.points[0]
                ex, ey = self.points[1]
                r = math.hypot(ex-cx, ey-cy)
                self.mask_painter(cx, cy, r)

    def mask_painter(self, x, y, r): #When Has Mouse Event
            self.c_video = models.Current_Video
            self.video_name = self.c_video.video_name
            
            # Draw Preview on Label preview
            orig_pixmap = self.pixmap()
            preview_pixmap = self.pixmap().copy()
            painter = QPainter(preview_pixmap)
            painter.setPen(QPen(QColor("#c74a4a"), 2))

            # Pool Mask
            painter.drawEllipse(QPointF(x, y), r, r)

            #Wall Huggins Mask
            inner_r = r *0.80
            painter.setPen(QPen(QColor("#c98b4a"), 1))
            painter.drawEllipse(QPointF(x, y), inner_r, inner_r)

            #Quadrants
            painter.setPen(QPen(QColor("#6bb7d6"), 1))
            painter.drawLine(x, y - r, x, y + r)
            painter.drawLine(x - r, y, x + r, y)

            #Quadrants Identification Text
            painter.setPen(QPen(QColor("#c74a4a")))
            painter.drawText(int(x - r/2), int(y - r/2), "Q1")
            painter.drawText(int(x + r/2), int(y - r/2), "Q2")
            painter.drawText(int(x - r/2), int(y + r/2), "Q3")
            painter.drawText(int(x + r/2), int(y + r/2), "Q4")

            #Plataform Mask Identification
            plat_r = r * 0.145
            offset_x = -r * 0.12
            offset_y = r * 0.44
            px = x + offset_x
            py = y + offset_y
            painter.setPen(QPen(QColor("#689179")))
            painter.drawEllipse(QPointF(px,py), plat_r, plat_r)

            painter.end()
            self.setPixmap(preview_pixmap)
            if len(self.points) == 2:
                if pop_messages.message_box("Salvar Máscara? ", "", "info"):
                    mask_x, mask_y, mask_r = data_manager.scale_to_video(x, y, r, self.pixmap().width(), self.pixmap().height())
                    data_manager.save_mask(self.video_name, mask_x, mask_y, mask_r)
                    self.points.clear()
                else:
                    self.points.clear()
                    self.setPixmap(orig_pixmap)

    def mask_loader(self, x, y, r): # When has Mask_data
        self.c_video = models.Current_Video
        self.video_name = self.c_video.video_name
        x, y, r = data_manager.scale_to_thumb(self.pixmap().width(), self.pixmap().height())
            
        # Label Preview Drawn
        preview_pixmap = self.pixmap().copy()
        painter = QPainter(preview_pixmap)
        painter.setPen(QPen(QColor("#c74a4a"), 2))

        painter.drawEllipse(QPointF(x, y), r, r)
        inner_r = r *0.85
        painter.setPen(QPen(QColor("#c98b4a"), 1))
        painter.drawEllipse(QPointF(x, y), inner_r, inner_r)
        painter.setPen(QPen(QColor("#6bb7d6"), 1))
        painter.drawLine(x, y - r, x, y + r)
        painter.drawLine(x - r, y, x + r, y)

        #Quadrants Identification Text
        painter.setPen(QPen(QColor("#c74a4a")))
        painter.drawText(int(x - r/2), int(y - r/2), "Q1")
        painter.drawText(int(x + r/2), int(y - r/2), "Q2")
        painter.drawText(int(x - r/2), int(y + r/2), "Q3")
        painter.drawText(int(x + r/2), int(y + r/2), "Q4")

        #Plataform Mask Identification
        plat_r = r * 0.145
        offset_x = -r * 0.12
        offset_y = r * 0.44
        px = x + offset_x
        py = y + offset_y
        painter.setPen(QPen(QColor("#f1c40f"), 2, Qt.DashLine))
        painter.drawEllipse(QPointF(px,py), plat_r, plat_r)

        painter.end()
        self.setPixmap(preview_pixmap)



    
        

