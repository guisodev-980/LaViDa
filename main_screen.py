import sys
from PySide6.QtWidgets import QApplication, QMenu, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QWidget, QStackedWidget
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap, QAction

from screens.home_frame import Home_Frame
from screens.reader_frame import Reader_Frame
from screens.analytics_frame import Analytics_Frame
from screens.cad_frame import Cad_Frame
from screens.login_Frame import Login_Frame
from screens.schedule_dialog import Schedule_Dialog
from screens.about_dialog import AboutDialog
from screens import pop_messages
from data import models
from data.models import Const_Vars
from services import users_man
from data import crud

#pyinstaller --onefile --windowed --icon="C:\Users\Guiso\Desktop\Dev\LaViDa\imgs\LaViDa_Tecla.png" main.py --add-data "C:\Users\Guiso\Desktop\Dev\LaViDa\screens\themes:themes" --add-data "C:\Users\Guiso\Desktop\Dev\LaViDa\imgs:imgs" --add-data "C:\Users\Guiso\Desktop\Dev\LaViDa\data\users_db.db:data/users_db.db

class Main_Screen(QWidget):

   def __init__(self):
      super().__init__()
      self.setMinimumSize(750,650)
      self.window_icon = QIcon("imgs/La-viDa-identidade-04.svg")
      self.setWindowIcon(self.window_icon)
      self.setWindowTitle("LaViDa")
      
      self.ui_main_screen()

      self.lst_nav_btns = [self.btn_home, self.btn_register, self.btn_reader, self.btn_analytics, self.btn_schedule]
      self.btn_home.clicked.connect(lambda: self.frame_switch(0))
      self.btn_register.clicked.connect(lambda: self.frame_switch(1))
      self.btn_reader.clicked.connect(lambda: self.frame_switch(2))
      self.btn_reader.clicked.connect(self.frm_reader.fill_table)
      self.btn_analytics.clicked.connect(lambda: self.frame_switch(3))
      self.btn_schedule.clicked.connect(self.open_schedule)
      self.btn_theme.toggled.connect(self.toggle_theme)
      self.btn_ico_about.clicked.connect(self.open_about)
      self.btn_analytics.clicked.connect(lambda: self.frm_analytics.fill_table())
      self.frm_reader.read_now.connect(lambda: self.frame_switch(2))
      

      self.frame_switch(0) #Force Home initialization
      
   def ui_main_screen(self):
      self.setup_labels()
      self.setup_buttons()
      self.setup_misc()
      self.setup_frames()
      self.setup_layout()

   def setup_labels(self):

      #Software Identification

      self.pmap_logo_header = QPixmap(f'{Const_Vars.PATH_TO_IMGS}La viDa identidade-03.png').scaled(QSize(70, 120), Qt.KeepAspectRatio, Qt.SmoothTransformation)
      self.lbl_ico_software = QLabel(pixmap=self.pmap_logo_header)
      self.ico_user_header = QIcon(f'{Const_Vars.PATH_TO_ICONS}User_ico.png')
      
   def setup_buttons(self):
      
      #User ICO as QPushButton
      self.btn_ico_user = QPushButton()
      self.btn_ico_user.setIcon(self.ico_user_header)
      self.btn_ico_user.setCursor(Qt.PointingHandCursor)
      self.btn_ico_user.setToolTip("Clique para Opções de Usuário")
      self.btn_ico_user.setStyleSheet("""QPushButton {border: none; background-color: transparent; }
                                      QPushButton::menu-indicator {image: none; width: 0px; height: 0px;}""")
      
      
      #Theme Ico As QPushButton
      self.btn_theme = QPushButton()
      self.btn_theme.setCursor(Qt.PointingHandCursor)
      self.btn_theme.setToolTip("Para Salvar o tema \n Faça um LogOut")
      self.btn_theme.setStyleSheet("background-color: transparent")
      self.ico_theme_light = QIcon(f'{Const_Vars.PATH_TO_ICONS}ThemeLight.png')
      self.btn_theme.setIcon(QIcon(self.ico_theme_light))
      self.btn_theme.setIconSize(QSize(22, 22))
      self.btn_theme.setCheckable(True)
      self.btn_theme.setFixedSize(18, 18)
      
      #About ICO as QPushtButton
      self.ico_about_header = QIcon(f'{Const_Vars.PATH_TO_ICONS}3d_Int.png')
      self.btn_ico_about = QPushButton()
      self.btn_ico_about.setIcon(self.ico_about_header)
      self.btn_ico_about.setCursor(Qt.PointingHandCursor)
      self.btn_ico_about.setToolTip("Sobre")
      self.btn_ico_about.setStyleSheet("background-color: transparent")

      #Frames Navigation Buttons
      self.btn_home = QPushButton("Home")
      self.btn_register = QPushButton("Usuários")
      self.btn_reader = QPushButton("Leitor")
      self.btn_analytics = QPushButton("Análises")
      self.btn_schedule = QPushButton("Agendamento")

   def setup_misc(self):
      self.user_menu = QMenu()
      self.user_menu.setObjectName("s_user_menu")
      self.logout_action = QAction("Logout")
      self.user_menu.addAction(self.logout_action)
      self.btn_ico_user.setMenu(self.user_menu)
      self.logout_action.triggered.connect(self.logout)
   
   def setup_frames(self):

      #Button Theme
      self.frm_btn_theme = QFrame()
      self.frm_btn_theme.setObjectName("frm_btn_theme")
      self.frm_btn_theme.setFixedSize(50, 25)
      self.frm_btn_theme_h_layout = QHBoxLayout()
      self.frm_btn_theme_h_layout.addWidget(self.btn_theme, alignment=Qt.AlignLeft)
      self.frm_btn_theme_h_layout.setContentsMargins(0, 0, 0, 0)
      self.frm_btn_theme_h_layout.setSpacing(0)
      self.frm_btn_theme.setLayout(self.frm_btn_theme_h_layout)
      
      #Header
      self.frm_header = QFrame()
      self.frm_header.setFixedHeight(60)
      self.frm_header_h_layout = QHBoxLayout()
      self.frm_header_h_layout.addWidget(self.lbl_ico_software)
      self.frm_header_h_layout.addStretch(1)
      self.frm_header_h_layout.addWidget(self.btn_ico_user)
      self.frm_header_h_layout.addWidget(self.frm_btn_theme)
      self.frm_header_h_layout.addWidget(self.btn_ico_about)
      
      self.frm_header.setLayout(self.frm_header_h_layout)

      #Nav Buttons
      self.frm_header_btns_menu = QFrame()
      self.frm_header_btns_menu.setFixedHeight(55)
      self.frm_btns_header_h_layout = QHBoxLayout()
      self.frm_btns_header_h_layout.addWidget(self.btn_home)
      self.frm_btns_header_h_layout.addWidget(self.btn_register)
      self.frm_btns_header_h_layout.addWidget(self.btn_reader)
      self.frm_btns_header_h_layout.addWidget(self.btn_analytics)
      self.frm_btns_header_h_layout.addWidget(self.btn_schedule)

      self.frm_header_btns_menu.setLayout(self.frm_btns_header_h_layout)

      #Place Holder
      self.stack_frm_place_holder = QStackedWidget()
      self.frm_home = Home_Frame()
      self.frm_reg = Cad_Frame(logout_callback=self.logout, update_reg_user_callback=self.main_update_user, home_frame=self.frm_home)
      self.frm_reader = Reader_Frame()
      self.frm_analytics = Analytics_Frame()
      self.stack_frm_place_holder.addWidget(self.frm_home)       # 0
      self.stack_frm_place_holder.addWidget(self.frm_reg)        # 1
      self.stack_frm_place_holder.addWidget(self.frm_reader)     # 2
      self.stack_frm_place_holder.addWidget(self.frm_analytics)  # 3
      
   def setup_layout(self):
      self.v_layout = QVBoxLayout()
      self.v_layout.addWidget(self.frm_header, 1)
      self.v_layout.addWidget(self.frm_header_btns_menu, 1)
      self.v_layout.addWidget(self.stack_frm_place_holder, 6)
      
      self.setLayout(self.v_layout)

   def frame_switch(self, index):
      current_index = self.stack_frm_place_holder.currentIndex()
      self.lst_nav_btns[current_index].setChecked(False)
      self.lst_nav_btns[current_index].setEnabled(True)
      self.lst_nav_btns[index].setChecked(True)      
      self.lst_nav_btns[index].setEnabled(False)
      self.stack_frm_place_holder.setCurrentIndex(index)

   def open_schedule(self):
      self.frm_reader.timer_stop()
      sch_dialog = Schedule_Dialog()
      sch_dialog.exec()
      self.frm_reader.check_time_start()
   
   def open_about(self):
      about_dialog = AboutDialog(self)
      about_dialog.exec()

   def logout(self):
      user = models.Current_User
      crud.update_user_theme(user.user_theme, user.user_email)
      self.setEnabled(False)
      self.frame_switch(0)
      self.setWindowOpacity(0.8)
      dialog = Login_Frame(self)
      if dialog.exec():
         dialog.login_sucess.connect(self.frm_home.home_update_user())
         dialog.login_sucess.connect(self.frm_reg.fill_user())
         dialog.login_sucess.connect(self.main_update_user())
         self.setEnabled(True)
         self.setWindowOpacity(1.0)
         
      else:
         QApplication.quit()

   def closeEvent(self, event):
      c_user = models.Current_User
      c_json_data = models.Current_Js_Data
      if c_json_data.js_files_to_do and c_user:
         if not pop_messages.message_box(f"Há Tarefas Agendadas para às {c_json_data.js_time} que não serão Executadas", "Sair Assim mesmo?", "warn"):
            event.ignore()
            return
      return event.accept()
   
   def main_update_user(self):
      user = models.Current_User
      theme = user.user_theme
      user_ico = users_man.get_user_img()
      self.btn_ico_user.setIcon(QIcon(user_ico))
      self.btn_theme.setChecked(theme)
      self.toggle_theme()
      self.frm_reader.check_time_start()


   def toggle_theme(self):
      user = models.Current_User
      if self.btn_theme.isChecked():
         user.user_theme = 1
         self.theme_icon = QIcon(QIcon(f'{Const_Vars.PATH_TO_ICONS}ThemeDark.png'))
         self.frm_btn_theme_h_layout.setAlignment(Qt.AlignRight)
         self.btn_theme.setIcon(QIcon(self.theme_icon))
         with open("screens/themes/dark_theme.qss", "r") as theme_file:
               QApplication.instance().setStyleSheet(theme_file.read())
      else:
         user.user_theme = 0
         self.theme_icon = QIcon(QIcon(f'{Const_Vars.PATH_TO_ICONS}ThemeLight.png'))
         self.frm_btn_theme_h_layout.setAlignment(Qt.AlignLeft)
         self.btn_theme.setIcon(QIcon(self.theme_icon))
         with open("screens/themes/light_theme.qss", "r") as theme_file:
            QApplication.instance().setStyleSheet(theme_file.read())
      
      self.frm_analytics.toggle_graph_theme()


