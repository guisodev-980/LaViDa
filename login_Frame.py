from PySide6.QtWidgets import QLabel, QDialog, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QFrame, QGridLayout, QSizePolicy
from PySide6.QtCore import Qt, QSize, Signal, QTimer
from PySide6.QtGui import QIcon, QPixmap

from data import models
from data import crud
from services import data_manager 
from services import users_man
from screens.welcome_screen import Welcome_Screen


class Login_Frame(QDialog):
    login_sucess = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
       
        self.setFixedSize(550,350)
        
        #starts Functions
        
        models.Users_Email = users_man.get_users_email() # Get exist email list to ensure login
        if len(models.Users_Email) < 1: users_man.ensure_admin_exists() # Create super admin user if db is empty
        data_manager.construct_json() # Check configs.json and csv exists and health
        data_manager.get_json_data() # Fill models.current_json_data with atual archive data <- call os_check for normalize options compatibility
        data_manager.check_videos_in_json() #Check if video names in json_data exists in folder
        
        self.ui_login_screen()

        self.user_input_timer = QTimer()
        self.user_input_timer.setSingleShot(True)
        self.user_input_timer.setInterval(300)
        self.user_input_timer.timeout.connect(self.is_new_user)

        self.txt_user.textChanged.connect(self.user_input_timer.start)
        self.txt_pass.textChanged.connect(self.user_input_timer.start)
        self.txt_pass_confirm.textChanged.connect(self.user_input_timer.start)
        self.btn_save_new.clicked.connect(self.new_user_update)
        self.btn_pass_view.clicked.connect(self.toggle_pass_view)

    def ui_login_screen(self):
        self.setup_labels()
        self.setup_text()
        self.setup_btns()
        self.setup_frames()
        self.setup_layout()
        



    def setup_labels(self):
        self.pmap_logo = QPixmap(f'{models.Const_Vars.PATH_TO_IMGS}La viDa identidade-01.png').scaled(QSize(150, 150), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.lbl_software = QLabel(pixmap=self.pmap_logo, alignment=Qt.AlignCenter)
        self.lbl_user = QLabel("e-mail:")
        self.lbl_pass = QLabel("Senha")
        self.lbl_pass_confirm = QLabel("Confirmar Senha")
        self.lbl_pass_confirm.setVisible(False)
        self.lbl_log_info = QLabel("Digite email e senha válidos", alignment=Qt.AlignCenter)
        self.lbl_log_info.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def setup_text(self):
        self.txt_user = QLineEdit()
        self.txt_pass = QLineEdit()
        self.txt_pass.setEchoMode(QLineEdit.Password)
        self.txt_pass_confirm = QLineEdit()
        self.txt_pass_confirm.setEchoMode(QLineEdit.Password)
        self.txt_pass_confirm.setVisible(False)

    def setup_btns(self):
        self.btn_login = QPushButton("Entrar")
        self.btn_login.setEnabled(False)
        self.btn_exit = QPushButton("Sair")
        self.btn_save_new = QPushButton("Salvar")
        self.btn_pass_view = QPushButton()
        self.btn_pass_view.setObjectName("s_btn_pass_view")
        self.btn_pass_view.setCursor(Qt.PointingHandCursor)
        self.btn_pass_view.setFixedSize(25, 25)
        self.ico_eye_open = QIcon(f'{models.Const_Vars.PATH_TO_ICONS}OpenEye.png')
        self.ico_eye_close = QIcon(f'{models.Const_Vars.PATH_TO_ICONS}ClosedEye.png')
        self.btn_pass_view.setIcon(QIcon(self.ico_eye_close))
        self.btn_pass_view.setFocusPolicy(Qt.NoFocus)
        self.btn_pass_view.setIconSize(QSize(25, 25))
        self.btn_pass_view.setCheckable(True)
        self.btn_save_new.setVisible(False)
        self.btn_save_new.setEnabled(False)

    def setup_frames(self):
        #Software Idendification
        self.frm_software = QFrame()
        self.frm_software_v_layout = QVBoxLayout()
        self.frm_software_v_layout.addWidget(self.lbl_software, alignment=Qt.AlignCenter)
        self.frm_software.setLayout(self.frm_software_v_layout)

        #Login
        self.frm_login = QFrame()
        self.frm_login.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.frm_login_g_layout = QGridLayout()
        self.frm_login_g_layout.addWidget(self.lbl_user, 0, 0, alignment=Qt.AlignRight)
        self.frm_login_g_layout.addWidget(self.lbl_pass, 1, 0, alignment=Qt.AlignRight)
        self.frm_login_g_layout.addWidget(self.lbl_pass_confirm, 2, 0, alignment=Qt.AlignRight)
        self.frm_login_g_layout.addWidget(self.txt_user, 0, 1)
        self.frm_login_g_layout.addWidget(self.txt_pass, 1, 1)
        self.frm_login_g_layout.addWidget(self.btn_pass_view, 1, 2)
        self.frm_login_g_layout.addWidget(self.txt_pass_confirm, 2, 1)
        self.frm_login_g_layout.addWidget(self.btn_save_new, 3, 1)
        self.frm_login.setLayout(self.frm_login_g_layout)

        #Buttons

        self.frm_btns = QFrame()
        self.frm_btns.setFixedHeight(50)
        self.frm_btns_h_layout = QHBoxLayout()
        self.frm_btns_h_layout.addWidget(self.btn_login)
        self.frm_btns_h_layout.addWidget(self.btn_exit)
        self.frm_btns.setLayout(self.frm_btns_h_layout)

        #Informations
        self.frm_info = QFrame()
        self.frm_info.setMaximumHeight(75)
        self.frm_info_v_layout = QVBoxLayout()
        self.frm_info_v_layout.addWidget(self.lbl_log_info)
        self.frm_info.setLayout(self.frm_info_v_layout)

    def setup_layout(self):
        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.frm_login)
        self.v_layout.addWidget(self.frm_info)
        self.v_layout.addWidget(self.frm_btns)
        self.h_layout.addWidget(self.frm_software)
        self.h_layout.addLayout(self.v_layout)

        self.setLayout(self.h_layout)

        self.btn_login.clicked.connect(self.validade)
        self.btn_exit.clicked.connect(self.reject)
    
    def toggle_pass_view(self):
        if self.btn_pass_view.isChecked():
            self.txt_pass.setEchoMode(QLineEdit.Normal)
            self.txt_pass_confirm.setEchoMode(QLineEdit.Normal)
            self.btn_pass_view.setIcon(QIcon(self.ico_eye_open))
        else:
            self.txt_pass.setEchoMode(QLineEdit.Password)
            self.txt_pass_confirm.setEchoMode(QLineEdit.Password)
            self.btn_pass_view.setIcon(QIcon(self.ico_eye_close))
    
    def is_password_valid(self, pass1, pass2):
        return pass1 and pass2 and pass1 == pass2
    
    def is_new_user(self):
        in_user_email = self.txt_user.text()
        in_user_pass = self.txt_pass.text()
        in_user_pass_confirm = self.txt_pass_confirm.text()
        user_theme = "0"
        is_valid_email = users_man.is_valid_email(in_user_email)
        self.btn_login.setEnabled(is_valid_email)
        if is_valid_email:
            user = crud.get_user_by_pass_mail(in_user_email, "__Temp__")
            if user:
                models.Current_User = models.User(user.user_id, user.is_admin, user.user_name, user.user_role, user.user_phone,
                                                  user.user_email, user.user_pass, user.user_reg_by, user.user_img, user_theme)
                self.lbl_pass_confirm.setVisible(True)
                self.txt_pass_confirm.setVisible(True)
                self.btn_save_new.setVisible(True)

                if not in_user_pass or not in_user_pass_confirm:
                    self.lbl_log_info.setText(f'Bem Vindo\n{user.user_name}\nCadastre uma Senha para Acessar')
                elif self.is_password_valid(in_user_pass, in_user_pass_confirm):
                    self.lbl_log_info.setText("Confira e Salve seus dados de Login")
                    self.btn_save_new.setEnabled(True)
                else:
                    self.lbl_log_info.setText("Senha inválida ou confirmação diferente")
                    self.btn_save_new.setEnabled(False)
                    return
            else:
                self.btn_login.setEnabled(True)
        else:
            self.lbl_log_info.setText("Digite um e_mail Válido")

    def new_user_update(self):
        self.lbl_log_info.setText("Senha Definida com Sucesso")
        in_user_mail = self.txt_user.text()
        in_user_pass = self.txt_pass.text()
        users_man.update_user_pass(in_user_pass, in_user_mail)
        self.btn_save_new.setVisible(False)
        self.lbl_pass_confirm.setVisible(False)
        self.txt_pass_confirm.setVisible(False)
        self.btn_login.setEnabled(True)

    def validade(self):
        in_user_email = self.txt_user.text()
        in_user_pass = self.txt_pass.text()
        user = users_man.user_by_email_pass(in_user_email, in_user_pass)
        
        if user:
            models.Current_User = models.User(user.user_id, user.is_admin, user.user_name, user.user_role,
                                              user.user_phone, user.user_email, user.user_pass, user.user_reg_by, user.user_img, user.user_theme)
            self.login_sucess.emit(models.Current_User)
            user.user_pass = ""
            self.txt_pass.clear()
            self.txt_pass_confirm.clear()
            self.accept()
        else:
            self.lbl_log_info.setText("Email ou senha Inválidos")
            
