from data import models
from data import crud
from data.models import Const_Vars
from pathlib import Path

def is_valid_email(email):
    return "@" in email and "." in email

def exists_email(email):
    users_email = models.Users_Email
    if not is_valid_email(email):
        return None
    if email not in users_email:
        return None
    else:
        return crud.get_mail_exists(email)
    
def update_current_user(user_data):
    return models.User(
        user_id=user_data[0],
        is_admin=user_data[1],
        user_name=user_data[2],
        user_role=user_data[3],
        user_phone=user_data[4],
        user_email=user_data[5],
        user_pass=models.Current_User.user_pass,
        user_reg_by=models.Current_User.user_reg_by,
        user_img=user_data[8],
        user_theme = user_data[9]
    )

def get_users_email():
    return set(email[0] for email in crud.get_users_email())

def user_by_email_pass(user_email, user_pass):
    return crud.get_user_by_pass_mail(user_email, user_pass)

def update_user(user_data):
    crud.update_user(user_data)

def get_user_img():
    user = models.Current_User
    default_ico = Path(Const_Vars.PATH_TO_ICONS)/'User_ico.png'
    user_img_path = Path(user.user_img) if user.user_img else None
    if user.user_img and user_img_path:
        return str(user.user_img)
    return str(default_ico)

def update_user_pass(user_pass, user_email):
    crud.update_user_pass(user_pass, user_email)

def delete_user_by_email(user_email):
    crud.delete_by_email(user_email)

def insert_new_user(is_admin, user_name, user_role, user_phone, user_email, user_reg_by, user_img, user_theme):
    crud.insert_new_user(is_admin, user_name, user_role, user_phone, user_email, user_reg_by, user_img, user_theme)

def ensure_admin_exists():
    is_admin = "1"
    user_name = "Admin"
    user_email = "@admin.local"
    user_role =  None
    user_phone = None
    user_reg_by = "System"
    user_img = None
    user_theme = "0"
    insert_new_user(is_admin, user_name, user_role, user_phone, user_email, user_reg_by, user_img, user_theme)
        
