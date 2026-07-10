
from PySide6.QtWidgets import QLabel, QPushButton, QLineEdit, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QGridLayout, QSizePolicy, QCheckBox, QFileDialog
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap
from pathlib import Path
import shutil

from screens import pop_messages
from data.models import Const_Vars as Vars
from data import models
from services import users_man


class Cad_Frame(QWidget):

    def __init__(self, logout_callback=None, update_reg_user_callback=None, home_frame=None, parent=None):
        super().__init__(parent)
        self.logout_callback = logout_callback
        self.update_reg_user_callback = update_reg_user_callback
        self.home_frame = home_frame

        self.img_orig_path = ""
        self.ico_user_big = QIcon(f'{Vars.PATH_TO_ICONS}User_ico.png')
        self.img_software = QPixmap(f'{Vars.PATH_TO_IMGS}La viDa identidade-01.png').scaled(QSize(200,200), Qt.KeepAspectRatio, Qt.SmoothTransformation) #La viDa identidade-01
        
        self.ui_cad_screen()

        self.btn_user_img.setIcon(self.ico_user_big)
        self.btn_user_img.setIconSize(QSize(150, 150))
        self.btn_new.clicked.connect(lambda: self.sync_btn_sate("new"))
        self.btn_edit.clicked.connect(lambda: self.sync_btn_sate("edit"))
        self.btn_delete.clicked.connect(lambda: self.sync_btn_sate("del"))
        self.btn_edit.clicked.connect(self.edit_user_ui)
        self.btn_clear_pass.clicked.connect(self.clear_user_pass)
        self.btn_user_img.clicked.connect(self.user_img_select)
        self.btn_edit_save.clicked.connect(self.edit_user_submit)
        self.btn_delete.clicked.connect(self.delete_user_ui)
        self.btn_delete_save.clicked.connect(self.delete_user_submit)
        self.btn_new.clicked.connect(self.new_user_ui)
        self.btn_new_save.clicked.connect(self.new_user_submit)
        
    def ui_cad_screen(self):
        self.setup_labels()
        self.setup_txt()
        self.setup_btns()
        self.setup_misc()
        self.setup_frames()
        self.setup_layout()

    def setup_labels(self):
        self.lbl_user_info = QLabel("Informações do Usuário", alignment=Qt.AlignCenter)
        self.lbl_cat_title = QLabel("Cadastro de Usuário")
        self.lbl_user_id = QLabel("ID:")
        self.lbl_user_name = QLabel("Nome Completo:")
        self.lbl_user_role = QLabel("Cargo:")
        self.lbl_user_tel = QLabel("Telefone:")
        self.lbl_user_mail = QLabel("E-mail:")
        self.lbl_user_cad_by = QLabel("Cadastrado Por:")
        self.lbl_software = QLabel(pixmap=self.img_software)
    
    def setup_btns(self):
        self.btn_user_img = QPushButton()
        self.btn_user_img.setEnabled(False)
        self.btn_user_img.setFixedSize(150, 150)
        self.btn_user_img.setStyleSheet("background-color: transparent")
        self.btn_user_img.setToolTip("Carregar Foto")
        self.btn_new = QPushButton("Novo")
        self.btn_new.setEnabled(False)
        self.btn_new.setCheckable(True)
        self.btn_new.setFixedSize(80, 30)
        self.btn_new_save = QPushButton("Salvar")
        self.btn_new_save.setFixedSize(80, 30)
        self.btn_new_save.setEnabled(False)
        self.btn_new_save.setVisible(False)
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.setFixedSize(80, 30)
        self.btn_cancel.setEnabled(False)
        self.btn_edit = QPushButton("Editar")
        self.btn_edit.setFixedSize(80, 30)
        self.btn_edit.setEnabled(True)
        self.btn_edit.setCheckable(True)
        self.btn_edit_save = QPushButton("Salvar")
        self.btn_edit_save.setFixedSize(80, 30)
        self.btn_edit_save.setEnabled(False)
        self.btn_edit_save.setVisible(False)
        self.btn_delete = QPushButton("Excluir")
        self.btn_delete.setFixedSize(80, 30)
        self.btn_delete.setCheckable(True)
        self.btn_delete.setEnabled(True)
        self.btn_delete_save = QPushButton("Excluir")
        self.btn_delete_save.setFixedSize(80, 30)
        self.btn_delete_save.setEnabled(False)
        self.btn_delete_save.setVisible(False)
        self.btn_clear_pass = QPushButton("Limpar Senha")
        self.btn_clear_pass.setEnabled(False)
        self.btn_clear_pass.setFixedSize(80, 30)
        self.btn_log_of = QPushButton("Sair")

    def setup_misc(self):
        self.ckb_adm = QCheckBox("Adm ?")
        self.ckb_adm.setEnabled(False)    

    def setup_txt(self):
        self.txt_user_id = QLineEdit()
        self.txt_user_id.setEnabled(False)
        self.txt_user_id.setFixedWidth(50)
        self.txt_user_name = QLineEdit()
        self.txt_user_name.setEnabled(False)
        self.txt_user_name.setFixedWidth(250)
        self.txt_user_role = QLineEdit()
        self.txt_user_role.setFixedWidth(250)
        self.txt_user_role.setEnabled(False)
        self.txt_user_phone = QLineEdit()
        self.txt_user_phone.setInputMask("(99) 99999-9999;_")
        self.txt_user_phone.setCursorPosition(0)
        self.txt_user_phone.setFixedWidth(150)
        self.txt_user_phone.setEnabled(False)
        self.txt_user_mail = QLineEdit()
        self.txt_user_mail.setFixedWidth(250)
        self.txt_user_mail.setEnabled(False)
        self.txt_user_cad_by = QLineEdit()
        self.txt_user_cad_by.setFixedWidth(250)
        self.txt_user_cad_by.setEnabled(False)
    
    def setup_frames(self):
        
        #User Data
        self.frm_user_data = QFrame()
        self.frm_user_data.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.frm_user_data.setMinimumWidth(300)
        self.frm_user_data_g_layout = QGridLayout()
        self.frm_user_data_g_layout.addWidget(self.lbl_user_id, 0, 0, alignment=Qt.AlignRight)
        self.frm_user_data_g_layout.addWidget(self.lbl_user_name, 1, 0, alignment=Qt.AlignRight)
        self.frm_user_data_g_layout.addWidget(self.lbl_user_tel, 2, 0, alignment=Qt.AlignRight)
        self.frm_user_data_g_layout.addWidget(self.lbl_user_mail, 3, 0, alignment=Qt.AlignRight)
        self.frm_user_data_g_layout.addWidget(self.lbl_user_role, 4, 0, alignment=Qt.AlignRight)
        self.frm_user_data_g_layout.addWidget(self.lbl_user_cad_by, 5, 0, alignment=Qt.AlignRight)
        self.frm_user_data_g_layout.addWidget(self.txt_user_id, 0, 1)
        self.frm_user_data_g_layout.addWidget(self.txt_user_name, 1, 1, 1, 2)
        self.frm_user_data_g_layout.addWidget(self.txt_user_phone, 2, 1, 1, 2)
        self.frm_user_data_g_layout.addWidget(self.txt_user_mail, 3, 1, 1, 2)
        self.frm_user_data_g_layout.addWidget(self.txt_user_role, 4, 1, 1, 2)
        self.frm_user_data_g_layout.addWidget(self.txt_user_cad_by, 5, 1, 1, 2)
        self.frm_user_data_g_layout.addWidget(self.ckb_adm, 0, 2, alignment=Qt.AlignRight)

        self.frm_user_data.setLayout(self.frm_user_data_g_layout)

        #Registration Buttons
        self.frm_cad_btns = QFrame()
        self.frm_cad_btns.setStyleSheet("border: none;")
        self.frm_cad_btns.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.frm_cad_btns_g_layout = QGridLayout()
        self.frm_cad_btns_g_layout.addWidget(self.btn_new, 0, 0)
        self.frm_cad_btns_g_layout.addWidget(self.btn_new_save, 0, 1)
        self.frm_cad_btns_g_layout.addWidget(self.btn_edit, 1, 0)
        self.frm_cad_btns_g_layout.addWidget(self.btn_edit_save, 1, 1)
        self.frm_cad_btns_g_layout.addWidget(self.btn_delete, 2, 0)
        self.frm_cad_btns_g_layout.addWidget(self.btn_delete_save, 2, 1)
        self.frm_cad_btns_g_layout.addWidget(self.btn_clear_pass, 3, 0)

        self.frm_cad_btns.setLayout(self.frm_cad_btns_g_layout)

        #User Frame
        self.frm_user = QFrame()
        self.frm_user_h_layout = QHBoxLayout()
        self.frm_user_h_layout.addWidget(self.btn_user_img)
        self.frm_user_h_layout.addWidget(self.frm_user_data)
        self.frm_user_h_layout.addWidget(self.frm_cad_btns)
        self.frm_user_h_layout.addWidget(self.lbl_user_info, alignment=Qt.AlignCenter | Qt.AlignVCenter)
        self.frm_user_h_layout.addStretch(1)

        self.frm_user.setLayout(self.frm_user_h_layout)

        #Software Frame
        self.frm_software = QFrame()
        self.frm_software.setStyleSheet("border: none")
        self.frm_software_v_layout = QVBoxLayout()
        self.frm_software_v_layout.addWidget(self.lbl_software)
        self.frm_software_v_layout.setAlignment(Qt.AlignCenter)

        self.frm_software.setLayout(self.frm_software_v_layout)

    def setup_layout(self):
        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.frm_user)
        self.v_layout.addWidget(self.frm_software)

        self.setLayout(self.v_layout)

    #Sync edit, new e delete states
    def sync_btn_sate(self, btn):
        if btn == "edit":
            self.btn_delete.setChecked(False)
            self.btn_new.setChecked(False)
        elif btn == "new":
            self.btn_delete.setChecked(False)
            self.btn_edit.setChecked(False)
        elif btn == "del":
            self.btn_edit.setChecked(False)
            self.btn_new.setChecked(False)

    #toggle TexChange Connection
    def toggle_text_conn(self, btn, function):
        try:
            if btn.isChecked() and models.Current_User.is_admin:
                self.txt_user_mail.textChanged.connect(function)
            else:
                self.txt_user_mail.textChanged.disconnect(function)
        except TypeError:
            pass

    #check if "Any" is empty
    def is_fill_fields(self):
        return bool(self.txt_user_name.text()) and bool(self.txt_user_phone.text()) and bool(self.txt_user_role.text())
    
    # fill UI with current user data
    def fill_user(self):
        user = models.Current_User
        user_img = users_man.get_user_img()
        self.btn_new.setEnabled(user.is_admin)
        self.ckb_adm.setChecked(user.is_admin)
        self.txt_user_id.setText(str(user.user_id))
        self.txt_user_name.setText(user.user_name)
        self.txt_user_role.setText(user.user_role)
        self.txt_user_phone.setText(user.user_phone)
        self.txt_user_cad_by.setText(user.user_reg_by)
        self.txt_user_mail.setText(user.user_email)
        self.btn_user_img.setIcon(QIcon(user_img))

