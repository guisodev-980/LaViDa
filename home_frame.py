from PySide6.QtWidgets import QLabel, QLineEdit, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QGridLayout, QSizePolicy
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap

from data import models
from services import users_man
from data import models

class Home_Frame(QWidget):
   
   ICON_PATH = "imgs/icons/"
   IMG_PATH = "imgs/"
   def __init__(self, parent=None):
      super().__init__(parent)
       
      self.ui_home_screen()

   def ui_home_screen(self):
      self.setup_labels()
      self.setup_text()
      self.setup_frames()
      self.setup_layout()
      
        
   def setup_labels(self):
      version = models.Const_Vars.VERSION
      self.ico_user_large = QPixmap(f'{self.ICON_PATH}User_ico').scaled(QSize(150,150), Qt.KeepAspectRatio, Qt.SmoothTransformation)
      self.img_software = QPixmap(f'{self.IMG_PATH}La viDa identidade-01.png').scaled(QSize(200, 200), Qt.KeepAspectRatio, Qt.SmoothTransformation) #La viDa identidade-01
      
      self.lbl_user_large = QLabel(pixmap=self.ico_user_large)
      self.lbl_user_large.setMargin(5)
      self.lbl_user = QLabel("Usuário:")
      self.lbl_user_id = QLabel("Id:")
      self.lbl_adm_tag = QLabel("Administrador")
      self.lbl_user_name = QLabel("Nome:")
      self.lbl_user_role = QLabel("Cargo:")
      self.lbl_logo = QLabel(pixmap=self.img_software)
      self.lbl_logo.setMaximumHeight(150)
      self.lbl_software = QLabel(f"Desenvolvido por: Guilherme S. Oliveira\n Versão: {version}", alignment=Qt.AlignRight)
      

   def setup_text(self):
      self.txt_user_id = QLineEdit("id")
      self.txt_user_id.setMaximumWidth(50)
      self.txt_user_id.setEnabled(False)
      self.txt_user_name = QLineEdit("Name")
      self.txt_user_name.setMaximumWidth(250)
      self.txt_user_name.setEnabled(False)
      self.txt_user_role = QLineEdit("role")
      self.txt_user_role.setMaximumWidth(250)
      self.txt_user_role.setEnabled(False)
    
   def setup_frames(self):
      self.frm_user = QFrame()
      self.frm_user.setMaximumWidth(500)
      self.frm_user.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
      
      self.frm_logo = QFrame()
      self.frm_logo.setStyleSheet("border: none")


   def setup_layout(self):
       #   ***   Frames   ****

      #User Frame
      self.g_frm_user_layout = QGridLayout()
      self.g_frm_user_layout.addWidget(self.lbl_user_id, 0, 0, alignment=Qt.AlignRight)
      self.g_frm_user_layout.addWidget(self.lbl_user_name, 1, 0, alignment=Qt.AlignRight)
      self.g_frm_user_layout.addWidget(self.lbl_user_role, 2, 0, alignment=Qt.AlignRight)
      self.g_frm_user_layout.addWidget(self.txt_user_id, 0, 1)
      self.g_frm_user_layout.addWidget(self.txt_user_name, 1, 1, 1, 2)
      self.g_frm_user_layout.addWidget(self.txt_user_role, 2, 1, 1, 2)
      self.g_frm_user_layout.addWidget(self.lbl_adm_tag, 0, 2, alignment=Qt.AlignRight)

       
      self.h_frm_user_layout = QHBoxLayout()
      self.h_frm_user_layout.addWidget(self.lbl_user_large)
      self.h_frm_user_layout.addLayout(self.g_frm_user_layout)
      self.frm_user.setLayout(self.h_frm_user_layout)

      #Apresentation/Logo Frame

      self.v_frm_logo_layout = QVBoxLayout()
      self.v_frm_logo_layout.addWidget(self.lbl_logo, alignment=Qt.AlignCenter)
      self.v_frm_logo_layout.addWidget(self.lbl_software, alignment=Qt.AlignRight | Qt.AlignBottom)

      self.frm_logo.setLayout(self.v_frm_logo_layout)

      #General
      self.v_layout = QVBoxLayout()
      self.v_layout.addWidget(self.frm_user)
      self.v_layout.addWidget(self.frm_logo)

      self.setLayout(self.v_layout)

   def home_update_user(self):
      user = models.Current_User
      user_ico = users_man.get_user_img()
      self.txt_user_id.setText(str(user.user_id))
      self.txt_user_name.setText(user.user_name)
      self.txt_user_role.setText(user.user_role)
      self.lbl_user_large.setPixmap(QPixmap(user_ico).scaled(QSize(150,150), Qt.KeepAspectRatio, Qt.SmoothTransformation))
      



       

      
