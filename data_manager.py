import os
import shutil
from pathlib import Path
import csv
import cv2
import json
import datetime

# ***PYINSTALLER COMMAND
#pyinstaller --onefile --windowed main.py --name=LaViDa --icon=imgs/icons/LaVida_Icon.ico



from data.models import Const_Vars as Vars
from data import models

def get_exists_files():
    video_files = [f.name for f in Path(Vars.PATH_TO_VIDEOS).glob("*.mp4")]
    return video_files

def check_videos_in_json(): # check if videos_to_do exists in folder
    video_files = get_exists_files()
    data_json = Path(Vars.PATH_TO_CONFIG)
    if not is_valid_json(data_json):
        construct_json()

    get_json_data()
    json_data = models.Current_Js_Data
    js_videos = json_data.js_files_to_do
    op_count = 0

    for video in js_videos[:]:
        if video not in video_files:
            js_videos.remove(video)
            op_count +=1

    if op_count > 0:
        update_json()

def video_in_csv(video_name: str) -> bool:
    results_csv = Path(Vars.PATH_TO_RESULTS)
    if not results_csv.exists():
        return False
    with results_csv.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["VIDEO"] == video_name:
                return True
    return False

def is_video_cad(video_name):
        results_csv = Path(Vars.PATH_TO_RESULTS)
        with results_csv.open("r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["VIDEO"] == video_name:
                    has_cad = row["TEST"] != "No_Cad_Test" or row["SUBJECT"] != "No_Cad_Sub" or row["GROUP"] != "No_Cad_Group" or row["DAY"] != "No_Cad_Day" or row["TRY_N"] != "No_Cad_Try" or row["CAD_BY"] != "No_Cad"
                    return has_cad
        return False

def construct_json():
    data_json = Path(Vars.PATH_TO_CONFIG)
    if not data_json.exists() or not is_valid_json(data_json):
        data = models.Json_Default
        data_json.parent.mkdir(parents=True, exist_ok=True)
        with data_json.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    get_json_data()
    construct_csv()

def construct_csv():
    results_csv = Path(Vars.PATH_TO_RESULTS)
    if not results_csv.exists() or not is_valid_csv(results_csv):
        last_bkp = get_last_backup(results_csv)
        if last_bkp:
            restore_last_bkp(last_bkp, results_csv)
        else:
            results_csv.write_text(models.Csv_Header + '\n')
            _set_json_last_bkp(days_ago=6)

    get_video_thumb()

def restore_last_bkp(backup_file: Path, results_csv: Path):
    shutil.copy(backup_file, results_csv)
    _set_json_last_bkp(days_ago=6)

def _set_json_last_bkp(days_ago: int=0):
    new_date = (datetime.date.today() - datetime.timedelta(days=days_ago)).strftime('%Y/%m/%d')
    models.Current_Js_Data.js_last_bkp = new_date
    update_json()


def is_valid_json(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8") as json_file:
            data = json.load(json_file)
        #Check Json file Integrity
        required_keys = {"j_time", "j_ck_shutdown", "j_last_bkp", "j_schedule_by", "video_files_to_do"}
        return required_keys.issubset(set(data.keys()))
    except Exception as e:
        return False

def is_valid_csv(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8") as csv_file:
            first_line = csv_file.readline().strip()
        #Check Json file Integrity
        return first_line == models.Csv_Header
    except Exception as e:
        return False
    
def do_backup():
    c_json = models.Current_Js_Data
    results_csv = Path(Vars.PATH_TO_RESULTS)
    bkps_folder = Path(Vars.PATH_TO_BKP) #PATH_TO_BKP = data/bak/
    bkps_folder.mkdir(parents=True, exist_ok=True)
    max_bkp = 10
    if results_csv.exists():
        ts = datetime.date.today().strftime("%Y-%m-%d")
        bkp_name = bkps_folder / f"{results_csv.stem}_{ts}.csv.bak"
        shutil.copy(results_csv, bkp_name)
    bkp_files = sorted(bkps_folder.glob(f"{results_csv.stem}bak_*.bak"), key=lambda f:f.stat().st_mtime)
    if len(bkp_files) > max_bkp:
        for old_bkp in bkp_files[:-max_bkp]:
            old_bkp.unlink()
    c_json.js_last_bkp = ts
    update_json()


def get_last_backup(csv_file: Path) -> Path | None:
    bkps_folder = Path(Vars.PATH_TO_BKP)
    pattern = f"{csv_file.stem}_*.csv.bak"
    bak_files = list(bkps_folder.glob(pattern))
    if not bak_files:
        return None
    return max(bak_files, key=lambda f: f.stat().st_mtime)

def check_bkp_last():
    today = datetime.date.today()
    lst_bkp = models.Current_Js_Data.js_last_bkp
    if lst_bkp <= today - datetime.timedelta(days=7):
        do_backup()

def get_video_data():
    results_csv = Path(Vars.PATH_TO_RESULTS)
    video_data = []
    if results_csv.exists():
        with open(results_csv, newline='', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row_data = (
                    row.get("TEST"),
                    row.get("SUBJECT"),
                    row.get("GROUP"),
                    row.get("DAY"),
                    row.get("TRY_N"),
                    row.get("VIDEO"),
                    row.get("STATUS"),
                    row.get("CAD_BY")
                )
                video_data.append(row_data)

    return video_data


def get_json_data():
    can_os_shut = os_check()
    configs_json = Path(Vars.PATH_TO_CONFIG)
    with configs_json.open("r", encoding="utf-8") as file:
        json_data = json.load(file)
        
        js_time = json_data["j_time"]
        js_shut = json_data.get("j_ck_shutdown", False) if can_os_shut else False
        js_last_bkp = json_data.get("j_last_bkp")
        js_sched_by = json_data.get("j_schedule_by")
        js_files_to_do = json_data.get("video_files_to_do", [])

        models.Current_Js_Data = models.Json_Data(js_time, js_shut, js_last_bkp, js_sched_by, js_files_to_do)

        if js_shut and not can_os_shut: #Change state only if needed
            update_json()
    check_bkp_last()

def update_json():
    js_data = models.Current_Js_Data
    configs_json = Path(Vars.PATH_TO_CONFIG)
    data =  {"j_time": str(js_data.js_time),
            "j_ck_shutdown": js_data.js_shut,
            "j_last_bkp": str(js_data.js_last_bkp),
            "j_schedule_by": js_data.js_sched_by,
            "video_files_to_do": js_data.js_files_to_do}
            
    with configs_json.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    get_json_data() # Recriate models.js_data from config.json files updated

def get_video_thumb():
    dest_folder = Path(Vars.PATH_TO_THUMBS)
    dest_folder.mkdir(parents=True, exist_ok=True)
    
    for video_name in get_exists_files():
        video_path = Path(Vars.PATH_TO_VIDEOS) / video_name
        base_name = Path(video_name).stem
        thumb_path = dest_folder / f'{base_name}.png'
        if not thumb_path.exists() or not video_in_csv(video_name):
            construct_thumb(video_name, video_path, str(thumb_path))

def set_thumb_img(file):
    base_video = Path(file).stem
    tumb_dir = Path(Vars.PATH_TO_THUMBS)
    traj_dir = Path(Vars.PATH_TO_VIDEO_IMGS)
    default_img = str(Path(Vars.PATH_TO_ICONS)/'Image_Holder.png')
    for existing_traj in traj_dir.glob(f'{base_video}.*'):
        if existing_traj:
            return existing_traj
    for existing_thumb in tumb_dir.glob(f'{base_video}.*'):
        return existing_thumb
    return default_img

def construct_thumb(video_name, video_path, thumb_path):
    try:
        results_csv = Path(Vars.PATH_TO_RESULTS)
        vid_cap = cv2.VideoCapture(video_path)
        width  = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        sucess, frame = vid_cap.read()
        if sucess:
            cv2.imwrite(thumb_path, frame)
        
        if not results_csv.exists():
            results_csv.write_text(models.Csv_Header + '\n')

        with open(results_csv, newline= '', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
        
        found = False
        for row in rows:
            if row["VIDEO"] == video_name:
                row["S_WIDTH"] = width
                row["S_HEIGHT"] = height
                found = True
                break

        if not found:
            new_row = {
                "ID": str(len(rows)+1),
                "TEST": "No_Cad_Test",
                "SUBJECT": "No_Cad_Sub",
                "GROUP": "No_Cad_Group",
                "DAY": "No_Cad_Day",
                "TRY_N": "No_Cad_Try",
                "CAD_BY": "No_Cad",
                "VIDEO": video_name,
                "S_WIDTH": width,
                "S_HEIGHT": height,
                "MASK_X": "0",
                "MASK_Y": "0",
                "MASK_R": "0",
                "STATUS": "pendente",
                "IMG_TRAJ": "No_Traj",
                "TIME": "0.0",
                "SPEED": "0.0",
                "DISTANCE": "0.0",
                "Q1" : "0.0",
                "Q2" : "0.0",
                "Q3" : "0.0",
                "Q4" : "0.0",
                "TGM_T": "0.0",
                "TGM_R": "0.0",
                "CENTER_T": "0.0"
            }

            rows.append(new_row)
        with open(results_csv, 'w', newline='', encoding='utf-8') as file:
            writer= csv.DictWriter(file, fieldnames=models.Csv_Header.split(','))
            writer.writeheader()
            writer.writerows(rows)

    finally:
        vid_cap.release()


def set_c_video(selected):
    results_csv = Path(Vars.PATH_TO_RESULTS)
    with open(results_csv, newline= '', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
    for row in rows:
        if row["VIDEO"] == selected:
            models.Current_Video = models.Video(row["ID"],
                                                row["TEST"],
                                                row["SUBJECT"],
                                                row["GROUP"],
                                                row["DAY"],
                                                row["TRY_N"],
                                                row["VIDEO"],
                                                row["CAD_BY"],
                                                row["S_WIDTH"],
                                                row["S_HEIGHT"],
                                                row["MASK_X"],
                                                row["MASK_Y"],
                                                row["MASK_R"],
                                                row["STATUS"],
                                                row["IMG_TRAJ"],
                                                row["TIME"],
                                                row["SPEED"],
                                                row["DISTANCE"],
                                                row["Q1"],
                                                row["Q2"],
                                                row["Q3"],
                                                row["Q4"],
                                                row["TGM_T"],
                                                row["TGM_R"],
                                                row["CENTER_T"]
                                                )
            break
            
def get_exists_mask(video_name):
    results_csv = Path(Vars.PATH_TO_RESULTS)
    with open(results_csv, newline= '', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for row in rows:
            if row["VIDEO"] == video_name:
                has_mask = row["MASK_X"] != "0" and row["MASK_Y"] != "0" and row["MASK_R"] != "0"
                return bool(has_mask)
    return False

def get_scale(pmap_width, pmap_height):
    c_video = models.Current_Video
    scale_x = int(c_video.video_width) / pmap_width
    scale_y = int(c_video.video_height) / pmap_height
    return scale_x, scale_y

def scale_to_thumb(pmap_width, pmap_height):
    c_video = models.Current_Video
    scale_x, scale_y = get_scale(pmap_width, pmap_height)
    scale = min(scale_x, scale_y)
    return (
        int(int(c_video.mask_x) / scale_x),
        int(int(c_video.mask_y) / scale_y),
        int(int(c_video.mask_r) / scale))

def scale_to_video(cx, cy, r, pmap_width, pmap_height):
    scale_x, scale_y = get_scale(pmap_width, pmap_height)
    scale = min(scale_x, scale_y)

    return int(cx * scale_x), int(cy * scale_y), int(r * scale)
        
def get_width_height(selected_video):
        results_csv = Path(Vars.PATH_TO_RESULTS)
        origin_size = []
        with open(results_csv, newline= '', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            found = False
            for row in rows:
                if row["VIDEO"] == selected_video:
                    origin_size.append(row["S_WIDTH"])
                    origin_size.append(row["S_HEIGHT"])
                    found = True
            if found:
                return origin_size
            
def update_video_data(video_name, test, group, day, try_n, subject, cad_by, new_name):
    results_csv = Path(models.Const_Vars.PATH_TO_RESULTS)
    with open(results_csv, newline="", encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for row in rows:
            if row["VIDEO"] == video_name:
                row["VIDEO"] = new_name
                row["TEST"] = test
                row["SUBJECT"] = subject
                row["GROUP"] = group
                row["DAY"] = day
                row["TRY_N"] = try_n
                row["CAD_BY"] = cad_by
                #If alwread has trajetory image
                if row["IMG_TRAJ"] != "No_Traj": #No_Traj = default value or empty
                    _, ext = row["IMG_TRAJ"].split(".")
                    row["IMG_TRAJ"] = f"{new_name}.{ext}"


    with open(results_csv, "w", newline="", encoding="utf-8") as file_in:
        writer = csv.DictWriter(file_in, fieldnames=models.Csv_Header.split(','))
        writer.writeheader()
        writer.writerows(rows)

def redefine_files(name, new_name):
    thumb_path = Path(models.Const_Vars.PATH_TO_THUMBS)
    video_path = Path(models.Const_Vars.PATH_TO_VIDEOS)
    traj_path = Path(models.Const_Vars.PATH_TO_VIDEO_IMGS)

    #Thumb Rename
    thumb_candidates = list(thumb_path.glob(f"{Path(name).stem}.*"))
    old_thumb = thumb_candidates[0] if thumb_candidates else None
    if old_thumb:
        thumb_ext = old_thumb.suffix
        new_thumb = thumb_path / f"{new_name}{thumb_ext}"
        if old_thumb.exists():
            old_thumb.rename(new_thumb)

    #Trajectory Image
    traj_candidates = list(traj_path.glob(f"{Path(name).stem}.*"))
    old_traj = traj_candidates[0] if traj_candidates else None
    if old_traj:
        traj_name, _ = new_name.split(".")
        traj_ext = old_traj.suffix
        new_traj = traj_path / f"{traj_name}{traj_ext}"
        if old_traj.exists():
            old_traj.rename(new_traj)
    
    #Video Rename
    old_video = video_path / name
    new_video = video_path / f"{new_name}"
    if old_video.exists():
        old_video.rename(new_video)


def update_csv_status(video_name, status):
    results_csv = Path(Vars.PATH_TO_RESULTS)
    with results_csv.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for row in rows:
            if row["VIDEO"] == video_name:
                row["STATUS"] = status
            if not row["VIDEO"] == video_name and row["STATUS"] == status:
                row["STATUS"] = "pendente"

    with results_csv.open("w", encoding="utf-8", newline="") as file_in:
        writer = csv.DictWriter(file_in, fieldnames=models.Csv_Header.split(','))
        writer.writeheader()
        writer.writerows(rows)

def update_shc_status(unselected, selected):
    results_csv = Path(Vars.PATH_TO_RESULTS)
    with results_csv.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    for row in rows:
        file = row["VIDEO"]
        if file in selected:
            row["STATUS"] = "agendado"
        elif file in unselected:
            if row["TIME"] != "0.0" or row["SPEED"] != "0.0" or row["DISTANCE"] != "0.0":
                row["STATUS"] = "pronto"
            else:
                row["STATUS"] = "pendente"

    with results_csv.open("w", encoding="utf-8", newline="") as file_in:
        writer = csv.DictWriter(file_in, fieldnames=models.Csv_Header.split(','))
        writer.writeheader()
        writer.writerows(rows)


def has_results(video_name):
    c_video = models.Current_Video
    if not video_name == c_video.video_name:
        return False
    if not (c_video.time == "0.0" or c_video.distance == "0.0" or c_video.speed == "0.0"):
        return True
    return False

def set_hold_mask(video_name):
    c_video = models.Current_Video
    models.current_mask_holder = models.Mask_Holder(video_name,
                                                    c_video.mask_x,
                                                    c_video.mask_y,
                                                    c_video.mask_r)
    return

def save_mask(video_name, mask_x, mask_y, mask_r):
    results_csv = Path(Vars.PATH_TO_RESULTS)
    with open(results_csv, newline= '', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for row in rows:
            if row["VIDEO"] == video_name:
                row["MASK_X"] = mask_x
                row["MASK_Y"] = mask_y
                row["MASK_R"] = mask_r
    
    with open(results_csv, 'w', newline= '', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=models.Csv_Header.split(','))
        writer.writeheader()
        writer.writerows(rows)

def save_traj_csv(video_name, traj_img):
    results_csv = Path(Vars.PATH_TO_RESULTS)
    with results_csv.open(newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for row in rows:
            if row["VIDEO"] == video_name:
                row["IMG_TRAJ"] = traj_img
    
    with results_csv.open('w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=models.Csv_Header.split(','))
        writer.writeheader()
        writer.writerows(rows)

def results_to_csv():
    c_video = models.Current_Video
    results_csv = Path(Vars.PATH_TO_RESULTS)
    with results_csv.open(newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for row in rows:
            if row["VIDEO"] == c_video.video_name:
                row["STATUS"] = c_video.video_status
                row["IMG_TRAJ"] = c_video.img_traj
                row["TIME"] = c_video.time
                row["SPEED"] = c_video.speed
                row["DISTANCE"] = c_video.distance
                row["Q1"] = c_video.q1
                row["Q2"] = c_video.q2
                row["Q3"] = c_video.q3
                row["Q4"] = c_video.q4
                row["TGM_T"] = c_video.tgm_t
                row["TGM_R"] = c_video.tgm_r
                row["CENTER_T"] = c_video.center_t_

    with results_csv.open('w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=models.Csv_Header.split(','))
        writer.writeheader()
        writer.writerows(rows)

def erase_video_results(video):
    results_csv = Path(Vars.PATH_TO_RESULTS)
    base_name = Path(video).stem
    traj_dir = Path(Vars.PATH_TO_VIDEO_IMGS)

    file = next(traj_dir.glob(f"{base_name}.*"), None)

    if file:
        file.unlink()
    get_json_data()
    c_json_data = models.Current_Js_Data
    files_schedule = c_json_data.js_files_to_do
    with results_csv.open(newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for row in rows:
            if row["VIDEO"] == video:
                video_status = "pendente" if video not in files_schedule else "agendado"
                row["STATUS"] = video_status
                row["IMG_TRAJ"] = "No_Traj"
                row["TIME"] = "0.0"
                row["SPEED"] = "0.0"
                row["DISTANCE"] = "0.0"
                row["Q1"] = "0.0"
                row["Q2"] = "0.0"
                row["Q3"] = "0.0"
                row["Q4"] = "0.0"
                row["TGM_T"] = "0.0"
                row["TGM_R"] = "0.0"
                row["CENTER_T"] = "0.0"

    with results_csv.open('w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=models.Csv_Header.split(','))
        writer.writeheader()
        writer.writerows(rows)

def os_check():
    return True if os.name == "nt" else False