#               *****Edit User****                     #

    #Starts UI to edit
    def edit_user_ui(self):
        user = models.Current_User
        self.toggle_text_conn(self.btn_edit, self.edit_user_fields)
        edit_check = self.btn_edit.isChecked()
        self.btn_user_img.setEnabled(edit_check)
        self.txt_user_name.setEnabled(edit_check)
        self.txt_user_phone.setEnabled(edit_check)
        self.txt_user_mail.setEnabled(edit_check)
        self.txt_user_role.setEnabled(edit_check)
        self.txt_user_mail.setEnabled(user.is_admin and edit_check)
        self.ckb_adm.setEnabled(user.is_admin and edit_check)
        self.btn_edit.setText("Cancelar" if edit_check else "Editar")
        self.btn_edit_save.setVisible(edit_check)
        self.btn_delete.setEnabled(not edit_check)
        self.btn_new.setEnabled(not edit_check)
        self.btn_clear_pass.setEnabled(edit_check)
        self.lbl_user_info.setText("Digite o Email do Usuário\nque deseja editar" if user.is_admin and edit_check else "")
        #self.edit_user_fields()
        if not edit_check:
            self.img_orig_path = ""
            self.toggle_text_conn(self.btn_edit, self.edit_user_fields)
            self.fill_user()
            
           
    #Update fields with editables
    def edit_user_fields(self):
        edit_check = self.btn_edit.isChecked()
        user = models.Current_User
        email = self.txt_user_mail.text().strip().lower()
        email_data = users_man.exists_email(email)
        has_data = bool(email_data)
        can_save = has_data and self.is_fill_fields()
        if edit_check:
            self.btn_clear_pass.setEnabled(has_data)
            self.btn_edit_save.setEnabled(can_save or not user.is_admin)
            self.txt_user_name.setEnabled(has_data or not user.is_admin)
            self.txt_user_phone.setEnabled(has_data or not user.is_admin)
            self.txt_user_role.setEnabled(has_data or not user.is_admin)
            self.btn_user_img.setEnabled(has_data or not user.is_admin)
        self.txt_user_id.setText(str(email_data[0]) if email_data else "")
        self.txt_user_name.setText(email_data[2] if email_data else "")
        self.txt_user_role.setText(email_data[3] if email_data else "")
        self.txt_user_phone.setText(email_data[4] if email_data else "")
        self.ckb_adm.setChecked(bool(email_data[1]) if email_data else False)
        if email_data:
            self.btn_user_img.setIcon(QIcon(email_data[8]) if (email_data[8]) else QIcon(self.ico_user_big))

    #Select new image - "Memory only"
    def user_img_select(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Selecione uma Imagem", "", "Imagens (*.png *.jpg *.jpeg *.bmp *.webp)")
        if not file_path:
            self.img_orig_path = ""
            return
        self.img_orig_path = file_path
        self.btn_user_img.setIcon(QIcon(self.img_orig_path))

    #Submit Changes
    def edit_user_submit(self):
        if not self.is_fill_fields():
            self.lbl_user_info.setText("Preencha todos os Campos")
        else:
            if pop_messages.message_box("Deseja Realmente Editar os dados de ", self.txt_user_mail.text().strip(), "info"):
                user = models.Current_User
                edit_email = self.txt_user_mail.text().lower().strip()
                email_data = list(users_man.exists_email(edit_email))
                email_data[2] = self.txt_user_name.text().strip()
                email_data[3] = self.txt_user_role.text().strip()
                email_data[4] = self.txt_user_phone.text().strip()
                email_data[1] = bool(self.ckb_adm.isChecked())
                if self.img_orig_path:
                    dest_folder = Path(Vars.PATH_TO_USER_IMGS)
                    dest_folder.mkdir(parents=True, exist_ok=True)
                    ext = Path(self.img_orig_path).suffix
                    base_name = f'{email_data[0]}_{str(email_data[2]).strip().lower().replace(" ", "_")}'
                    file_name = f'{base_name}{ext}'
                    email_data[8] = str(dest_folder / file_name)
                    for existing_files in Path(email_data[8]).glob(f'{Path(dest_folder).stem}.*'):
                        existing_files.unlink()
                    shutil.copy(self.img_orig_path, email_data[8])
                    self.img_orig_path = ""
                    email_data[9] = user.user_theme
                users_man.update_user(tuple(email_data)) #Connect with CRUD
                if edit_email == user.user_email:
                    models.Current_User = users_man.update_current_user(email_data)
                    if self.update_reg_user_callback:
                        self.update_reg_user_callback()
                    if self.home_frame:
                        self.home_frame.home_update_user()
                self.btn_edit.setChecked(False)
                self.edit_user_ui()
                self.fill_user()
        

    #Redefine user pass to temporary         
    def clear_user_pass(self):
        user = models.Current_User
        reset_email = self.txt_user_mail.text().lower().strip()
        if pop_messages.message_box(f'Usuário {self.txt_user_mail.text()}<br> Poderá Cadastrar nova senha no login', "Confirmar ?", "crit"):
            users_man.update_user_pass("__Temp__", reset_email)
            if reset_email == user.user_email:
                if self.logout_callback:
                    self.logout_callback()
            else:
                self.edit_user_ui()
                self.fill_user()

#               *****Delete User****                     #

    #Prepare UI for delete
    def delete_user_ui(self):
        user = models.Current_User
        self.txt_user_mail.setEnabled(user.is_admin)
        self.lbl_user_info.setText("Digite o Email do Usuário\nque deseja Excluir" if user.is_admin else "Clique em Excluir para confirmar")
        if user.is_admin:
            self.txt_user_mail.clear()
        self.toggle_text_conn(self.btn_delete, self.delete_user_fields)
        delete_user = self.btn_delete.isChecked()
        self.txt_user_id.clear()
        self.txt_user_name.clear()
        self.txt_user_phone.clear()
        self.txt_user_role.clear()
        self.btn_delete.setText("Cancelar" if delete_user else "Excluir")
        self.btn_new.setEnabled(not delete_user)
        self.btn_edit.setEnabled(not delete_user)
        self.btn_delete_save.setVisible(delete_user)
        self.txt_user_mail.setEnabled(delete_user)
        self.delete_user_fields()
        if not delete_user:
            self.toggle_text_conn(self.btn_delete, self.delete_user_fields)
            self.txt_user_name.setEnabled(False)
            self.txt_user_phone.setEnabled(False)
            self.txt_user_mail.setEnabled(False)
            self.txt_user_role.setEnabled(False)
            self.fill_user()

    #Fill fields with selected user data 
    def delete_user_fields(self):
        user = models.Current_User
        delete_email = self.txt_user_mail.text().strip().lower()
        self.txt_user_mail.setEnabled(user.is_admin)
        email_data = users_man.exists_email(delete_email)
        has_data = bool(email_data)
        self.btn_delete_save.setEnabled(has_data or not user.is_admin)
        self.txt_user_id.setText(str(email_data[0]) if email_data else "")
        self.txt_user_name.setText(email_data[2] if email_data else "")
        self.txt_user_role.setText(email_data[3] if email_data else "")
        self.txt_user_phone.setText(email_data[4] if email_data else "")
        self.ckb_adm.setChecked(bool(email_data[1]) if email_data else False)
        if email_data:
            self.btn_user_img.setIcon(QIcon(email_data[8]) if (email_data[8]) else QIcon(self.ico_user_big))


    #Submit user to delect and logout with deleted == Logged User
    def delete_user_submit(self):
        user = models.Current_User
        if not self.is_fill_fields():
            self.lbl_user_info.setText("Usuário inválido ou sem\npermissão para exclusão")
            return
        if pop_messages.message_box("Deseja Realmente Excluir",f'{self.txt_user_mail.text()} ?', "crit"):
            current_mail = user.user_email
            delete_mail = self.txt_user_mail.text().strip().lower()
            users_man.delete_user_by_email(delete_mail)
            models.Users_Email = users_man.get_users_email()
            if delete_mail == current_mail:
                if self.logout_callback:
                    self.logout_callback()
            else:
                self.btn_delete.setChecked(False)
                self.delete_user_ui()
                self.fill_user()

#               *****Insert User****                     #

    #Prepare UI to insert
    def new_user_ui(self):
        new_user = self.btn_new.isChecked()
        self.toggle_text_conn(self.btn_new, self.new_user_fields)
        self.btn_new.setText("Cancelar" if new_user else "Novo")
        self.btn_edit.setEnabled(not new_user)
        self.btn_delete.setEnabled(not new_user)
        self.btn_new_save.setVisible(new_user)
        self.txt_user_mail.setEnabled(new_user)
        self.ckb_adm.setEnabled(new_user)
        self.ckb_adm.setChecked(False)
        self.lbl_user_info.setText("")
        self.txt_user_id.clear()
        self.txt_user_mail.clear()
        self.txt_user_name.clear()
        self.txt_user_role.clear()
        self.txt_user_phone.clear()
        self.new_user_fields()
        if not new_user:
            self.toggle_text_conn(self.btn_new, self.new_user_fields)
            self.txt_user_name.setEnabled(False)
            self.txt_user_phone.setEnabled(False)
            self.txt_user_mail.setEnabled(False)
            self.txt_user_role.setEnabled(False)
            self.btn_user_img.setEnabled(False)
            self.img_orig_path = ""
            self.fill_user()

    #Prepare fields for new user
    def new_user_fields(self):
        user = models.Current_User
        new_email = self.txt_user_mail.text().lower().strip()
        can_save = users_man.is_valid_email(new_email) and not users_man.exists_email(new_email)
        self.lbl_user_info.setText("Digite o e_mail do usuário\nQue Deseja Cadastrar" if can_save else "Email Inválido ou já Cadastrado")
        self.btn_user_img.setIcon(QIcon(self.ico_user_big))
        self.txt_user_cad_by.setText(user.user_name)
        self.txt_user_name.setEnabled(can_save)
        self.txt_user_phone.setEnabled(can_save)
        self.txt_user_role.setEnabled(can_save)
        self.btn_new_save.setEnabled(can_save)
        self.btn_user_img.setEnabled(can_save)

    def new_user_submit(self):
        if not self.is_fill_fields():
            self.lbl_user_info.setText("Preencha todos os Campos")
            return
        if pop_messages.message_box("Deseja Realmente Adicionar",f'{self.txt_user_mail.text()} ?', "info"):
            is_admin = self.ckb_adm.isChecked()
            user_name = self.txt_user_name.text().strip()
            user_role = self.txt_user_role.text().strip()
            user_phone = self.txt_user_phone.text()
            user_reg_by = self.txt_user_cad_by.text()
            user_email = self.txt_user_mail.text().strip()
            user_img = self.img_orig_path
            user_theme = "0"
            users_man.insert_new_user(is_admin, user_name, user_role, user_phone, user_email, user_reg_by, user_img, user_theme)
            models.Users_Email = users_man.get_users_email()
            self.img_orig_path = ""
            self.btn_new.setChecked(False)
            self.new_user_ui()
        
