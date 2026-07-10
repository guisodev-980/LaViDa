from datetime import datetime, date

class User():
    def __init__(self,
                user_id,
                is_admin,
                user_name,
                user_role,
                user_phone,
                user_email,
                user_pass,
                user_reg_by,
                user_img,
                user_theme):
        
        self.user_id = user_id
        self.is_admin = bool(is_admin)
        self.user_name = user_name
        self.user_role = user_role
        self.user_phone = user_phone
        self.user_email = user_email
        self.user_pass = user_pass
        self.user_reg_by = user_reg_by
        self.user_img = user_img
        self.user_theme = bool(user_theme)
    

    def is_adm_user(self):
        return self.is_admin
    
Current_User: User | None = None

class Video():
    def __init__(self,
                id,
                test,
                subject,
                group,
                day,
                try_n,
                video_name,
                cad_by,
                video_width,
                video_height,
                mask_x,
                mask_y,
                mask_r,
                video_status,
                img_traj,
                time,
                speed,
                distance,
                q1,
                q2,
                q3,
                q4,
                tgm_t,
                tgm_r,
                center_t_):
        
            self.id = id
            self.test = test
            self.subject = subject
            self.group = group
            self.day = day
            self.try_n = try_n
            self.video_name = video_name
            self.cad_by = cad_by
            self.video_width = video_width
            self.video_height = video_height
            self.mask_x = mask_x
            self.mask_y = mask_y
            self.mask_r = mask_r
            self.video_status = video_status
            self.img_traj = img_traj
            self.time = time
            self.speed = speed
            self.distance = distance
            self.q1 = q1
            self.q2 = q2
            self.q3 = q3
            self.q4 = q4
            self.tgm_t = tgm_t
            self.tgm_r = tgm_r
            self.center_t_ = center_t_
        
Current_Video: Video | None = None

class Result_Totals():
     def __init__(self,
                  av_time: float, max_time: float, min_time: float, 
                  av_speed: float, max_speed: float, min_speed: float,
                  av_dist: float, max_dist: float, min_dist: float,
                  av_q1: float, max_q1: float, min_q1: float,
                  av_q2: float, max_q2: float, min_q2: float,
                  av_q3: float, max_q3: float, min_q3: float,
                  av_q4: float, max_q4: float, min_q4: float,
                  av_tgm: float, max_tgm: float, min_tgm: float,
                  av_tgm_r: float, max_tgm_r: float, min_tgm_r: float,
                  av_center_t: float, max_center_t: float, min_center_t: float,
                  subject_out, group_out,
                  day_out, try_n_out
                  ):
          
          self.av_time = round(float(av_time), 3)
          self.max_time = round(float(max_time), 3)
          self.min_time = round(float(min_time), 3)
          self.av_speed = round(float(av_speed), 3)
          self.max_speed = round(float(max_speed), 3)
          self.min_speed = round(float(min_speed), 3)
          self.av_dist = round(float(av_dist), 3)
          self.max_dist = round(float(max_dist), 3)
          self.min_dist = round(float(min_dist), 3)
          self.av_q1 = round(float(av_q1), 3)
          self.max_q1 = round(float(max_q1), 3)
          self.min_q1 = round(float(min_q1), 3)
          self.av_q2 = round(float(av_q2), 3)
          self.max_q2 = round(float(max_q2), 3)
          self.min_q2 = round(float(min_q2), 3)
          self.av_q3 = round(float(av_q3), 3)
          self.max_q3 = round(float(max_q3), 3)
          self.min_q3 = round(float(min_q3), 3)
          self.av_q4 = round(float(av_q4), 3)
          self.max_q4 = round(float(max_q4), 3)
          self.min_q4 = round(float(min_q4), 3)
          self.av_tgm = round(float(av_tgm), 3)
          self.max_tgm = round(float(max_tgm), 3)
          self.min_tgm = round(float(min_tgm), 3)
          self.av_tgm_r = round(float(av_tgm_r), 3)
          self.max_tgm_r = round(float(max_tgm_r), 3)
          self.min_tgm_r = round(float(min_tgm_r), 3)
          self.av_center_t = round(float(av_center_t), 3)
          self.max_center_t = round(float(max_center_t), 3)
          self.min_center_t = round(float(min_center_t), 3)

          self.subject_out = subject_out
          self.group_out = group_out
          self.day_out = day_out
          self.try_n_out = try_n_out

Current_Totals: Result_Totals | None = None

class Json_Data():
     def __init__(self,
                  js_time,
                  js_shut,
                  js_last_bkp,
                  js_sched_by,
                  js_files_to_do = None):
          
          self.js_time = self._normalize_time(js_time)
          
          if isinstance(js_shut, str):
               self.js_shut = js_shut == "1"
          else:
               self.js_shut = bool(js_shut)
          
          self.js_last_bkp = self._normalize_date(js_last_bkp)
          
          self.js_sched_by = self._get_sched_by(js_sched_by)
          

          if isinstance(js_files_to_do, list):
               self.js_files_to_do = js_files_to_do
          elif js_files_to_do is None:
               self.js_files_to_do = []
          else:
               self.js_files_to_do = [js_files_to_do]

     def _normalize_time(self, js_time_str):
          hour, min = js_time_str.split(":")

          return f"{hour.zfill(2)}:{min.zfill(2)}"

     def _normalize_date(self, date_str):
          try:
               return datetime.strptime(date_str, '%Y/%m/%d').date()
          except Exception:
               return date.today()
          
     def _get_sched_by(self, sched_by):
          if sched_by in ("0" or None):
               return "Sem Agendamento"
          else:
               return sched_by

Current_Js_Data: Json_Data | None = None

class Mask_Holder():
     def __init__(self,
                  video,
                  mask_x,
                  mask_y,
                  mask_z):
          self.video = video
          self.mask_x = mask_x
          self.mask_y = mask_y
          self.mask_z = mask_z

current_mask_holder: Mask_Holder | None = None

Json_Default = {"j_time": "-1:-1", "j_ck_shutdown": "0", "j_last_bkp": date.today().strftime("%Y/%m/%d"), "j_schedule_by": "0", "video_files_to_do": []}
Users_Email = set()
Pmap_Scale = int(350)
Csv_Header = "ID,TEST,SUBJECT,GROUP,DAY,TRY_N,VIDEO,CAD_BY,S_WIDTH,S_HEIGHT,MASK_X,MASK_Y,MASK_R,STATUS,IMG_TRAJ,TIME,SPEED,DISTANCE,Q1,Q2,Q3,Q4,TGM_T,TGM_R,CENTER_T"

class Const_Vars:
    POOL_DIAMETER_CM = 120
    ERROR_MARGIN = 1.234
    VERSION = "1.3.0"
    PATH_TO_THEMES = "screens/themes"
    PATH_TO_TEMPS = "data/temps"
    PATH_TO_ICONS = "imgs/icons/"
    PATH_TO_IMGS = "imgs/"
    PATH_TO_USER_IMGS = "data/user_imgs/" 
    PATH_TO_VIDEOS = "LV_videos/"
    PATH_TO_THUMBS = "LV_videos/video_thumbs/"
    PATH_TO_VIDEO_IMGS = "data/video_imgs/"
    PATH_TO_RESULTS = "data/results.csv"
    PATH_TO_PDFS = "data/pdfs"
    PATH_TO_CONFIG = "data/config.json"
    PATH_TO_BKP = "data/bak/"